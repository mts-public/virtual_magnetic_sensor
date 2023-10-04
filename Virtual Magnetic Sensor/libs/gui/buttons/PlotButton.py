from tkinter import ttk
from tkinter.messagebox import showinfo
from typing import Union

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler

from libs.elements.sensors.GMRSensor import GMRSensor

from libs.gui.plot.PlotHandler import PlotHandler
from libs.gui.GUIHandler import GUIHandler


class PlotButton:
    """description of class"""

    def __init__(self,
                 master: Union[ttk.LabelFrame, ttk.Frame],
                 data_handler: DataHandler,
                 config_handler: ConfigHandler,
                 gui_handler: GUIHandler) -> None:
        self.sensor: Union[GMRSensor, None] = None

        self.button = ttk.Button(master, text="plot", command=lambda: self.click(data_handler, self.sensor))
        self.button.pack(side="left", fill="x", anchor="ne", expand=True,
                         padx=config_handler.config['GUI']['padding'], pady=config_handler.config['GUI']['h_spacing'])
        gui_handler.buttons.append(self.button)

    @staticmethod
    def click(data_handler: DataHandler, sensor: Union[GMRSensor, None]) -> None:
        if sensor is not None:
            if len(sensor.u_sin) != 0:
                PlotHandler(data_handler, sensor)
            else:
                showinfo(title='Error', message='No data available for plot.')
        else:
            showinfo(title='Error', message='No data available for plot.')
