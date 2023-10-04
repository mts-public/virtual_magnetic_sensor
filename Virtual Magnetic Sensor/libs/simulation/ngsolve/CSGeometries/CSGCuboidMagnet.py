import netgen.csg as csg
import numpy as np

from libs.elements.magnets.CuboidMagnet import CuboidMagnet


class CSGCuboidMagnet:
    """Generates the geometry for a cuboid magnet in the simulation with netgen.csg.CSGeometry elements.

    :param cuboid_magnet: Object of the CuboidMagnet class.
    :type cuboid_magnet: CuboidMagnet
    """

    cuboid_magnet: CuboidMagnet
    body: csg.Solid

    def __init__(self,
                 cuboid_magnet: CuboidMagnet) -> None:
        """Constructor method."""

        self.cuboid_magnet = cuboid_magnet
        self.body = self.build_body()

    def build_body(self) -> csg.Solid:
        """Builds the geometry of the cuboid magnet with netgen.csg.CSGeometry elements.

        :return: Cuboid magnet geometry.
        :type: netgen.csg.Solid
        """

        left: csg.Solid = csg.Plane(
            csg.Pnt(self.cuboid_magnet.pos - self.cuboid_magnet.transformation_matrix.dot(self.cuboid_magnet.dim / 2)),
            csg.Vec(self.cuboid_magnet.transformation_matrix.dot(np.array([-1, 0, 0])))).bc("magnet")
        right: csg.Solid = csg.Plane(
            csg.Pnt(self.cuboid_magnet.pos + self.cuboid_magnet.transformation_matrix.dot(self.cuboid_magnet.dim / 2)),
            csg.Vec(self.cuboid_magnet.transformation_matrix.dot(np.array([1, 0, 0])))).bc("magnet")
        front: csg.Solid = csg.Plane(
            csg.Pnt(self.cuboid_magnet.pos - self.cuboid_magnet.transformation_matrix.dot(self.cuboid_magnet.dim / 2)),
            csg.Vec(self.cuboid_magnet.transformation_matrix.dot(np.array([0, -1, 0])))).bc("magnet")
        back: csg.Solid = csg.Plane(
            csg.Pnt(self.cuboid_magnet.pos + self.cuboid_magnet.transformation_matrix.dot(self.cuboid_magnet.dim / 2)),
            csg.Vec(self.cuboid_magnet.transformation_matrix.dot(np.array([0, 1, 0])))).bc("magnet")

        bottom: csg.Solid = csg.Plane(
            csg.Pnt(self.cuboid_magnet.pos - self.cuboid_magnet.transformation_matrix.dot(self.cuboid_magnet.dim / 2)),
            csg.Vec(self.cuboid_magnet.transformation_matrix.dot(np.array([0, 0, -1])))).bc("magnet")
        top: csg.Solid = csg.Plane(
            csg.Pnt(self.cuboid_magnet.pos + self.cuboid_magnet.transformation_matrix.dot(self.cuboid_magnet.dim / 2)),
            csg.Vec(self.cuboid_magnet.transformation_matrix.dot(np.array([0, 0, 1])))).bc("magnet")

        body: csg.Solid = left * right * front * back * bottom * top

        return body
