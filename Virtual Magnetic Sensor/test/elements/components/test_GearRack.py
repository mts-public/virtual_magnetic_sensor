import numpy as np
from math import radians

from libs.elements.components.GearRack import GearRack


def test_from_dict_and_to_dict():
    gear_rack = GearRack(pos=np.array([1.0, 2.0, 3.0]),
                         dim=np.array([7.0, 2.0, 3.0]),
                         rot=np.radians(np.array([10.0, 20.0, 30.0])),
                         velocity=np.array([0.3, 0.7, 0.5]),
                         tooth_height=2.0,
                         tooth_width=0.5,
                         tooth_pitch=2.0,
                         tooth_flank_angle=radians(15.0),
                         mu_r=6000.0,
                         chamfer_depth=0.1 * 1e-3,
                         chamfer_angle=radians(30.0),
                         maxh=3.0)
    for key, value in GearRack.template().from_dict(gear_rack.to_dict()).__dict__.items():
        if not np.allclose(value, gear_rack.__dict__[key]):
            assert False

    assert True


def test_si_to_gui_to_si():
    gear_rack = GearRack.template()
    gear_rack.gui().convert_to_si()
    for key, value in gear_rack.__dict__.items():
        if not np.allclose(value, gear_rack.__dict__[key]):
            assert False

    assert True


def test_update():
    t = 1.0
    gear_rack = GearRack.template()
    gear_rack.update(t)

    assert np.allclose(gear_rack.shift, gear_rack.velocity * t)


def test_reset():
    t = 1.0
    gear_rack = GearRack.template()
    gear_rack.update(t)
    gear_rack.reset()

    assert np.allclose(gear_rack.shift, 0.0)


def test_transformation_matrix():
    gear_rack = GearRack.template()
    gear_rack.rot = np.array([np.pi / 2, np.pi / 2, 0.0])
    trans_matrix = np.array([[0.0, 0.0, -1.0],
                             [1.0, 0.0, 0.0],
                             [0.0, -1.0, 0.0]])

    assert np.allclose(gear_rack.transformation_matrix(), trans_matrix)


def test_pos():
    t = 1.0
    gear_rack = GearRack.template()
    gear_rack.update(t)

    assert np.allclose(gear_rack.position(), gear_rack.pos + gear_rack.velocity * t)
