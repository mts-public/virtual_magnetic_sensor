from tkinter.messagebox import showinfo, showerror
from multiprocessing import Process, Queue, Manager
from concurrent import futures
from typing import List, Union
import os
import psutil

from libs.simulation.MagneticFieldFactory import MagneticFieldFactory

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler

from libs.gui.GUIHandler import GUIHandler

thread_pool_executor = futures.ThreadPoolExecutor(max_workers=3)


class SimulationHandler:

    def __init__(self) -> None:
        """Constructor method."""

        pass

    @staticmethod 
    def run_process(data_handler: DataHandler, max_memory: float, shared_list: Manager, queue: Queue) -> None:

        n = queue.get()

        field_factory = MagneticFieldFactory()
        field = field_factory.init_field('ngsolve', data_handler)

        temp_list = list([dict()] * len(data_handler.objects))

        while n < data_handler.sim_params().samples and psutil.Process(
                os.getpid()).memory_info().rss / 1024 ** 2 < max_memory:

            t = data_handler.sim_params().t0 + n * data_handler.sim_params().dt

            for component in data_handler.components():
                if hasattr(component, "update"):
                    component.update(t)

            field.create_field(data_handler, t)

            for num, obj in enumerate(data_handler.objects):
                if hasattr(obj, "set_data"):
                    temp_list[num] = obj.set_data(temp_list[num].copy(), field)

            n += 1

        shared_list.extend(temp_list)
        queue.put(n)

    @staticmethod
    def run_thread(multiprocessing_tasks, data_stack: List[DataHandler],
                   config_handler: ConfigHandler, gui_handler: GUIHandler, idx: Union[int, None] = None) -> None:

        if idx is not None:
            sim_stack = [data_stack[idx]]
            sim_tabs = [gui_handler.tabs[idx]]
        else:
            sim_stack = data_stack
            sim_tabs = gui_handler.tabs

        gui_handler.disable_gui_operation()
        gui_handler.status_bar().set("Working...")

        for num, data_handler in enumerate(sim_stack):

            sim_tabs[num].progress_frame().reset()
            data_handler.update_objects(sim_tabs[num].frames)
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
                    process = Process(target=multiprocessing_tasks.run_process,
                                      args=(data_handler, config_handler.config['GENERAL']['max_process_memory'],
                                            shared_list, queue))
                    process.start()
                    process.join()
                    n = queue.get()
                    measurement_data.append(list(shared_list))

                sim_tabs[num].progress_frame().refresh(data_handler, config_handler, gui_handler, n)

            for i, obj in enumerate(data_handler.objects):
                if hasattr(obj, "get_data"):
                    for data in measurement_data:
                        obj.get_data(**data[i])

            if config_handler.config['GENERAL']['auto_save']:
                if not data_handler.save_h5():
                    showerror(title="Error", message="File could not be saved.")
                    gui_handler.enable_gui_operation()
                    gui_handler.status_bar().set("Error. File could not be saved.")
                    return

        if config_handler.config['GENERAL']['auto_save']:
            showinfo(title="Info", message="All files successfully saved.")
        gui_handler.enable_gui_operation()
        gui_handler.status_bar().set("Finished")

    @staticmethod
    def run(multiprocessing_tasks, data_stack: List[DataHandler], config_handler: ConfigHandler,
            gui_handler: GUIHandler, idx: Union[int, None] = None) -> Union[None, futures.Future]:
        """Method updates the data handler with the entries in the gui and performs the simulation"""

        if data_stack:
            return thread_pool_executor.submit(SimulationHandler.run_thread, multiprocessing_tasks,
                                               data_stack, config_handler, gui_handler, idx)
        else:
            showerror(title="Error", message="No data to run.")
            return

    @staticmethod
    def draw_process(data_handler: DataHandler):

        import netgen.gui

        field_factory = MagneticFieldFactory()
        field = field_factory.init_field('ngsolve', data_handler)
        field.create_field(data_handler, data_handler.sim_params().t0)
        field.draw()

        netgen.gui.win.mainloop()

    @staticmethod
    def draw_thread(multiprocessing_tasks, data_stack: List[DataHandler], gui_handler: GUIHandler, idx: int) -> None:
        """Method updates the data handler with the entries in the gui, performs a simulation of the frame at t0 and
            draws the result in the netgen gui"""

        data_handler = data_stack[idx]

        data_handler.update_objects(gui_handler.tabs[idx].frames)
        gui_handler.status_bar().set("Working...")

        for component in data_handler.components():
            component.update(data_handler.sim_params().t0)

        process = Process(target=multiprocessing_tasks.draw_process, args=(data_handler,))
        process.start()
        process.join()

        gui_handler.status_bar().set("Finished...")

    @staticmethod
    def draw(multiprocessing_tasks, data_stack: List[DataHandler],
             gui_handler: GUIHandler, idx: int) -> Union[None, futures.Future]:
        if data_stack:
            return thread_pool_executor.submit(SimulationHandler.draw_thread, multiprocessing_tasks,
                                               data_stack, gui_handler, idx)
        else:
            showerror(title="Error", message="No data to draw.")
            return
