import tkinter as tk
from tkinter import ttk
import configparser
from typing import List

from libs.ConfigHandler import ConfigHandler

from libs.gui.GUIElements import GUIElements as Gui


class SettingsFrame(tk.Tk):

    def __init__(self, config_handler: ConfigHandler):

        super().__init__()
        self.title("Settings")
        tab_control = ttk.Notebook(self)
        tab_control.pack()

        self.apply_button = ttk.Button(self, text="Apply",
                                       command=lambda: self.apply(config_handler)).pack(side='right')
        self.cancel_button = ttk.Button(self, text="Cancel", command=self.cancel).pack(side='right')
        self.ok_button = ttk.Button(self, text="Ok", command=lambda: self.ok(config_handler)).pack(side='right')

        tabs: list = list()
        self.entries: list = list()

        for key, value in config_handler.config.items():
            tabs.append(ttk.Frame(tab_control))
            tab_control.add(tabs[-1], text=key.capitalize())
            for num, (option, val) in enumerate(value.items()):
                self.entries.append(
                    Gui.settings_line(tabs[-1], config_handler.config, num, self.format_option(option), val))

        tab_control.pack(expand=1, fill="both")

        self.mainloop()

    def apply(self, config_handler: ConfigHandler):
        config_handler.config_parser = self.get_config(config_handler)
        config_handler.update_config()
        config_handler.write_configfile()

    def cancel(self):
        self.destroy()
        self.quit()

    def ok(self, config_handler: ConfigHandler):
        config_handler.config_parser = self.get_config(config_handler)
        config_handler.update_config()
        config_handler.write_configfile()
        self.destroy()
        self.quit()

    def get_config(self, config_handler: ConfigHandler):
        cfg: configparser.ConfigParser = configparser.ConfigParser()
        i: int = 0

        for section, keys in config_handler.config.items():
            cfg.add_section(section)
            for key, _ in keys.items():
                # Check for correct values
                cfg.set(section, key, str(self.entries[i].get()))
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
