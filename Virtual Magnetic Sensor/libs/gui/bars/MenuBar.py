import tkinter as tk
from tkinter.messagebox import showinfo
from typing import List

from libs.simulation.SimulationHandler import SimulationHandler
from libs.gui.frames.SettingsFrame import SettingsFrame
from libs.gui.frames.AboutFrame import AboutFrame

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler

from libs.gui.GUIHandler import GUIHandler
from libs.gui.FileDialogs import FileDialogs


class MenuBar(tk.Menu):

    def __init__(self, root: tk.Tk, data_stack: List[DataHandler], config_handler: ConfigHandler,
                 gui_handler: GUIHandler, multiprocessing_tasks) -> None:
        super().__init__(root)
        root.config(menu=self)

        self.file_menu = tk.Menu(self, tearoff=False)
        self.export_menu = tk.Menu(self.file_menu, tearoff=0)
        self.export_menu.add_command(label="Export as .PY",
                                     command=lambda: FileDialogs.export_py(data_stack, gui_handler))
        self.export_menu.add_command(label="Export as .INI",
                                     command=lambda: FileDialogs.export_ini(data_stack, gui_handler))
        self.file_menu.add_command(
            label='New',
            command=lambda: gui_handler.add_tab(DataHandler().template(), data_stack, config_handler),
            accelerator="Alt+Insert"
        )
        self.file_menu.add_command(
            label='Open',
            command=lambda: FileDialogs.open(data_stack, config_handler, gui_handler)
        )
        self.file_menu.add_command(
            label='Save',
            command=lambda: FileDialogs.save(data_stack, gui_handler),
            accelerator="Ctrl+S"
        )
        self.file_menu.add_command(
            label='Save as',
            command=lambda: FileDialogs.save_as(data_stack, gui_handler)
        )
        self.file_menu.add_cascade(
            label='Export',
            menu=self.export_menu
        )
        self.file_menu.add_cascade(
            label='Close',
            command=lambda: gui_handler.close_tab(data_stack),
            accelerator="Strg+X"
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label='Settings',
            command=lambda: SettingsFrame(config_handler),
            accelerator="Ctrl+Alt+S"
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label='Exit',
            command=gui_handler.exit,
            accelerator="Ctrl+Q"
        )

        self.sim_menu = tk.Menu(self, tearoff=False)
        self.sim_menu.add_command(
            label='Draw (Netgen)',
            command=lambda: SimulationHandler.draw(multiprocessing_tasks, data_stack, gui_handler,
                                                   gui_handler.selected_tab()),
            accelerator='F8')
        self.sim_menu.add_command(
            label='Run',
            command=lambda: SimulationHandler.run(multiprocessing_tasks, data_stack, config_handler, gui_handler,
                                                  gui_handler.selected_tab()),
            accelerator='F9'
        )
        self.sim_menu.add_command(
            label='Run All',
            command=lambda: SimulationHandler.run(multiprocessing_tasks, data_stack, config_handler, gui_handler),
            accelerator='F10'
        )

        self.help_menu = tk.Menu(self, tearoff=False)
        self.help_menu.add_command(
            label='Documentation',
            command=lambda: showinfo(title='Documentation', message='Coming soon.'),
        )
        self.help_menu.add_command(
            label='Info',
            command=AboutFrame,
        )

        self.add_cascade(
            label="File",
            menu=self.file_menu,
            underline=0
        )
        self.add_cascade(
            label='Simulation',
            menu=self.sim_menu,
            underline=0
        )
        self.add_cascade(
            label="?",
            menu=self.help_menu,
            underline=0
        )

    def enable(self) -> None:
        self.file_menu.entryconfig("New", state=tk.NORMAL)
        self.file_menu.entryconfig("Open", state=tk.NORMAL)
        self.file_menu.entryconfig("Save", state=tk.NORMAL)
        self.file_menu.entryconfig("Save as", state=tk.NORMAL)
        self.file_menu.entryconfig("Export", state=tk.NORMAL)
        self.file_menu.entryconfig("Close", state=tk.NORMAL)
        self.file_menu.entryconfig("Settings", state=tk.NORMAL)
        self.sim_menu.entryconfig("Run", state=tk.NORMAL)
        self.sim_menu.entryconfig("Run All", state=tk.NORMAL)
        self.sim_menu.entryconfig("Draw (NGSolve)", state=tk.NORMAL)
        self.help_menu.entryconfig("Documentation", state=tk.NORMAL)
        self.help_menu.entryconfig("Info", state=tk.NORMAL)

    def disable(self):
        self.file_menu.entryconfig("New", state=tk.DISABLED)
        self.file_menu.entryconfig("Open", state=tk.DISABLED)
        self.file_menu.entryconfig("Save", state=tk.DISABLED)
        self.file_menu.entryconfig("Save as", state=tk.DISABLED)
        self.file_menu.entryconfig("Export", state=tk.DISABLED)
        self.file_menu.entryconfig("Settings", state=tk.DISABLED)
        self.file_menu.entryconfig("Close", state=tk.DISABLED)
        self.sim_menu.entryconfig("Run", state=tk.DISABLED)
        self.sim_menu.entryconfig("Run All", state=tk.DISABLED)
        self.sim_menu.entryconfig("Draw (NGSolve)", state=tk.DISABLED)
        self.help_menu.entryconfig("Documentation", state=tk.DISABLED)
        self.help_menu.entryconfig("Info", state=tk.DISABLED)
