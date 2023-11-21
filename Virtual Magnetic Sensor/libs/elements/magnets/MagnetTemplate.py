from __future__ import annotations
from libs.elements.Magnet import Magnet
from typing import Dict


class MagnetTemplate(Magnet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @ classmethod
    def template(cls) -> MagnetTemplate:
        """Class method to init the class with a set of default values.

        :return: Object of the MagnetTemplate class.
        :rtype: SensorTemplate
        """

        # Return object of the MagnetTemplate class with default values

        return cls()

    @classmethod
    def from_dict(cls, dictionary: Dict[any]) -> MagnetTemplate:
        """Method to init an instance of the MagnetTemplate class by passing a dictionary with the corresponding
            arguments.

        :return: Instance of the MagnetTemplate class.
        :rtype: MagnetTemplate
        """

        # No adjustment necessary

        template = MagnetTemplate.template()

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

    def reset(self) -> None:
        """Calls the init method with the actual class attributes."""

        # Replace **vars(self) by the attributes of the init method to reset all values that are not passed to the
        # init method when calling reset

        self.__init__(**vars(self))

    def convert_to_si(self) -> None:
        """Calls the init method and converts the parameters from gui units to SI units."""

        # Convert GUI values into SI values and call the __init__() method. Lengths are given in mm.

        self.__init__()

    def gui(self) -> MagnetTemplate:
        """Returns a copy of the class with attributes converted to units used in the gui.

        :return: Object of the MagnetTemplate class.
        :rtype: SensorTemplate
        """

        # Convert SI values into values that are used in the GUI and return the result as object of the
        # MagnetTemplate class

        return MagnetTemplate()
