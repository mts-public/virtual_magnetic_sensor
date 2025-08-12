from __future__ import annotations
import numpy as np
from typing import Dict

from libs.elements.Component import Component


class Shaft(Component):
    """Contains all the parameters to describe the position, rotation and shape of a shaft.

    :param pos: Position of the shaft in the 3D space.
    :type pos: numpy.ndarray
    :param axis: The direction of the rotation axis of the shaft without wobbling.
    :type axis: numpy.ndarray
    :param diameter: Inner and outer diameter of the shaft.
    :type diameter: float
    :param length: Length of the shaft.
    :type length: float
    :param mu_r: Permeability of the shaft.
    :type mu_r: float
    :param maxh: Mesh size of the shaft.
    :type maxh: float
    """

    pos: np.ndarray
    axis: np.ndarray
    diameter: np.ndarray
    length: float
    mu_r: float
    maxh: float

    def __init__(self,
                 pos: np.ndarray,
                 axis: np.ndarray,
                 diameter: np.ndarray,
                 length: float,
                 mu_r: float,
                 maxh: float) -> None:
        """Constructor method."""

        super().__init__(pos, mu_r, maxh)
        self.axis = axis
        self.diameter = diameter
        self.length = length

    @classmethod
    def template(cls) -> Shaft:
        """Class method to init the class with a set of standard values.

        :return: Object of the Shaft class.
        :rtype: Shaft
        """

        return cls(pos=np.array([0.0, 0.0, 0.0]),
                   axis=np.array([0.0, 0.0, 1.0]),
                   diameter=np.array([1.0, 10.0]),
                   length=1.0,
                   mu_r=4000.0,
                   maxh=2.0)

    @classmethod
    def from_dict(cls, dictionary: Dict[any]) -> Shaft:
        """Method to init an instance of the Gear class by passing a dictionary with the corresponding
            arguments. Arguments that are in the dictionary and not in the class are ignored while arguments missing in
            the dictionary get initialised with the standard values defined in the template class method.

        :return: Instance of the Shaft class.
        :rtype: Shaft
        """

        template = Shaft.template()

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
        self.__init__(self.pos, self.axis, self.diameter, self.length, self.mu_r, self.maxh)

    def convert_to_si(self) -> None:
        """Calls the init method and converts the parameters from gui units to SI units."""

        self.__init__(self.pos,
                      self.axis,
                      self.diameter,
                      self.length,
                      self.mu_r,
                      self.maxh)

    def gui(self) -> Shaft:
        """Returns a copy of the class with attributes converted to units used in the gui."""

        return Shaft(self.pos,
                     self.axis,
                     self.diameter,
                     self.length,
                     self.mu_r,
                     self.maxh)

    def update(self, t: float) -> None:
        """Stub
        """
        pass
