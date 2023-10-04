import tkinter as tk

import matplotlib.figure
import numpy as np

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt

from libs.DataHandler import DataHandler
from libs.elements.sensors.GMRSensor import GMRSensor


class Figure2:
    """description of class"""

    def __init__(self,
                 data_handler: DataHandler,
                 sensor: GMRSensor,
                 root: tk.Tk) -> None:
        self.data_handler = data_handler
        self.sensor = sensor
        self.root = root

        self.fig = matplotlib.figure.Figure
        self.plot1 = matplotlib.lines.Line2D
        self.plot2 = matplotlib.lines.Line2D
        self.plot3 = matplotlib.lines.Line2D
        self.canvas = FigureCanvasTkAgg
        self.sliderbar = tk.Scale

        self.draw()

    def draw(self) -> None:
        self.fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(7, 5), dpi=100)
        self.plot1, = ax[0].plot(self.data_handler.sim_params().t, 1e3 * np.asarray(self.sensor.u_sin))
        self.plot2, = ax[1].plot(self.data_handler.sim_params().t, 1e3 * np.asarray(self.sensor.u_cos))
        self.plot3, = ax[2].plot(np.array([i for i in range(0, self.sensor.sensor_sampling)]),
                                 1e-3*np.asarray(self.sensor.h_sensor)[0, :, 0])
        self.fig.subplots_adjust(hspace=0.262)

        ax[0].set_xlabel("Time in s"), ax[0].set_ylabel("Usin in mV")
        ax[0].grid(color='k', linestyle=':', linewidth=0.5)
        ax[1].set_xlabel("Time in s"), ax[1].set_ylabel("Ucos in mV")
        ax[1].grid(color='k', linestyle=':', linewidth=0.5)
        ax[2].set_xlabel("p"), ax[2].set_ylabel("H_x in kA/m"), ax[2].grid(color='k', linestyle=':', linewidth=0.5)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=0, sticky='nw')

        sliderbar_label = tk.Label(master=self.root, text="Time in s:")
        sliderbar_label.grid(column=0, row=1)

        self.sliderbar = tk.Scale(self.root,
                                  from_=self.data_handler.sim_params().t0,
                                  to=self.data_handler.sim_params().t1,
                                  tickinterval=
                                  (self.data_handler.sim_params().t1 - self.data_handler.sim_params().t0) / 10,
                                  resolution=self.data_handler.sim_params().dt,
                                  length=700,
                                  digits=4,
                                  orient=tk.HORIZONTAL,
                                  command=self.update
                                  )
        self.sliderbar.grid(column=0, row=2, sticky='nw')
        self.sliderbar.set(self.data_handler.sim_params().t0)

        toolbar_frame = tk.Frame(master=self.root)
        toolbar_frame.grid(column=0, row=3, sticky='nw')
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()

    def update(self, *args) -> None:
        self.plot3.set_ydata(1e-3*np.asarray(self.sensor.h_sensor)[self.convert(self.sliderbar.get()), :, 0])

        self.canvas.draw()

    def convert(self, val: float) -> int:
        return int(np.round((val - self.data_handler.sim_params().t0) / self.data_handler.sim_params().dt))
