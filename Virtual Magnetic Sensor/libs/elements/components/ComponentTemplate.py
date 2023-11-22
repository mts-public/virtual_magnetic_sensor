from __future__ import annotations
from libs.elements.Component import Component
from typing import Dict


class ComponentTemplate(Component):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @ classmethod
    def template(cls) -> ComponentTemplate:
        """Class method to init the class with a set of default values.

        :return: Object of the SensorTemplate class.
        :rtype: SensorTemplate
        """

        # Return object of the ComponentTemplate class with default values

        return cls()

    @classmethod
    def from_dict(cls, dictionary: Dict[any]) -> ComponentTemplate:
        """Method to init an instance of the SensorTemplate class by passing a dictionary with the corresponding
            arguments.

        :return: Instance of the ComponentTemplate class.
        :rtype: ComponentTemplate
        """

        # No adjustment necessary

        template = ComponentTemplate.template()

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

    def gui(self) -> ComponentTemplate:
        """Returns a copy of the class with attributes converted to units used in the gui.

        :return: Object of the ComponentTemplate class.
        :rtype: ComponentTemplate
        """

        # Convert SI values into values that are used in the GUI and return the result as object of the
        # SensorTemplate class

        return ComponentTemplate()

    def update(self, t: float) -> None:
        """Method to update the states of a time dependent component.

        :param t: Current time stamp.
        :type t: float
        """

        # Add the time dependent behaviour of moving components in the simulation here
