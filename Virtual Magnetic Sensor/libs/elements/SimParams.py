from __future__ import annotations
import numpy as np
from typing import Dict


class SimParams:
    """The parameters to specify the finite element space are summarized in this class.

    :param boundaries: The dimensions in mm of the 3D space containing the scenery.
    :type boundaries: numpy.ndarray
    :param t0: Start time of the simulation.
    :type t0: float
    :param t1: End time of the simulation.
    :type t1: float
    :param samples: Number of time samples.
    :type samples: int
    :param maxh_global: The maximum mesh size of all simulation elements including the air surrounding the elements.
    :type maxh_global: float
    :param tol: The maximum tolerated iteration error of the finite element magnetic field calculation.
    :type tol: float
    :param maxit: The maximum number of allowed iterations to calculate the magnetic field.
    :type maxit: int
    :param t: Array containing the time stamps of the simulation.
    :type t: np.ndarray
    """

    boundaries: np.ndarray
    t0: float
    t1: float
    samples: int
    maxh_global: float
    tol: float
    maxit: int
    t: np.ndarray

    def __init__(self,
                 boundaries: np.ndarray,
                 t0: float,
                 t1: float,
                 samples: int,
                 maxh_global: float,
                 tol: float,
                 maxit: int,
                 **kwargs) -> None:
        """Constructor method."""

        self.boundaries = boundaries
        self.t0 = t0
        self.t1 = t1
        self.samples = samples
        self.maxh_global = maxh_global
        self.tol = tol
        self.maxit = maxit

        self.t = np.linspace(self.t0, self.t1, samples)
        if samples > 1:
            self.dt = (t1 - t0) / (samples - 1)
        else:
            self.dt = 0.0

    @classmethod
    def template(cls):

        return cls(boundaries=np.array([[-10.0, -10.0, -5.0], [10.0, 10.0, 5.0]]),
                   t0=0.0,
                   t1=1.0,
                   samples=11,
                   maxh_global=5.0,
                   tol=1e-6,
                   maxit=100)

    @classmethod
    def from_dict(cls, dictionary: Dict[any]) -> SimParams:
        """Method to init an instance of the Gear class by passing a dictionary with the corresponding
            arguments. Arguments that are in the dictionary and not in the class are ignored while arguments missing in
            the dictionary get initialised with the standard values defined in the template class method.

        :return: Instance of the SimParams class.
        :rtype: SimParams
        """

        template = SimParams.template()

        for key, value in dictionary.items():
            if hasattr(template, key):
                setattr(template, key, value)

        return cls(**template.to_dict())

    def to_dict(self) -> Dict[str, any]:
        """Method creates a dictionary of the class members that will be stored in the HDF5 file. Variables created
            automatically when instantiating an object of the class are excluded from the dictionary. This creates the
            opportunity to initiate an instance of the class by parsing the dictionary as argument.

        :return: The dictionary of the classes members.
        :rtype: Dict[str, any]s
        """

        dictionary: Dict[str, any] = vars(self).copy()

        return dictionary

    def gui_dict(self) -> Dict[str, any]:
        """Method creates a dictionary of the class members that will be stored in the HDF5 file. Variables created
            automatically when instantiating an object of the class are excluded from the dictionary. This creates the
            opportunity to initiate an instance of the class by parsing the dictionary as argument.

        :return: The dictionary of the classes members.
        :rtype: Dict[str, any]
        """

        dictionary: dict = vars(self).copy()
        dictionary.pop('t')
        dictionary.pop('dt')

        return dictionary

    def reset(self) -> None:
        """Calls the init method with the actual class attributes."""

        self.__init__(self.boundaries, self.t0, self.t1, self.samples, self.maxh_global, self.tol, self.maxit)
