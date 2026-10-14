import tkinter as tk
from tkinter import ttk
import configparser
from typing import Any, Callable, Dict, List, Tuple

from libs.ConfigHandler import ConfigHandler

from libs.gui.GUIElements import GUIElements as Gui


class SettingsFrame(tk.Tk):

    themes: List[str] = ['awdark', 'awlight']

    # option: (minimum, maximum, resolution, unit)
    gui_sliders: Dict[str, Tuple[float, float, float, str]] = {
        'padding': (0, 20, 1, "px"),
        'v_spacing': (0, 20, 1, "px"),
        'h_spacing': (0, 20, 1, "px"),
        'column_width': (200, 800, 10, "px"),
        'entry_width': (5, 30, 1, "chars"),
        'height': (400, 1600, 10, "px"),
        'arrow_size': (5, 40, 1, "px")
    }

    setup_filetypes: List[Tuple[str, str]] = [('INI Files', '*.ini *.INI'),
                                              ('PY Files', '*.py'),
                                              ('HDF5 Files', '*.hdf5 *.hdf *.h4 *.hdf4 *.he2 *.h5 *.he'),
                                              ('All Files', '*.*')]

    def __init__(self, config_handler: ConfigHandler):

        super().__init__()
        self.title("Settings")
        Gui.init_style(self, config_handler.config)

        tab_control = ttk.Notebook(self)
        tab_control.pack(expand=1, fill="both")

        # themed frame spanning the full width, so the window background does not show next to the buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(side='bottom', fill='x')

        self.apply_button = ttk.Button(button_frame, text="Apply", command=lambda: self.apply(config_handler))
        self.apply_button.pack(side='right')
        self.cancel_button = ttk.Button(button_frame, text="Cancel", command=self.cancel)
        self.cancel_button.pack(side='right')
        self.ok_button = ttk.Button(button_frame, text="Ok", command=lambda: self.ok(config_handler))
        self.ok_button.pack(side='right')

        # getter for every option returning the value as it is written into the config file
        self.entries: Dict[Tuple[str, str], Callable[[], str]] = dict()

        for section, options in config_handler.config.items():
            tab = ttk.Frame(tab_control)
            tab_control.add(tab, text=section.capitalize())
            for row, (option, value) in enumerate(options.items()):
                self.entries[(section, option)] = self.settings_widget(tab, config_handler, row, section, option,
                                                                       value)

        self.mainloop()

    def settings_widget(self, master: ttk.Frame, config_handler: ConfigHandler, row: int, section: str, option: str,
                        value: Any) -> Callable[[], str]:
        config = config_handler.config
        label = self.format_option(option)

        if section == 'GENERAL' and option == 'setup':
            var = Gui.settings_path_line(master, config, row, label, value, filetypes=self.setup_filetypes)
            return var.get
        if section == 'GENERAL' and option == 'measurement_path':
            var = Gui.settings_path_line(master, config, row, label, value, directory=True)
            return var.get
        if section == 'GENERAL' and option == 'auto_save':
            var = Gui.settings_switch_line(master, config, row, label, value)
            return lambda: str(var.get())
        if section == 'GENERAL' and option == 'max_process_memory':
            # stored in MB, displayed in GB
            memory_slider = Gui.settings_slider_line(master, config, row, label, float(value) / 1024, 1, 16, 1, "GB")
            return lambda: str(float(round(memory_slider.get()) * 1024))
        if section == 'GUI' and option == 'theme':
            var = Gui.settings_combobox_line(master, config, row, label, value, self.themes)
            return var.get
        if section == 'GUI' and option in self.gui_sliders:
            from_, to, resolution, unit = self.gui_sliders[option]
            slider = Gui.settings_slider_line(master, config, row, label, value, from_, to, resolution, unit)
            return lambda: str(int(round(slider.get())))

        entry = Gui.settings_line(master, config, row, label, value)
        return entry.get

    def apply(self, config_handler: ConfigHandler):
        config_handler.config_parser = self.get_config()
        config_handler.update_config()
        config_handler.write_configfile()

    def cancel(self):
        self.destroy()
        self.quit()

    def ok(self, config_handler: ConfigHandler):
        self.apply(config_handler)
        self.destroy()
        self.quit()

    def get_config(self) -> configparser.ConfigParser:
        cfg: configparser.ConfigParser = configparser.ConfigParser()

        for (section, key), getter in self.entries.items():
            if not cfg.has_section(section):
                cfg.add_section(section)
            cfg.set(section, key, getter())

        return cfg

    @staticmethod
    def format_option(option: str):
        string_list: List[str] = option.split('_')
        entry: str = ""
        for string in string_list:
            entry += string.capitalize() + " "
        entry = entry.rstrip() + ":"
        return entry
