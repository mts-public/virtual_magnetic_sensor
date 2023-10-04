from __future__ import annotations
import numpy as np
from typing import Dict
from math import pi


class UniField:
    """Holds the parameters of a uniform magnetic field and creates the related B-Field.
        This field is then superimposed with the fields emanating from the magnets in the simulation.

    :param direction: The direction of the uniform magnetic field.
    :type direction: numpy array [1, 3] (float)
    :param strength: The strength of the uniform magnetic field.
    :type strength: float
    :param mu0: Magnetic field constant.
    :type mu0: float
    :param h_vec: Vector of the uniform magnetic field.
    :type h_vec: numpy.ndarray
    :param b_vec: Vector of the uniform magnetic flux density.
    :type b_vec: numpy.ndarray
    """

    direction: np.ndarray
    strength: float
    mu0: float
    h_vec: np.ndarray
    b_vec: np.ndarray

    def __init__(self,
                 direction: np.ndarray,
                 strength: float) -> None:
        """Constructor method."""

        self.direction = direction / np.linalg.norm(direction)
        self.strength = strength

        self.mu0 = 4 * pi * 1e-7
        self.h_vec = self.strength * self.direction / self.mu0
        self.b_vec = self.strength * self.direction

    @classmethod
    def template(cls) -> UniField:
        """Class method to init the class with a set of standard values.

        :return: Object of the UniField class.
        :rtype: UniField
        """

        return cls(direction=np.array([0.0, 1.0, 0.0]),
                   strength=10.0 * 1e-3)

    @classmethod
    def from_dict(cls, dictionary: Dict[any]) -> UniField:
        """Method to init an instance of the Gear class by passing a dictionary with the corresponding
            arguments. Arguments that are in the dictionary and not in the class are ignored while arguments missing in
            the dictionary get initialised with the standard values defined in the template class method.

        :return: Instance of the UniField class.
        :rtype: UniField
        """

        template = UniField.template()

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
        dictionary.pop('mu0', None)
        dictionary.pop('h_vec', None)
        dictionary.pop('b_vec', None)

        return dictionary

    def gui_dict(self) -> Dict[str, any]:
        """Method creates a dictionary of the class members that will be stored in the HDF5 file. Variables created
            automatically when instantiating an object of the class are excluded from the dictionary. This creates the
            opportunity to initiate an instance of the class by parsing the dictionary as argument.

        :return: The dictionary of the classes members.
        :rtype: Dict[str, any]
        """

        dictionary: dict = vars(self.gui()).copy()
        dictionary.pop('mu0', None)
        dictionary.pop('h_vec', None)
        dictionary.pop('b_vec', None)

        return dictionary

    def reset(self):
        """Calls the init method with the actual class attributes."""
        self.__init__(self.direction, self.strength)

    def convert_to_si(self) -> None:
        """Calls the init method and converts the parameters from gui units to SI units."""

        self.__init__(self.direction,
                      self.strength * 1e-3)

    def gui(self) -> UniField:
        """Returns a copy of the class with attributes converted to units used in the gui."""

        return UniField(self.direction,
                        self.strength * 1e3)
