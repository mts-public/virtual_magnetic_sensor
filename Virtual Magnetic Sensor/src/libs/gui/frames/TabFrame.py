import tkinter as tk
from tkinter import ttk
from typing import List

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler

from libs.gui.GUIHandler import GUIHandler
from libs.gui.ScrolledFrame import ScrolledFrame
from libs.gui.frames.MagnetsFrame import MagnetsFrame
from libs.gui.frames.ComponentsFrame import ComponentsFrame
from libs.gui.frames.SensorsFrame import SensorsFrame
from libs.gui.frames.SimParamsFrame import SimParamsFrame
from libs.gui.frames.ProgressFrame import ProgressFrame


class TabFrame(ttk.Frame):
    """

    """

    def __init__(self,
                 project_id: str,
                 data_handler: DataHandler,
                 config_handler: ConfigHandler,
                 gui_handler: GUIHandler) -> None:
        super().__init__(gui_handler.notebook)
        gui_handler.notebook.add(self, text=project_id)

        self.frames: List[any] = list()

        scrolled_frame = ScrolledFrame(self, scrollbars='both', use_ttk=True, relief=tk.FLAT,
                                       background=ttk.Style().lookup('TFrame', 'background'))
        scrolled_frame.pack(side="top", expand=1, fill="both")
        self.inner_frame = scrolled_frame.display_widget(ttk.Frame)

        left_box = ttk.Frame(self.inner_frame)
        left_box.pack(side='left', anchor='nw', padx=config_handler.config['GUI']['padding'])

        self.frames.append(SimParamsFrame(master=left_box, side='top',
                                          data_handler=data_handler,
                                          config_handler=config_handler,
                                          gui_handler=gui_handler))
        self.frames.append(ProgressFrame(master=left_box, side='top',
                                         data_handler=data_handler,
                                         config_handler=config_handler,
                                         gui_handler=gui_handler))
        self.frames.append(MagnetsFrame(master=self.inner_frame, side='left',
                                        data_handler=data_handler,
                                        config_handler=config_handler,
                                        gui_handler=gui_handler))
        self.frames.append(ComponentsFrame(master=self.inner_frame, side='left',
                                           data_handler=data_handler,
                                           config_handler=config_handler,
                                           gui_handler=gui_handler))
        self.frames.append(SensorsFrame(master=self.inner_frame, side='left',
                                        data_handler=data_handler,
                                        config_handler=config_handler,
                                        gui_handler=gui_handler))

    def refresh_frames(self, data_handler: DataHandler, config_handler: ConfigHandler, gui_handler: GUIHandler):
        for frame in self.frames:
            if hasattr(frame, "refresh"):
                frame.refresh(data_handler, config_handler, gui_handler)

    def progress_frame(self):
        for frame in self.frames:
            if type(frame).__name__ == "ProgressFrame":
                return frame

        return None
