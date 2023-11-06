import netgen.csg as csg
from math import pi, sin, cos, tan
import numpy as np

from libs.elements.components.Gear import Gear


class CSGGear:
    """Generates the geometry for a gear in the simulation with netgen.csg.CSGeometry elements.

    :param gear: Object of the gear class.
    :type gear: Gear
    """

    gear: Gear
    body: csg.Solid

    def __init__(self,
                 gear: Gear) -> None:
        """Constructor method."""

        self.gear = gear

        self.body = self.build_body()

    def build_body(self) -> csg.Solid:
        """Builds the geometry of the gear with netgen.csg.CSGeometry elements.

        :return: Gear geometry.
        :type: netgen.csg.Solid
        """

        angle: float = self.gear.theta
        position: np.ndarray = self.gear.position(angle)
        axis: np.ndarray = self.gear.rotation_axis(angle)
        trans_matrix: np.ndarray = self.gear.transformation_matrix(axis)

        front = csg.Plane(csg.Pnt(position - self.gear.length/2 * axis), csg.Vec(-axis))
        back = csg.Plane(csg.Pnt(position + self.gear.length/2 * axis), csg.Vec(axis))

        if self.gear.diameter[0] > 0.0:
            body = (csg.Cylinder(csg.Pnt(position - self.gear.length/2 * axis),
                                 csg.Pnt(position + self.gear.length/2 * axis),
                                 self.gear.diameter[1] / 2 - self.gear.tooth_height / 2)
                    - csg.Cylinder(csg.Pnt(position - self.gear.length/2 * axis),
                                   csg.Pnt(position + self.gear.length/2 * axis),
                                   self.gear.diameter[0] / 2)) * front * back
        else:
            body = csg.Cylinder(csg.Pnt(position - self.gear.length/2 * axis),
                                csg.Pnt(position + self.gear.length/2 * axis),
                                self.gear.diameter[1] / 2 - self.gear.tooth_height / 2) * front * back

        n_idx = 0
        phi = angle

        if self.gear.n > 0:
            while n_idx < self.gear.n:
                if self.gear.display_teeth_angle[0] <= phi % (2*pi) <= self.gear.display_teeth_angle[1]:
                    phi_vec = np.array([cos(phi), sin(phi), 0.0])

                    top_support = csg.Pnt(position + (self.gear.diameter[1] / 2 + self.gear.tooth_height / 2 + (
                        self.gear.tooth_deviations[1] if n_idx == self.gear.dev_tooth_num else 0)) * trans_matrix.dot(
                        phi_vec))
                    top_normal = csg.Vec(trans_matrix.dot(phi_vec))
                    top = csg.Plane(top_support, top_normal)

                    bottom_support = csg.Pnt(position + (
                            self.gear.diameter[1] / 2 - self.gear.tooth_height) * trans_matrix.dot(phi_vec))
                    bottom_normal = csg.Vec(trans_matrix.dot(-phi_vec))
                    bottom = csg.Plane(bottom_support, bottom_normal)

                    left_flank_support = csg.Pnt(position + trans_matrix.dot(
                        (self.gear.tooth_width / 2 + self.gear.diameter[1] / 2 * tan(self.gear.tooth_flank_angle + (
                            self.gear.tooth_deviations[0] if n_idx == self.gear.dev_tooth_num else 0.0))) * np.array(
                            [-sin(phi), cos(phi), 0.0])))
                    left_flank_normal = csg.Vec(trans_matrix.dot(np.array([-sin(phi - self.gear.tooth_flank_angle),
                                                                           cos(phi - self.gear.tooth_flank_angle),
                                                                           0.0])))
                    left_flank = csg.Plane(left_flank_support, left_flank_normal)

                    right_flank_support = csg.Pnt(position - trans_matrix.dot(
                        (self.gear.tooth_width / 2 + self.gear.diameter[1] / 2 * tan(self.gear.tooth_flank_angle + (
                            self.gear.tooth_deviations[2] if n_idx == self.gear.dev_tooth_num else 0.0))) * np.array(
                            [-sin(phi), cos(phi), 0.0])))
                    right_flank_normal = csg.Vec(trans_matrix.dot(np.array([sin(phi + self.gear.tooth_flank_angle),
                                                                            -cos(phi + self.gear.tooth_flank_angle),
                                                                            0.0])))
                    right_flank = csg.Plane(right_flank_support, right_flank_normal)

                    left_chamfer_support = csg.Pnt(
                        position + (self.gear.diameter[1] / 2 + self.gear.tooth_height / 2) * trans_matrix.dot(phi_vec)
                        + (self.gear.tooth_width / 2 - sin(self.gear.tooth_flank_angle) * self.gear.tooth_height / 2)
                        * trans_matrix.dot(
                            np.array([-sin(phi), cos(phi), 0.0])
                            + (self.gear.chamfer_depth * trans_matrix.dot(
                                np.array([-sin(self.gear.chamfer_angle), -cos(self.gear.chamfer_angle), 0.0]))
                               * trans_matrix.dot(phi_vec))))
                    left_chamfer_normal = csg.Vec(
                        trans_matrix.dot(np.array(
                            [cos(phi + self.gear.chamfer_angle), sin(phi + self.gear.chamfer_angle), 0.0])))
                    left_chamfer = csg.Plane(left_chamfer_support, left_chamfer_normal)

                    right_chamfer_support = csg.Pnt(
                        position + (self.gear.diameter[1] / 2 + self.gear.tooth_height / 2) * trans_matrix.dot(phi_vec)
                        - (self.gear.tooth_width / 2 - sin(self.gear.tooth_flank_angle) * self.gear.tooth_height / 2)
                        * trans_matrix.dot(
                            np.array([-sin(phi), cos(phi), 0.0])
                            - (self.gear.chamfer_depth * trans_matrix.dot(
                                np.array([-sin(self.gear.chamfer_angle), -cos(self.gear.chamfer_angle), 0.0]))
                               * trans_matrix.dot(phi_vec))))
                    right_chamfer_normal = csg.Vec(trans_matrix.dot(np.array(
                        [cos(phi - self.gear.chamfer_angle), sin(phi - self.gear.chamfer_angle), 0.0])))
                    right_chamfer = csg.Plane(right_chamfer_support, right_chamfer_normal)

                    if np.isclose(self.gear.chamfer_depth, 0.0):
                        tooth = top * front * back * left_flank * right_flank * bottom
                    else:
                        tooth = top * front * back * left_flank * right_flank * left_chamfer * right_chamfer * bottom

                    body += tooth

                phi += 2 * pi / self.gear.n
                n_idx += 1

        return body
