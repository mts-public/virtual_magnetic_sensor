from tkinter import ttk
from typing import Callable

from libs.gui.frames.ObjectFrame import ObjectFrame
from libs.gui.GUIHandler import GUIHandler
from libs.gui.GUIElements import GUIElements as Gui

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler


class SensorTemplateFrame(ObjectFrame):
    """The GUI window for the new element is designed here.
    inputs.
    1. Rename this class. The class name must match the elements class name with an additional 'Frame'. For example:
    A class called 'NewSensor' expects a class called 'NewSensorFrame'.
    2. Move this file in the right package (a frame for a magnet in the magnets package for instance).
    2. Add the entries. The names in the entries dictionary must match the class attributes! Prefabricated methods in
    the GUIElements class allow single, 2D, 3D and 6D vectors.
    3. Arrange the entries using the col and row attributes.
    """

    def __init__(self,
                 master: ttk.Frame,
                 data_handler: DataHandler,
                 config_handler: ConfigHandler,
                 gui_handler: GUIHandler,
                 remove_sensor: Callable) -> None:
        super().__init__(master=master, title="Template Element", data_handler=data_handler,
                         config_handler=config_handler, gui_handler=gui_handler, remove=remove_sensor)

        self.entries['attribute0'] = Gui.input_line(master=self, config=config_handler.config, col=0, row=0,
                                                    label="Input Line Example", unit="mm")
        self.entries['attribute1'] = Gui.vector2_input(master=self, config=config_handler.config, col=0, row=1,
                                                       width=10,
                                                       label='2D Vector Example:', unit="mm")
        self.entries['attribute2'] = Gui.vector3_input(master=self, config=config_handler.config,
                                                       head_label="3D Vector Example", col=0, row=2, column_span=3,
                                                       entry_labels=["x:", "y:", "z:"])
        self.entries['attribute3'] = Gui.vector6_input(master=self, config=config_handler.config,
                                                       col=0, row=3, column_span=3, head_label="6D Vector Example")

        self.button_frame.grid(column=0, row=4, columnspan=3, rowspan=1, sticky='s,w,e')
