import numpy as np

from libs.elements.magnets.RodMagnet import RodMagnet


def test_from_dict_and_to_dict():
    rod_magnet = RodMagnet(pos=np.array([1.0, 2.0, 3.0]),
                           axis=np.array([np.sqrt(1 / 2), np.sqrt(1 / 4), np.sqrt(1 / 4)]),
                           direction=np.array([np.sqrt(1 / 4), np.sqrt(1 / 2), np.sqrt(1 / 4)]),
                           radius=3.0,
                           length=2.0,
                           m=3e3 * 1e3,
                           mu_r=1.5,
                           temperature=30.0,
                           tk=-0.3,
                           maxh=1.0)
    for key, value in RodMagnet.template().from_dict(rod_magnet.to_dict()).__dict__.items():
        if not np.allclose(value, rod_magnet.__dict__[key]):
            assert False

    assert True


def test_si_to_gui_to_si():
    rod_magnet = RodMagnet.template()
    rod_magnet.gui().convert_to_si()
    for key, value in rod_magnet.__dict__.items():
        if not np.allclose(value, rod_magnet.__dict__[key]):
            assert False

    assert True


def test_magnetisation_temperature_decrease():
    rod_magnet = RodMagnet.template()
    rod_magnet.tk = -0.3
    rod_magnet.temperature = 30.0
    rod_magnet.reset()
    m_vec = rod_magnet.m * rod_magnet.direction / np.linalg.norm(rod_magnet.direction) * (
            1 + rod_magnet.tk * (rod_magnet.temperature - 20.0)/100)

    assert np.allclose(rod_magnet.m_vec, m_vec)
