#!/usr/bin/env python

"""main.py: Run the application."""
import faulthandler
from pyngcore import SetNumThreads
from multiprocessing import cpu_count

from libs.gui.frames.MainFrame import MainFrame
from libs.simulation.SimulationHandler import SimulationHandler


# Define the multiprocessing tasks in the top-level module
class MultiprocessingTasks:

    @staticmethod
    def run_process(*args) -> None:
        SimulationHandler.run_process(*args)

    @staticmethod
    def draw_process(*args) -> None:
        SimulationHandler.draw_process(*args)


if __name__ == '__main__':
    faulthandler.enable()
    SetNumThreads(cpu_count())
    MainFrame(MultiprocessingTasks())
