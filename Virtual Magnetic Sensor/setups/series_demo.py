import numpy as np

SimParams = {
    "boundaries": np.array([[-7.5, -5.5, -3.0], [7.5, 8.5, 3.0]]),
    "t0": 0,
    "t1": 1.0,
    "samples": 3,
    "maxh_global": 2.0,
    "tol": 1e-3,
    "maxit": 100
}

Gear0 = {
    "pos": np.array([0.0, 0.0, 0.0]),
    "axis_0": np.array([0.0, 0.0, 1.0]),
    "omega": 15.0,
    "diameter": np.array([0.0, 7.64]),
    "length": 3.0,
    "tooth_height": 0.5,
    "tooth_width": 0.333,
    "n": 24,
    "display_teeth_angle": np.array([0.0, 360.0]),
    "tooth_flank_angle": 10.0,
    "mu_r": 4000.0,
    "eccentricity": 0.0,
    "wobble_angle": 0.0,
    "chamfer_depth": 0.0,
    "chamfer_angle": 45,
    "dev_tooth_num": 7,
    "tooth_deviations": np.array([0.0, 0.0, 0.0]),
    "maxh": 2.0,
    "rotate_mesh": True,
    "rotate_mesh_max_angle": 3.0
}

CuboidMagnet0 = {
    "pos": np.array([0.0, 5.52, 0.0]),
    "rot": np.array([0.0, 0.0, 0.0]),
    "dim": np.array([10.0, 2.5, 1.3]),
    "direction": np.array([0.0, 0.0, 1.0]),
    "m": 1e3,
    "mu_r": 1.0,
    "temperature": 20.0,
    "tk": -0.2,
    "maxh": 2.0
}

GMRSensor0 = {
    "pos": np.array([0.0, 4.27, -0.7]),
    "rot": np.array([0.0, 0.0, 0.0]),
    "depth": 100.0,
    "height": 100.0,
    "gmr_offset": np.array([-455.0, -295.0, -205.0, -45.0, 45.0, 205.0, 295.0, 455.0]),
    "gmr_length": 85.0,
    "gmr_sampling": 100,
    "sensor_sampling": 1000,
    "maxh": 0.1
}

FieldRecorder0 = {
    "field_specifier": 1,
    "boundaries": np.array([[-7.5, -5.5, 0.0], [7.5, 8.5, 0.0]]),
    "samples": np.array([11, 11, 1])
}

FieldRecorder1 = {
    "field_specifier": 2,
    "boundaries": np.array([[-7.5, -5.5, 0.0], [7.5, 8.5, 0.0]]),
    "samples": np.array([11, 11, 1])
}

heights = np.array([4.27, 4.37, 4.47])
series = {
    "CuboidMagnet0": {
        "pos": np.array([[0.0, h + 1.25, 0] for h in heights])
    },
    "GMRSensor0": {
        "pos": np.array([[0.0, h, -0.7] for h in heights])
    },
    "FieldRecorder0": {
        "samples": np.array([[11, 11, 1], [22, 22, 1], [33, 33, 1]])
    },
    "FieldRecorder1": {
        "samples": np.array([[44, 44, 1], [33, 33, 1], [22, 22, 1]])
    },
}

