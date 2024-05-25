from __future__ import annotations
import numpy as np
from math import sin, cos, tan, radians, degrees
from typing import Dict

from libs.elements.Component import Component


class EvoGear(Component):
    """Contains all the parameters to describe the position, rotation, shape and movement of the gear in the simulation.
    
    :param pos: Position of the gear in the 3D space.
    :type pos: numpy.ndarray
    :param axis_0: The direction of the rotation axis of the gear without wobbling.
    :type axis_0: numpy.ndarray
    :param omega: Angular velocity of the gear.
    :type omega: float
    :param diameter: Inner and outer diameter of the cylinderbody .
    :type diameter: float
    :param length: Length of the gear.
    :type length: float
    :param n: Total number of teeth.
    :type n: int
    :param display_teeth_angle: Opening angle related to the sensors position in which the gear teeth are drawn.
    :type display_teeth_angle: np.ndarray
    :param alpha: normal pressure angle in radians.
    :type alpha: float
    :param mu_r: Permeability of the gear.
    :type mu_r: float
    :param eccentricity: Rotation eccentricity of the gear.
    :type eccentricity: float
    :param wobble_angle: Wobble angle around the rotation axis in radians.
    :type wobble_angle: float
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
    :param involute_points: Number of knots of the spline interpolation of the Involute.
    :type involute_points: int
    
    :param damage_index:
    :type damage_index: int
    :param damage_parameter_dict:
    :type damage_parameter_dict: dict
    
    :param theta: Current rotation angle of the gear.
    :type theta: float
    """

    pos: np.ndarray
    axis_0: np.ndarray
    omega: float
    diameter: np.ndarray
    length: float
    n: float
    display_teeth_angle: np.ndarray
    alpha:  float
    x: float
    d:  float
    m:  float
    n_gr: float
    d_a: float
    d_f: float
    inv_alpha: float
    s: float
    mu_r: float
    eccentricity: float
    wobble_angle: float
    dev_tooth_num: int
    tooth_deviations: np.ndarray
    maxh: float
    rotate_mesh: bool
    rotate_mesh_max_angle: float
    involute_points: int
    theta: float
    damage_index: int
    damage_parameter_dict: dict

    def __init__(self,
                 pos: np.ndarray,
                 axis_0: np.ndarray,
                 omega: float,
                 diameter: np.ndarray,
                 length: float,
                 n: float,
                 display_teeth_angle: np.ndarray,
                 alpha: float,
                 x:float,
                 mu_r: float,
                 eccentricity: float,
                 wobble_angle: float,
                 dev_tooth_num: int,
                 tooth_deviations: np.ndarray,
                 maxh: float,
                 rotate_mesh: bool,
                 rotate_mesh_max_angle: float,
                 involute_points: int,
                 damage_index: int,
                 damage_parameter_dict: dict,
                 theta: float) -> None:
        
        """Constructor method."""

        super().__init__(pos, mu_r, maxh)
        self.axis_0 = axis_0
        self.omega = omega
        self.diameter = diameter
        self.length = length
        self.n = n
        self.display_teeth_angle = display_teeth_angle
        self.alpha = alpha
        self.x = x
        self.d = diameter[1] / (1 - (2 / self.n) * ((5 / 4) - self.x))
        self.m = self.d / n
        self.n_gr = (2 * (1 - self.x)) / pow(sin(self.alpha), 2)
        self.d_a = self.d + 2 * self.m + 2 * self.x * self.m
        self.d_b = self.d * np.cos(self.alpha)
        self.d_f = self.diameter[1]
        self.inv_alpha = np.tan(self.alpha) - self.alpha
        self.s = self.m * np.pi / 2
        self.eccentricity = eccentricity
        self.wobble_angle = wobble_angle
        self.dev_tooth_num = dev_tooth_num
        self.tooth_deviations = tooth_deviations
        self.rotate_mesh = rotate_mesh
        self.rotate_mesh_max_angle = rotate_mesh_max_angle
        self.involute_points = involute_points
        self.damage_index = damage_index
        self.damage_parameter_dict=damage_parameter_dict
        
        self.theta = theta
    
    @classmethod
    def template(cls) -> EvoGear:
        """Class method to init the class with a set of standard values.

        :return: Object of the EvoGear class.
        :rtype: Evogear
        """

        return cls(pos=np.array([0.0, 0.0, 0.0]),
                   axis_0=np.array([0.0, 0.0, 1.0]),
                   omega=radians(11.25),
                   diameter=np.array([1.0, 10.0]),
                   length=1.0,
                   n=32,
                   display_teeth_angle=np.radians(np.array([0.0, 360.0])),
                   alpha=radians(20),
                   x=0.0,
                   mu_r=4000.0,
                   eccentricity=0.0 * 1e-3,
                   wobble_angle=radians(0.0),
                   dev_tooth_num=1,
                   tooth_deviations=np.array([0.0, 0.0, 0.0]) * 1e-3,
                   maxh=2.0,
                   rotate_mesh=True,
                   rotate_mesh_max_angle=radians(3.0),
                   involute_points=7,
                   damage_index=0,
                   damage_parameter_dict={},
                   theta=0.0)

    @classmethod
    def from_dict(cls, dictionary: Dict[any]) -> EvoGear:
        """Method to init an instance of the Gear class by passing a dictionary with the corresponding
            arguments. Arguments that are in the dictionary and not in the class are ignored while arguments missing in
            the dictionary get initialised with the standard values defined in the template class method.

        :return: Instance of the Gear class.
        :rtype: Gear
        """
        
        template = EvoGear.template()

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
        
        #dictionary.pop('damage_index',None)
        #dictionary.pop('x', None)
        dictionary.pop('d', None)
        dictionary.pop('m', None)
        dictionary.pop('n_gr', None)
        dictionary.pop('d_a', None)
        dictionary.pop('d_b', None)
        dictionary.pop('d_f', None)
        dictionary.pop('inv_alpha', None)
        dictionary.pop('s', None)

        return dictionary

    def gui_dict(self) -> Dict[str, any]:
        """Method creates a dictionary of the class members that will be stored in the HDF5 file. Variables created
            automatically when ins:tantiating an object of the class are excluded from the dictionary. This creates the
            opportunity to initiate an instance of the class by parsing the dictionary as argument.

        :return: The dictionary of the classes members.
        :rtype: Dict[str, any]
        """
        
        dictionary: dict = vars(self.gui()).copy()
        
        dictionary.pop('x', None)
        dictionary.pop('d', None)
        dictionary.pop('m', None)
        dictionary.pop('n_gr', None)
        dictionary.pop('d_a', None)
        dictionary.pop('d_b', None)
        dictionary.pop('d_f', None)
        dictionary.pop('inv_alpha', None)
        dictionary.pop('s', None)
        return dictionary

    def reset(self):
        """Calls the init method with the actual class attributes."""
        
        self.__init__(self.pos, self.axis_0, self.omega, self.diameter, self.length, self.n, self.display_teeth_angle,
                      self.alpha,self.x,self.mu_r, self.eccentricity, self.wobble_angle, self.dev_tooth_num,
                      self.tooth_deviations, self.maxh, self.rotate_mesh, self.rotate_mesh_max_angle,
                      self.involute_points,self.damage_index,self.damage_parameter_dict,self.theta)

    def convert_to_si(self) -> None:
        """Calls the init method and converts the parameters from gui units to SI units."""
        
        self.__init__(self.pos,
                      self.axis_0,
                      radians(self.omega),
                      self.diameter,
                      self.length,
                      self.n,
                      np.radians(self.display_teeth_angle),
                      radians(self.alpha),
                      self.x,
                      self.mu_r,
                      self.eccentricity * 1e-3,
                      radians(self.wobble_angle),
                      self.dev_tooth_num,
                      self.tooth_deviations * 1e-3,
                      self.maxh,
                      self.rotate_mesh,
                      radians(self.rotate_mesh_max_angle),
                      self.involute_points,
                      self.damage_index,
                      self.damage_parameter_dict,
                      self.theta)

    def gui(self) -> EvoGear:
        """Returns a copy of the class with attributes converted to units used in the gui."""
        
        return EvoGear(self.pos,
                       self.axis_0,
                       degrees(self.omega),
                       self.diameter,
                       self.length,
                       self.n,
                       np.degrees(self.display_teeth_angle),
                       degrees(self.alpha),
                       self.x,
                       self.mu_r,
                       self.eccentricity * 1e3,
                       degrees(self.wobble_angle),
                       self.dev_tooth_num,
                       self.tooth_deviations * 1e3,
                       self.maxh,
                       self.rotate_mesh,
                       degrees(self.rotate_mesh_max_angle),
                       self.involute_points,
                       self.damage_index,
                       self.damage_parameter_dict)

    def update(self, t: float) -> None:
        """Method to update the gear rotation angle theta for the next simulation step.

        :param t: Current time stamp.
        :type t: float
        """

        self.theta = self.omega * t

    def position(self, angle: float) -> np.ndarray:
        """Method to calculate the angle based center of the EvoGear with eccentricity.

        :param angle: EvoGear rotation angle.
        :type angle: float
        :return: EvoGear position with eccentricity.
        :rtype: numpy.ndarray
        """

        pos = self.pos + self.eccentricity_vector(angle)

        return pos

    @staticmethod
    def transformation_matrix(axis: np.ndarray) -> np.ndarray:
        """Method for calculating the transformation matrix to transform the global coordinate system into the
            body-fixed coordinate system, where the z-axis points in the direction of the rotation axis.

        :param axis: The rotation axis of the EvoGear.
        :type axis: numpy.ndarray
        :return: The transformation matrix.
        :rtype: numpy.ndarray
        """

        if (axis == np.array([0.0, 0.0, 1.0])).all():
            return np.eye(3)
        elif (axis == np.array([0.0, 0.0, -1.0])).all():
            return -np.eye(3)
        else:
            z_vec: np.ndarray = axis / np.linalg.norm(axis)
            x_vec = np.cross(np.array([0.0, 0.0, -1.0]), z_vec)
            x_vec /= np.linalg.norm(x_vec)
            y_vec = np.cross(z_vec, x_vec)
            return np.column_stack((x_vec, y_vec, z_vec))

    def rotation_axis(self, angle: float) -> np.ndarray:
        """Method to calculate the final rotation axis considering the wobble angle.

        :param angle: EvoGear rotation angle.
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
        """Method to calculate the rotation matrix of the EvoGear.

        :param angle: EvoGear rotation angle.
        :type angle: float
        :return: Rotation matrix of the EvoGear.
        :rtype: numpy.ndarray
        """

        matrix: np.ndarray = np.array([[cos(angle), -sin(angle), 0.0], 
                                       [sin(angle), cos(angle), 0.0], 
                                       [0.0, 0.0, 1.0]])

        return matrix

    def eccentricity_vector(self, angle: float) -> np.ndarray:
        """Method for calculation the eccentricity vector containing the position shift along the three coordinate
            system axes due eccentricity.

        :param angle: EvoGear rotation angle.
        :type angle: float
        :return: Eccentricity vector.
        :rtype: numpy.ndarray
        """

        return self.eccentricity * self.transformation_matrix(
            self.rotation_axis(angle)).dot(np.array([cos(angle), sin(angle), 0.0]))
        
    def coordinates(self, points: int) -> np.array:
        """Method to calculate coordinates of the involute function.

        :param points: How many points are being used to calculate the involute >=5
        :return: Coordinates Array
        :rtype: numpy.array
        """

        r_x = np.linspace(self.d_b/2, self.d_a/2, num=points,
                          endpoint=True, retstep=False, dtype=None, axis=0)
        alpha_x = np.arccos(self.d_b/(2*r_x))
        inv_alpha_x = np.tan(alpha_x)-alpha_x
        s_x = r_x * ((np.pi+4*self.x*np.tan(self.alpha))/(2*self.n)+self.inv_alpha-inv_alpha_x)
        coordinates: np.array = np.column_stack((s_x, -s_x, r_x))
        
        return coordinates

    