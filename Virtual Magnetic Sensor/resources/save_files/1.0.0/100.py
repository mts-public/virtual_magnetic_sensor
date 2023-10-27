import numpy as np

SimParams = {
    "boundaries": np.array([[-7.5, - 5.5, - 3.0], [7.5, 8.5, 3.0]]),
    "t0": 0.0,
    "t1": 1.0,
    "samples": 3,
    "maxh_global": 2.0,
    "tol": 0.001,
    "maxit": 100,
}

CuboidMagnet0 = {
    "pos": np.array([0.0, 5.52, 0.0]),
    "m": 1000.0,
    "mu_r": 1.0,
    "temperature": 20.0,
    "tk": -0.2,
    "maxh": 2.0,
    "rot": np.array([0.0, 0.0, 0.0]),
    "dim": np.array([10.0, 2.5,1.3]),
    "direction": np.array([0.0, 0.0, 1.0])
}

RodMagnet0 = {
    "pos": np.array([0.0, 0.0, 0.0]),
    "m": 1000.0,
    "mu_r": 1.0,
    "temperature": 20.0,
    "tk": -0.2,
    "maxh": 2.0,
    "axis": np.array([0.0, 0.0, 1.0]),
    "direction": np.array([0.0, 0.0, 1.0]),
    "radius": 1.0,
    "length": 1.0
}

UniField0 = {
    "direction": np.array([0.0, 1.0, 0.0]),
    "strength": 10.0
}

Gear0 = {
    "pos": np.array([0.0, 0.0, 0.0]),
    "mu_r": 4000.0,
    "maxh": 2.0,
    "axis_0": np.array([0.0, 0.0, 1.0]),
    "omega": 15.0,
    "diameter": np.array([0.0, 7.64]),
    "length": 3.0,
    "tooth_height": 0.5,
    "tooth_width": 0.333,
    "n": 24,
    "display_teeth_angle": np.array([0.0, 360.0]),
    "tooth_flank_angle": 10.0,
    "eccentricity": 0.0,
    "wobble_angle": 0.0,
    "chamfer_depth": 0.0,
    "chamfer_angle": 45.0,
    "dev_tooth_num": 7,
    "tooth_deviations": np.array([0.0, 0.0, 0.0]),
    "rotate_mesh": True,
    "rotate_mesh_max_angle": 3.0
}


GearRack0 = {
    "pos": np.array([0.0, 0.0, 0.0]),
    "mu_r": 4000.0,
    "maxh": 2.0,
    "dim": np.array([10.0, 1.0, 1.0]),
    "rot": np.array([0.0, 0.0, 0.0]),
    "velocity": np.array([0.1, 0.0, 0.0]),
    "tooth_height": 1.0,
    "tooth_width": 0.333,
    "tooth_pitch": 1.0,
    "tooth_flank_angle": 10.0,
    "chamfer_depth": 0.0,
    "chamfer_angle": 45.0,
    "shift": np.array([0.0, 0.0, 0.0])
}

Shaft0 = {
    "pos": np.array([0.0, 0.0, 0.0]),
    "mu_r": 4000.0,
    "maxh": 2.0,
    "axis": np.array([0.0, 0.0, 1.0]),
    "diameter": np.array([1.0, 10.0]),
    "length": 1.0
}

FieldRecorder0 = {
    "field_specifier": 1,
    "boundaries": np.array([[-7.5, -5.5, -3.0], [7.5, 8.5, 3.0]]),
    "samples": np.array([11.0, 11.0, 1.0]),
    "maxh": 2.0
}

GMRSensor0 = {
    "pos": np.array([0.0, 4.27, -0.7]),
    "maxh": 0.1,
    "rot": np.array([0.0, 0.0, 0.0]),
    "depth": 100.0,
    "height": 100.0,
    "current": 1.0,
    "gmr_offset": np.array([-455.0, -295.0, -205.0, -45.0, 45.0, 205.0, 295.0, 455.0]),
    "gmr_length": 85.0,
    "gmr_sampling": 100,
    "sensor_sampling": 1000
}

