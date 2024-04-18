import tkinter as tk
import matplotlib.figure
import numpy as np
from math import pi

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from libs.DataHandler import DataHandler
from libs.elements.sensors.GMRSensor import GMRSensor


class Figure1:
    """Description of class"""

    def __init__(self,
                 data_handler: DataHandler,
                 sensor: GMRSensor,
                 root: tk.Tk) -> None:
        self.data_handler = data_handler
        self.sensor = sensor
        self.root = root
        self.mu0 = 4 * pi * 1e-7

        self.fig = matplotlib.figure.Figure(figsize=(7, 5), dpi=100)
        self.ax = self.fig.subplots(nrows=3, ncols=1)

        self.plot1 = matplotlib.lines.Line2D
        self.plot2 = matplotlib.lines.Line2D
        self.plot3 = matplotlib.lines.Line2D

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.root.bind('<Configure>', self.on_resize)

        self.sliderbar = tk.Scale(self.root,
                                  from_=(self.sensor.gmr_offset[0] - self.sensor.gmr_length / 2) * 1e3,
                                  to=(self.sensor.gmr_offset[-1] + self.sensor.gmr_length / 2) * 1e3,
                                  tickinterval=(self.sensor.gmr_offset[-1] - self.sensor.gmr_offset[
                                      0] + self.sensor.gmr_length) * 1e3 / 10,
                                  resolution=(self.sensor.gmr_offset[-1] - self.sensor.gmr_offset[
                                      0] + self.sensor.gmr_length) * 1e3 / self.sensor.sensor_sampling,
                                  digits=4,
                                  orient=tk.HORIZONTAL
                                  )
        self.sliderbar.pack(fill=tk.X)
        self.sliderbar.bind('<Motion>', self.update)

        self.draw()

    def on_resize(self, event):
        width, height = event.width, event.height
        self.fig.set_size_inches(width / 100, max(height / 100 - 1, 0), forward=True)
        self.canvas.draw()

    def draw(self) -> None:
        self.plot1, = self.ax[0].plot(self.data_handler.sim_params().t,
                                 1e3 * self.mu0 * np.asarray(self.sensor.h_sensor)[:, self.convert(0.0), 0])
        self.plot2, = self.ax[1].plot(self.data_handler.sim_params().t,
                                 1e3 * self.mu0 * np.asarray(self.sensor.h_sensor)[:, self.convert(0.0), 1])
        self.plot3, = self.ax[2].plot(self.data_handler.sim_params().t,
                                 1e3 * self.mu0 * np.asarray(self.sensor.h_sensor)[:, self.convert(0.0), 2])

        self.fig.subplots_adjust(hspace=0.262, bottom=0.05)

        self.ax[0].set_xlabel("Time in s"), self.ax[0].set_ylabel("B_x in mT")
        self.ax[0].grid(color='k', linestyle=':', linewidth=0.5)
        self.ax[1].set_xlabel("Time in s"), self.ax[1].set_ylabel("B_y in mT")
        self.ax[1].grid(color='k', linestyle=':', linewidth=0.5)
        self.ax[2].set_xlabel("Time in s"), self.ax[2].set_ylabel("B_z in mT")
        self.ax[2].grid(color='k', linestyle=':', linewidth=0.5)

    def update(self, *args) -> None:
        self.plot1.set_ydata(
            1e3 * self.mu0 * np.asarray(self.sensor.h_sensor)[:, self.convert(self.sliderbar.get()), 0])
        self.plot2.set_ydata(
            1e3 * self.mu0 * np.asarray(self.sensor.h_sensor)[:, self.convert(self.sliderbar.get()), 1])
        self.plot3.set_ydata(
            1e3 * self.mu0 * np.asarray(self.sensor.h_sensor)[:, self.convert(self.sliderbar.get()), 2])

        for ax in self.ax:
            ax.relim()
            ax.autoscale_view()

        self.canvas.draw()

    def convert(self, val: float) -> int:
        return int(np.round((self.sensor.sensor_sampling - 1) / (
                    self.sensor.gmr_offset[-1] - self.sensor.gmr_offset[0] + self.sensor.gmr_length) * (
                                        val * 1e-3 - self.sensor.gmr_offset[0] + self.sensor.gmr_length / 2)))
