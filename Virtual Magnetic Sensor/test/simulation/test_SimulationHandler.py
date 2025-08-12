from pathlib import Path
import random
import string
import os
import threading
import numpy as np

from libs.gui.frames.MainFrame import MainFrame
from libs.gui.FileDialogs import FileDialogs

from libs.simulation.SimulationHandler import SimulationHandler


class MultiprocessingTasks:

    @staticmethod
    def run_process(*args) -> None:
        SimulationHandler.run_process(*args)

    @staticmethod
    def draw_process(*args) -> None:
        SimulationHandler.draw_process(*args)


def test_run():

    def run_simulation():
        SimulationHandler.run(MultiprocessingTasks(), main_frame.data_stack, main_frame.config_handler,
                              main_frame.gui_handler).result()
        main_frame.gui_handler.exit()

    main_frame = MainFrame(MultiprocessingTasks(), 1)
    main_frame.gui_handler.close_all_tabs(main_frame.data_stack)
    FileDialogs.open(main_frame.data_stack, main_frame.config_handler, main_frame.gui_handler,
                     filename=Path('src\\libs\\resources\\save_files\\test_configuration.ini').as_posix())
    main_frame.config_handler.config['GENERAL']['auto_save'] = 0
    thread = threading.Thread(target=run_simulation)
    main_frame.after(1000, lambda: thread.start())
    main_frame.mainloop()
    thread.join()

    for data_handler in main_frame.data_stack:
        for sensor in data_handler.gmr_sensors():
            if data_handler.sim_params().samples != len(sensor.u_sin) != len(sensor.u_cos) != len(sensor.h_sensor) != \
                    len(sensor.resistance):
                assert False

        for recorder in data_handler.field_recorders():
            if np.array(recorder.field).shape != (data_handler.sim_params().samples, recorder.samples[0],
                                                  recorder.samples[1], recorder.samples[2], 3):
                assert False

        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        data_handler.filepath = Path(main_frame.config_handler.config['GENERAL']['measurement_path'], filename)
        while os.path.exists(data_handler.filepath.with_suffix('.hdf5')):
            filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            data_handler.filepath = Path(main_frame.config_handler.config['GENERAL']['measurement_path'], filename)
        if not data_handler.save_h5(data_handler.filepath.parent):
            assert False
        else:
            os.remove(data_handler.filepath.with_suffix('.hdf5'))

    assert True
