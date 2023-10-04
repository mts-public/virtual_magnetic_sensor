from __future__ import annotations
import numpy as np
from math import sin, cos, tan, radians, degrees
from typing import Dict

from libs.elements.Component import Component


class Gear(Component):
    """Contains all the parameters to describe the position, rotation, shape and movement of the gear in the simulation.
    
    :param pos: Position of the gear in the 3D space.
    :type pos: numpy.ndarray
    :param axis_0: The direction of the rotation axis of the gear without wobbling.
    :type axis_0: numpy.ndarray
    :param omega: Angular velocity of the gear.
    :type omega: float
    :param diameter: Inner and outer diameter of the gear.
    :type diameter: float
    :param length: Length of the gear.
    :type length: float
    :param tooth_height: Tooth height.
    :type tooth_height: float
    :param tooth_width: Tooth width.
    :type tooth_width: float
    :param n: Total number of teeth.
    :type n: int
    :param display_teeth_angle: Opening angle related to the sensors position in which the gear teeth are drawn.
    :type display_teeth_angle: np.ndarray
    :param tooth_flank_angle: Tooth flank angle in radians.
    :type tooth_flank_angle: float
    :param mu_r: Permeability of the gear.
    :type mu_r: float
    :param eccentricity: Rotation eccentricity of the gear.
    :type eccentricity: float
    :param wobble_angle: Wobble angle around the rotation axis in radians.
    :type wobble_angle: float
    :param chamfer_depth: Extension of the phase along the phases normal.
    :type chamfer_depth: float
    :param chamfer_angle: Angle of the chamfer based on the flanks.
    :type chamfer_angle: float
    :param dev_tooth_num: Number of the tooth with deviating geometry.
    :type dev_tooth_num: int
    :param tooth_deviations: Array containing the tooth deviations specified by n_dev. The first entry describes the deviation of the
        left flank, the middle entry the top deviation and the last entry describes the deviation of the right flank.
    :type tooth_deviations: numpy.ndarray
    :param maxh: Mesh size of the gear.
    :type maxh: float
    :param rotate_mesh: Specifies wether to use the rotated mesh approach or to build up the mesh at every time step
        from scratch for the specific gear.
    :type rotate_mesh: bool
    :param rotate_mesh_max_angle: Maximum permissible angle of rotation of the gear before the mesh is rebuilt.
    :type rotate_mesh_max_angle: float
    :param theta: Current rotation angle of the gear.
    :type theta: float
    """

    pos: np.ndarray
    axis_0: np.ndarray
    omega: float
    diameter: np.ndarray
    length: float
    tooth_height: float
    tooth_width: float
    n: int
    display_teeth_angle: np.ndarray
    tooth_flank_angle: float
    mu_r: float
    eccentricity: float
    wobble_angle: float
    chamfer_depth: float
    chamfer_angle: float
    dev_tooth_num: int
    tooth_deviations: np.ndarray
    maxh: float
    rotate_mesh: bool
    rotate_mesh_max_angle: float
    theta: float

    def __init__(self,
                 pos: np.ndarray,
                 axis_0: np.ndarray,
                 omega: float,
                 diameter: np.ndarray,
                 length: float,
                 tooth_height: float,
                 tooth_width: float,
                 n: int,
                 display_teeth_angle: np.ndarray,
                 tooth_flank_angle: float,
                 mu_r: float,
                 eccentricity: float,
                 wobble_angle: float,
                 chamfer_depth: float,
                 chamfer_angle: float,
                 dev_tooth_num: int,
                 tooth_deviations: np.ndarray,
                 maxh: float,
                 rotate_mesh: bool,
                 rotate_mesh_max_angle: float,
                 theta: float = None) -> None:
        """Constructor method."""

        super().__init__(pos, mu_r, maxh)
        self.axis_0 = axis_0
        self.omega = omega
        self.diameter = diameter
        self.length = length
        self.tooth_height = tooth_height
        self.tooth_width = tooth_width
        self.n = n
        self.display_teeth_angle = display_teeth_angle
        self.tooth_flank_angle = tooth_flank_angle
        self.eccentricity = eccentricity
        self.wobble_angle = wobble_angle
        self.chamfer_depth = chamfer_depth
        self.chamfer_angle = chamfer_angle
        self.dev_tooth_num = dev_tooth_num
        self.tooth_deviations = tooth_deviations
        self.rotate_mesh = rotate_mesh
        self.rotate_mesh_max_angle = rotate_mesh_max_angle

        self.theta = 0.0

    @classmethod
    def template(cls) -> Gear:
        """Class method to init the class with a set of standard values.

        :return: Object of the Gear class.
        :rtype: Gear
        """

        return cls(pos=np.array([0.0, 0.0, 0.0]),
                   axis_0=np.array([0.0, 0.0, 1.0]),
                   omega=radians(11.25),
                   diameter=np.array([1.0, 10.0]),
                   length=1.0,
                   tooth_height=1.0,
                   tooth_width=0.333,
                   n=32,
                   display_teeth_angle=np.radians(np.array([0.0, 360.0])),
                   tooth_flank_angle=radians(10.0),
                   mu_r=4000.0,
                   eccentricity=0.0 * 1e-3,
                   wobble_angle=radians(0.0),
                   chamfer_depth=0.0 * 1e-3,
                   chamfer_angle=radians(45.0),
                   dev_tooth_num=1,
                   tooth_deviations=np.array([0.0, 0.0, 0.0]) * 1e-3,
                   maxh=2.0,
                   rotate_mesh=True,
                   rotate_mesh_max_angle=radians(3.0))

    @classmethod
    def from_dict(cls, dictionary: Dict[any]) -> Gear:
        """Method to init an instance of the Gear class by passing a dictionary with the corresponding
            arguments. Arguments that are in the dictionary and not in the class are ignored while arguments missing in
            the dictionary get initialised with the standard values defined in the template class method.

        :return: Instance of the Gear class.
        :rtype: Gear
        """

        template = Gear.template()

        for key, value in dictionary.items():
            if hasattr(template, key):
                setattr(template, key, value)

        return cls(**template.to_dict())

    def to_dict(self) -> Dict[str, any]:
        """Method creates a dictionary of the class members that will be stored in the HDF5 file. Variables created
            automatically when instantiating an object of the class are excluded from the dictionary. This creates the
            opportunity to initiate an instance of the class by parsing the dictionary as argument.

        :return: The dictionary of the classes members.
        :rtype: Dict[str, any]
        """

        dictionary: dict = vars(self).copy()
        dictionary.pop('theta', None)

        return dictionary

    def gui_dict(self) -> Dict[str, any]:
        """Method creates a dictionary of the class members that will be stored in the HDF5 file. Variables created
            automatically when instantiating an object of the class are excluded from the dictionary. This creates the
            opportunity to initiate an instance of the class by parsing the dictionary as argument.

        :return: The dictionary of the classes members.
        :rtype: Dict[str, any]
        """

        dictionary: dict = vars(self.gui()).copy()
        dictionary.pop('theta', None)

        return dictionary

    def ini_dict(self) -> Dict[str, any]:
        """Method creates a dictionary of the class members that will be stored in the HDF5 file. Variables created
            automatically when instantiating an object of the class are excluded from the dictionary. This creates the
            opportunity to initiate an instance of the class by parsing the dictionary as argument.

        :return: The dictionary of the classes members.
        :rtype: Dict[str, any]
        """

        dictionary: dict = vars(self.gui()).copy()
        dictionary.pop('theta', None)

        return dictionary

    def reset(self):
        """Calls the init method with the actual class attributes."""
        self.__init__(self.pos, self.axis_0, self.omega, self.diameter, self.length,
                      self.tooth_height, self.tooth_width, self.n, self.display_teeth_angle, self.tooth_flank_angle,
                      self.mu_r, self.eccentricity, self.wobble_angle, self.chamfer_depth, self.chamfer_angle,
                      self.dev_tooth_num, self.tooth_deviations, self.maxh, self.rotate_mesh,
                      self.rotate_mesh_max_angle)

    def convert_to_si(self) -> None:
        """Calls the init method and converts the parameters from gui units to SI units."""

        self.__init__(self.pos,
                      self.axis_0,
                      radians(self.omega),
                      self.diameter,
                      self.length,
                      self.tooth_height,
                      self.tooth_width,
                      self.n,
                      np.radians(self.display_teeth_angle),
                      radians(self.tooth_flank_angle),
                      self.mu_r,
                      self.eccentricity * 1e-3,
                      radians(self.wobble_angle),
                      self.chamfer_depth * 1e-3,
                      radians(self.chamfer_angle),
                      self.dev_tooth_num,
                      self.tooth_deviations * 1e-3,
                      self.maxh,
                      self.rotate_mesh,
                      radians(self.rotate_mesh_max_angle))

    def gui(self) -> Gear:
        """Returns a copy of the class with attributes converted to units used in the gui."""

        return Gear(self.pos,
                    self.axis_0,
                    degrees(self.omega),
                    self.diameter,
                    self.length,
                    self.tooth_height,
                    self.tooth_width,
                    self.n,
                    np.degrees(self.display_teeth_angle),
                    degrees(self.tooth_flank_angle),
                    self.mu_r,
                    self.eccentricity * 1e3,
                    degrees(self.wobble_angle),
                    self.chamfer_depth * 1e3,
                    degrees(self.chamfer_angle),
                    self.dev_tooth_num,
                    self.tooth_deviations * 1e3,
                    self.maxh,
                    self.rotate_mesh,
                    degrees(self.rotate_mesh_max_angle))

    def update(self, t: float) -> None:
        """Method to update the gear rotation angle theta for the next simulation step.

        :param t: Current time stamp.
        :type t: float
        """

        self.theta = self.omega * t

    def position(self, angle: float) -> np.ndarray:
        """Method to calculate the angle based center of the gear with eccentricity.

        :param angle: Gear rotation angle.
        :type angle: float
        :return: Gear position with eccentricity.
        :rtype: numpy.ndarray
        """

        pos = self.pos + self.eccentricity_vector(angle)

        return pos

    @staticmethod
    def transformation_matrix(axis: np.ndarray) -> np.ndarray:
        """Method for calculating the transformation matrix to transform the global coordinate system into the
            body-fixed coordinate system, where the z-axis points in the direction of the rotation axis.

        :param axis: The rotation axis of the gear.
        :type axis: numpy.ndarray
        :return: The transformation matrix.
        :rtype: numpy.ndarray
        """

        z_vec: np.ndarray = axis / np.linalg.norm(axis)

        if z_vec[0] != 0 or z_vec[1] != 0:
            x_vec: np.ndarray = np.array([z_vec[2], 0, -z_vec[0]])
        else:
            x_vec: np.ndarray = np.array([z_vec[2], 0.0, 0.0])
        x_vec /= np.linalg.norm(x_vec)
        y_vec: np.ndarray = np.cross(x_vec, z_vec)
        y_vec /= np.linalg.norm(y_vec)

        return np.column_stack((x_vec, y_vec, z_vec))

    def rotation_axis(self, angle: float) -> np.ndarray:
        """Method to calculate the final rotation axis considering the wobble angle.

        :param angle: Gear rotation angle.
        :type angle: float
        :return: Final rotation axis including the wobble angle.
        :rtype: numpy.ndarray
        """

        axis = self.axis_0 + tan(self.wobble_angle) * np.linalg.norm(self.axis_0) * self.transformation_matrix(
            self.axis_0).dot(np.array([cos(angle), sin(angle), 0.0]))
        axis /= np.linalg.norm(axis)

        return axis

    @staticmethod
    def rotation_matrix(angle: float) -> np.ndarray:
        """Method to calculate the rotation matrix of the gear.

        :param angle: Gear rotation angle.
        :type angle: float
        :return: Rotation matrix of the gear.
        :rtype: numpy.ndarray
        """

        matrix: np.ndarray = np.array([[cos(angle), -sin(angle), 0.0], [sin(angle), cos(angle), 0.0], [0.0, 0.0, 1.0]])

        return matrix

    def eccentricity_vector(self, angle: float) -> np.ndarray:
        """Method for calculation the eccentricity vector containing the position shift along the three coordinate
            system axes due eccentricity.

        :param angle: Gear rotation angle.
        :type angle: float
        :return: Eccentricity vector.
        :rtype: numpy.ndarray
        """

        return self.eccentricity * self.transformation_matrix(
            self.rotation_axis(angle)).dot(np.array([cos(angle), sin(angle), 0.0]))
