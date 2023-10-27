import numpy as np

from libs.elements.magnets.UniField import UniField


def test_from_dict_and_to_dict():
    uni_field = UniField(direction=np.array([1.0, 2.0, 3.0]),
                         strength=100.0 * 1e-3)
    for key, value in UniField.template().from_dict(uni_field.to_dict()).__dict__.items():
        if not np.allclose(value, uni_field.__dict__[key]):
            assert False

    assert True


def test_si_to_gui_to_si():
    uni_field = UniField.template()
    uni_field.gui().convert_to_si()
    for key, value in uni_field.__dict__.items():
        if not np.allclose(value, uni_field.__dict__[key]):
            assert False

    assert True
