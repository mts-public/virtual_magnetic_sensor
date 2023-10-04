import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Union

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler

from libs.gui.GUIElements import GUIElements as Gui

from libs.gui.GUIHandler import GUIHandler


class SimParamsFrame(ttk.LabelFrame):
    """description of class"""

    def __init__(self,
                 master: tk.Frame,
                 side: str,
                 data_handler: DataHandler,
                 config_handler: ConfigHandler,
                 gui_handler: GUIHandler) -> None:

        super().__init__(master=master, text="Simulation Parameters", width=config_handler.config['GUI']['column_width'])
        self.pack(side=side, fill=tk.X, padx=config_handler.config['GUI']['padding'],
                  pady=config_handler.config['GUI']['padding'])

        self.time_frame = Gui.label_frame(master=self, config=config_handler.config, col=1, row=1,
                                          column_span=3,
                                          row_span=1, label="Time Dynamics")

        self.entries: Dict[str, Union[ttk.Entry, List[ttk.Entry]]] = dict()

        self.entries['t0'] = Gui.input_line(master=self.time_frame, config=config_handler.config, col=1, row=1,
                                            label=u'Starting Time t\u2080: ', unit='s')
        self.entries['t1'] = Gui.input_line(master=self.time_frame, config=config_handler.config, col=1, row=2,
                                            label=u'Ending Time t\u2081: ', unit='s')
        self.entries['samples'] = Gui.input_line(master=self.time_frame, config=config_handler.config, col=1, row=3,
                                                 label="Samples N:")

        self.entries['boundaries'] = Gui.vector6_input(master=self, config=config_handler.config, col=1,
                                                       row=2, column_span=3, head_label="Boundaries in mm")
        self.entries['maxh_global'] = Gui.input_line(master=self, config=config_handler.config, col=1, row=3,
                                                     label="Global Max Mesh Size:", unit="mm")
        self.entries['tol'] = Gui.input_line(master=self, config=config_handler.config, col=1, row=4,
                                             label="Error Tolerance:")
        self.entries['maxit'] = Gui.input_line(master=self, config=config_handler.config, col=1, row=5,
                                               label="Max Iterations:")

    def get_parameters(self) -> Dict[str, any]:
        return Gui.extract(self.entries)

    def refresh(self, data_handler: DataHandler, config_handler: ConfigHandler, gui_handler: GUIHandler) -> None:
        Gui.insert(self.entries, data_handler.sim_params())
