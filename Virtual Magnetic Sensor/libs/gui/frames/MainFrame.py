import tkinter as tk
from pathlib import Path
from typing import List

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler

from libs.gui.frames.TabFrame import TabFrame

from libs.simulation.SimulationHandler import SimulationHandler

from libs.gui.FileDialogs import FileDialogs
from libs.gui.GUIHandler import GUIHandler
from libs.gui.GUIElements import GUIElements as Gui
from libs.gui.frames.SettingsFrame import SettingsFrame
from libs.gui.bars.MenuBar import MenuBar
from libs.gui.bars.StatusBar import StatusBar


class MainFrame(tk.Tk):
    """Generates the main user interface and implements objects for data and gui management."""

    data_stack: List[DataHandler]
    config_handler: ConfigHandler
    gui_handler: GUIHandler

    def __init__(self,
                 multiprocessing_tasks) -> None:
        self.multiprocessing_tasks = multiprocessing_tasks

        screen_width, screen_height = Gui.screen_size()

        self.data_stack: List[DataHandler] = list()
        self.data_stack.append(DataHandler().template())

        self.config_handler = ConfigHandler()

        super().__init__()
        self.title("Virtual Magnetic Sensor")
        Gui.init_style(self, self.config_handler.config)
        self.gui_handler = GUIHandler(self, self.bindings_enable, self.bindings_disable)
        self.protocol("WM_DELETE_WINDOW", self.gui_handler.exit)

        self.gui_handler.bars.append(MenuBar(self, self.data_stack, self.config_handler, self.gui_handler,
                                             self.multiprocessing_tasks))
        self.gui_handler.bars.append(StatusBar(self))

        self.config_handler.load_setup(self.data_stack)

        for num, data_handler in enumerate(self.data_stack):
            self.gui_handler.tabs.append(TabFrame(Path(self.config_handler.config['GENERAL']['setup']).stem+str(num),
                                                  data_handler, self.config_handler, self.gui_handler))

        Gui.auto_frame_size(self, self.gui_handler.tabs[0].inner_frame, self.config_handler.config,
                            screen_width, screen_height)

        for num, tab in enumerate(self.gui_handler.tabs):
            tab.refresh_frames(self.data_stack[num], self.config_handler, self.gui_handler)

        self.bindings_enable()

        self.mainloop()

    def bindings_enable(self):
        self.bind_all("<Alt-Insert>", lambda event: self.gui_handler.add_tab(DataHandler.template(),
                                                                             self.data_stack, self.config_handler))
        self.bind_all("<Control-s>", lambda event: FileDialogs.save(self.data_stack, self.gui_handler))
        self.bind_all("<Control-x>", lambda event: self.gui_handler.close_tab(self.data_stack))
        self.bind_all("<Control-Alt-s>", lambda event: self.settings_menu())
        self.bind_all("<Control-q>", lambda event: self.gui_handler.exit())
        self.bind_all("<F8>", lambda event: SimulationHandler.draw(
            self.multiprocessing_tasks, self.data_stack, self.gui_handler, self.gui_handler.selected_tab()))
        self.bind_all("<F9>", lambda event: SimulationHandler.run(
            self.multiprocessing_tasks, self.data_stack, self.config_handler, self.gui_handler,
            self.gui_handler.selected_tab()))
        self.bind_all("<F10>", lambda event: SimulationHandler.run(
            self.multiprocessing_tasks, self.data_stack, self.config_handler, self.gui_handler))

    def bindings_disable(self):
        self.unbind_all("<Alt-Insert>")
        self.unbind_all("<Control-s>")
        self.unbind_all("<Control-x>")
        self.unbind_all("<Control-Alt-s>")
        self.unbind_all("<F8>")
        self.unbind_all("<F9>")
        self.unbind_all("<F10>")

    def settings_menu(self):
        SettingsFrame(self.config_handler)
        self.config_handler.load_config()