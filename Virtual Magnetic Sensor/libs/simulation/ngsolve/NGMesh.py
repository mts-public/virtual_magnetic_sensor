import ngsolve as ng
import netgen.meshing as msh
from math import sqrt
import numpy as np
from typing import Union, List, Tuple, Dict
from pyngcore import TaskManager

from libs.DataHandler import DataHandler
from libs.elements.components.Gear import Gear
from libs.elements.components.GearRack import GearRack

from libs.simulation.ngsolve.CSGeometry import CSGeometry


class NGMesh:
    """Generates the CSGeometries for the objects in the scenery and generates the mesh on which the finite element
        simulation is calculated. Includes the necessary mesh operations to fulfill the manual mesh approach.

    :param data_handler: Object of the Data class containing all simulation relevant data.
    :type data_handler: DataHandler
    :param mp: Meshing parameters.
    :type mp: netgen.meshing.MeshingParameters
    :param netgen_mesh: Full mesh in Netgen.
    :type netgen_mesh: netgen.meshing.Mesh
    :param mesh_badness: Initial badness of unrotated automatically generated netgen mesh.
    :type mesh_badness: float
    :param mesh:  Full mesh converted to Ngsolve.
    :type mesh: ngsolve.Mesh
    :param init_mesh_t: Time stamp of the frame the mesh got rebuilt.
    :type init_mesh_t: float
    """

    data_handler: DataHandler
    mp: msh.MeshingParameters
    mesh_badness: float
    netgen_mesh: msh.Mesh
    mesh: ng.Mesh
    init_mesh_t: float

    def __init__(self,
                 data_handler: DataHandler) -> None:
        """Constructor method."""

        self.data_handler = data_handler

        self.mp = msh.MeshingParameters(
            curvaturesafety=2,
            segmentsperedge=1,
            grading=0.3,
            chartdistfac=1.5,
            linelengthfac=0.5,
            closeedgefac=2,
            minedgelen=0.2,
            surfmeshcurvfac=2.0,
            optsteps3d=1,
            optimize3d="m"
        )
        self.restrict_mesh(self.mp)

        self.netgen_mesh = msh.Mesh()
        self.mesh_badness = 0
        self.mesh = ng.Mesh(self.netgen_mesh)
        self.init_mesh_t = self.data_handler.sim_params().t0

    def init_mesh(self, mp: msh.MeshingParameters) -> List[Union[msh.Mesh, float]]:
        """Method to initialize the full mesh and geometry.

        :param mp: Meshing parameters.
        :type mp: netgen.mesh.MeshingParameters

        :return: Full mesh and its badness.
        :rtype: List[Union[netgen.meshing.Mesh, float]]
        """

        ng_geometry: CSGeometry = CSGeometry(self.data_handler)
        with TaskManager():
            net_mesh = ng_geometry.geometry.GenerateMesh(mp)
        init_badness = net_mesh.CalcTotalBadness(mp)

        return [net_mesh, init_badness]

    def update(self, t: float) -> None:
        """The method updates the mesh based on the current rotation angle of the gear theta. When possible, the gears
            mesh gets rotated and optimized. If the badness of the rotated mesh exceeds a certain badness, the full mesh
            gets rebuild.
        """

        temp_mesh = self.mesh.ngmesh.Copy()
        rebuild_mesh = True

        for component in self.data_handler.components():
            if isinstance(component, Gear):
                if component.rotate_mesh and temp_mesh.Points():
                    [temp_mesh, rotated_badness] = self.rotate_gear_mesh(temp_mesh, self.mp, component,
                                                                         self.data_handler, t)
                    print("Initial Badness: " + str(self.mesh_badness))
                    print("Badness after Rotation: " + str(rotated_badness))
                    print("Init Mesh T: " + str(self.init_mesh_t))
                    print("T: " + str(t))

                    if rotated_badness < self.mesh_badness * 1.1 and \
                            component.omega * t < component.omega * self.init_mesh_t + component.rotate_mesh_max_angle:
                        rebuild_mesh = False

        if rebuild_mesh:
            print("-------> Rebuild Mesh")
            [temp_mesh, self.mesh_badness] = self.init_mesh(self.mp)
            print("New Badness: " + str(self.mesh_badness))
            self.init_mesh_t = t

        self.netgen_mesh = temp_mesh.Copy()
        self.mesh = ng.Mesh(temp_mesh)

        ng.Redraw()

    @staticmethod
    def rotate_gear_mesh(mesh: msh.Mesh, mp: msh.MeshingParameters, gear: Gear, data_handler: DataHandler,
                         t: float) -> List[Union[msh.Mesh, float]]:
        """Method to rotate the gear in the mesh by one time step and optimize it.

        :param mesh: Netgen mesh.
        :type mesh: netgen.meshing.Mesh
        :param mp: Meshing parameters.
        :type mp: netgen.meshing.MeshingParameters
        :param gear: Global instance of the Gear class.
        :type gear: Gear
        :param data_handler: Object of the Data class containing all simulation relevant data.
        :type data_handler: DataHandler
        :param t: Current time stamp.
        :type t: float

        :return: The rotated and optimized mesh and its badness.
        :rtype: List[union[netgen.meshing.Mesh, float]]
        """

        position_t1 = gear.position(gear.theta)
        axis_t1 = gear.rotation_axis(gear.theta)
        if not np.isclose(t, data_handler.sim_params().t0):
            position_t0 = gear.position(gear.theta - gear.omega * data_handler.sim_params().dt)
            axis_t0 = gear.rotation_axis(gear.theta - gear.omega * data_handler.sim_params().dt)
            dt: float = data_handler.sim_params().dt
        else:
            position_t0 = position_t1
            axis_t0 = axis_t1
            dt: float = 0.0

        trans_matrix_t1 = gear.transformation_matrix(axis_t1)
        trans_matrix_t0 = gear.transformation_matrix(axis_t0)

        for num, p in enumerate(mesh.Points()):
            p_canonical: np.ndarray = np.linalg.inv(trans_matrix_t0).dot(np.array([p[0], p[1], p[2]]) - position_t0)
            if abs(p_canonical[2]) <= gear.length/2 * (1 + 1e-3) and sqrt(
                    pow(p_canonical[0], 2) + pow(p_canonical[1], 2)) <= (
                    gear.diameter[1] + gear.tooth_height)/2 * (1 + 1e-3):
                p_rotated: np.ndarray = gear.rotation_matrix(gear.omega*dt).dot(p_canonical)
                p_new: np.ndarray = trans_matrix_t1.dot(p_rotated)
                p[0] = p_new[0] + position_t1[0]
                p[1] = p_new[1] + position_t1[1]
                p[2] = p_new[2] + position_t1[2]

        mesh.OptimizeVolumeMesh(mp)
        badness: float = mesh.CalcTotalBadness(mp)
        return [mesh, badness]

    def restrict_mesh(self, mp: msh.MeshingParameters) -> None:
        """Restrict the maximum mesh size on chosen points of the grid.

        :param mp: Meshing parameters.
        :type mp: msh.MeshingParameters
        """

        for sensor in self.data_handler.field_recorders():
            for x in sensor.x:
                for y in sensor.y:
                    for z in sensor.z:
                        mp.RestrictH(x=x, y=y, z=z, h=sensor.maxh)

    @staticmethod
    def facedescriptor_list(mesh: msh.Mesh) -> list:
        """Return list of face descriptors of the mesh."""

        return [mesh.FaceDescriptor(fd_index) for fd_index in
                range(1, mesh.GetNFaceDescriptors() + 1)]

    def nr_bcs(self, mesh: msh.Mesh) -> int:
        """Return number of boundary conditions of the mesh."""

        return max((fd.bc for fd in self.facedescriptor_list(mesh)), default=0)

    def max_surfnr(self, mesh: msh.Mesh) -> int:
        """Return biggest surface number of occurring in mesh."""

        return max((fd.surfnr for fd in self.facedescriptor_list(mesh)), default=-1)

    @staticmethod
    def transfer_materials(mesh_to: msh.Mesh, mesh_from: msh.Mesh) -> None:
        """Transfers the materials from mesh_from to mesh_to."""

        from_mat: str = ""

        for from_idx in range(1, mesh_from.GetNDomains() + 1):
            from_mat = mesh_from.GetMaterial(from_idx)

        if from_mat:
            to_idx: int = mesh_to.AddRegion(from_mat, dim=3)
            mesh_to.SetMaterial(to_idx, from_mat)

    def add_fd(self, mesh_to: msh.Mesh, domin: int, domout: int, bcname: str):
        """Add the face descriptors related to bcname from mesh_from to mesh_to.
            Returns a map of the transferred surface numbers."""

        bc_offset: int = self.nr_bcs(mesh_to) + 1

        if self.max_surfnr(mesh_to) == -1:
            surfnr_offset: int = 0
        else:
            surfnr_offset: int = self.max_surfnr(mesh_to) + 1

        to_fd: msh.FaceDescriptor = msh.FaceDescriptor(domin=domin, domout=domout, surfnr=surfnr_offset, bc=bc_offset)
        mesh_to.Add(to_fd)
        mesh_to.SetBCName(to_fd.bc - 1, bcname)

    @staticmethod
    def pmap2d(mesh_to: msh.Mesh, mesh_from: msh.Mesh) -> Dict[int, int]:
        """Creates a dictionary mapping the indexes of points building elements of the input mesh to the output mesh.
            Only 2D elements are considered.

        :param mesh_to: Output mesh.
        :type mesh_to: msh.Mesh
        :param mesh_from: Input mesh.
        :type mesh_from: Output mesh.

        :return: Dictionary of the mapped indexes.
        :rtype: Dict[int, int]
        """

        pmap: Dict[int, int] = dict()
        points_to: List[Tuple[float, float]] = list()

        # Create list of tuples of points already in the target mesh.
        for p in mesh_to.Points():
            points_to.append((p[0], p[1]))  # Convert MeshPoint to tuple.

        for e in mesh_from.Elements2D():
            for v in e.vertices:
                if v not in pmap:
                    p_tuple: tuple = (mesh_from[v][0], mesh_from[v][1])  # Convert MeshPoint to tuple.
                    if p_tuple in points_to:
                        # Point already existing in the target mesh.
                        # Set map pointer to existing point.
                        for idx, p in enumerate(points_to):
                            if p_tuple == p:
                                pmap[v] = idx + 1  # Point indexes are 1-based.
                                break
                    else:
                        # Point not existing in the target mesh.
                        # Add point to the mesh and set the map pointer.
                        pmap[v] = mesh_to.Add(mesh_from[v])

        return pmap

    @staticmethod
    def pmap3d(mesh_to: msh.Mesh, mesh_from: msh.Mesh) -> Dict[int, int]:
        """Creates a dictionary mapping the indexes of points building elements of the input mesh to the output mesh.
            Considers 2D and 3D elements.

        :param mesh_to: Output mesh.
        :type mesh_to: msh.Mesh
        :param mesh_from: Input mesh.
        :type mesh_from: Output mesh.

        :return: Dictionary of the mapped indexes.
        :rtype: Dict[int, int]
        """

        pmap: Dict[int, int] = dict()
        points_to: List[Tuple[float, float, float]] = list()

        # Create list of tuples of points already in the target mesh.
        for p in mesh_to.Points():
            points_to.append((p[0], p[1], p[2]))  # Convert MeshPoint to tuple.

        for e in mesh_from.Elements3D():
            for v in e.vertices:
                if v not in pmap:
                    p_tuple: tuple = (mesh_from[v][0], mesh_from[v][1], mesh_from[v][2])  # Convert MeshPoint to tuple.
                    if p_tuple in points_to:
                        # Point already existing in the target mesh.
                        # Set map pointer to existing point.
                        for idx, p in enumerate(points_to):
                            if p_tuple == p:
                                pmap[v] = idx + 1  # Point indexes are 1-based.
                                break
                    else:
                        # Point not existing in the target mesh.
                        # Add point to the mesh and set the map pointer.
                        pmap[v] = mesh_to.Add(mesh_from[v])

        return pmap

    def copy_2d(self, mesh_to: msh.Mesh, mesh_from: msh.Mesh, pmap: Dict[int, int], domin: int, domout: int,
                bcname: str) -> None:
        """Method to copy 2D elements from one mesh to another.

        :param mesh_to: Output mesh.
        :type mesh_to: msh.Mesh
        :param mesh_from: Input mesh.
        :type mesh_from: Output mesh.
        :param pmap: Dictionary of the mapped indexes.
        :type pmap: Dict[int, int]
        :param domin: Domain of the 3D elements enclosed by the copied 2D elements.
        :type domin: int
        :param domout: Domain of the 3D elements enclosing the copied 2D elements.
        :type domout: int
        :param bcname: Name of the boundary which is built by the copied 2D elements.
        :type bcname: str
        """

        fd_offset: int = mesh_to.GetNFaceDescriptors()
        self.add_fd(mesh_to, domin, domout, bcname)
        for e in mesh_from.Elements2D():
            mesh_to.Add(msh.Element2D(fd_offset + 1, [pmap[v] for v in e.vertices]))

    def copy_3d(self, mesh_to: msh.Mesh, mesh_from: msh.Mesh, pmap: Dict[int, int]):
        """Method to copy 3D elements from one mesh to another.

        :param mesh_to: Output mesh.
        :type mesh_to: msh.Mesh
        :param mesh_from: Input mesh.
        :type mesh_from: Output mesh.
        :param pmap: Dictionary of the mapped indexes.
        :type pmap: Dict[int, int]
        """

        mat_offset: int = mesh_to.GetNDomains()
        self.transfer_materials(mesh_to, mesh_from)

        for e in mesh_from.Elements3D():
            mesh_to.Add(msh.Element3D(e.index + mat_offset, [pmap[v] for v in e.vertices]))

    def copy_surface(self, mesh_to: msh.Mesh, mesh_from: msh.Mesh, domin: int, domout: int, bcname: str) -> None:
        """Method to copy an entire surface of a solid body.

        :param mesh_to: Output mesh.
        :type mesh_to: msh.Mesh
        :param mesh_from: Input mesh.
        :type mesh_from: Output mesh.
        :param domin: Domain of the 3D elements enclosed by the copied 2D elements.
        :type domin: int
        :param domout: Domain of the 3D elements enclosing the copied 2D elements.
        :type domout: int
        :param bcname: Name of the boundary which is built by the copied 2D elements.
        :type bcname: str
        """

        pmap = self.pmap2d(mesh_to, mesh_from)
        self.copy_2d(mesh_to, mesh_from, pmap, domin, domout, bcname)

    def copy_mesh(self, mesh_to: msh.Mesh, mesh_from: msh.Mesh, domin: int, domout: int, bcname: str) -> None:
        """Method to copy an entire mesh including 2D and 3D elements.

        :param mesh_to: Output mesh.
        :type mesh_to: msh.Mesh
        :param mesh_from: Input mesh.
        :type mesh_from: Output mesh.
        :param domin: Domain of the 3D elements enclosed by the copied 2D elements.
        :type domin: int
        :param domout: Domain of the 3D elements enclosing the copied 2D elements.
        :type domout: int
        :param bcname: Name of the boundary which is built by the copied 2D elements.
        :type bcname: str
        """

        pmap = self.pmap3d(mesh_to, mesh_from)
        self.copy_3d(mesh_to, mesh_from, pmap)
        self.copy_2d(mesh_to, mesh_from, pmap, domin, domout, bcname)

    @staticmethod
    def mesh_diagnose(mesh: msh.Mesh, description: str = ""):
        """Print several mesh parameters mainly for the purpose of debugging.

        :param mesh: Mesh investigated.
        :type mesh: msh.Mesh
        :param description: Name to identify the printed mesh parameters in case of multiple method calls.
        :type description: str
        """

        print("############################################################")
        print(description)
        print("Domains: " + str(mesh.GetNDomains()))
        for idx in range(1, mesh.GetNDomains() + 1):
            print(str(idx) + ", Mat: " + mesh.GetMaterial(idx))

        print("FaceDescriptors: " + str(mesh.GetNFaceDescriptors()))
        #for i in range(1, mesh.GetNFaceDescriptors() + 1):
        #    print([i, mesh.FaceDescriptor(i)])

        elmts: int = 0
        for e in mesh.Elements2D():
            elmts += 1
        print("2D Elements: " + str(elmts))

        elmts: int = 0
        for e in mesh.Elements3D():
            elmts += 1
        print("3D Elements: " + str(elmts))

        print("############################################################")

    @staticmethod
    def aspect_ratio(mesh: msh.Mesh):
        """ Calculates the maximum aspect ratio of the edges in the cells of the mesh.

        :param mesh: Netgen Mesh
        :type mesh: netgen.meshing.Mesh

        :return: The maximum ratio of all cell edge length ratios in the mesh.
        :rtype: float
        """

        ratios: List = list()

        for el in mesh.Elements3D():
            vertices: List = list()
            for vertex in el.vertices:
                vertices.append(np.array([mesh[vertex][0], mesh[vertex][1], mesh[vertex][2]]))
            edge_lengths: List = list()
            for i1, v1 in enumerate(vertices):
                for i2, v2 in enumerate(vertices[i1+1:]):
                    edge_lengths.append(np.linalg.norm(v1-v2))

            ratios.append(max(edge_lengths)/min(edge_lengths))

        return max(ratios)

    @staticmethod
    def skewness(mesh: msh.Mesh):
        """ Calculates the maximum skewness of the edges in the cells of the mesh.

        :param mesh: Netgen Mesh
        :type mesh: netgen.meshing.Mesh

        :return: The maximum skewness of all cells in the mesh.
        :rtype: float
        """

        skew: List = list()

        for el in mesh.Elements3D():
            vertices_list: List = list()
            for vertex in el.vertices:
                vertices_list.append(np.array([mesh[vertex][0], mesh[vertex][1], mesh[vertex][2]]))
            vertices = np.row_stack((vertices_list[0], vertices_list[1], vertices_list[2], vertices_list[3]))

            # hard coded because the order of the edges is important to calculate the radius
            edge_lengths: List = list()
            edge_lengths.append(np.linalg.norm(vertices_list[0] - vertices_list[1]))
            edge_lengths.append(np.linalg.norm(vertices_list[0] - vertices_list[2]))
            edge_lengths.append(np.linalg.norm(vertices_list[0] - vertices_list[3]))
            edge_lengths.append(np.linalg.norm(vertices_list[2] - vertices_list[3]))
            edge_lengths.append(np.linalg.norm(vertices_list[1] - vertices_list[3]))
            edge_lengths.append(np.linalg.norm(vertices_list[1] - vertices_list[2]))

            matrix = np.column_stack((np.array([1, 1, 1, 1]), vertices))

            delta_abs = np.linalg.norm(np.linalg.det(matrix))

            cell_size = delta_abs/6

            p = (edge_lengths[0]*edge_lengths[3] + edge_lengths[1]*edge_lengths[4] + edge_lengths[2]*edge_lengths[5])/2

            radius = sqrt(p*(p-edge_lengths[0]*edge_lengths[3])*(p-edge_lengths[1]*edge_lengths[4])*(
                    p-edge_lengths[2]*edge_lengths[5]))/delta_abs

            optimal_size = pow(4/sqrt(6)*radius, 3)*sqrt(2)/12

            skew.append((optimal_size-cell_size)/optimal_size)

        return max(skew)

    @staticmethod
    def smoothness(mesh: msh.Mesh):
        """To be implemented."""
        pass