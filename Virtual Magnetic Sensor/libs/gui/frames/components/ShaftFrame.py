from tkinter import ttk
from typing import Callable

from libs.gui.frames.ObjectFrame import ObjectFrame
from libs.gui.GUIElements import GUIElements as Gui
from libs.gui.GUIHandler import GUIHandler

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler


class ShaftFrame(ObjectFrame):
    """description of class"""

    def __init__(self,
                 master: ttk.Frame,
                 data_handler: DataHandler,
                 gui_handler: GUIHandler,
                 config_handler: ConfigHandler,
                 remove_shaft: Callable) -> None:
        super().__init__(master=master, title="Shaft", data_handler=data_handler, config_handler=config_handler,
                         gui_handler=gui_handler, remove=remove_shaft)

        self.entries['pos'] = Gui.vector3_input(master=self, config=config_handler.config,
                                                head_label="Center x", col=0,
                                                row=0, column_span=4, entry_labels=["x: ", "y: ", "z: "])

        self.entries['axis'] = Gui.vector3_input(master=self, config=config_handler.config,
                                                 head_label="Axis a", col=0, row=1, column_span=4,
                                                 entry_labels=["x: ", "y: ", "z: "])
        self.entries['diameter'] = Gui.vector2_input(master=self, config=config_handler.config, col=0, row=2,
                                                     width=10,
                                                     label='Inner/Outer Diameters d:', unit="mm")
        self.entries['length'] = Gui.input_line(master=self, config=config_handler.config, col=0, row=3,
                                                label="Length l:",
                                                unit="mm", col_shift=1)
        self.entries['mu_r'] = Gui.input_line(master=self, config=config_handler.config, col=0, row=4,
                                              label=u'Relative Permeability µ\u1D63:', col_shift=1)
        self.entries['maxh'] = Gui.input_line(master=self, config=config_handler.config, col=0, row=5,
                                              label="Max Mesh Size:", unit="mm", col_shift=1)

        self.button_frame.grid(column=0, row=6, columnspan=4, rowspan=1, sticky='s,w,e')
