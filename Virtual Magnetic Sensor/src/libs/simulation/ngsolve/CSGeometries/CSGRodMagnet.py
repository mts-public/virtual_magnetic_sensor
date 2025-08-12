import netgen.csg as csg

from libs.elements.magnets.RodMagnet import RodMagnet


class CSGRodMagnet:
    """Generates the geometry for a rod magnet in the simulation with netgen.csg.CSGeometry elements.

    :param rod_magnet: Object of the RodMagnet class.
    :type rod_magnet: RodMagnet
    """

    rod_magnet: RodMagnet
    body: csg.Solid

    def __init__(self,
                 rod_magnet: RodMagnet) -> None:
        """Constructor method."""

        self.rod_magnet = rod_magnet
        self.body = self.build_body()

    def build_body(self) -> csg.Solid:
        """Builds the geometry of the rod magnet with netgen.csg.CSGeometry elements.

        :return: Rod magnet geometry.
        :type: netgen.csg.Solid
        """

        front: csg.Solid = csg.Plane(
            csg.Pnt(self.rod_magnet.pos - self.rod_magnet.length / 2 * self.rod_magnet.axis),
            csg.Vec(-self.rod_magnet.axis)).bc("magnet")
        back: csg.Solid = csg.Plane(
            csg.Pnt(self.rod_magnet.pos + self.rod_magnet.length / 2 * self.rod_magnet.axis),
            csg.Vec(self.rod_magnet.axis)).bc("magnet")

        body: csg.Solid = csg.Cylinder(
            csg.Pnt(self.rod_magnet.pos - self.rod_magnet.length / 2 * self.rod_magnet.axis),
            csg.Pnt(self.rod_magnet.pos + self.rod_magnet.length / 2 * self.rod_magnet.axis),
            self.rod_magnet.radius).bc("magnet") * front * back

        return body
