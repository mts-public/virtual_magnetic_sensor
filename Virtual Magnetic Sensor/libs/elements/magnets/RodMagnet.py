from __future__ import annotations
import numpy as np
from typing import Dict

from libs.elements.Magnet import Magnet


class RodMagnet(Magnet):
    """Subclass of magnets in rod shape. Inherits from the Magnet parent class.

    :param axis: Longitudinal axis of the rod. The magnetic field points along the axis
        determined by this parameter.
    :type axis: numpy.ndarray
    :param direction: Direction of the magnetic field.
    :type direction: np.ndarray
    :param radius: Radius of the rod.
    :type radius: float
    :param length: Length of the rod.
    :type length: float

    :param m: Magnetisation of the magnet along the rod high axis.
    :type m: numpy.ndarray
    """

    axis: np.ndarray
    direction: np.ndarray
    radius: float
    length: float
    m: float

    def __init__(self,
                 pos: np.ndarray,
                 axis: np.ndarray,
                 direction: np.ndarray,
                 radius: float,
                 length: float,
                 m: float,
                 mu_r: float,
                 temperature: float,
                 tk: float,
                 maxh: float) -> None:
        """Constructor method."""

        super().__init__(pos, m, mu_r, temperature, tk, maxh)

        self.axis = axis / np.linalg.norm(axis)
        self.direction = direction / np.linalg.norm(direction)
        self.radius = radius
        self.length = length

        self.m_vec = self.m * (1 + self.tk * (
            (self.temperature - 20.0 if self.temperature > 20 else 0) if self.temperature <= 100 else 80.0) / 100) \
            * self.direction

    @classmethod
    def template(cls) -> RodMagnet:
        """Class method to init the class with a set of standard values.

        :return: Object of the RodMagnet class.
        :rtype: RodMagnet
        """

        return cls(pos=np.array([0.0, 0.0, 0.0]),
                   axis=np.array([0.0, 0.0, 1.0]),
                   direction=np.array([0.0, 0.0, 1.0]),
                   radius=1.0,
                   length=1.0,
                   m=1e3 * 1e3,
                   mu_r=1.0,
                   temperature=20.0,
                   tk=-0.2,
                   maxh=2.0)

    @classmethod
    def from_dict(cls, dictionary: Dict[any]) -> RodMagnet:
        """Method to init an instance of the Gear class by passing a dictionary with the corresponding
            arguments. Arguments that are in the dictionary and not in the class are ignored while arguments missing in
            the dictionary get initialised with the standard values defined in the template class method.

        :return: Instance of the RodMagnet class.
        :rtype: RodMagnet
        """

        template = RodMagnet.template()

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
        dictionary.pop('m_vec', None)

        return dictionary

    def reset(self):
        """Calls the init method with the actual class attributes."""

        self.__init__(self.pos, self.axis, self.direction, self.radius, self.length, self.m, self.mu_r, self.temperature, self.tk,
                      self.maxh)

    def convert_to_si(self) -> None:
        """Calls the init method and converts the parameters from gui units to SI units."""

        self.__init__(self.pos,
                      self.axis,
                      self.direction,
                      self.radius,
                      self.length,
                      self.m * 1e3,
                      self.mu_r,
                      self.temperature,
                      self.tk,
                      self.maxh)

    def gui(self) -> RodMagnet:
        """Returns a copy of the class with attributes converted to units used in the gui."""

        return RodMagnet(self.pos,
                         self.axis,
                         self.direction,
                         self.radius,
                         self.length,
                         self.m * 1e-3,
                         self.mu_r,
                         self.temperature,
                         self.tk,
                         self.maxh)
