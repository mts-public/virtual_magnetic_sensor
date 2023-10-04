import netgen.csg as csg
from math import sin, cos
import numpy as np

from libs.elements.components.GearRack import GearRack


class CSGGearRack:
    """Generates the geometry for a gear rack in the simulation with netgen.csg.CSGeometry elements.

    :param gear_rack: Object of the gear rack class.
    :type gear_rack: GearRack
    """

    gear_rack: GearRack
    body: csg.Solid

    def __init__(self,
                 gear_rack: GearRack) -> None:
        """Constructor method."""

        self.gear_rack = gear_rack

        self.body = self.build_body()

    def build_body(self) -> csg.Solid:
        """Builds the geometry of the gear rack with netgen.csg.CSGeometry elements.

        :return: Gear Rack geometry.
        :type: netgen.csg.Solid
        """

        trans_matrix = self.gear_rack.transformation_matrix()

        left: csg.Solid = csg.Plane(
            csg.Pnt(self.gear_rack.position() - trans_matrix.dot(self.gear_rack.dim / 2)),
            csg.Vec(trans_matrix.dot(np.array([-1, 0, 0]))))
        right: csg.Solid = csg.Plane(
            csg.Pnt(self.gear_rack.position() + trans_matrix.dot(self.gear_rack.dim / 2)),
            csg.Vec(trans_matrix.dot(np.array([1, 0, 0]))))
        bottom: csg.Solid = csg.Plane(
            csg.Pnt(self.gear_rack.position() - trans_matrix.dot(self.gear_rack.dim / 2)),
            csg.Vec(trans_matrix.dot(np.array([0, -1, 0]))))
        top: csg.Solid = csg.Plane(
            csg.Pnt(self.gear_rack.position() + trans_matrix.dot(self.gear_rack.dim / 2)),
            csg.Vec(trans_matrix.dot(np.array([0, 1, 0]))))
        back: csg.Solid = csg.Plane(
            csg.Pnt(self.gear_rack.position() - trans_matrix.dot(self.gear_rack.dim / 2)),
            csg.Vec(trans_matrix.dot(np.array([0, 0, -1]))))
        front: csg.Solid = csg.Plane(
            csg.Pnt(self.gear_rack.position() + trans_matrix.dot(self.gear_rack.dim / 2)),
            csg.Vec(trans_matrix.dot(np.array([0, 0, 1]))))

        body: csg.Solid = left * right * bottom * top * back * front

        if self.gear_rack.tooth_height > 0 and self.gear_rack.tooth_width > 0:
            tooth_top: csg.Solid = csg.Plane(
                csg.Pnt(self.gear_rack.position() + trans_matrix.dot(
                    self.gear_rack.dim / 2 + np.array([0.0, self.gear_rack.tooth_height, 0.0]))),
                csg.Vec(trans_matrix.dot(np.array([0, 1, 0]))))
            tooth_bottom: csg.Solid = csg.Plane(
                csg.Pnt(self.gear_rack.position() + trans_matrix.dot(self.gear_rack.dim / 2)),
                csg.Vec(trans_matrix.dot(np.array([0, -1, 0]))))

            idx: int = 0
            while self.gear_rack.tooth_width + idx*self.gear_rack.tooth_pitch <= self.gear_rack.dim[0]:
                left_flank_support = csg.Pnt(self.gear_rack.position() + trans_matrix.dot(
                    (-self.gear_rack.dim / 2 + np.array([idx * self.gear_rack.tooth_pitch + sin(
                        self.gear_rack.tooth_flank_angle) * self.gear_rack.tooth_height / 2,
                                                         self.gear_rack.dim[1] + self.gear_rack.tooth_height / 2,
                                                         0.0]))))
                left_flank_normal = csg.Vec(trans_matrix.dot(np.array([-cos(self.gear_rack.tooth_flank_angle),
                                                                       sin(self.gear_rack.tooth_flank_angle),
                                                                       0.0])))
                left_flank = csg.Plane(left_flank_support, left_flank_normal)

                right_flank_support = csg.Pnt(self.gear_rack.position() + trans_matrix.dot(
                    (-self.gear_rack.dim / 2 + np.array(
                        [self.gear_rack.tooth_width + idx * self.gear_rack.tooth_pitch + sin(
                            self.gear_rack.tooth_flank_angle) * self.gear_rack.tooth_height / 2,
                         self.gear_rack.dim[1] + self.gear_rack.tooth_height / 2,
                         0.0]))))
                right_flank_normal = csg.Vec(trans_matrix.dot(np.array([cos(self.gear_rack.tooth_flank_angle),
                                                                       sin(self.gear_rack.tooth_flank_angle),
                                                                       0.0])))
                right_flank = csg.Plane(right_flank_support, right_flank_normal)

                tooth = tooth_top * tooth_bottom * back * front * left_flank * right_flank

                body += tooth
                idx += 1

        return body
