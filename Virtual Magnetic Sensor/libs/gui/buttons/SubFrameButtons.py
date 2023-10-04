from tkinter import ttk
from typing import Callable
from typing import Union
from configparser import ConfigParser

from libs.gui.GUIHandler import GUIHandler


class AddButton:
    """description of the class"""

    def __init__(self,
                 master: ttk.Frame,
                 label: str,
                 gui_handler: GUIHandler,
                 command: Callable) -> None:

        self.button = ttk.Button(master, text=label, command=command)
        self.button.pack(side="left", fill="x", anchor="ne", expand=True, padx=1)
        gui_handler.buttons.append(self.button)


class RemoveButton:
    """description of the class"""

    def __init__(self,
                 master: Union[ttk.LabelFrame, ttk.Frame],
                 config: ConfigParser,
                 gui_handler: GUIHandler,
                 command: Callable) -> None:

        self.button = ttk.Button(master, text="remove", command=command)
        self.button.pack(side="left", fill="x", anchor="ne", expand=True, padx=config['GUI']['padding'],
                         pady=config['GUI']['h_spacing'])
        gui_handler.buttons.append(self.button)
