import numpy as np
SimParams = {"boundaries": np.array([[-5.5, -4.0, -2.0],[5.5, 7.5, 2.0]]),
              't0': 0.0,
              't1': 4.5,
              'samples': 0,
              'maxh_global': 5.0,
              'tol': 1e-06,
              'maxit': 100}
CuboidMagnet0 = {'pos': np.array([0.0, 5.26, 0.0]),
                 'm': 1000.0,
                 'mu_r': 1.0,
                 'temperature': 20.0,
                 'tk': -0.2,
                 'maxh': 2.0,
                 'rot': np.array([0.0, 0.0, 0.0]),
                 'dim': np.array([10.0, 2.5, 1.3]),
                 'direction': np.array([0.0, 0.0, 1.0])}
EvoGear0 = {'pos': np.array([0.0, 0.0, 0.0]),
            'mu_r': 4000.0,
            'maxh': 2.0,
            'axis_0': np.array([0.0, 0.0, 1.0]),
            'omega': 11.25,
            'diameter': np.array([0.0, 5.97312]),
            'length': 1.0,
            'n': 21,
            'x':0,
            'display_teeth_angle': np.array([45.0, 90.0]),
            'alpha': 20.0,
            'eccentricity': 0.0,
            'wobble_angle': 0.0,
            'dev_tooth_num': 1,
            'tooth_deviations': np.array([0.0, 0.0, 0.0]),
            'rotate_mesh': True,
            'rotate_mesh_max_angle': 3.0000000000000004,
            'involute_points': 7,
            'damage_index': 0,
            'damage_parameter_dict': {},
            'theta': 0.0}
GMRSensor0 = {'pos': np.array([0.0, 4.01, -0.7]),
              'maxh': 0.1,
              'rot': np.array([0.0, 0.0, 0.0]),
              'depth': 100.0,
              'height': 100.0,
              'gmr_offset': np.array([-455.0, -295.0, -205.00000000000006, -45.0, 45.0, 205.00000000000006, 295.0, 455.0]),
              'gmr_length': 85.0,
              'gmr_sampling': 100,
              'sensor_sampling': 1000}
FieldRecorder0 = {'field_specifier': 1,
                  'boundaries': np.array([[-5.5, -4.0, -2.0], [5.5, 7.5, 2.0]]),
                  'samples': np.array([11.0, 11.0, 1.0]),
                  'maxh': 2.0}
FieldRecorder1 = {'field_specifier': 2,
                  'boundaries': np.array([[-5.5, -4.0, -2.0], [5.5, 7.5, 2.0]]),
                  'samples': np.array([11.0, 11.0, 1.0]),
                  'maxh': 2.0}