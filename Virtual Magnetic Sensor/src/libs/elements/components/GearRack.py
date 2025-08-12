from __future__ import annotations
import numpy as np
from math import sin, cos, radians, degrees
from typing import Dict

from libs.elements.Component import Component


class GearRack(Component):
    """Contains all the parameters to describe the position, rotation, shape and movement of the gear in the simulation.

    :param pos: Position of the gear in the 3D space.
    :type pos: numpy.ndarray
    :param dim: Dimension of the gear rack body along the body-fixed coordinate axes.
    :type dim: numpy.ndarray
    :param rot: Rotation of the gear rack in the 3D space in radians.
    :type rot: numpy.ndarray
    :param velocity: Velocity of the gear rack along the global coordinate axes.
    :type velocity: np.ndarray
    :param tooth_height: Tooth height.
    :type tooth_height: float
    :param tooth_width: Tooth width.
    :type tooth_width: float
    :param tooth_pitch: Distance between two adjacent teeth.
    :type tooth_pitch: float
    :param tooth_flank_angle: Tooth flank angle in radians.
    :type tooth_flank_angle: float
    :param mu_r: Permeability of the gear.
    :type mu_r: float
    :param chamfer_depth: Extension of the phase along the phases normal.
    :type chamfer_depth: float
    :param chamfer_angle: Angle of the chamfer based on the flanks.
    :type chamfer_angle: float
    :param maxh: Mesh size of the gear.
    :type maxh: float
    :param pos: Current position of the gear rack.
    :type pos: np.ndarray
    """

    pos: np.ndarray
    dim: np.ndarray
    rot: np.ndarray
    velocity: np.ndarray
    tooth_height: float
    tooth_width: float
    tooth_pitch: float
    tooth_flank_angle: float
    mu_r: float
    chamfer_depth: float
    chamfer_angle: float
    maxh: float

    def __init__(self,
                 pos: np.ndarray,
                 dim: np.ndarray,
                 rot: np.ndarray,
                 velocity: np.ndarray,
                 tooth_height: float,
                 tooth_width: float,
                 tooth_pitch: float,
                 tooth_flank_angle: float,
                 mu_r: float,
                 chamfer_depth: float,
                 chamfer_angle: float,
                 maxh: float,
                 shift: np.ndarray = None) -> None:
        """Constructor method."""

        super().__init__(pos, mu_r, maxh)
        self.dim = dim
        self.rot = rot
        self.velocity = velocity
        self.tooth_height = tooth_height
        self.tooth_width = tooth_width
        self.tooth_pitch = tooth_pitch
        self.tooth_flank_angle = tooth_flank_angle
        self.chamfer_depth = chamfer_depth
        self.chamfer_angle = chamfer_angle

        self.shift = np.array([0.0, 0.0, 0.0])

    @classmethod
    def template(cls) -> GearRack:
        """Class method to init the class with a set of standard values.

        :return: Object of the GearRack class.
        :rtype: GearRack
        """

        return cls(pos=np.array([0.0, 0.0, 0.0]),
                   dim=np.array([10.0, 1.0, 1.0]),
                   rot=np.array([0.0, 0.0, 0.0]),
                   velocity=np.array([0.1, 0.0, 0.0]),
                   tooth_height=1.0,
                   tooth_width=0.333,
                   tooth_pitch=1.0,
                   tooth_flank_angle=radians(10.0),
                   mu_r=4000.0,
                   chamfer_depth=0.0 * 1e-3,
                   chamfer_angle=radians(45.0),
                   maxh=2.0)

    @classmethod
    def from_dict(cls, dictionary: Dict[any]) -> GearRack:
        """Method to init an instance of the Gear class by passing a dictionary with the corresponding
            arguments. Arguments that are in the dictionary and not in the class are ignored while arguments missing in
            the dictionary get initialised with the standard values defined in the template class method.

        :return: Instance of the GearRack class.
        :rtype: GearRack
        """

        template = GearRack.template()

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

        return dictionary

    def gui_dict(self) -> Dict[str, any]:
        """Method creates a dictionary of the class members that will be stored in the HDF5 file. Variables created
            automatically when instantiating an object of the class are excluded from the dictionary. This creates the
            opportunity to initiate an instance of the class by parsing the dictionary as argument.

        :return: The dictionary of the classes members.
        :rtype: Dict[str, any]
        """

        dictionary: dict = vars(self.gui()).copy()

        return dictionary

    def reset(self):
        """Calls the init method with the actual class attributes."""
        self.__init__(self.pos, self.dim, self.rot, self.velocity, self.tooth_height, self.tooth_width,
                      self.tooth_pitch, self.tooth_flank_angle, self.mu_r, self.chamfer_depth, self.chamfer_angle,
                      self.maxh)

    def convert_to_si(self) -> None:
        """Calls the init method and converts the parameters from gui units to SI units."""

        self.__init__(self.pos,
                      self.dim,
                      self.rot,
                      self.velocity,
                      self.tooth_height,
                      self.tooth_width,
                      self.tooth_pitch,
                      radians(self.tooth_flank_angle),
                      self.mu_r,
                      self.chamfer_depth * 1e-3,
                      radians(self.chamfer_angle),
                      self.maxh)

    def gui(self) -> GearRack:
        """Returns a copy of the class with attributes converted to units used in the gui."""

        return GearRack(self.pos,
                        self.dim,
                        self.rot,
                        self.velocity,
                        self.tooth_height,
                        self.tooth_width,
                        self.tooth_pitch,
                        degrees(self.tooth_flank_angle),
                        self.mu_r,
                        self.chamfer_depth * 1e3,
                        degrees(self.chamfer_angle),
                        self.maxh)

    def update(self, t: float) -> None:
        """Method to update the gear rotation angle theta for the next simulation step.

        :param t: Current time stamp.
        :type t: float
        """

        self.shift = self.velocity * t

    def position(self) -> np.ndarray:
        """Method to calculate the angle based center of the gear with eccentricity.

        :return: Gear Rack position with eccentricity.
        :rtype: numpy.ndarray
        """

        pos = self.pos + self.shift

        return pos

    def transformation_matrix(self) -> np.ndarray:
        """Method for calculating the transformation matrix to transform the global coordinate system into the
            body-fixed coordinate system.

        :return: The transformation matrix.
        :rtype: numpy.ndarray
        """

        return np.array([[cos(self.rot[1]) * cos(self.rot[2]), cos(self.rot[1]) * sin(self.rot[2]), -sin(self.rot[1])],
                         [sin(self.rot[0]) * sin(self.rot[1]) * cos(self.rot[2]) - cos(self.rot[0]) * sin(self.rot[2]),
                          sin(self.rot[0]) * sin(self.rot[1]) * sin(self.rot[2]) + cos(self.rot[0]) * cos(self.rot[2]),
                          sin(self.rot[0]) * cos(self.rot[1])],
                         [cos(self.rot[0]) * sin(self.rot[1]) * cos(self.rot[2]) + sin(self.rot[0]) * sin(self.rot[2]),
                          cos(self.rot[0]) * sin(self.rot[1]) * sin(self.rot[2]) - sin(self.rot[0]) * cos(self.rot[2]),
                          cos(self.rot[0]) * cos(self.rot[1])]
                         ])
