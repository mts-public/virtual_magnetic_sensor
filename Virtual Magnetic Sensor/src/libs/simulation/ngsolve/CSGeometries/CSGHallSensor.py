import netgen.csg as csg
import numpy as np

from libs.elements.sensors.HallSensor import HallSensor


class CSGHallSensor:
    """Generates the geometry for a hall sensor case in the simulation with netgen.csg.CSGeometry elements.

    :param hall_sensor: Object of the HallSensor class.
    :type hall_sensor: HallSensor
    """

    hall_sensor: HallSensor
    body: csg.Solid

    def __init__(self,
                 hall_sensor: HallSensor) -> None:
        """Constructor method."""

        self.hall_sensor = hall_sensor

        self.body = self.build_body()

    def build_body(self) -> csg.Solid:
        """Builds the geometry of the hall sensor with netgen.csg.CSGeometry elements.

        :return: Hall sensor geometry.
        :type: netgen.csg.Solid
        """

        left: csg.Solid = csg.Plane(
            csg.Pnt(self.hall_sensor.pos - self.hall_sensor.transformation_matrix.dot(self.hall_sensor.dim / 2)),
            csg.Vec(self.hall_sensor.transformation_matrix.dot(np.array([-1, 0, 0])))).bc("magnet")
        right: csg.Solid = csg.Plane(
            csg.Pnt(self.hall_sensor.pos + self.hall_sensor.transformation_matrix.dot(self.hall_sensor.dim / 2)),
            csg.Vec(self.hall_sensor.transformation_matrix.dot(np.array([1, 0, 0])))).bc("magnet")
        front: csg.Solid = csg.Plane(
            csg.Pnt(self.hall_sensor.pos - self.hall_sensor.transformation_matrix.dot(self.hall_sensor.dim / 2)),
            csg.Vec(self.hall_sensor.transformation_matrix.dot(np.array([0, -1, 0])))).bc("magnet")
        back: csg.Solid = csg.Plane(
            csg.Pnt(self.hall_sensor.pos + self.hall_sensor.transformation_matrix.dot(self.hall_sensor.dim / 2)),
            csg.Vec(self.hall_sensor.transformation_matrix.dot(np.array([0, 1, 0])))).bc("magnet")
        bottom: csg.Solid = csg.Plane(
            csg.Pnt(self.hall_sensor.pos - self.hall_sensor.transformation_matrix.dot(self.hall_sensor.dim / 2)),
            csg.Vec(self.hall_sensor.transformation_matrix.dot(np.array([0, 0, -1])))).bc("magnet")
        top: csg.Solid = csg.Plane(
            csg.Pnt(self.hall_sensor.pos + self.hall_sensor.transformation_matrix.dot(self.hall_sensor.dim / 2)),
            csg.Vec(self.hall_sensor.transformation_matrix.dot(np.array([0, 0, 1])))).bc("magnet")

        body: csg.Solid = left * right * front * back * bottom * top

        return body
