import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

from libs.DataHandler import DataHandler
from libs.elements.sensors.HallSensor import HallSensor


class HallSensorPlot:
    """description of class"""

    def __init__(self, data_handler: DataHandler, sensor: HallSensor) -> None:
        self.data_handler = data_handler
        self.sensor = sensor

        if len(self.data_handler.sim_params().t) > 1:
            self.open_figure()

    def open_figure(self) -> None:
        root = tk.Tk()
        root.title("U_H")

        # Single axes instead of 3 subplots
        fig, ax = plt.subplots(figsize=(7, 3), dpi=100)

        t = self.data_handler.sim_params().t
        u_h = 1e3 * np.asarray(self.sensor.hall_voltage)

        ax.plot(t, u_h)
        ax.set_xlabel("Time in s")
        ax.set_ylabel("U_H in mV")
        ax.grid(color='k', linestyle=':', linewidth=0.5)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().grid(column=0, row=0, sticky='nw')
