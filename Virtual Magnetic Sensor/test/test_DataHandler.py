import numpy as np
import os
from pathlib import Path
import random
import string
from math import radians

from libs.ConfigHandler import ConfigHandler
from libs.DataHandler import DataHandler


def template() -> DataHandler:
    parameters = {
        'SimParams': {
            "boundaries": np.array([[-7.5, - 5.5, - 3.0], [7.5, 8.5, 3.0]]),
            "t0": 0.0,
            "t1": 1.0,
            "samples": 3,
            "maxh_global": 2.0,
            "tol": 0.001,
            "maxit": 100
        },
        'CuboidMagnet0': {
            "pos": np.array([0.0, 5.52, 0.0]),
            "m": 1000.0*1e3,
            "mu_r": 1.0,
            "temperature": 20.0,
            "tk": -0.2,
            "maxh": 2.0,
            "rot": np.radians(np.array([0.0, 0.0, 0.0])),
            "dim": np.array([10.0, 2.5, 1.3]),
            "direction": np.array([0.0, 0.0, 1.0])
        },
        'RodMagnet0': {
            "pos": np.array([0.0, 0.0, 0.0]),
            "m": 1000.0*1e3,
            "mu_r": 1.0,
            "temperature": 20.0,
            "tk": -0.2,
            "maxh": 2.0,
            "axis": np.array([0.0, 0.0, 1.0]),
            "direction": np.array([0.0, 0.0, 1.0]),
            "radius": 1.0,
            "length": 1.0
        },
        'UniField0': {
            "direction": np.array([0.0, 1.0, 0.0]),
            "strength": 10.0*1e-3
        },
        'Gear0': {
            "pos": np.array([0.0, 0.0, 0.0]),
            "mu_r": 4000.0,
            "maxh": 2.0,
            "axis_0": np.array([0.0, 0.0, 1.0]),
            "omega": radians(15.0),
            "diameter": np.array([0.0, 7.64]),
            "length": 3.0,
            "tooth_height": 0.5,
            "tooth_width": 0.333,
            "n": 24,
            "display_teeth_angle": np.radians(np.array([0.0, 360.0])),
            "tooth_flank_angle": radians(10.0),
            "eccentricity": 0.0*1e-3,
            "wobble_angle": radians(0.0),
            "chamfer_depth": 0.0*1e-3,
            "chamfer_angle": radians(45.0),
            "dev_tooth_num": 7,
            "tooth_deviations": np.array([0.0, 0.0, 0.0])*1e-3,
            "rotate_mesh": True,
            "rotate_mesh_max_angle": radians(3.0)
        },
        'GearRack0': {
            "pos": np.array([0.0, 0.0, 0.0]),
            "mu_r": 4000.0,
            "maxh": 2.0,
            "dim": np.array([10.0, 1.0, 1.0]),
            "rot": np.radians(np.array([0.0, 0.0, 0.0])),
            "velocity": np.array([0.1, 0.0, 0.0]),
            "tooth_height": 1.0,
            "tooth_width": 0.333,
            "tooth_pitch": 1.0,
            "tooth_flank_angle": radians(10.0),
            "chamfer_depth": 0.0*1e-3,
            "chamfer_angle": radians(45.0),
            "shift": np.array([0.0, 0.0, 0.0])
        },
        'Shaft0': {
            "pos": np.array([0.0, 0.0, 0.0]),
            "mu_r": 4000.0,
            "maxh": 2.0,
            "axis": np.array([0.0, 0.0, 1.0]),
            "diameter": np.array([1.0, 10.0]),
            "length": 1.0
        },
        'FieldRecorder0': {
            "field_specifier": 1,
            "boundaries": np.array([[-7.5, -5.5, -3.0], [7.5, 8.5, 3.0]]),
            "samples": np.array([11.0, 11.0, 1.0]),
            "maxh": 2.0
        },
        'GMRSensor0': {
            "pos": np.array([0.0, 4.27, -0.7]),
            "maxh": 0.1,
            "rot": np.radians(np.array([0.0, 0.0, 0.0])),
            "depth": 100.0*1e-3,
            "height": 100.0*1e-3,
            "current": 1.0,
            "gmr_offset": np.array([-455.0, -295.0, -205.0, -45.0, 45.0, 205.0, 295.0, 455.0])*1e-3,
            "gmr_length": 85.0*1e-3,
            "gmr_sampling": 100,
            "sensor_sampling": 1000,
        }
    }

    data_handler = DataHandler(list())
    data_handler.deploy_dict(parameters)

    return data_handler


def compare_data_handler(data_handler_1: DataHandler, data_handler_2: DataHandler) -> bool:
    compare_obj = None
    for obj1 in data_handler_1.objects:
        for obj2 in data_handler_2.objects:
            if type(obj1) == type(obj2):
                compare_obj = obj2
        for key, value in obj1.__dict__.items():
            if key in compare_obj.__dict__:
                if type(value) == np.ndarray:
                    if not np.allclose(value, np.array(compare_obj.__dict__[key])):
                        print(obj1, key, value, compare_obj.__dict__[key], type(value), type(compare_obj.__dict__[key]))
                        return False
                elif type(value) == list:
                    if value != list(compare_obj.__dict__[key]):
                        print(obj1, key, value, compare_obj.__dict__[key], type(value), type(compare_obj.__dict__[key]))
                        return False
                elif value:
                    if not np.isclose(value, compare_obj.__dict__[key]):
                        print(obj1, key, value, compare_obj.__dict__[key], type(value), type(compare_obj.__dict__[key]))
                        return False

    return True


def test_load_h5():
    # v1.0.0
    data_handler100 = DataHandler()
    data_handler100.load_h5(Path('src/libs/resources/save_files/1.0.0/100.hdf5'))

    assert compare_data_handler(data_handler100, template())


def test_load_ini():
    # v1.0.0
    data_handler100 = DataHandler()
    data_handler100.load_ini(Path('src/libs/resources/save_files/1.0.0/100.ini'))

    assert compare_data_handler(data_handler100, template())


def test_load_py():
    # v1.0.0
    data_handler100 = DataHandler()
    data_handler100.load_py(Path('src/libs/resources/save_files/1.0.0/100.py'))

    assert compare_data_handler(data_handler100, template())


def test_load_series():
    data_handler = DataHandler()
    data_stack = data_handler.load_py(Path('src/libs/resources/save_files/1.0.0/series_100.py'))

    assert len(data_stack) == 3


def test_save_h5():
    data_handler = DataHandler()
    config_handler = ConfigHandler()
    data_handler.load_h5(Path('src/libs/resources/save_files/1.0.0/100.hdf5'))
    filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    data_handler.filepath = Path(config_handler.config['GENERAL']['measurement_path'], filename)
    while os.path.exists(data_handler.filepath.with_suffix('.hdf5')):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        data_handler.filepath = Path(config_handler.config['GENERAL']['measurement_path'], filename)
    if not data_handler.save_h5(data_handler.filepath.parent):
        assert False
    else:
        os.remove(data_handler.filepath.with_suffix('.hdf5'))

    assert compare_data_handler(data_handler, template())


def test_save_ini():
    data_handler = DataHandler()
    config_handler = ConfigHandler()
    data_handler.load_h5(Path('src/libs/resources/save_files/1.0.0/100.hdf5'))
    filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    data_handler.filepath = Path(config_handler.config['GENERAL']['measurement_path'], filename)
    while os.path.exists(data_handler.filepath.with_suffix('.ini')):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        data_handler.filepath = Path(config_handler.config['GENERAL']['measurement_path'], filename)
    if not data_handler.save_ini():
        assert False
    else:
        os.remove(data_handler.filepath.with_suffix('.ini'))

    assert compare_data_handler(data_handler, template())

