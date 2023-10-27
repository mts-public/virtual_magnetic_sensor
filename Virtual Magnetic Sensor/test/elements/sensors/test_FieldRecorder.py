import numpy as np

from libs.elements.sensors.FieldRecorder import FieldRecorder


def test_from_dict_and_to_dict():
    field_recorder = FieldRecorder(field_specifier=0,
                                   boundaries=np.array([[-10.0, -20.0, -30.0], [10.0, 20.0, 30.0]]),
                                   samples=np.array([11, 22, 33]),
                                   maxh=1.0)
    for key, value in FieldRecorder.template().from_dict(field_recorder.to_dict()).__dict__.items():
        if not np.allclose(value, field_recorder.__dict__[key]):
            assert False

    assert True


def test_si_to_gui_to_si():
    field_recorder = FieldRecorder.template()
    field_recorder.gui().convert_to_si()
    for key, value in field_recorder.__dict__.items():
        if not np.allclose(value, field_recorder.__dict__[key]):
            assert False

    assert True
