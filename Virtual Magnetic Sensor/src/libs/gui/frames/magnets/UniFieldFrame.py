from tkinter import ttk
from typing import Callable

from libs.gui.frames.ObjectFrame import ObjectFrame
from libs.gui.GUIHandler import GUIHandler
from libs.gui.GUIElements import GUIElements as Gui

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler


class UniFieldFrame(ObjectFrame):
    """description of class"""

    def __init__(self,
                 master: ttk.Frame,
                 data_handler: DataHandler,
                 config_handler: ConfigHandler,
                 gui_handler: GUIHandler,
                 remove_magnet: Callable) -> None:

        super().__init__(master=master, title="Uniform Magnetic Field", data_handler=data_handler,
                         config_handler=config_handler, gui_handler=gui_handler, remove=remove_magnet)

        self.entries['direction'] = Gui.vector3_input(master=self, config=config_handler.config,
                                                      head_label="Direction n\u2098", col=0, row=0, column_span=3,
                                                      entry_labels=["x:", "y:", "z:"])
        self.entries['strength'] = Gui.input_line(master=self, config=config_handler.config, col=0, row=1,
                                                  label="Field Strength B\u2080:", unit="mT")
        self.button_frame.grid(column=0, row=2, columnspan=3, rowspan=1, sticky='s,w,e')
