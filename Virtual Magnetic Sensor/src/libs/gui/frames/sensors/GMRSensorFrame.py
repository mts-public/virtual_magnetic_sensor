import tkinter as tk
from tkinter import ttk
from typing import Callable

from libs.gui.frames.ObjectFrame import ObjectFrame

from libs.gui.buttons.PlotButton import PlotButton
from libs.gui.GUIElements import GUIElements as Gui
from libs.gui.GUIHandler import GUIHandler

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler

from libs.elements.sensors.GMRSensor import GMRSensor
from libs.elements.sensors.GMRSensor import GMRSensorProperties


class GMRSensorFrame(ObjectFrame):
    """description of class"""

    def __init__(self,
                 master: ttk.Frame,
                 data_handler: DataHandler,
                 config_handler: ConfigHandler,
                 gui_handler: GUIHandler,
                 remove_sensor: Callable) -> None:

        super().__init__(master=master, title="GMR Sensor", data_handler=data_handler, config_handler=config_handler,
                         gui_handler=gui_handler, remove=remove_sensor)

        self.entries['pos'] = Gui.vector3_input(master=self, config=config_handler.config,
                                                head_label="Center x in mm", col=0, row=0, column_span=3,
                                                entry_labels=["x: ", "y: ", "z: "])

        self.entries['rot'] = Gui.vector3_input(master=self, config=config_handler.config,
                                                head_label="Rotation θ in °", col=0, row=1, column_span=3,
                                                entry_labels=["x:", "y:", "z:"])

        self.menu_var = Gui.dropdown_menu(master=self, config=config_handler.config, col=0, row=2,
                                          architecture_list=GMRSensor.architectures)
        self.menu_var.trace("w", self.menu_callback)

        self.entries['gmr_offset'] = Gui.vector8_input(
            master=self,
            config=config_handler.config,
            col=0, row=3, column_span=3,
            head_label="GMR Position in µm",
            entry_labels=[u'R\u2081', u'R\u2082', u'R\u2083', u'R\u2084', u'R\u2085', u'R\u2086', u'R\u2087',
                          u'R\u2088']
        )

        self.entries['gmr_length'] = Gui.input_line(master=self, config=config_handler.config, col=0, row=4,
                                                    label="GMR Length:", unit="µm")

        self.sim_params_frame = Gui.label_frame(master=self, config=config_handler.config, col=0, row=5,
                                                column_span=3, row_span=1, label="Simulation Parameters")
        self.entries['gmr_sampling'] = Gui.input_line(master=self.sim_params_frame, config=config_handler.config,
                                                      col=0, row=0, label="GMR Sampling:")

        self.entries['sensor_sampling'] = Gui.input_line(master=self.sim_params_frame, config=config_handler.config,
                                                         col=0, row=1, label="Sensor H-Field Sampling:")
        self.entries['depth'] = Gui.input_line(master=self.sim_params_frame, config=config_handler.config, col=0, row=2,
                                               label="Depth b:", unit="µm")
        self.entries['height'] = Gui.input_line(master=self.sim_params_frame, config=config_handler.config,
                                                col=0, row=3, label="Height h:", unit="µm")
        self.entries['maxh'] = Gui.input_line(master=self.sim_params_frame, config=config_handler.config, col=0, row=4,
                                              label="Max Mesh Size:", unit="mm")

        self.plot_button = PlotButton(master=self.button_frame, data_handler=data_handler,
                                      config_handler=config_handler, gui_handler=gui_handler)
        self.buttons.append(self.plot_button.button)

        self.info_button = ttk.Button(master=self.button_frame, text="?", width=3, command=InfoFrame)
        self.info_button.pack(side="right", anchor="ne", padx=(1, config_handler.config['GUI']['padding']),
                              pady=config_handler.config['GUI']['h_spacing'])
        gui_handler.buttons.append(self.info_button)
        self.buttons.append(self.info_button)

        self.button_frame.grid(column=0, row=7, columnspan=3, rowspan=1, sticky='s,w,e')

    def menu_callback(self, *args) -> None:
        if not self.menu_var.get() == "-":
            for i in range(0, len(self.entries['gmr_offset'])):
                self.entries['gmr_offset'][i].delete(0, 'end')
                self.entries['gmr_offset'][i].insert(0, GMRSensorProperties[self.menu_var.get()].value[0][i])
            self.entries['gmr_length'].delete(0, 'end')
            self.entries['gmr_length'].insert(0, GMRSensorProperties[self.menu_var.get()].value[1])
            self.menu_var.set("select")

    def update_buttons(self, sensor: GMRSensor):
        self.plot_button.sensor = sensor


class InfoFrame:

    def __init__(self) -> None:
        self.frame = tk.Toplevel()
        self.frame.title("Info")
        self.frame.protocol("WM_DELETE_WINDOW", self.destroy)

        img = (tk.PhotoImage(file=r"resources/images/GMRsensor.png"))
        image_width = int(1.0 * img.width())
        image_height = int(1.0 * img.height())
        self.resized_img = img.subsample(1, 1)
        self.frame.geometry(f"{image_width}x{image_height}+{100}+{100}")

        image_frame = ttk.Label(master=self.frame, image=self.resized_img)
        image_frame.pack(expand=True, fill="both", side="top", anchor="center")

    def destroy(self):
        self.frame.destroy()
