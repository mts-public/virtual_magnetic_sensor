import _tkinter
from tkinter import simpledialog, messagebox, NORMAL, DISABLED, Tk
from tkinter import ttk
from pathlib import Path
from typing import List, Callable, Union

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler


class GUIHandler:
    """description of class"""

    def __init__(self, root_frame: Tk, bindings_enable: Callable, bindings_disable: Callable) -> None:
        """Constructor method."""

        self.root_frame = root_frame
        self.notebook = ttk.Notebook(self.root_frame)
        self.notebook.pack(fill='both', expand=True)
        self.buttons: List[ttk.Button] = list()
        self.bars: List[any] = list()
        self.tabs: List[any] = list()

        self.bindings_enable = bindings_enable
        self.bindings_disable = bindings_disable

    def add_tab(self, data_handler: DataHandler, data_stack: List[DataHandler], config_handler: ConfigHandler,
                project_id: str = "") -> int:
        if not project_id:
            project_id: str = simpledialog.askstring("Project Name", "Enter Project Name\t\t")

        if project_id:
            if project_id.lower() in [self.notebook.tab(idx, option="text").lower() for idx in self.notebook.tabs()]:
                messagebox.showerror(title="Error", message="Project ID already in use.")
                return 0
            else:
                data_handler.filepath = Path(config_handler.config['GENERAL']['measurement_path'], project_id)
                data_stack.append(data_handler)

                from libs.gui.frames.TabFrame import TabFrame
                self.tabs.append(TabFrame(project_id, data_stack[-1], config_handler, self))
                self.tabs[-1].refresh_frames(data_stack[-1], config_handler, self)
                return 1

    def close_tab(self, data_stack: List[DataHandler], idx: Union[int, None] = None):
        if not idx:
            if data_stack:
                idx = self.selected_tab()
            else:
                return

        if idx < len(data_stack):
            self.notebook.forget(idx)
            data_stack.pop(idx)
            self.tabs.pop(idx)

    def selected_tab(self) -> int:
        try:
            return self.notebook.index(self.notebook.select())
        except _tkinter.TclError:
            return 0

    def status_bar(self):
        for bar in self.bars:
            if type(bar).__name__ == "StatusBar":
                return bar

    def menu_bar(self):
        for bar in self.bars:
            if type(bar).__name__ == "MenuBar":
                return bar

    def enable_gui_operation(self) -> None:
        self.bindings_enable()
        for bar in self.bars:
            if hasattr(bar, 'enable'):
                bar.enable()
        for button in self.buttons:
            button['state'] = NORMAL

    def disable_gui_operation(self) -> None:
        self.bindings_disable()
        for bar in self.bars:
            if hasattr(bar, 'disable'):
                bar.disable()
        for button in self.buttons:
            button['state'] = DISABLED

    def exit(self):
        import multiprocessing
        children = multiprocessing.active_children()
        for child in children:
            child.terminate()
        self.root_frame.quit()
