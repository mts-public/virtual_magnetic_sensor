import abc
import numpy as np
from typing import Union


class MagneticField(metaclass=abc.ABCMeta):
    """Metaclass for magnetic fields. The virtual methods a magnetic field must provide to be able to communicate with
        the other classes of the application are specified in this class.
    """

    @abc.abstractmethod
    def create_field(self, t) -> None:
        """Method to initialize the magnetic field and perform the necessary calculations.

        :param t: Current time stamp:
        :type t: float

        """

        pass

    @abc.abstractmethod
    def draw(self) -> None:
        """Method to draw the magnetic field."""

        pass

    @abc.abstractmethod
    def get_h_field(self, x: np.ndarray, y: np.ndarray, z: np.ndarray) -> Union[np.ndarray, None]:
        """Method to extract the magnetic field strength on positions defined by a grid on x, y and z.

        :param x: x grid.
        :type x: numpy.ndarray
        :param y: y grid.
        :type y: numpy.ndarray
        :param z: z grid.
        :type z: numpy.ndarray

        :return: Magnetic field strength on the grid passed.
        :rtype: Union[np.ndarray, None]
        """

        return

    @abc.abstractmethod
    def get_b_field(self, x: np.ndarray, y: np.ndarray, z: np.ndarray) -> Union[np.ndarray, None]:
        """Method to extract the magnetic flux density on positions defined by a grid on x, y and z.

        :param x: x grid.
        :type x: numpy.ndarray
        :param y: y grid.
        :type y: numpy.ndarray
        :param z: z grid.
        :type z: numpy.ndarray

        :return: Magnetic flux density on the grid passed.
        :rtype: Union[np.ndarray, None]
        """

        return
