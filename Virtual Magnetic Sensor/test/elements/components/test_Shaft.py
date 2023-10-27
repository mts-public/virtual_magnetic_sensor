import numpy as np

from libs.elements.components.Shaft import Shaft


def test_from_dict_and_to_dict():
    shaft = Shaft(pos=np.array([1.0, 2.0, 3.0]),
                  axis=np.array([np.sqrt(1 / 2), np.sqrt(1 / 4), np.sqrt(1 / 4)]),
                  diameter=np.array([2.0, 15.0]),
                  length=3.0,
                  mu_r=6000.0,
                  maxh=1.0)
    for key, value in Shaft.template().from_dict(shaft.to_dict()).__dict__.items():
        if not np.allclose(value, shaft.__dict__[key]):
            assert False

    assert True


def test_si_to_gui_to_si():
    shaft = Shaft.template()
    shaft.gui().convert_to_si()
    for key, value in shaft.__dict__.items():
        if not np.allclose(value, shaft.__dict__[key]):
            assert False

    assert True
