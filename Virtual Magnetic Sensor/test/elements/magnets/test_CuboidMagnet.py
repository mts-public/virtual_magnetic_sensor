import numpy as np

from libs.elements.magnets.CuboidMagnet import CuboidMagnet


def test_from_dict_and_to_dict():
    cuboid_magnet = CuboidMagnet(pos=np.array([1.0, 2.0, 3.0]),
                                 rot=np.radians(np.array([10.0, 20.0, 30.0])),
                                 dim=np.array([10.0, 12.0, 13.0]),
                                 direction=np.array([np.sqrt(1 / 2), np.sqrt(1 / 4), np.sqrt(1 / 4)]),
                                 m=3e3 * 1e3,
                                 mu_r=1.5,
                                 temperature=30.0,
                                 tk=-0.3,
                                 maxh=1.0)
    for key, value in CuboidMagnet.template().from_dict(cuboid_magnet.to_dict()).__dict__.items():
        if not np.allclose(value, cuboid_magnet.__dict__[key]):
            assert False

    assert True


def test_si_to_gui_to_si():
    cuboid_magnet = CuboidMagnet.template()
    cuboid_magnet.gui().convert_to_si()
    for key, value in cuboid_magnet.__dict__.items():
        if not np.allclose(value, cuboid_magnet.__dict__[key]):
            assert False

    assert True


def test_transformation_matrix():
    cuboid_magnet = CuboidMagnet.template()
    cuboid_magnet.rot = np.array([np.pi / 2, np.pi / 2, 0.0])
    trans_matrix = np.array([[0.0, 0.0, -1.0],
                             [1.0, 0.0, 0.0],
                             [0.0, -1.0, 0.0]])

    assert np.allclose(cuboid_magnet.get_transformation_matrix(), trans_matrix)


def test_magnetisation_temperature_decrease():
    cuboid_magnet = CuboidMagnet.template()
    cuboid_magnet.tk = -0.3
    cuboid_magnet.temperature = 30.0
    cuboid_magnet.reset()
    m_vec = cuboid_magnet.m * cuboid_magnet.direction / np.linalg.norm(cuboid_magnet.direction) * (
            1 + cuboid_magnet.tk * (cuboid_magnet.temperature - 20.0)/100)

    assert np.allclose(cuboid_magnet.m_vec, m_vec)
