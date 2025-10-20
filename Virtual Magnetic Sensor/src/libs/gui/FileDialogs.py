from pathlib import Path
from tkinter.messagebox import showinfo, showerror
from tkinter import filedialog as fd
from typing import List

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler

from libs.gui.GUIHandler import GUIHandler


class FileDialogs:

    @staticmethod
    def open(data_stack: List[DataHandler], config_handler: ConfigHandler, gui_handler: GUIHandler,
             filename: str = "", init_flag: int = 0) -> None:

        filetypes = [('HDF5 Files', '*.hdf5 *.hdf *.h4 *.hdf4 *.he2 *.h5 *.he'),
                     ('INI Files', '*.ini *.INI'),
                     ('PY Files', '*.py'),
                     ('All Files', '*.*')]

        if data_stack:
            idx = gui_handler.selected_tab()
        else:
            if not filename:
                gui_handler.add_tab(DataHandler.template(), data_stack, config_handler)
            else:
                gui_handler.add_tab(DataHandler.template(), data_stack, config_handler, Path(filename).stem)
            idx = 0

        if not filename:
            filename = fd.askopenfilename(title='Select a File',
                                          initialdir=data_stack[idx].filepath.parent.as_posix(),
                                          filetypes=filetypes)

        if filename:
            filepath = Path(filename)
            data_stack[idx].filepath = Path(filepath.parent.as_posix(), filepath.stem)

            if filepath.suffix.lower() in ['.hdf5', '.hdf', '.h4', '.hdf4', '.he2', '.h5', '.he']:
                data_stack[idx].load_h5(filepath)
                gui_handler.tabs[idx].refresh_frames(data_stack[idx], config_handler, gui_handler)
            elif filepath.suffix.lower() in ['.ini']:
                data_stack[idx].load_ini(filepath)
                gui_handler.tabs[idx].refresh_frames(data_stack[idx], config_handler, gui_handler)
            elif filepath.suffix.lower() in ['.py']:
                new_stack: List[DataHandler] = data_stack[idx].load_py(filepath)
                gui_handler.close_tab(data_stack, idx)
                for num, data_handler in enumerate(new_stack):
                    gui_handler.add_tab(data_handler, data_stack, config_handler, filepath.stem+str(num).zfill(2))
            else:
                showerror(title="Error", message="Filetype not supported.")

            if init_flag:
                data_stack[idx].filepath = Path(config_handler.get_save_files_path().as_posix(), Path(filename).stem)

    @staticmethod
    def save_as(data_stack: List[DataHandler], gui_handler: GUIHandler) -> None:

        filetypes = [('HDF5 Files', '*.hdf5 *.hdf *.h4 *.hdf4 *.he2 *.h5 *.he'),
                     ('All Files', '*.*')]

        if data_stack:
            idx = gui_handler.selected_tab()

            filename: str = fd.asksaveasfilename(
                title='Select a File', initialdir=data_stack[idx].filepath.parent.as_posix(),
                initialfile=Path(data_stack[idx].filepath.stem).with_suffix(".hdf5"), filetypes=filetypes)

            if filename:
                filepath = Path(filename)
                data_stack[idx].filepath = Path(filepath.parent.as_posix(), filepath.stem)
                data_stack[idx].update_objects(gui_handler.tabs[idx].frames)

                success = data_stack[idx].save_h5(data_stack[idx].filepath.parent)

                if success:
                    showinfo(title="Info", message="File successfully saved.")
                else:
                    showerror(title="Error", message="File could not be saved.")
        else:
            showerror(title="Error", message="No data to save.")

    @staticmethod
    def export_ini(data_stack: List[DataHandler], gui_handler: GUIHandler) -> None:

        filetypes = [('INI Files', '*.ini *.INI'),
                     ('All Files', '*.*')]

        if data_stack:
            idx = gui_handler.selected_tab()

            filename: str = fd.asksaveasfilename(
                title='Select a File', initialdir=data_stack[idx].filepath.parent.as_posix(),
                initialfile=Path(data_stack[idx].filepath.stem).with_suffix(".ini"), filetypes=filetypes)

            if filename:
                filepath = Path(filename)
                data_stack[idx].filepath = Path(filepath.parent.as_posix(), filepath.stem)
                data_stack[idx].update_objects(gui_handler.tabs[idx].frames)

                success = data_stack[idx].save_ini()

                if success:
                    showinfo(title="Info", message="File successfully saved.")
                else:
                    showerror(title="Error", message="File could not be saved.")
        else:
            showerror(title="Error", message="No data to export.")

    @staticmethod
    def export_py(data_stack: List[DataHandler], gui_handler: GUIHandler) -> None:
        showinfo(title='Error', message='Not implemented yet.')
        """filetypes = [('PY Files', '*.py'),
                     ('All Files', '*.*')]

        idx = gui_handler.notebook.index(gui_handler.notebook.select())

        filename: str = fd.asksaveasfilename(
            title='Select a File', initialdir=data_stack[idx].filepath.parent.as_posix(),
            initialfile=Path(data_stack[idx].filepath.stem).with_suffix(".py"), filetypes=filetypes)

        if filename:
            filepath = Path(filename)
            data_stack[idx].filepath = Path(filepath.parent.as_posix(), filepath.stem)
            data_stack[idx].update_objects(gui_handler.tabs[idx].frames)

            if filepath.suffix.lower() in ['.py']:
                success = data_stack[idx].save_py(filepath)
            else:
                showerror(title="Error", message="Filetype not supported.")
                return

            if success:
                showinfo(title="Info", message="File successfully saved.")
            else:
                showerror(title="Error", message="File could not be saved.")"""

    @staticmethod
    def save(data_stack: List[DataHandler], gui_handler: GUIHandler) -> None:

        if data_stack:
            idx = gui_handler.selected_tab()

            if data_stack[idx].filepath:

                data_stack[idx].update_objects(gui_handler.tabs[idx].frames)

                success = data_stack[idx].save_h5(data_stack[idx].filepath.parent)

                if success:
                    showinfo(title="Info", message="File successfully saved.")
                else:
                    showerror(title="Error", message="File could not be saved.")

            else:
                showinfo(title='Error', message='No filename specified.')
        else:
            showerror(title="Error", message="No data to save.")
