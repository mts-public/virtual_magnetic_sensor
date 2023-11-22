import numpy as np

from libs.elements.sensors.HallSensor import HallSensor


def test_from_dict_and_to_dict():
    hall_sensor = HallSensor(pos=np.array([1.0, 2.0, 3.0]),
                             rot=np.radians(np.array([10.0, 20.0, 30.0])),
                             dim=np.array([10.0, 20.0, 30.0]),
                             hall_coefficient=-100e-12,
                             conductor_thickness=0.2,
                             current=3.0,
                             maxh=0.05)
    for key, value in HallSensor.template().from_dict(hall_sensor.to_dict()).__dict__.items():
        if not np.allclose(value, hall_sensor.__dict__[key]):
            assert False

    assert True


def test_si_to_gui_to_si():
    hall_sensor = HallSensor.template()
    hall_sensor.gui().convert_to_si()
    for key, value in hall_sensor.__dict__.items():
        if not np.allclose(value, hall_sensor.__dict__[key]):
            assert False

    assert True


def test_reset():
    hall_sensor = HallSensor.template()
    hall_sensor.hall_voltage = [1.0, 2.0, 3.0]
    hall_sensor.reset()

    assert len(hall_sensor.hall_voltage) == 0


def test_transformation_matrix():
    hall_sensor = HallSensor.template()
    hall_sensor.rot = np.array([np.pi / 2, np.pi / 2, 0.0])
    trans_matrix = np.array([[0.0, 0.0, -1.0],
                             [1.0, 0.0, 0.0],
                             [0.0, -1.0, 0.0]])

    assert np.allclose(hall_sensor.get_transformation_matrix(), trans_matrix)
