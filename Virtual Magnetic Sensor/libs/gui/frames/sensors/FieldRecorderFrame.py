import tkinter as tk
from tkinter import ttk
from typing import Callable

from libs.gui.frames.ObjectFrame import ObjectFrame
from libs.gui.GUIElements import GUIElements as Gui
from libs.gui.GUIHandler import GUIHandler

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler


class FieldRecorderFrame(ObjectFrame):
    """description of class"""

    def __init__(self,
                 master: tk.Frame,
                 data_handler: DataHandler,
                 config_handler: ConfigHandler,
                 gui_handler: GUIHandler,
                 remove_sensor: Callable) -> None:

        super().__init__(master=master, title="Magnetic Field Recording", data_handler=data_handler,
                         config_handler=config_handler, gui_handler=gui_handler, remove=remove_sensor)
        self.entries['field_specifier'] = tk.IntVar()

        ttk.Radiobutton(master=self, text="B-Field", variable=self.entries['field_specifier'], value=1).grid(
            column=0, row=0, sticky='w', padx=config_handler.config['GUI']['padding'],
            pady=config_handler.config['GUI']['h_spacing'])
        ttk.Radiobutton(master=self, text="H-Field", variable=self.entries['field_specifier'], value=2).grid(
            column=0, row=1, sticky='w', padx=config_handler.config['GUI']['padding'],
            pady=config_handler.config['GUI']['h_spacing'])

        self.entries['boundaries'] = Gui.vector6_input(master=self, config=config_handler.config,
                                                       col=0, row=2, column_span=3, head_label="Area in mm")

        self.entries['samples'] = Gui.vector3_input(master=self, config=config_handler.config,
                                                    head_label="Samples",
                                                    col=0, row=3, column_span=3, entry_labels=["x: ", "y: ", "z: "])
        self.entries['maxh'] = Gui.input_line(master=self, config=config_handler.config, col=0, row=4,
                                              label="Max Mesh Size:", unit="mm")

        self.button_frame.grid(column=0, row=5, columnspan=3, rowspan=1, sticky='s,w,e')
