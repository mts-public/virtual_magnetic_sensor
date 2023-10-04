import tkinter as tk

import matplotlib.figure
import numpy as np
from math import pi

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt

from libs.DataHandler import DataHandler
from libs.elements.sensors.GMRSensor import GMRSensor


class Figure1:
    """description of class"""

    def __init__(self,
                 data_handler: DataHandler,
                 sensor: GMRSensor,
                 root: tk.Tk) -> None:
        self.data_handler = data_handler
        self.sensor = sensor
        self.root = root
        self.mu0 = 4 * pi * 1e-7

        self.fig = matplotlib.figure.Figure
        self.plot1 = matplotlib.lines.Line2D
        self.plot2 = matplotlib.lines.Line2D
        self.plot3 = matplotlib.lines.Line2D
        self.canvas = FigureCanvasTkAgg
        self.sliderbar = tk.Scale

        self.draw()

    def draw(self) -> None:
        self.fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(7, 5), dpi=100)
        self.plot1, = ax[0].plot(self.data_handler.sim_params().t,
                                 1e3 * self.mu0 * np.asarray(self.sensor.h_sensor)[:, self.convert(0.0), 0])
        self.plot2, = ax[1].plot(self.data_handler.sim_params().t,
                                 1e3 * self.mu0 * np.asarray(self.sensor.h_sensor)[:, self.convert(0.0), 1])
        self.plot3, = ax[2].plot(self.data_handler.sim_params().t,
                                 1e3 * self.mu0 * np.asarray(self.sensor.h_sensor)[:, self.convert(0.0), 2])
        self.fig.subplots_adjust(hspace=0.262)

        ax[0].set_xlabel("Time in s"), ax[0].set_ylabel("B_x in mT")
        ax[0].grid(color='k', linestyle=':', linewidth=0.5)
        ax[1].set_xlabel("Time in s"), ax[1].set_ylabel("B_y in mT")
        ax[1].grid(color='k', linestyle=':', linewidth=0.5)
        ax[2].set_xlabel("Time in s"), ax[2].set_ylabel("B_z in mT")
        ax[2].grid(color='k', linestyle=':', linewidth=0.5)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=0, sticky='nw')

        sliderbar_label = tk.Label(master=self.root, text="Offset to Sensor Center in µm:")
        sliderbar_label.grid(column=0, row=1)

        self.sliderbar = tk.Scale(self.root,
                                  from_=(self.sensor.gmr_offset[0] - self.sensor.gmr_length / 2) * 1e3,
                                  to=(self.sensor.gmr_offset[-1] + self.sensor.gmr_length / 2) * 1e3,
                                  tickinterval=(self.sensor.gmr_offset[-1] - self.sensor.gmr_offset[
                                      0] + self.sensor.gmr_length) * 1e3 / 10,
                                  resolution=(self.sensor.gmr_offset[-1] - self.sensor.gmr_offset[
                                      0] + self.sensor.gmr_length) * 1e3 / self.sensor.sensor_sampling,
                                  length=700,
                                  digits=4,
                                  orient=tk.HORIZONTAL,
                                  command=self.update
                                  )
        self.sliderbar.grid(column=0, row=2, sticky='nw')
        self.sliderbar.set(0)

        toolbar_frame = tk.Frame(master=self.root)
        toolbar_frame.grid(column=0, row=3, sticky='nw')
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()

    def update(self, *args) -> None:
        self.plot1.set_ydata(
            1e3 * self.mu0 * np.asarray(self.sensor.h_sensor)[:, self.convert(self.sliderbar.get()), 0])
        self.plot2.set_ydata(
            1e3 * self.mu0 * np.asarray(self.sensor.h_sensor)[:, self.convert(self.sliderbar.get()), 1])
        self.plot3.set_ydata(
            1e3 * self.mu0 * np.asarray(self.sensor.h_sensor)[:, self.convert(self.sliderbar.get()), 2])

        self.canvas.draw()

    def convert(self, val: float) -> int:
        return int(np.round((self.sensor.sensor_sampling - 1) / (
                self.sensor.gmr_offset[-1] - self.sensor.gmr_offset[0] + self.sensor.gmr_length) * (
                                    val * 1e-3 - self.sensor.gmr_offset[0] + self.sensor.gmr_length / 2)))
