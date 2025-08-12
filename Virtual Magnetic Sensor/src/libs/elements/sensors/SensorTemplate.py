from __future__ import annotations
from libs.elements.Sensor import Sensor
from libs.simulation.MagneticField import MagneticField
from typing import Dict, List


class SensorTemplate(Sensor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'measurement_data' in kwargs:
            self.measurement_data = kwargs['measurement_data']
        else:
            self.measurement_data = list()

    @ classmethod
    def template(cls) -> SensorTemplate:
        """Class method to init the class with a set of default values.

        :return: Object of the SensorTemplate class.
        :rtype: SensorTemplate
        """

        # Return object of the SensorTemplate class with default values

        return cls()

    @classmethod
    def from_dict(cls, dictionary: Dict[any]) -> SensorTemplate:
        """Method to init an instance of the SensorTemplate class by passing a dictionary with the corresponding
            arguments.

        :return: Instance of the SensorTemplate class.
        :rtype: SensorTemplate
        """

        # No adjustment necessary

        template = SensorTemplate.template()

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

        # Remove attributes from the dictionary that should not be part of the metadata
        # dictionary.pop('attribute', None)

        return dictionary

    def gui_dict(self) -> Dict[str, any]:
        """Method creates a dictionary of the class members that will be stored in the ini file. Variables not passed
        to the init method are excluded from the dictionary. This creates the opportunity to initiate an instance of
        the class by parsing the dictionary as argument.

        :return: The dictionary of the classes members.
        :rtype: Dict[str, any]
        """

        dictionary: Dict[str, any] = vars(self.gui()).copy()

        # Remove attributes from the dictionary that should not be part of the metadata
        # dictionary.pop('attribute', None)

        return dictionary

    def reset(self) -> None:
        """Calls the init method with the actual class attributes."""

        # Replace **vars(self) by the attributes of the init method to reset all values that are not passed to the
        # init method when calling reset

        self.__init__(**vars(self))

    def convert_to_si(self) -> None:
        """Calls the init method and converts the parameters from gui units to SI units."""

        # Convert GUI values into SI values and call the __init__() method. Lengths are given in mm.

        self.__init__()

    def gui(self) -> SensorTemplate:
        """Returns a copy of the class with attributes converted to units used in the gui.

        :return: Object of the SensorTemplate class.
        :rtype: SensorTemplate
        """

        # Convert SI values into values that are used in the GUI and return the result as object of the
        # SensorTemplate class

        return SensorTemplate()

    def get_data(self, measurement_data) -> None:
        """Method to pass the measurement data saved in a dictionary to the sensor object."""

        self.measurement_data += measurement_data  # Expand with further measurement parameters if necessary

    def set_data(self, data_dict: Dict[str, List], field: MagneticField) -> Dict[str, List]:
        """Method to update the sensor measurement parameters for the current simulation step.

        :param data_dict: Dictionary with the measurement data, shared between processes.
        :type data_dict: Dict[str, List]
        :param field: Instance of the MagneticField class.
        :type field: MagneticField
        """

        # Implement sensor logic here
        # Save the measured variables in the measurement_data attribute or create own attributes according to the
        # example of measurement_data (modify get_data method as well)

        measured_value_at_current_time_step: float = 0.0

        if "measurement_data" not in data_dict:
            data_dict['measurement_data'] = list()
        data_dict['measurement_data'].append(measured_value_at_current_time_step)

        return data_dict
