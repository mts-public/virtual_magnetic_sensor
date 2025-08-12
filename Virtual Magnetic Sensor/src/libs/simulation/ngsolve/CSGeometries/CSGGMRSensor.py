import netgen.csg as csg
import numpy as np

from libs.elements.sensors.GMRSensor import GMRSensor


class CSGGMRSensor:
    """Generates the geometry for a Sensitec GMR sensor in the simulation with netgen.csg.CSGeometry elements.

    :param gmr_sensor: Object of the GMRSensor class
    :type gmr_sensor: GMRSensor
    """

    gmr_sensor: GMRSensor
    body: csg.Solid

    def __init__(self,
                 gmr_sensor: GMRSensor) -> None:
        """Constructor method."""

        self.gmr_sensor = gmr_sensor
        self.body = self.build_body()

    def build_body(self) -> csg.Solid:
        """Builds the geometry of the Sensitec GMR sensor with netgen.csg.CSGeometry elements.

        :return: GMR Sensor geometry.
        :type: netgen.csg.Solid
        """

        left: csg.Solid = csg.Plane(
            csg.Pnt(self.gmr_sensor.pos - self.gmr_sensor.transformation_matrix.dot(self.gmr_sensor.dim / 2)),
            csg.Vec(self.gmr_sensor.transformation_matrix.dot(np.array([-1, 0, 0])))).bc("sensor")
        right: csg.Solid = csg.Plane(
            csg.Pnt(self.gmr_sensor.pos + self.gmr_sensor.transformation_matrix.dot(self.gmr_sensor.dim / 2)),
            csg.Vec(self.gmr_sensor.transformation_matrix.dot(np.array([1, 0, 0])))).bc("sensor")
        front: csg.Solid = csg.Plane(
            csg.Pnt(self.gmr_sensor.pos - self.gmr_sensor.transformation_matrix.dot(self.gmr_sensor.dim / 2)),
            csg.Vec(self.gmr_sensor.transformation_matrix.dot(np.array([0, -1, 0])))).bc("sensor")
        back: csg.Solid = csg.Plane(
            csg.Pnt(self.gmr_sensor.pos + self.gmr_sensor.transformation_matrix.dot(self.gmr_sensor.dim / 2)),
            csg.Vec(self.gmr_sensor.transformation_matrix.dot(np.array([0, 1, 0])))).bc("sensor")
        bottom: csg.Solid = csg.Plane(
            csg.Pnt(self.gmr_sensor.pos - self.gmr_sensor.transformation_matrix.dot(self.gmr_sensor.dim / 2)),
            csg.Vec(self.gmr_sensor.transformation_matrix.dot(np.array([0, 0, -1])))).bc("sensor")
        top: csg.Solid = csg.Plane(
            csg.Pnt(self.gmr_sensor.pos + self.gmr_sensor.transformation_matrix.dot(self.gmr_sensor.dim / 2)),
            csg.Vec(self.gmr_sensor.transformation_matrix.dot(np.array([0, 0, 1])))).bc("sensor")

        body: csg.Solid = left * right * front * back * bottom * top

        return body
