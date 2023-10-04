import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, List, Union

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler

from libs.gui.GUIHandler import GUIHandler
from libs.gui.GUIElements import GUIElements as Gui

from libs.gui.buttons.SubFrameButtons import RemoveButton


class ObjectFrame(ttk.LabelFrame):

    def __init__(self,
                 master: ttk.Frame,
                 title: str,
                 data_handler: DataHandler,
                 config_handler: ConfigHandler,
                 gui_handler: GUIHandler,
                 remove: Callable) -> None:

        super().__init__(master=master, text=title)
        self.pack(side="top", fill="x")
        self.remove = remove

        self.entries: Dict[str, Union[ttk.Entry, List[ttk.Entry], tk.IntVar, tk.BooleanVar]] = dict()
        self.buttons: List[ttk.Button] = list()

        self.button_frame = ttk.Frame(self)
        remove_button = RemoveButton(master=self.button_frame, config=config_handler.config, gui_handler=gui_handler,
                                     command=lambda: self.remove_frame(gui_handler))
        self.buttons.append(remove_button.button)

    def get_parameters(self) -> Dict[str, any]:
        return Gui.extract(self.entries)

    def refresh(self, sim_object: any) -> None:
        if hasattr(sim_object, "gui"):
            Gui.insert(self.entries, sim_object.gui())
        else:
            Gui.insert(self.entries, sim_object)

    def remove_frame(self, gui_handler: GUIHandler) -> None:
        self.remove(self)
        for button in self.buttons:
            gui_handler.buttons.remove(button)
        self.destroy()
