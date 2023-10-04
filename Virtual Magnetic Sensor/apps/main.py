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
    def run_work(*args) -> None:
        SimulationHandler.run_work(*args)

    @staticmethod
    def draw_work(*args) -> None:
        SimulationHandler.draw_work(*args)


if __name__ == '__main__':
    faulthandler.enable()
    SetNumThreads(cpu_count())
    MainFrame(MultiprocessingTasks())
