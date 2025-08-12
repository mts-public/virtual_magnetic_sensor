import netgen.csg as csg

from libs.elements.components.Shaft import Shaft


class CSGShaft:
    """Generates the geometry for a shaft in the simulation with netgen.csg.CSGeometry elements.

    :param shaft: Object of the shaft class.
    :type shaft: Shaft
    """

    shaft: Shaft
    body: csg.Solid

    def __init__(self,
                 shaft: Shaft) -> None:
        """Constructor method."""

        self.shaft = shaft

        self.body = self.build_body()

    def build_body(self) -> csg.Solid:
        """Builds the geometry of the shaft with netgen.csg.CSGeometry elements.

        :return: Shaft geometry.
        :type: netgen.csg.Solid
        """

        front = csg.Plane(csg.Pnt(self.shaft.pos - self.shaft.length/2 * self.shaft.axis), csg.Vec(-self.shaft.axis))
        back = csg.Plane(csg.Pnt(self.shaft.pos + self.shaft.length/2 * self.shaft.axis), csg.Vec(self.shaft.axis))

        if self.shaft.diameter[0] > 0.0:
            body = (csg.Cylinder(csg.Pnt(self.shaft.pos - self.shaft.length/2 * self.shaft.axis),
                                 csg.Pnt(self.shaft.pos + self.shaft.length/2 * self.shaft.axis),
                                 self.shaft.diameter[1] / 2)
                    - csg.Cylinder(csg.Pnt(self.shaft.pos - self.shaft.length/2 * self.shaft.axis),
                                   csg.Pnt(self.shaft.pos + self.shaft.length/2 * self.shaft.axis),
                                   self.shaft.diameter[0] / 2)) * front * back
        else:
            body = csg.Cylinder(csg.Pnt(self.shaft.pos - self.shaft.length/2 * self.shaft.axis),
                                csg.Pnt(self.shaft.pos + self.shaft.length/2 * self.shaft.axis),
                                self.shaft.diameter[1] / 2) * front * back

        return body
