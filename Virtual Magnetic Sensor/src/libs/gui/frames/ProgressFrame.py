import tkinter as tk
from tkinter import ttk
import time

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler

from libs.gui.GUIHandler import GUIHandler


class ProgressFrame(ttk.LabelFrame):
    """description of class"""

    def __init__(self,
                 master: tk.Frame,
                 side: str,
                 data_handler: DataHandler,
                 config_handler: ConfigHandler,
                 gui_handler: GUIHandler):
        self.master = master

        self.start_time = time.time()

        super().__init__(master=master, text="Progress", width=config_handler.config['GUI']['column_width'])
        self.pack(side=side, fill=tk.X, padx=config_handler.config['GUI']['padding'],
                  pady=config_handler.config['GUI']['padding'])
        self.columnconfigure(1, weight=100)

        self.progressBar = ttk.Progressbar(self, orient=tk.HORIZONTAL, mode='determinate')
        self.progressBar.grid(column=0, columnspan=2, row=0, sticky='n,w,e',
                              padx=config_handler.config['GUI']['v_spacing'],
                              pady=config_handler.config['GUI']['h_spacing'])
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.progressVar = tk.StringVar()
        self.progressVar.set("0%")
        progress_label = ttk.Label(master=self, textvariable=self.progressVar)
        progress_label.grid(column=2, row=0, sticky='nw', padx=(0, config_handler.config['GUI']['v_spacing']),
                            pady=config_handler.config['GUI']['h_spacing'])

        self.idxVar = tk.StringVar()
        self.idxVar.set("-")
        idx_label = ttk.Label(master=self, text="Frame:")
        idx_label.grid(column=0, row=1, sticky="nw", padx=config_handler.config['GUI']['v_spacing'],
                       pady=config_handler.config['GUI']['h_spacing'])
        idx_var = ttk.Label(master=self, textvariable=self.idxVar)
        idx_var.grid(column=1, row=1, sticky='nw', padx=config_handler.config['GUI']['v_spacing'],
                     pady=config_handler.config['GUI']['h_spacing'])

        self.timeVar = tk.StringVar()
        self.timeVar.set("-")
        time_label = ttk.Label(master=self, text="Remaining Time:")
        time_label.grid(column=0, row=2, sticky="nw", padx=config_handler.config['GUI']['v_spacing'],
                        pady=config_handler.config['GUI']['h_spacing'])
        time_var = ttk.Label(master=self, textvariable=self.timeVar)
        time_var.grid(column=1, row=2, sticky='nw', padx=config_handler.config['GUI']['v_spacing'],
                      pady=config_handler.config['GUI']['h_spacing'])

        self.durationVar = tk.StringVar()
        self.durationVar.set("-")
        duration_label = ttk.Label(master=self, text="Duration:")
        duration_label.grid(column=0, row=3, sticky="nw", padx=config_handler.config['GUI']['v_spacing'],
                            pady=config_handler.config['GUI']['h_spacing'])
        duration_var = ttk.Label(master=self, textvariable=self.durationVar)
        duration_var.grid(column=1, row=3, sticky='nw', padx=config_handler.config['GUI']['v_spacing'],
                          pady=config_handler.config['GUI']['h_spacing'])

    def reset(self) -> None:
        self.start_time = time.time()
        self.progressBar['value'] = 0
        self.progressVar.set("0%")
        self.idxVar.set("-")
        self.timeVar.set("-")
        self.durationVar.set("-")

    def refresh(self, data_handler: DataHandler, config_handler: ConfigHandler, gui_handler: GUIHandler,
                n: int = 0) -> None:
        if n > 0:
            self.progressBar['value'] = int(round(100 * n / data_handler.sim_params().samples))
            self.progressVar.set(str(int(round(100 * n / data_handler.sim_params().samples))) + "%")

            self.idxVar.set(str(n) + " of " + str(data_handler.sim_params().samples))
            self.timeVar.set(
                str(round((time.time() - self.start_time) / n * (data_handler.sim_params().samples - n), 1)) + "s")
            self.durationVar.set(str(round(time.time() - self.start_time, 1)) + "s")

        self.master.update_idletasks()
