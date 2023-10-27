import numpy as np
from math import radians

from libs.elements.components.Gear import Gear


def test_from_dict_and_to_dict():
    gear = Gear(pos=np.array([1.0, 2.0, 3.0]),
                axis_0=np.array([np.sqrt(1 / 2), np.sqrt(1 / 4), np.sqrt(1 / 4)]),
                omega=radians(11.25),
                diameter=np.array([5.0, 20.37]),
                length=3.0,
                tooth_height=0.7,
                tooth_width=0.5,
                n=64,
                display_teeth_angle=np.radians(np.array([10.0, 350.0])),
                tooth_flank_angle=radians(5.0),
                mu_r=6000.0,
                eccentricity=100.0 * 1e-3,
                wobble_angle=radians(3.0),
                chamfer_depth=100.0 * 1e-3,
                chamfer_angle=radians(30.0),
                dev_tooth_num=32,
                tooth_deviations=np.array([0.0, -500.0, 0.0]) * 1e-3,
                maxh=2.5,
                rotate_mesh=True,
                rotate_mesh_max_angle=radians(4.0))
    for key, value in Gear.template().from_dict(gear.to_dict()).__dict__.items():
        if not np.allclose(value, gear.__dict__[key]):
            assert False

    assert True


def test_si_to_gui_to_si():
    gear = Gear.template()
    gear.gui().convert_to_si()
    for key, value in gear.__dict__.items():
        if not np.allclose(value, gear.__dict__[key]):
            assert False

    assert True


def test_update():
    t = 1.0
    gear = Gear.template()
    gear.update(t)

    assert np.allclose(gear.theta, Gear.template().omega * t)


def test_reset():
    t = 1.0
    gear = Gear.template()
    gear.update(t)
    gear.reset()

    assert gear.theta == 0.0


def test_transformation_matrix():
    axis = np.array([1.0, 1.0, 1.0])
    trans_matrix = np.array([[np.sqrt(1 / 2), np.sqrt(1 / 6), np.sqrt(1 / 3)],
                             [-np.sqrt(1 / 2), np.sqrt(1 / 6), np.sqrt(1 / 3)],
                             [0.0, -np.sqrt(2 / 3), np.sqrt(1 / 3)]])

    assert np.allclose(Gear.template().transformation_matrix(axis), trans_matrix)


def test_transformation_matrix_eye():
    axis = np.array([0.0, 0.0, 1.0])

    assert np.allclose(Gear.template().transformation_matrix(axis), np.eye(3))


def test_transformation_matrix_negativ_eye():
    axis = np.array([0.0, 0.0, -1.0])

    assert np.allclose(Gear.template().transformation_matrix(axis), -np.eye(3))


def test_rotation_axis():

    def rot_x(phi: float):
        return np.array([[1, 0, 0], [0, np.cos(phi), -np.sin(phi)], [0, np.sin(phi), np.cos(phi)]])

    def rot_y(phi: float):
        return np.array([[np.cos(phi), 0, np.sin(phi)], [0, 1, 0], [-np.sin(phi), 0, np.cos(phi)]])

    gear = Gear.template()
    alpha = radians(45.0)
    gear.wobble_angle = alpha
    vec1 = np.column_stack((gear.rotation_axis(radians(0.0)),
                           gear.rotation_axis(radians(90.0)),
                           gear.rotation_axis(radians(180.0)),
                           gear.rotation_axis(radians(270.0))))

    vec2 = np.column_stack((np.matmul(rot_y(alpha), gear.axis_0),
                           np.matmul(rot_x(-alpha), gear.axis_0),
                           np.matmul(rot_y(-alpha), gear.axis_0),
                           np.matmul(rot_x(alpha), gear.axis_0)))

    assert np.allclose(vec1, vec2)


def test_pos_and_eccentricity():
    gear = Gear.template()
    e = 1.0
    gear.eccentricity = e
    vec1 = np.column_stack((gear.position(radians(0.0)),
                           gear.position(radians(90.0)),
                           gear.position(radians(180.0)),
                           gear.position(radians(270.0))))

    vec2 = np.column_stack((np.array([1, 0, 0]),
                           np.array([0, 1, 0]),
                           np.array([-1, 0, 0]),
                           np.array([0, -1, 0])))

    assert np.allclose(vec1, vec2)
