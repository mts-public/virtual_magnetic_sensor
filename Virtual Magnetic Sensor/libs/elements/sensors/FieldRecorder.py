from __future__ import annotations
import numpy as np
from typing import Dict, List

from libs.simulation.MagneticField import MagneticField


class FieldRecorder:
    """The values necessary to describe an area for recording the magnetic field are determined in this class.
    
    :param field_specifier: Determines wether the magnetic flux density or the magnetic field strength field is recorded.
    :type field_specifier: int
    :param boundaries: Defines the boundaries in which the magnetic field is recorded.
    :type boundaries: numpy.ndarray
    :param samples: Defines the number of sample points in each dimension.
    :type samples: numpy.ndarray
    :param maxh: Maximum mesh size of the field recorder measurement area.
    :type maxh: float
    :param field: The measured H- or B-field:
    :type field: List[numpy.ndarray]
    """

    field_specifier: int
    boundaries: np.ndarray
    samples: np.ndarray
    maxh: float
    field: List[np.ndarray]

    def __init__(self,
                 field_specifier: int,
                 boundaries: np.ndarray,
                 samples: np.ndarray,
                 maxh: float,
                 field: List[np.ndarray] = list(),
                 x: np.ndarray = None,
                 y: np.ndarray = None,
                 z: np.ndarray = None,
                 X: np.ndarray = None,
                 Y: np.ndarray = None,
                 Z: np.ndarray = None,
                 h: np.ndarray = None) -> None:
        """Constructor method."""

        self.field_specifier = field_specifier
        self.boundaries = boundaries
        self.samples = samples
        self.maxh = maxh
        self.field = field

        self.h = np.zeros(3)

        if samples[0] > 1:
            self.x = np.linspace(boundaries[0, 0], boundaries[1, 0], int(samples[0]))
            self.h[0] = (boundaries[1, 0] - boundaries[0, 0]) / float(samples[0] - 1)
        else:
            self.x = np.array([(boundaries[0, 0] + boundaries[1, 0]) / 2])
        if samples[1] > 1:
            self.y = np.linspace(boundaries[0, 1], boundaries[1, 1], int(samples[1]))
            self.h[1] = (boundaries[1, 1] - boundaries[0, 1]) / float(samples[1] - 1)
        else:
            self.y = np.array([(boundaries[0, 1] + boundaries[1, 1]) / 2])
        if samples[2] > 1:
            self.z = np.linspace(boundaries[0, 2], boundaries[1, 2], int(samples[2]))
            self.h[2] = (boundaries[1, 2] - boundaries[0, 2]) / float(samples[2] - 1)
        else:
            self.z = np.array([(boundaries[0, 2] + boundaries[1, 2]) / 2])

        self.X, self.Y, self.Z = np.meshgrid(self.x, self.y, self.z)

    @classmethod
    def template(cls, sim_params: Dict[str, any] = None):

        if sim_params is not None:
            boundaries = sim_params['boundaries']
        else:
            boundaries = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])

        return cls(field_specifier=1,
                   boundaries=boundaries,
                   samples=np.array([11, 11, 1]),
                   maxh=2.0)

    @classmethod
    def from_dict(cls, dictionary: Dict[any]) -> FieldRecorder:
        """Method to init an instance of the Gear class by passing a dictionary with the corresponding
            arguments. Arguments that are in the dictionary and not in the class are ignored while arguments missing in
            the dictionary get initialised with the standard values defined in the template class method.

        :return: Instance of the FieldRecorder class.
        :rtype: FieldRecorder
        """

        template = FieldRecorder.template()

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
        dictionary.pop('x', None)
        dictionary.pop('y', None)
        dictionary.pop('z', None)
        dictionary.pop('X', None)
        dictionary.pop('Y', None)
        dictionary.pop('Z', None)
        dictionary.pop('h', None)
        dictionary.pop('field', None)

        return dictionary

    def reset(self):
        """Calls the init method with the actual class attributes."""

        self.__init__(self.field_specifier, self.boundaries, self.samples, self.maxh, list())

    def convert_to_si(self) -> None:
        """Calls the init method and converts the parameters from gui units to SI units."""

        self.__init__(self.field_specifier,
                      self.boundaries,
                      self.samples,
                      self.maxh)

    def gui(self) -> FieldRecorder:
        """Returns a copy of the class with attributes converted to units used in the gui."""

        return FieldRecorder(self.field_specifier,
                             self.boundaries,
                             self.samples,
                             self.maxh)

    def update(self, current_field: MagneticField) -> None:
        """Method to update the sensor measurement parameters for the current simulation step. Parameters to be updated
            are the B- or H-field.

        :param current_field: Current instance of the MagneticField class.
        :type current_field: MagneticField

        """

        if self.field_specifier == 1:
            self.field.append(current_field.get_b_field(self.X, self.Y, self.Z))
        elif self.field_specifier == 2:
            self.field.append(current_field.get_h_field(self.X, self.Y, self.Z))

    def get_data(self, field: List[np.ndarray]):
        self.field += field

    def set_data(self, data_dict: Dict[str, List], magnetic_field: MagneticField):
        if "field" not in data_dict:
            data_dict['field'] = list()
        if self.field_specifier == 1:
            data_dict['field'].append(magnetic_field.get_b_field(self.X, self.Y, self.Z))
        elif self.field_specifier == 2:
            data_dict['field'].append(magnetic_field.get_b_field(self.X, self.Y, self.Z))

        return data_dict
