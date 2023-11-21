import netgen.csg as csg
from typing import List

from libs.elements.Sensor import Sensor

from libs.elements.sensors.GMRSensor import GMRSensor

from libs.simulation.ngsolve.CSGeometries.CSGGMRSensor import CSGGMRSensor


class CSGSensors:
    """Wrapper class to determine the type of the sensor and initiate an object of the specific class to build the
        geometry with netgen.csg.CSGeometry elements.

    :param sensors: List of sensors parameters.
    :type sensors: List[Sensor]
    """

    sensors: List[Sensor]
    bodies: List[csg.Solid]

    def __init__(self,
                 sensors: List[Sensor]) -> None:
        """Constructor method."""

        self.sensors = sensors
        self.bodies: List[csg.Solid] = list()
        for sensor in self.sensors:
            self.bodies.append(self.build_sensor_body(sensor))

    @staticmethod
    def build_sensor_body(sensor: Sensor) -> csg.Solid:
        """Method to generate the geometry of a sensor with the parameters specified in the committed component
            object.

        :param sensor: Sensor parameters.
        :type sensor: Sensor
        :return: Sensor geometry.
        :rtype: netgen.csg.Solid
        """

        sensor_geometry = csg.Solid
        if isinstance(sensor, GMRSensor):
            sensor_geometry = CSGGMRSensor(sensor)

        """from libs.elements.sensors.SensorTemplate import SensorTemplate
        from libs.simulation.ngsolve.CSGeometries.CSGSensorTemplate import CSGSensorTemplate
        if isinstance(sensor, SensorTemplate):
            sensor_geometry = CSGSensorTemplate(sensor)"""

        return sensor_geometry.body
