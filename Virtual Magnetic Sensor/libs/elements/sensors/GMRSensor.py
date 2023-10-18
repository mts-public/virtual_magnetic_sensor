from __future__ import annotations
from math import sin, cos
import numpy as np
from enum import Enum
from typing import Dict, List
import configparser
from pathlib import Path

from libs.elements.Sensor import Sensor

from libs.simulation.MagneticField import MagneticField


class GMRSensor(Sensor):
    """Represents the sensor properties and includes the methods to calculate the output voltages of the sensor.
    
    :param pos: Position of the sensor in the 3D space.
    :type pos: numpy.ndarray
    :param rot: Rotation of the sensor in the 3D space in radians. The GMR elements are arranged along the body-fixed
        x-axis.
    :type rot: numpy.ndarray
    :param depth: Size of the sensor along the body-fixed y-axis.
    :type depth: float
    :param height: Size of the sensor along the body-fixed z-axis.
    :type height: float
    :param current: Operating current of the measurement bridges.
    :type current: float
    :param gmr_offset: Positions of the GMR elements along the body-fixed x-axis.
    :type gmr_offset: numpy.ndarray
    :param gmr_length: Length of the GMR elements along the body-fixed x-axis.
    :type gmr_length: float
    :param gmr_sampling: Number of sampling points at which the magnetic field strengths in a GMR element are measured
        and summarized.
    :type gmr_sampling: int
    :param sensor_sampling: Number of sampling points at which the magnetic field is recorded along the sensor length.
    :type sensor_sampling: int
    :param maxh: Maximum mesh size of the sensor.
    :type maxh: float
    :param resistance: List of arrays with the resistance of each GMR element at each time step.
    :type resistance: List[numpy.ndarray]
    :param u_sin: List of the sensor voltage output U_sin at each time step.
    :type u_sin: List[float]
    :param u_cos: List of the sensor voltage output U_cos at each time step.
    :type u_cos: List[float]
    :param h_sensor: Magnetic field components along the sensor during the current simulation step.
    :type h_sensor: List[numpy.ndarray]
    :param architectures: Deposited sensor designs which can be selected in the gui.
    :type architectures: List[str]
    :param width: Sensor length along the body-fixed x-axis regarding the GMR elements and the GMR length.
    :type width: float
    :param dim: Dimension of the sensor along the body-fixed coordinate axes.
    :type dim: numpy.ndarray
    :param transformation_matrix: The transformation matrix to transform the global coordinate system to the body-fixed
        coordinate system with the arrangement of the GMR elements along the body-fixed x-axis.
    :type transformation_matrix: numpy.ndarray
    :param gmr_position_matrix: Array of points in the 3D space describing the position of each GMR element of the
        sensor.
    :type gmr_position_matrix: numpy.ndarray
    :param gmr_sampling_matrix: Array of points in the 3D space describing the sampling points of each GMR element of
        the sensor.
    :type gmr_sampling_matrix: numpy.ndarray
    :param sensor_sampling_matrix: Array of sampling points in the 3D space at which the magnetic field is measured
        along the sensor length.
    :type sensor_sampling_matrix: numpy.ndarray
    """

    pos: np.ndarray
    rot: np.ndarray
    depth: float
    height: float
    current: float
    gmr_offset: np.ndarray
    gmr_length: float
    gmr_sampling: int
    sensor_sampling: int
    maxh: float
    resistance: List[np.ndarray]
    u_sin: List[float]
    u_cos: List[float]
    h_sensor: List[np.ndarray]
    width: float
    dim: np.ndarray
    transformation_matrix: np.ndarray
    sensor_sampling_matrix: np.ndarray
    gmr_position_matrix: np.ndarray

    architectures: List[str] = [
        "select",
        "GL711",
        "GL712",
        "GL713",
        "GL714",
        "GL715",
    ]

    def __init__(self,
                 pos: np.ndarray,
                 rot: np.ndarray,
                 depth: float,
                 height: float,
                 current: float,
                 gmr_offset: np.ndarray,
                 gmr_length: float,
                 gmr_sampling: int,
                 sensor_sampling: int,
                 maxh: float,
                 resistance: List[np.ndarray] = None,
                 u_sin: List[float] = None,
                 u_cos: List[float] = None,
                 h_sensor: List[np.ndarray] = None) -> None:
        """Constructor method."""

        super().__init__(pos, maxh)

        self.rot = rot
        self.depth = depth
        self.height = height
        self.current = current
        self.gmr_offset = gmr_offset
        self.gmr_length = gmr_length
        self.gmr_sampling = gmr_sampling
        self.sensor_sampling = sensor_sampling
        self.resistance = resistance
        self.u_sin = u_sin
        self.u_cos = u_cos
        self.resistance = resistance
        self.u_sin = u_sin
        self.u_cos = u_cos
        self.h_sensor = h_sensor

        if resistance is None:
            self.resistance = list()
        else:
            self.resistance = resistance
        if u_sin is None:
            self.u_sin = list()
        else:
            self.u_sin = u_sin
        if u_cos is None:
            self.u_cos = list()
        else:
            self.u_cos = u_cos
        if h_sensor is None:
            self.h_sensor = list()
        else:
            self.h_sensor = h_sensor

        self.width = (self.gmr_offset[-1] - self.gmr_offset[0]) + self.gmr_length
        self.dim = np.array([self.width, self.depth, self.height])
        self.transformation_matrix = self.get_transformation_matrix()
        self.gmr_position_matrix = self.get_gmr_position_matrix()
        self.gmr_sampling_matrix = self.get_gmr_sampling_matrix()
        self.sensor_sampling_matrix = self.get_sensor_sampling_matrix()

        gmr_config: configparser.ConfigParser = configparser.ConfigParser()
        gmr_config.read(Path('cfg/gmr_characteristics.ini'))
        self.coeffs: list = [1.442, -1.26e-6, 0.0, 0.0, 0.0]
        if gmr_config.has_section('COEFFICIENTS'):
            self.coeffs = [
                float(gmr_config['COEFFICIENTS'].get('q0', '1.442')),
                float(gmr_config['COEFFICIENTS'].get('q1', '-1.26e-6')),
                float(gmr_config['COEFFICIENTS'].get('q2', '0.0')),
                float(gmr_config['COEFFICIENTS'].get('q3', '0.0')),
                float(gmr_config['COEFFICIENTS'].get('q4', '0.0'))
            ]

    @classmethod
    def template(cls) -> GMRSensor:
        """Class method to init the class with a set of standard values.

        :return: Object of the GMRSensor class.
        :rtype: GMRSensor
        """

        return cls(pos=np.array([0.0, 4.27, -0.7]),
                   rot=np.radians(np.array([0.0, 0.0, 0.0])),
                   depth=100.0 * 1e-3,
                   height=100.0 * 1e-3,
                   current=1.0,
                   gmr_offset=np.array([-455.0, -295.0, -205.0, -45.0, 45.0, 205.0, 295.0, 455.0]) * 1e-3,
                   gmr_length=85.0 * 1e-3,
                   gmr_sampling=100,
                   sensor_sampling=1000,
                   maxh=0.1)

    @classmethod
    def from_dict(cls, dictionary: Dict[any]) -> GMRSensor:
        """Method to init an instance of the Gear class by passing a dictionary with the corresponding
            arguments. Arguments that are in the dictionary and not in the class are ignored while arguments missing in
            the dictionary get initialised with the standard values defined in the template class method.

        :return: Instance of the GMRSensor class.
        :rtype: GMRSensor
        """

        template = GMRSensor.template()

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
        dictionary.pop('width', None)
        dictionary.pop('dim', None)
        dictionary.pop('transformation_matrix', None)
        dictionary.pop('gmr_position_matrix', None)
        dictionary.pop('gmr_sampling_matrix', None)
        dictionary.pop('sensor_sampling_matrix', None)
        dictionary.pop('gmr_config', None)
        dictionary.pop('coeffs', None)

        return dictionary

    def gui_dict(self) -> Dict[str, any]:
        """Method creates a dictionary of the class members that will be stored in the HDF5 file. Variables created
            automatically when instantiating an object of the class are excluded from the dictionary. This creates the
            opportunity to initiate an instance of the class by parsing the dictionary as argument.

        :return: The dictionary of the classes members.
        :rtype: Dict[str, any]
        """

        dictionary: dict = vars(self.gui()).copy()
        dictionary.pop('width', None)
        dictionary.pop('dim', None)
        dictionary.pop('transformation_matrix', None)
        dictionary.pop('gmr_position_matrix', None)
        dictionary.pop('gmr_sampling_matrix', None)
        dictionary.pop('sensor_sampling_matrix', None)
        dictionary.pop('gmr_config', None)
        dictionary.pop('coeffs', None)
        dictionary.pop('u_sin', None)
        dictionary.pop('u_cos', None)
        dictionary.pop('resistance', None)
        dictionary.pop('h_sensor', None)

        return dictionary

    def reset(self) -> None:
        """Calls the init method with the actual class attributes."""

        self.__init__(self.pos, self.rot, self.depth, self.height, self.current, self.gmr_offset, self.gmr_length,
                      self.gmr_sampling, self.sensor_sampling, self.maxh, list(), list(), list(), list())

    def convert_to_si(self) -> None:
        """Calls the init method and converts the parameters from gui units to SI units."""

        self.__init__(self.pos,
                      np.radians(self.rot),
                      self.depth * 1e-3,
                      self.height * 1e-3,
                      self.current,
                      self.gmr_offset * 1e-3,
                      self.gmr_length * 1e-3,
                      self.gmr_sampling,
                      self.sensor_sampling,
                      self.maxh)

    def gui(self) -> GMRSensor:
        """Returns a copy of the class with attributes converted to units used in the gui."""

        return GMRSensor(self.pos,
                         np.degrees(self.rot),
                         self.depth * 1e3,
                         self.height * 1e3,
                         self.current,
                         self.gmr_offset * 1e3,
                         self.gmr_length * 1e3,
                         self.gmr_sampling,
                         self.sensor_sampling,
                         self.maxh)

    def update(self, field: MagneticField) -> None:
        """Method to update the sensor measurement parameters for the current simulation step. Parameters to be updated
            are the resistances array, the output voltages u_sin and u_cos and the H-field along the sensor axis
            h_sensor.

        :param field: Instance of the MagneticField class.
        :type field: MagneticField
        """

        self.resistance.append(self.get_gmr_resistances(self.get_gmr_h_values(field)))
        self.u_sin.append(self.get_u_sin(self.resistance[-1]))
        self.u_cos.append(self.get_u_cos(self.resistance[-1]))
        self.h_sensor.append(field.get_h_field(self.sensor_sampling_matrix[:, 0],
                                               self.sensor_sampling_matrix[:, 1],
                                               self.sensor_sampling_matrix[:, 2]))

    def get_data(self, resistance: List[np.ndarray], u_sin: List[float], u_cos: List[float],
                 h_sensor: List[np.ndarray]):
        self.resistance += resistance
        self.u_sin += u_sin
        self.u_cos += u_cos
        self.h_sensor += h_sensor

    def set_data(self, data_dict: Dict[str, List], magnetic_field: MagneticField):
        if "resistance" not in data_dict:
            data_dict['resistance'] = list()
        if "u_sin" not in data_dict:
            data_dict['u_sin'] = list()
        if "u_cos" not in data_dict:
            data_dict['u_cos'] = list()
        if "h_sensor" not in data_dict:
            data_dict['h_sensor'] = list()
        data_dict['resistance'].append(self.get_gmr_resistances(self.get_gmr_h_values(magnetic_field)))
        data_dict['u_sin'].append(self.get_u_sin(data_dict['resistance'][-1]))
        data_dict['u_cos'].append(self.get_u_cos(data_dict['resistance'][-1]))
        data_dict['h_sensor'].append(magnetic_field.get_h_field(self.sensor_sampling_matrix[:, 0],
                                                                self.sensor_sampling_matrix[:, 1],
                                                                self.sensor_sampling_matrix[:, 2]))
        return data_dict

    def get_transformation_matrix(self) -> np.ndarray:
        """Method for calculating the transformation matrix to transform the global coordinate system into the
            body-fixed coordinate system, where the x-axis points along the arrangement of the GMR elements.

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

    def get_gmr_position_matrix(self) -> np.ndarray:
        """Method of calculating the coordinates in 3D space with the positions of the centers of the GMR elements.

        :return: Matrix of GMR elements center points.
        :rtype: np.ndarray
        """

        return np.array([self.pos + offset * self.transformation_matrix[:, 0] for offset in self.gmr_offset])

    def get_gmr_sampling_matrix(self) -> np.ndarray:
        """Method of calculating the coordinates in 3D space at which the magnetic field for a specific GMR
            element is sampled. Sample points are calculated by the midpoint rule.

        :return: Matrix of sample points.
        :rtype: numpy.ndarray
        """

        return np.array(
            [[gmr_element - self.gmr_length / 2 * self.transformation_matrix[:, 0]
              + self.gmr_length * (2 * i + 1) / (2 * self.gmr_sampling) * self.transformation_matrix[:, 0]
              for i in range(0, self.gmr_sampling)] for gmr_element in self.gmr_position_matrix])

    def get_sensor_sampling_matrix(self) -> np.ndarray:
        """Method for calculating the coordinates in 3D space at which the magnetic field is sampled over the entire
            sensor.

        :return: Matrix of sample points.
        :rtype: numpy.ndarray
        """

        return np.array(
            [self.pos - self.width / 2 * self.transformation_matrix[:, 0] + (2 * i + 1) / (2 * self.sensor_sampling)
             * self.width * self.transformation_matrix[:, 0] for i in range(0, self.sensor_sampling)])

    def get_gmr_h_values(self, field: MagneticField) -> np.ndarray:
        """Method to calculate the magnetic field strength sampled over the length of a GMR element for all GMR elements
            of the sensor.

        :param field: Magnetic field.
        :type field: MagneticField

        :return: Magnetic field strength at the GMR elements positions.
        :rtype: numpy.ndarray
        """

        h_field: np.ndarray = np.empty(shape=self.gmr_position_matrix.shape)
        for num, page in enumerate(self.gmr_sampling_matrix):
            h_field[num, :] = np.mean(field.get_h_field(page[:, 0], page[:, 1], page[:, 2]), axis=0)

        return h_field

    def get_gmr_resistances(self, h_field: np.ndarray) -> np.ndarray:
        """Method to calculate the GMR elements resistances in respect to a given magnetic field strength H.
            The characteristic curve which indicates the relationship between field strength and resistance is deposited
            here.

        :param h_field: Magnetic field strength over each GMR element.
        :type h_field: numpy.ndarray

        :return: Resulting resistances of each GMR element.
        :rtype: numpy.ndarray
        """

        h_x = np.matmul(self.transformation_matrix, h_field.transpose())[0, :]

        return self.coeffs[4] * np.power(h_x, 4) + self.coeffs[3] * np.power(h_x, 3) + \
               self.coeffs[2] * np.power(h_x, 2) + self.coeffs[1] * h_x + self.coeffs[0]

    def get_u_sin(self, r: np.ndarray) -> float:
        """Method for calculating the sinus sensor signal with the resistance values on each gmr element.

        :return: Sinus sensor signal.
        :rtype: float
        """

        return ((r[4] + r[5]) / (r[0] + r[1] + r[4] + r[5])
                - (r[0] + r[1]) / (r[0] + r[1] + r[4] + r[5])) * self.current

    def get_u_cos(self, r: np.ndarray) -> float:
        """Method for calculating the cosinus sensor signal with the resistance values on each gmr element.

        :return: Cosinus sensor signal.
        :rtype: float
        """

        return ((r[2] + r[3]) / (r[2] + r[3] + r[6] + r[7])
                - (r[6] + r[7]) / (r[2] + r[3] + r[6] + r[7])) * self.current


class GMRSensorProperties(Enum):
    """Enumeration class which assigns the properties of the stored sensors to their respective name."""

    GL711 = [[-455.0, -295.0, -205.0, -45.0, 45.0, 205.0, 295.0, 455.0], 85.0]
    GL712 = [[-910.0, -590.0, -410.0, -90.0, 90.0, 410.0, 590.0, 910.0], 160.0]
    GL713 = [[-1365.0, -885.0, -615.0, -135.0, 135.0, 615.0, 885.0, 1365.0], 245.0]
    GL714 = [[-427.7, -277.3, -192.7, -42.3, 42.3, 192.7, 277.3, 427.7], 75.0]
    GL715 = [[-714.35, -463.15, -321.85, -70.65, 70.65, 321.85, 463.15, 714.35], 125.0]
