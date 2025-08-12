from __future__ import annotations
import numpy as np
from math import sin, cos
from typing import Dict

from libs.elements.Magnet import Magnet


class CuboidMagnet(Magnet):
    """Subclass of magnets in cylinder shape. Inherits from the Magnet parent class.

    :param rot: Rotation of the magnet in the 3D space in radians. The magnetic field points along the body-fixed
        z-axis.
    :type rot: numpy.ndarray
    :param dim: Dimension of the cuboid along the body-fixed coordinate axes.
    :type dim: numpy.ndarray
    :param direction: Direction of the magnetic field.
    :type direction: np.ndarray
    :param transformation_matrix: The transformation matrix to transform the global coordinate system to the body-fixed
        coordinate system with direction of the magnetisation pointing along the body-fixed z-axis.
    :type transformation_matrix: numpy.ndarray
    :param m_vec: Magnetisation of the magnet along the three global coordinate axes.
    :type m_vec: numpy.ndarray
    """

    rot: np.ndarray
    dim: np.ndarray
    direction: np.ndarray
    transformation_matrix: np.ndarray
    m_vec: np.ndarray

    def __init__(self,
                 pos: np.ndarray,
                 rot: np.ndarray,
                 dim: np.ndarray,
                 direction: np.ndarray,
                 m: float,
                 mu_r: float,
                 temperature: float,
                 tk: float,
                 maxh: float) -> None:
        """Constructor method."""

        super().__init__(pos, m, mu_r, temperature, tk, maxh)
        self.rot = rot
        self.dim = dim
        self.direction = direction / np.linalg.norm(direction)

        self.transformation_matrix = self.get_transformation_matrix()
        self.m_vec = self.m * (1 + self.tk * (
            (self.temperature - 20.0 if self.temperature > 20 else 0) if self.temperature <= 100 else 80.0) / 100) \
            * self.direction

    @classmethod
    def template(cls) -> CuboidMagnet:
        """Class method to init the class with a set of standard values.

        :return: Object of the CuboidMagnet class.
        :rtype: CuboidMagnet
        """

        return cls(pos=np.array([0.0, 0.0, 0.0]),
                   rot=np.array([0.0, 0.0, 0.0]),
                   dim=np.array([1.0, 1.0, 1.0]),
                   direction=np.array([0.0, 0.0, 1.0]),
                   m=1e3 * 1e3,
                   mu_r=1.0,
                   temperature=20.0,
                   tk=-0.2,
                   maxh=2.0)

    @classmethod
    def from_dict(cls, dictionary: Dict[any]) -> CuboidMagnet:
        """Method to init an instance of the Gear class by passing a dictionary with the corresponding
            arguments. Arguments that are in the dictionary and not in the class are ignored while arguments missing in
            the dictionary get initialised with the standard values defined in the template class method.

        :return: Instance of the CuboidMagnet class.
        :rtype: CuboidMagnet
        """

        template = CuboidMagnet.template()

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

        dictionary: Dict[str, any] = vars(self).copy()
        dictionary.pop('transformation_matrix', None)
        dictionary.pop('m_vec', None)

        return dictionary

    def gui_dict(self) -> Dict[str, any]:
        """Method creates a dictionary of the class members that will be stored in the HDF5 file. Variables created
            automatically when instantiating an object of the class are excluded from the dictionary. This creates the
            opportunity to initiate an instance of the class by parsing the dictionary as argument.

        :return: The dictionary of the classes members.
        :rtype: Dict[str, any]
        """

        dictionary: dict = vars(self.gui()).copy()
        dictionary.pop('transformation_matrix', None)
        dictionary.pop('m_vec', None)

        return dictionary

    def reset(self):
        """Calls the init method with the actual class attributes."""
        self.__init__(self.pos, self.rot, self.dim, self.direction, self.m, self.mu_r, self.temperature, self.tk,
                      self.maxh)

    def convert_to_si(self) -> None:
        """Calls the init method and converts the parameters from gui units to SI units."""

        self.__init__(self.pos,
                      np.radians(self.rot),
                      self.dim,
                      self.direction,
                      self.m * 1e3,
                      self.mu_r,
                      self.temperature,
                      self.tk,
                      self.maxh)

    def gui(self) -> CuboidMagnet:
        """Returns a copy of the class with attributes converted to units used in the gui."""

        return CuboidMagnet(self.pos,
                            np.degrees(self.rot),
                            self.dim,
                            self.direction,
                            self.m * 1e-3,
                            self.mu_r,
                            self.temperature,
                            self.tk,
                            self.maxh)

    def get_transformation_matrix(self) -> np.ndarray:
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
