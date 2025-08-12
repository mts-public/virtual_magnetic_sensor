from abc import ABC
import ngsolve as ng
from math import pi
import numpy as np
from typing import Union

from libs.simulation.MagneticField import MagneticField

from libs.simulation.ngsolve.NGMesh import NGMesh

from libs.DataHandler import DataHandler


class NGField(MagneticField, ABC):
    """Implementation of MagneticField based on features provided by the ngsolve package.

    :param data_handler: Object of the Data class containing all simulation relevant data.
    :type data_handler: DataHandler
    :param mu0: Magnetic field constant.
    :type mu0: float
    :param mur: Magnetic permeability for the materials in the scenery.
    :type mur: ngsolve.CoefficientFunction
    :param b_field: Magnetic flux density field defined on the created mesh.
    :type b_field: ngsolve.CoefficientFunction
    :param h_field: Magnetic field strength field defined on the created mesh.
    :type h_field: ngsolve.CoefficientFunction
    :param gfu: Vector potential.
    :type gfu: ngsolve.GridFunction
    :param mag: Magnetisation of the objects in the scenery.
    :type mag: ngsolve.CoefficientFunction
    :param ng_mesh: Object of the mesh class handling the CSGeometries.
    :type ng_mesh: NGMesh
    """

    data_handler: DataHandler
    mu0: float
    mur: ng.CoefficientFunction
    b_field: ng.CoefficientFunction
    h_field: ng.CoefficientFunction
    gfu: ng.GridFunction
    mag: ng.CoefficientFunction
    ng_mesh: NGMesh

    def __init__(self, data_handler: DataHandler) -> None:
        """Constructor method."""

        self.mu0 = 4 * pi * 1e-7

        self.ng_mesh = NGMesh(data_handler)

    def create_field(self, data_handler: DataHandler, t: float) -> None:
        """Method to initialize and calculate the magnetic field based on the given parameters.

        :param data_handler: Object of the Data class containing all simulation relevant data.
        :type data_handler: DataHandler
        :param t: Current time stamp:
        :type t: float

        """

        # Update the mesh
        self.ng_mesh.update(data_handler, t)

        # Declare finite element space.
        fes = ng.HCurl(self.ng_mesh.mesh, order=3, nograds=True)
        # order:     Polynomial degree on each mesh element.
        # dirichlet: dirichlet="outer": Dirichlet boundary conditions on specified ("outer") elements.
        # nograds:   Remove higher order gradients of H1 basis functions from HCurl FESpace.

        # Return a tuple of trial and test-function
        u, v = fes.TnT()

        # Store the left hand side of the PDE.
        a = ng.BilinearForm(fes)

        # Store the material specific mu_r in a dict.
        mur_dict = {}
        for num, magnet in enumerate(data_handler.physical_magnets()):
            mur_dict["magnet" + str(num)] = magnet.mu_r
        for num, component in enumerate(data_handler.components()):
            mur_dict["iron" + str(num)] = component.mu_r
        self.mur = self.ng_mesh.mesh.MaterialCF(mur_dict, default=1)

        # Define the left side of the partial differential equation (PDE)
        a += 1 / (self.mu0 * self.mur) * ng.curl(u) * ng.curl(v) * ng.dx + 1e-8 / (
                    self.mu0 * self.mur) * u * v * ng.dx  # 1e-8...  -> regularization term

        # Preconditioner: Reshapes the system of equations in such a way that better conditions are created, but the
        # solution remains the same
        c = ng.Preconditioner(a, "bddc")

        # Store the right hand side of the PDE.
        f = ng.LinearForm(fes)

        # Store the magnetisation of the particular elements in the simulation in a dict.
        mag_dict = {}
        for num, magnet in enumerate(data_handler.physical_magnets()):
            mag_dict["magnet" + str(num)] = tuple(magnet.m_vec)
        self.mag = self.ng_mesh.mesh.MaterialCF(mag_dict, default=(0, 0, 0))

        # Define the right side of the pde
        for num, _ in enumerate(data_handler.physical_magnets()):
            f += self.mag * ng.curl(v) * ng.dx("magnet" + str(num))
        for field in data_handler.uni_fields():
            f += ng.CoefficientFunction(tuple(field.h_vec)) * ng.curl(v) * ng.dx

        # Assemble linear and bi-linear form
        with ng.TaskManager():
            a.Assemble()
            f.Assemble()

        # GridFunction(): A field approximated in some finite element space.
        self.gfu = ng.GridFunction(fes)

        # Return solution vector.
        with ng.TaskManager():
            ng.solvers.CG(sol=self.gfu.vec, rhs=f.vec, mat=a.mat, pre=c.mat, tol=data_handler.sim_params().tol,
                          maxsteps=data_handler.sim_params().maxit)
            # sol        : Start vector for CG method. Gets overwritten by the solution vector.
            # rhs        : Right hand side of the equation.
            # mat        : Left hand side of the equation.
            # pre        : Preconditioner.
            # tol        : Tolerance of the residuum. CG stops if tolerance is reached.
            # maxsteps   : Number of maximal steps fo CG. If the maximal number is reached before the tolerance is
            #              reached CG stops.

        # Create B- and H-field
        self.b_field: ng.comp.CoefficientFunction = ng.curl(self.gfu)
        self.h_field: ng.fem.CoefficientFunction = self.b_field / (self.mu0 * self.mur) - self.mag

    def draw(self) -> None:
        """Method to draw the magnetic field strength and the magnetic flux density in the Netgen gui."""

        ng.Draw(self.gfu, self.ng_mesh.mesh, "vector-potential", draw_surf=False)
        ng.Draw(self.b_field, self.ng_mesh.mesh, "B-field", draw_surf=False)
        ng.Draw(self.h_field, self.ng_mesh.mesh, "H-field", draw_surf=False)

    def get_h_field(self, x: np.ndarray, y: np.ndarray, z: np.ndarray) -> Union[np.ndarray, None]:
        """Method to extract the magnetic field strength on positions defined by a grid on x, y and z.

        :param x: x grid.
        :type x: numpy.ndarray
        :param y: y grid.
        :type y: numpy.ndarray
        :param z: z grid.
        :type z: numpy.ndarray

        :return: Magnetic field strength on the grid passed.
        :rtype: Union[np.ndarray, None]
        """

        if x.shape != y.shape or x.shape != z.shape or y.shape != z.shape:
            return None
        else:
            return self.h_field(self.ng_mesh.mesh(x.flatten(), y.flatten(), z.flatten())).reshape(x.shape + (3,))

    def get_b_field(self, x: np.ndarray, y: np.ndarray, z: np.ndarray) -> Union[np.ndarray, None]:
        """Method to extract the magnetic flux density on positions defined by a grid on x, y and z.

        :param x: x grid.
        :type x: numpy.ndarray
        :param y: y grid.
        :type y: numpy.ndarray
        :param z: z grid.
        :type z: numpy.ndarray
        
        :return: Magnetic flux density on the grid passed.
        :rtype: Union[np.ndarray, None]
        """

        if x.shape != y.shape or x.shape != z.shape or y.shape != z.shape:
            return None
        else:
            return self.b_field(self.ng_mesh.mesh(x.flatten(), y.flatten(), z.flatten())).reshape(x.shape+(3,))
