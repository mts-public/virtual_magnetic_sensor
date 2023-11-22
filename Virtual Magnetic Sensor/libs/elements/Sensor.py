from __future__ import annotations
import numpy as np
from typing import Dict, List
import abc

from libs.simulation.MagneticField import MagneticField


class Sensor:
    """Parent class contains the parameters to describe the position and max mesh size of a sensor in the
    simulation. The shape and rotation is defined in one of the subclasses.

    :param pos: Position of the sensor in the 3D space.
    :type pos: numpy.ndarray
    :param maxh: Maximum mesh size of the sensor.
    :type maxh: float

    """

    pos: np.ndarray
    maxh: float

    def __init__(self,
                 pos: np.ndarray,
                 maxh: float) -> None:
        """Constructor method."""

        self.pos = pos
        self.maxh = maxh

    @classmethod
    @abc.abstractmethod
    def template(cls) -> Sensor:
        """Class method to init the class with a set of standard values.

        :return: Object of the Sensor class.
        :rtype: Sensor
        """

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, dictionary: Dict[any]) -> Sensor:
        """Method to init an instance of the Sensor class by passing a dictionary with the corresponding
            arguments.

        :return: Instance of the Sensor class.
        :rtype: Sensor
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
    def reset(self) -> None:
        """Calls the init method with the actual class attributes."""

    @abc.abstractmethod
    def convert_to_si(self) -> None:
        """Calls the init method and converts the parameters from gui units to SI units."""

    @abc.abstractmethod
    def gui(self) -> Sensor:
        """Returns a copy of the class with attributes converted to units used in the gui."""

    @abc.abstractmethod
    def get_data(self, *args) -> None:
        """Method to pass the measurement data saved in a dictionary to the sensor object."""

    @abc.abstractmethod
    def set_data(self, data_dict: Dict[str, List], field: MagneticField) -> Dict[str, List]:
        """Method to update the sensor measurement parameters for the current simulation step.

        :param data_dict: Dictionary with the measurement data, shared between processes.
        :type data_dict: Dict[str, List]
        :param field: Instance of the MagneticField class.
        :type field: MagneticField
        """
