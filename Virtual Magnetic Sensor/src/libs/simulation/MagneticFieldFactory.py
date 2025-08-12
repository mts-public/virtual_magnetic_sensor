from libs.simulation.ngsolve.NGField import NGField
from libs.DataHandler import DataHandler


class MagneticFieldFactory:
    """Class handles the initialisation of the magnetic field based on the existing implementations."""

    @staticmethod
    def init_field(field_type: str, data_handler: DataHandler) -> NGField:
        """Initialize an object of the MagneticField class based on a subclass.

        :param field_type: Specifies the requested implementation.
        :type field_type: string
        :param data_handler: Object of the Data class containing all simulation relevant data.
        :type data_handler: DataHandler

        :return: Object of a certain magnetic field subclass.
        :rtype: NGField
        """

        if field_type == 'ngsolve':
            return NGField(data_handler)
