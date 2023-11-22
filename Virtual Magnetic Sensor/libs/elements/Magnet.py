from __future__ import annotations
import numpy as np
from typing import Dict
import abc


class Magnet:
    """Parent class contains the parameters to describe the position and magnetic properties of a magnet in the
    simulation. The shape and rotation is defined in one of the subclasses.

    :param pos: Position of the magnet in the 3D space.
    :type pos: numpy.ndarray
    :param m: Magnetisation of the magnet at room temperature.
    :type m: float
    :param mu_r: Permeability of the magnet.
    :type mu_r: float
    :param temperature: Temperature at which the magnet is operated.
    :type temperature: float
    :param tk: Temperature coefficiency of the magnetisation in the area of 20-100°C.
    :type tk: float
    :param maxh: Maximum mesh size of the magnet.
    :type maxh: float
    """

    pos: np.ndarray
    m: float
    mu_r: float
    temperature: float
    tk: float
    maxh: float

    def __init__(self,
                 pos: np.ndarray,
                 m: float,
                 mu_r: float,
                 temperature: float,
                 tk: float,
                 maxh: float) -> None:
        """Constructor method."""

        self.pos = pos
        self.m = m
        self.mu_r = mu_r
        self.temperature = temperature
        self.tk = tk
        self.maxh = maxh

    @classmethod
    @abc.abstractmethod
    def template(cls) -> Magnet:
        """Class method to init the class with a set of standard values.

        :return: Object of the Magnet class.
        :rtype: Magnet
        """

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, dictionary: Dict[any]) -> Magnet:
        """Method to init an instance of the Magnet class by passing a dictionary with the corresponding
            arguments.

        :return: Instance of the Magnet class.
        :rtype: Magnet
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
    def gui(self) -> Magnet:
        """Returns a copy of the class with attributes converted to units used in the gui."""
