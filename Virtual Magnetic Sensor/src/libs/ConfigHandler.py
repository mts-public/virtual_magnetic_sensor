from __future__ import annotations
import configparser
from pathlib import Path
from typing import Dict
import os
import platform

from importlib.resources import files


class ConfigHandler:
    """The class manages the loading, writing and managing of the configuration parameters.

    :param config: Dictionary with the options and their respective values.
    :type config: Dict[str, Dict[str, any]]
    :param config_parser: Configparser object containing the settings from the config.ini file.
    :type config_parser: configparser.Configparser
    """

    config: Dict[str, Dict[str, any]]
    config_parser: configparser.ConfigParser

    def __init__(self) -> None:
        """Constructor method."""

        self.config_path: Path = self.get_config_path()
        self.config_parser: configparser = configparser.ConfigParser()

        self.config = self.config_template()
        self.load_configfile()

    @staticmethod
    def get_config_path(filename="config.ini"):
        system = platform.system()

        if system == "Windows":
            # C:\Users\<username>\Documents
            documents_path = Path(os.environ.get("USERPROFILE",
                                                 Path.home())) / "Documents" / "Virtual Magnetic Sensor" / "cfg"
        elif system in ("Linux", "Darwin"):  # Darwin = macOS
            # ~/Documents
            documents_path = Path.home() / "Documents" / "Virtual Magnetic Sensor" / "cfg"
        else:
            raise OSError(f"Unsupported OS: {system}")

        # Ensure the folder exists
        documents_path.mkdir(parents=True, exist_ok=True)

        return documents_path / filename

    @staticmethod
    def get_save_files_path():
        system = platform.system()

        if system == "Windows":
            # C:\Users\<username>\Documents
            documents_path = Path(os.environ.get("USERPROFILE",
                                                 Path.home())) / "Documents" / "Virtual Magnetic Sensor" / "save_files"
        elif system in ("Linux", "Darwin"):  # Darwin = macOS
            # ~/Documents
            documents_path = Path.home() / "Documents" / "Virtual Magnetic Sensor" / "save_files"
        else:
            raise OSError(f"Unsupported OS: {system}")

        # Ensure the folder exists
        documents_path.mkdir(parents=True, exist_ok=True)

        return documents_path

    @staticmethod
    def config_template() -> Dict[str, Dict[str, any]]:
        return {
            'GENERAL': {
                'setup': files("libs") / "resources" / "save_files" / "1.0.0" / "standard.ini",
                'measurement_path': ConfigHandler.get_save_files_path(),
                'auto_save': 1,
                'max_process_memory': 2048.0
            },
            'GUI': {
                'theme': 'awdark',
                'padding': 3,
                'v_spacing': 5,
                'h_spacing': 1,
                'column_width': 360,
                'entry_width': 10,
                'height': 850,
                'arrow_size': 15
            }
        }

    @staticmethod
    def isfloat(element: any) -> bool:
        """Method checks if a string is convertible to float.

        :param element: Possible float value.
        :type element: any

        :return: True when element is convertible to float, false otherwise.
        :rtype: bool
        """

        if element is None:
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False

    def load_configfile(self):
        self.config_parser.read(self.config_path)
        self.update_config()

    def write_configfile(self):
        self.config_parser.read_dict(self.config)

        Path(self.config_path).parent.mkdir(parents=True, exist_ok=True)

        with open(self.config_path, 'w') as f:
            self.config_parser.write(f)

    def update_config(self):
        for section, keys in self.config.items():
            for key, _ in keys.items():
                if self.config_parser.has_option(section, key):
                    value = self.config_parser[section][key]
                    if value.isnumeric():
                        self.config[section][key] = int(value)
                    elif self.isfloat(value):
                        self.config[section][key] = float(value)
                    elif '/' in value or '\\' in value:
                        self.config[section][key] = Path(value)
                    else:
                        self.config[section][key] = value
