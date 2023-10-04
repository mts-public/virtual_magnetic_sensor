from __future__ import annotations
import configparser
from pathlib import Path
from typing import List

from libs.DataHandler import DataHandler


class ConfigHandler:
    """The class manages the loading, writing and managing of the configuration parameters.

    :param config: Configparser object containing the settings from the config.ini file.
    :type config: configparser.Configparser
    """

    config: configparser.ConfigParser

    def __init__(self) -> None:
        """Constructor method."""

        self.config: configparser = configparser.ConfigParser()
        self.config_path: Path = Path('cfg/config.ini')

        self.load_config()

    def load_setup(self, data_stack: List[DataHandler]):
        if self.config.has_option('GENERAL', 'setup'):
            if Path(self.config['GENERAL']['setup']).suffix.lower() == '.ini':
                data_stack[0].load_ini(Path(self.config['GENERAL']['setup']))
            elif Path(self.config['GENERAL']['setup']).suffix.lower() == '.py':
                data_stack = data_stack[0].load_py(Path(self.config['GENERAL']['setup']))
            else:
                data_stack[0].filepath = Path(self.config['GENERAL']['measurement_path'], 'Project 1')
            for data_handler in data_stack:
                data_handler.filepath = Path(self.config['GENERAL']['measurement_path'],
                                             Path(self.config['GENERAL']['setup']).stem)
        else:
            data_stack[0].filepath = Path(self.config['GENERAL']['measurement_path'], 'Project 1')

    def load_config(self):
        self.config.read(self.config_path)

    def write_config(self):
        with open(self.config_path, 'w') as f:
            self.config.write(f)
