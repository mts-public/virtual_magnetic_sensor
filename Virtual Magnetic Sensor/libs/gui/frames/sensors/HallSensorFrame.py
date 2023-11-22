from tkinter import ttk
from tkinter.messagebox import showinfo
from typing import Callable, Union

from libs.gui.frames.ObjectFrame import ObjectFrame
from libs.gui.GUIHandler import GUIHandler
from libs.gui.GUIElements import GUIElements as Gui
from libs.gui.plot.HallSensorPlot import HallSensorPlot

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler

from libs.elements.sensors.HallSensor import HallSensor


class HallSensorFrame(ObjectFrame):
    """"""

    def __init__(self,
                 master: ttk.Frame,
                 data_handler: DataHandler,
                 config_handler: ConfigHandler,
                 gui_handler: GUIHandler,
                 remove_sensor: Callable) -> None:
        super().__init__(master=master, title="Hall Sensor", data_handler=data_handler,
                         config_handler=config_handler, gui_handler=gui_handler, remove=remove_sensor)

        self.entries['pos'] = Gui.vector3_input(master=self, config=config_handler.config,
                                                head_label="Center x in mm", col=0, row=0, column_span=3,
                                                entry_labels=["x:", "y:", "z:"])
        self.entries['dim'] = Gui.vector3_input(master=self, config=config_handler.config,
                                                head_label="Size b in mm", col=0, row=1, column_span=3,
                                                entry_labels=["x:", "y:", "z:"])
        self.entries['rot'] = Gui.vector3_input(master=self, config=config_handler.config,
                                                head_label="Rotation θ in °", col=0, row=2, column_span=3,
                                                entry_labels=["x:", "y:", "z:"])
        self.entries['hall_coefficient'] = Gui.input_line(master=self, config=config_handler.config, col=0, row=3,
                                                          label="Hall Coefficient A_h", unit="mm^3/kC")
        self.entries['conductor_thickness'] = Gui.input_line(master=self, config=config_handler.config, col=0, row=4,
                                                             label="Conductor thickness t", unit="µm")
        self.entries['current'] = Gui.input_line(master=self, config=config_handler.config, col=0, row=5,
                                                 label="Current I", unit="mm")
        self.entries['maxh'] = Gui.input_line(master=self, config=config_handler.config, col=0, row=6,
                                              label="Max Mesh Size", unit="mm")

        self.plot_button = PlotButton(master=self.button_frame, data_handler=data_handler,
                                      config_handler=config_handler, gui_handler=gui_handler)
        self.buttons.append(self.plot_button.button)
        self.button_frame.grid(column=0, row=7, columnspan=3, rowspan=1, sticky='s,w,e')

    def update_buttons(self, sensor: HallSensor):
        self.plot_button.sensor = sensor


class PlotButton:
    """description of class"""

    def __init__(self,
                 master: Union[ttk.LabelFrame, ttk.Frame],
                 data_handler: DataHandler,
                 config_handler: ConfigHandler,
                 gui_handler: GUIHandler) -> None:
        self.sensor: Union[HallSensor, None] = None

        self.button = ttk.Button(master, text="plot", command=lambda: self.click(data_handler, self.sensor))
        self.button.pack(side="left", fill="x", anchor="ne", expand=True,
                         padx=config_handler.config['GUI']['padding'], pady=config_handler.config['GUI']['h_spacing'])
        gui_handler.buttons.append(self.button)

    @staticmethod
    def click(data_handler: DataHandler, sensor: Union[HallSensor, None]) -> None:
        if sensor is not None:
            if len(sensor.hall_voltage) != 0:
                HallSensorPlot(data_handler, sensor)
            else:
                showinfo(title='Error', message='No data available for plot.')
        else:
            showinfo(title='Error', message='No data available for plot.')
