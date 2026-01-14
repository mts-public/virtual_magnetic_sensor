from __future__ import annotations
from typing import Dict, List
import numpy as np
from math import sin, cos

from libs.elements.Sensor import Sensor
from libs.simulation.MagneticField import MagneticField


class HallSensor(Sensor):
    """"""

    def __init__(self,
                 pos: np.ndarray,
                 rot: np.ndarray,
                 dim: np.ndarray,
                 hall_coefficient: float,
                 conductor_thickness: float,
                 current: float,
                 maxh: float,
                 **kwargs):

        super().__init__(pos, maxh)

        self.rot = rot
        self.dim = dim
        self.hall_coefficient = hall_coefficient
        self.conductor_thickness = conductor_thickness
        self.current = current

        self.transformation_matrix = self.get_transformation_matrix()

        if 'hall_voltage' in kwargs:
            self.hall_voltage = kwargs['hall_voltage']
        else:
            self.hall_voltage = list()

    @classmethod
    def template(cls) -> HallSensor:
        """Class method to init the class with a set of default values.

        :return: Object of the HallSensor class.
        :rtype: HallSensor
        """

        return cls(pos=np.array([0.0, 0.0, 0.0]),
                   rot=np.radians(np.array([0.0, 0.0, 0.0])),
                   dim=np.array([1.0, 1.0, 1.0]),
                   hall_coefficient=-53e-12,
                   conductor_thickness=0.1,
                   current=1.0,
                   maxh=2.0)

    @classmethod
    def from_dict(cls, dictionary: Dict[any]) -> HallSensor:
        """Method to init an instance of the HallSensor class by passing a dictionary with the corresponding
            arguments.

        :return: Instance of the HallSensor class.
        :rtype: HallSensor
        """

        template = HallSensor.template()

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
        dictionary.pop('transformation_matrix')

        return dictionary

    def gui_dict(self) -> Dict[str, any]:
        """Method creates a dictionary of the class members that will be stored in the ini file. Variables not passed
        to the init method are excluded from the dictionary. This creates the opportunity to initiate an instance of
        the class by parsing the dictionary as argument.

        :return: The dictionary of the classes members.
        :rtype: Dict[str, any]
        """

        dictionary: dict = vars(self.gui()).copy()
        dictionary.pop('transformation_matrix', None)
        dictionary.pop('hall_voltage', None)

        return dictionary

    def reset(self) -> None:
        """Calls the init method with the actual class attributes."""

        self.__init__(self.pos, self.rot, self.dim, self.hall_coefficient, self.conductor_thickness, self.current,
                      self.maxh)

    def convert_to_si(self) -> None:
        """Calls the init method and converts the parameters from gui units to SI units."""

        self.__init__(self.pos,
                      np.radians(self.rot),
                      self.dim,
                      self.hall_coefficient*1e-12,
                      self.conductor_thickness*1e-3,
                      self.current,
                      self.maxh)

    def gui(self) -> HallSensor:
        """Returns a copy of the class with attributes converted to units used in the gui.

        :return: Object of the HallSensor class.
        :rtype: HallSensor
        """

        return HallSensor(self.pos,
                          np.degrees(self.rot),
                          self.dim,
                          self.hall_coefficient*1e12,
                          self.conductor_thickness*1e3,
                          self.current,
                          self.maxh)

    def get_data(self, hall_voltage: List[float]) -> None:
        """Method to pass the measurement data saved in a dictionary to the sensor object.

        :param hall_voltage: Hall Voltage
        :type hall_voltage: List[float]
        """

        self.hall_voltage += hall_voltage

    def set_data(self, data_dict: Dict[str, List], field: MagneticField) -> Dict[str, List]:
        """Method to update the sensor measurement parameters for the current simulation step. Parameter to be updated
            is the hall_voltage.

        :param data_dict: Dictionary with the measurement data, shared between processes.
        :type data_dict: Dict[str, List]
        :param field: Instance of the MagneticField class.
        :type field: MagneticField
        """

        if "hall_voltage" not in data_dict:
            data_dict['hall_voltage'] = list()
        data_dict['hall_voltage'].append(self.get_hall_voltage(field))

        return data_dict

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

    def get_hall_voltage(self, field: MagneticField) -> float:
        """Method for calculating the hall voltage along the body-fixed x-axis of the sensor.

                :param field: Instance of the MagneticField class.
                :type field: MagneticField
                :return: The transformation matrix.
                :rtype: numpy.ndarray
                """

        b_field = self.transformation_matrix.dot(field.get_b_field(self.pos[0], self.pos[1], self.pos[2]))
        u_h = self.current*b_field[1]*self.hall_coefficient/(self.conductor_thickness/1e3)  # conductor_thickness mm->m
        return u_h
