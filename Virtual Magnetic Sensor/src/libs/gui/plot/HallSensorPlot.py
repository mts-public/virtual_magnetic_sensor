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

        fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(7, 5), dpi=100)
        ax[0].plot(self.data_handler.sim_params().t, 1e3 * np.asarray(self.sensor.hall_voltage)[:, 0])
        ax[1].plot(self.data_handler.sim_params().t, 1e3 * np.asarray(self.sensor.hall_voltage)[:, 1])
        ax[2].plot(self.data_handler.sim_params().t, 1e3 * np.asarray(self.sensor.hall_voltage)[:, 2])
        fig.subplots_adjust(hspace=0.262)

        ax[0].set_xlabel("Time in s"), ax[0].set_ylabel("U_H(B_x) in mV")
        ax[0].grid(color='k', linestyle=':', linewidth=0.5)
        ax[1].set_xlabel("Time in s"), ax[1].set_ylabel("U_H(B_y) in mV")
        ax[1].grid(color='k', linestyle=':', linewidth=0.5)
        ax[2].set_xlabel("Time in s"), ax[2].set_ylabel("U_H(B_z) in mV")
        ax[2].grid(color='k', linestyle=':', linewidth=0.5)

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().grid(column=0, row=0, sticky='nw')
