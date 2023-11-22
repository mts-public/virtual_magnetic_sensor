import numpy as np
import configparser
from pathlib import Path

from libs.elements.sensors.GMRSensor import GMRSensor


def test_from_dict_and_to_dict():
    gmr_sensor = GMRSensor(pos=np.array([1.0, 2.0, 3.0]),
                           rot=np.radians(np.array([10.0, 20.0, 30.0])),
                           depth=200.0 * 1e-3,
                           height=300.0 * 1e-3,
                           gmr_offset=np.array([-910.0, -590.0, -410.0, -90.0, 90.0, 410.0, 590.0, 910.0]) * 1e-3,
                           gmr_length=160.0 * 1e-3,
                           gmr_sampling=200,
                           sensor_sampling=2000,
                           maxh=0.05)
    for key, value in GMRSensor.template().from_dict(gmr_sensor.to_dict()).__dict__.items():
        if not np.allclose(value, gmr_sensor.__dict__[key]):
            assert False

    assert True


def test_si_to_gui_to_si():
    gmr_sensor = GMRSensor.template()
    gmr_sensor.gui().convert_to_si()
    for key, value in gmr_sensor.__dict__.items():
        if not np.allclose(value, gmr_sensor.__dict__[key]):
            assert False

    assert True


def test_gmr_characteristics():
    gmr_config: configparser.ConfigParser = configparser.ConfigParser()
    gmr_config.read(Path('cfg/gmr_characteristics.ini'))
    coeffs: list = [1.442, -1.26e-6, 0.0, 0.0, 0.0]
    if gmr_config.has_section('COEFFICIENTS'):
        coeffs = [
            float(gmr_config['COEFFICIENTS'].get('q0', '1.442')),
            float(gmr_config['COEFFICIENTS'].get('q1', '-1.26e-6')),
            float(gmr_config['COEFFICIENTS'].get('q2', '0.0')),
            float(gmr_config['COEFFICIENTS'].get('q3', '0.0')),
            float(gmr_config['COEFFICIENTS'].get('q4', '0.0'))
        ]
    print("GMR Coefficients: ", coeffs)


def test_reset():
    gmr_sensor = GMRSensor.template()
    gmr_sensor.u_sin = [1.0, 2.0, 3.0]
    gmr_sensor.reset()

    assert len(gmr_sensor.u_sin) == len(gmr_sensor.u_cos) == len(gmr_sensor.h_sensor) == 0


def test_transformation_matrix():
    gmr_sensor = GMRSensor.template()
    gmr_sensor.rot = np.array([np.pi / 2, np.pi / 2, 0.0])
    trans_matrix = np.array([[0.0, 0.0, -1.0],
                             [1.0, 0.0, 0.0],
                             [0.0, -1.0, 0.0]])

    assert np.allclose(gmr_sensor.get_transformation_matrix(), trans_matrix)


def test_gmr_position_matrix():
    gmr_sensor = GMRSensor.template()
    gmr_position_matrix = np.array([gmr_sensor.pos + offset * gmr_sensor.transformation_matrix[:, 0]
                                    for offset in gmr_sensor.gmr_offset])

    assert np.allclose(gmr_sensor.get_gmr_position_matrix(), gmr_position_matrix)


def test_gmr_sampling_matrix():
    gmr_sensor = GMRSensor.template()
    gmr_sampling_matrix = np.array(
        [[gmr_element - gmr_sensor.gmr_length / 2 * gmr_sensor.transformation_matrix[:, 0]
          + gmr_sensor.gmr_length * (2 * i + 1) / (2 * gmr_sensor.gmr_sampling) *
          gmr_sensor.transformation_matrix[:, 0] for i in range(0, gmr_sensor.gmr_sampling)]
         for gmr_element in gmr_sensor.gmr_position_matrix])

    assert np.allclose(gmr_sensor.get_gmr_sampling_matrix(), gmr_sampling_matrix)


def test_sensor_sampling_matrix():
    gmr_sensor = GMRSensor.template()
    sensor_sampling_matrix = np.array(
            [[gmr_element - gmr_sensor.gmr_length / 2 * gmr_sensor.transformation_matrix[:, 0]
              + gmr_sensor.gmr_length * (2 * i + 1) / (2 * gmr_sensor.gmr_sampling) *
              gmr_sensor.transformation_matrix[:, 0] for i in range(0, gmr_sensor.gmr_sampling)]
             for gmr_element in gmr_sensor.gmr_position_matrix])

    assert np.allclose(gmr_sensor.get_gmr_sampling_matrix(), sensor_sampling_matrix)
