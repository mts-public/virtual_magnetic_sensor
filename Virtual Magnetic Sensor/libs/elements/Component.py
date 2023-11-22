from __future__ import annotations
import numpy as np
import abc
from typing import Dict


class Component:
    """Parent class contains the parameters to describe the position and magnetic properties of a component in the
    simulation. The shape and rotation is defined in one of the subclasses.

    :param pos: Position of the magnet in the 3D space.
    :type pos: numpy.ndarray
    :param mu_r: Permeability of the magnet.
    :type mu_r: float
    :param maxh: Maximum mesh size of the component.
    :type maxh: float
    """

    pos: np.ndarray
    mu_r: float
    maxh: float

    def __init__(self,
                 pos: np.ndarray,
                 mu_r: float,
                 maxh: float) -> None:
        """Constructor method."""

        self.pos = pos
        self.mu_r = mu_r
        self.maxh = maxh

    @classmethod
    @abc.abstractmethod
    def template(cls) -> Component:
        """Class method to init the class with a set of standard values.

        :return: Object of the Component class.
        :rtype: Component
        """

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, dictionary: Dict[any]) -> Component:
        """Method to init an instance of the Component class by passing a dictionary with the corresponding
            arguments.

        :return: Instance of the Component class.
        :rtype: Component
        """

    @abc.abstractmethod
    def to_dict(self) -> Dict[str, any]:
        """Method creates a dictionary of the class members that will be stored in the HDF5 file. Variables created
            automatically when instantiating an object of the class are excluded from the dictionary. This creates the
            opportunity to initiate an instance of the class by parsing the dictionary as argument.

        :return: The dictionary of the classes members.
        :rtype: Dict[str, any]
        """

    @abc.abstractmethod
    def gui_dict(self) -> Dict[str, any]:
        """Method creates a dictionary of the class members that will be stored in the ini file. Variables not passed
        to the init method are excluded from the dictionary. This creates the opportunity to initiate an instance of
        the class by parsing the dictionary as argument.

        :return: The dictionary of the classes members.
        :rtype: Dict[str, any]
        """

    @abc.abstractmethod
    def reset(self) -> None:
        """Calls the init method with the actual class attributes."""

    @abc.abstractmethod
    def convert_to_si(self) -> None:
        """Calls the init method and converts the parameters from gui units to SI units."""

    @abc.abstractmethod
    def gui(self) -> Component:
        """Returns a copy of the class with attributes converted to units used in the gui."""

    @abc.abstractmethod
    def update(self, t: float) -> None:
        """Method to update the states of a time dependent component.

        :param t: Current time stamp.
        :type t: float
        """

