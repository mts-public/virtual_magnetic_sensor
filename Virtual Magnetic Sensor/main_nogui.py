import faulthandler
# from pyngcore import SetNumThreads
from multiprocessing import cpu_count
from pathlib import Path
from tkinter.messagebox import showerror
from multiprocessing import Process, Queue, Manager

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler

from libs.simulation.SimulationHandler import SimulationHandler


class MultiprocessingTasks:

    @staticmethod
    def run_work(*args) -> None:
        SimulationHandler.run_process(*args)

    @staticmethod
    def draw_work(*args) -> None:
        SimulationHandler.draw_process(*args)


if __name__ == '__main__':
    faulthandler.enable()
    # SetNumThreads(cpu_count())

    config_handler = ConfigHandler()
    
    setups = ["./virtual_magnetic_sensor/Virtual Magnetic Sensor/setups/EvoGearDamages/EvoStandardWF.py"]

    for setup in setups:
        data_stack = DataHandler().load_py(Path(setup))
        
        for num, data_handler in enumerate(data_stack):

            data_handler.filepath = Path(
                data_handler.filepath.parent, data_handler.filepath.stem + str(num).zfill(2))
            print(data_handler.filepath)

            #!!DONT FORGET TO COMMENT OUT!!
            #MultiprocessingTasks.draw_work(data_handler)
            #!!DONT FORGET TO COMMENT OUT!!
            
            for obj in data_handler.objects:
                if hasattr(obj, "reset"):
                    obj.reset()
            
            n = 0
            measurement_data = list()
            while n < data_handler.sim_params().samples:
                with Manager() as manager:
                    queue = Queue()
                    queue.put(n)
                    shared_list = manager.list()
                    process = Process(target=MultiprocessingTasks.run_work,
                                      args=(data_handler, config_handler.config['GENERAL']['max_process_memory'],
                                            shared_list, queue))
                    process.start()
                    process.join()
                    n = queue.get()
                    measurement_data.append(list(shared_list))

            for i, obj in enumerate(data_handler.objects):
                if hasattr(obj, "get_data"):
                    for data in measurement_data:
                        obj.get_data(**data[i])

            if not data_handler.save_h5():
                showerror(title="Error", message="File could not be saved.")
