import tkinter as tk
from tkinter import ttk
import configparser
from typing import List

from libs.ConfigHandler import ConfigHandler
from libs.DataHandler import DataHandler

from libs.gui.GUIElements import GUIElements as Gui


class SettingsFrame(tk.Tk):

    def __init__(self, config_handler: ConfigHandler):
        self.config_handler = config_handler

        super().__init__()
        self.title("Settings")
        tab_control = ttk.Notebook(self)
        tab_control.pack()

        self.apply_button = ttk.Button(self, text="Apply", command=self.apply).pack(side='right')
        self.cancel_button = ttk.Button(self, text="Cancel", command=self.cancel).pack(side='right')
        self.ok_button = ttk.Button(self, text="Ok", command=self.ok).pack(side='right')

        self.data_dict = DataHandler.convert_dict(
            {section:
                dict(self.config_handler.config.items(section)) for section in self.config_handler.config.sections()})

        tabs: list = list()
        self.entries: list = list()

        for key, value in self.data_dict.items():
            tabs.append(ttk.Frame(tab_control))
            tab_control.add(tabs[-1], text=key.capitalize())
            for num, (option, val) in enumerate(value.items()):
                self.entries.append(
                    Gui.settings_line(tabs[-1], self.config_handler.config, num, self.format_option(option), val))

        tab_control.pack(expand=1, fill="both")

        self.mainloop()

    def apply(self):
        self.config_handler.config = self.get_config()
        self.config_handler.write_config()

    def cancel(self):
        self.destroy()
        self.quit()

    def ok(self):
        self.config_handler.config = self.get_config()
        self.config_handler.write_config()
        self.destroy()
        self.quit()

    def get_config(self):
        cfg: configparser.ConfigParser = configparser.ConfigParser()
        i: int = 0

        for key, value in self.data_dict.items():
            cfg.add_section(key)
            for option, val in value.items():
                # Check for correct values
                cfg.set(key, option, str(self.entries[i].get()))
                i += 1

        return cfg

    @staticmethod
    def format_option(option: str):
        string_list: List[str] = option.split('_')
        entry: str = ""
        for string in string_list:
            entry += string.capitalize() + " "
        entry = entry.rstrip() + ":"
        return entry
