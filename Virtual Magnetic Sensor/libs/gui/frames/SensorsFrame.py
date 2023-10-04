from __future__ import annotations
from tkinter import ttk
from tkinter import X

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler

from libs.elements.sensors.GMRSensor import GMRSensor
from libs.elements.sensors.FieldRecorder import FieldRecorder

from libs.gui.GUIHandler import GUIHandler
from libs.gui.buttons.SubFrameButtons import AddButton
from libs.gui.frames.sensors.GMRSensorFrame import GMRSensorFrame
from libs.gui.frames.sensors.FieldRecorderFrame import FieldRecorderFrame
from libs.gui.GUIElements import GUIElements as Gui


class SensorsFrame(ttk.LabelFrame):

    def __init__(self,
                 master: ttk.Frame,
                 side: str,
                 data_handler: DataHandler,
                 config_handler: ConfigHandler,
                 gui_handler: GUIHandler) -> None:

        self.sub_frames = list()

        super().__init__(master=master, text="Sensors", width=config_handler.config['GUI']['column_width'])
        self.pack(side=side, fill=X, padx=config_handler.config['GUI']['padding'],
                  pady=config_handler.config['GUI']['padding'])

        self.button_frame = Gui.button_frame(self, config_handler.config)

        self.scrollable_frame = Gui.scrollable_frame(self, config_handler.config)

        self.gmr_button = AddButton(master=self.button_frame, label="+ GMR Sensor", gui_handler=gui_handler,
                                    command=lambda: self.add_gmr(data_handler, config_handler, gui_handler))
        self.rec_field_button = AddButton(master=self.button_frame, label="+ Record Field", gui_handler=gui_handler,
                                          command=lambda: self.add_rec_field(data_handler, config_handler, gui_handler))
        """self.dummy1_button = AddButton(master=self.button_frame, label="+ Dummy", gui_handler=gui_handler,
                                       command=self.add_dummy1)"""
        self.update_sub_frames(data_handler, config_handler, gui_handler)

    def add_gmr(self, data_handler: DataHandler, config_handler: ConfigHandler, gui_handler: GUIHandler):
        self.sub_frames.append(GMRSensorFrame(master=self.scrollable_frame, data_handler=data_handler,
                                              config_handler=config_handler, gui_handler=gui_handler,
                                              remove_sensor=self.remove_sensor))
        self.sub_frames[-1].refresh(GMRSensor.template())

    def add_rec_field(self, data_handler: DataHandler, config_handler: ConfigHandler, gui_handler: GUIHandler):
        self.sub_frames.append(FieldRecorderFrame(master=self.scrollable_frame, data_handler=data_handler,
                                                  config_handler=config_handler, gui_handler=gui_handler,
                                                  remove_sensor=self.remove_sensor))
        self.sub_frames[-1].refresh(FieldRecorder.template(gui_handler.sim_frame().get_parameters()))

    """def add_dummy1(self):
        pass"""

    def erase_sub_frames(self, gui_handler: GUIHandler):
        for frame in reversed(self.sub_frames):
            frame.remove_frame(gui_handler)

    def update_sub_frames(self, data_handler: DataHandler, config_handler: ConfigHandler, gui_handler: GUIHandler):
        for sensor in data_handler.sensors():
            if isinstance(sensor, GMRSensor):
                self.sub_frames.append(GMRSensorFrame(master=self.scrollable_frame, data_handler=data_handler,
                                                      config_handler=config_handler, gui_handler=gui_handler,
                                                      remove_sensor=self.remove_sensor))
            if isinstance(sensor, FieldRecorder):
                self.sub_frames.append(FieldRecorderFrame(master=self.scrollable_frame, data_handler=data_handler,
                                                          config_handler=config_handler, gui_handler=gui_handler,
                                                          remove_sensor=self.remove_sensor))

    def remove_sensor(self, obj: GMRSensorFrame):
        self.sub_frames.remove(obj)
        self.update_idletasks()

    def refresh(self, data_handler: DataHandler, config_handler: ConfigHandler, gui_handler: GUIHandler):
        self.erase_sub_frames(gui_handler)
        self.update_sub_frames(data_handler, config_handler, gui_handler)
        for num, frame in enumerate(self.sub_frames):
            if hasattr(frame, "refresh"):
                frame.refresh(data_handler.sensors()[num])
