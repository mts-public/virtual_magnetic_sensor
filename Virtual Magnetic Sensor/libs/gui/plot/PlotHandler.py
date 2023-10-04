import tkinter as tk

from libs.gui.plot.Figure1 import Figure1
from libs.gui.plot.Figure2 import Figure2

from libs.DataHandler import DataHandler
from libs.elements.sensors.GMRSensor import GMRSensor


class PlotHandler:
    """description of class"""

    def __init__(self, data_handler: DataHandler, sensor: GMRSensor) -> None:
        self.data_handler = data_handler
        self.sensor = sensor

        if len(self.data_handler.sim_params().t) > 1:
            self.figure1()
            self.figure2()

    def figure1(self) -> None:
        root = tk.Tk()
        root.title("B Field")

        Figure1(self.data_handler, self.sensor, root)

    def figure2(self) -> None:
        root = tk.Tk()
        root.title("Sensor Signals")

        Figure2(self.data_handler, self.sensor, root)
