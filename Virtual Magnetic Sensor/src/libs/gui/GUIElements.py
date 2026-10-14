import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from pathlib import Path
import numpy as np
from typing import Any, Dict, Union, List, Tuple, Literal

from libs.gui.ScrolledFrame import ScrolledFrame

from importlib.resources import files, as_file


class GUIElements:
    """description of class"""

    @staticmethod
    def label_frame(master: Union[tk.Tk, tk.Frame, ttk.Labelframe, tk.Toplevel], config: Dict[str, Dict[str, Any]],
                    col: int, row: int, column_span: int, row_span: int, label: str) -> ttk.LabelFrame:
        frame = ttk.LabelFrame(master, text=label)
        frame.grid(column=col, row=row, columnspan=column_span, rowspan=row_span, sticky='n,w,e,s',
                   padx=config['GUI']['padding'], pady=(0, config['GUI']['padding']))
        master.rowconfigure(row, weight=1)
        master.columnconfigure(col, weight=1)

        return frame

    @staticmethod
    def info_label(master: ttk.LabelFrame, config: Dict[str, Dict[str, Any]], col: int, row: int,
                   info: str) -> ttk.Label:
        info_label = ttk.Label(master, text=info, relief="raised")
        info_label.grid(column=col, row=row, sticky='n,s,w,e', padx=config['GUI']['v_spacing'],
                        pady=config['GUI']['h_spacing'])
        master.rowconfigure(row, minsize=30)
        master.columnconfigure(col, weight=1)

        return info_label

    @staticmethod
    def input_line(master: ttk.LabelFrame, config: Dict[str, Dict[str, Any]], col: int, row: int, label: str,
                   unit: str = "", col_shift: int = 0,
                   justify: Literal["left", "center", "right"] = "right") -> ttk.Entry:
        label = ttk.Label(master, text=label)
        label.grid(column=col, row=row, sticky=tk.W, padx=config['GUI']['v_spacing'])
        entry = ttk.Entry(master, width=config['GUI']['entry_width'], justify=justify)
        entry.grid(column=col + col_shift + 1, row=row, sticky='n,s,w,e', pady=config['GUI']['h_spacing'])
        unit = ttk.Label(master, text=unit)
        unit.grid(column=col + col_shift + 2, row=row, sticky='w', padx=(2, config['GUI']['v_spacing']))
        master.rowconfigure(row, weight=1)
        master.columnconfigure(col, weight=1)

        return entry

    @staticmethod
    def settings_line(master: ttk.Frame, config: Dict[str, Dict[str, Any]], row: int, label: str,
                      value: str) -> ttk.Entry:
        label = ttk.Label(master, text=label)
        label.grid(column=0, row=row, sticky=tk.W, padx=config['GUI']['v_spacing'])
        entry = ttk.Entry(master, width=30, justify='left')
        entry.insert(0, value)
        entry.grid(column=1, row=row, sticky='n,s,w,e', pady=config['GUI']['h_spacing'])

        master.rowconfigure(row, weight=1)
        master.columnconfigure(0, weight=1)

        return entry

    @staticmethod
    def settings_path_line(master: ttk.Frame, config: Dict[str, Dict[str, Any]], row: int, label: str,
                           value: str, directory: bool = False,
                           filetypes: Union[List[Tuple[str, str]], None] = None) -> tk.StringVar:
        """Settings line with an entry and a button opening a file or directory dialog."""

        var = tk.StringVar(master, value=str(value))
        label = ttk.Label(master, text=label)
        label.grid(column=0, row=row, sticky=tk.W, padx=config['GUI']['v_spacing'])
        entry = ttk.Entry(master, textvariable=var, width=40, justify='left')
        entry.grid(column=1, row=row, sticky='n,s,w,e', pady=config['GUI']['h_spacing'])

        def browse() -> None:
            current = Path(var.get())
            initial_dir = current if current.is_dir() else current.parent
            if directory:
                path = fd.askdirectory(parent=master, title='Select a Directory', initialdir=initial_dir)
            else:
                path = fd.askopenfilename(parent=master, title='Select a File', initialdir=initial_dir,
                                          filetypes=filetypes or [('All Files', '*.*')])
            if path:
                var.set(path)

        button = ttk.Button(master, text="...", width=3, command=browse)
        button.grid(column=2, row=row, sticky='w', padx=(2, config['GUI']['v_spacing']))

        master.rowconfigure(row, weight=1)
        master.columnconfigure(1, weight=1)

        return var

    @staticmethod
    def settings_switch_line(master: ttk.Frame, config: Dict[str, Dict[str, Any]], row: int, label: str,
                             value: int) -> tk.IntVar:
        """Settings line with a switch returning 1 (on) or 0 (off)."""

        var = tk.IntVar(master, value=1 if int(value) else 0)
        label = ttk.Label(master, text=label)
        label.grid(column=0, row=row, sticky=tk.W, padx=config['GUI']['v_spacing'])
        state_label = ttk.Label(master, text="")
        switch = ttk.Checkbutton(master, variable=var, onvalue=1, offvalue=0,
                                 command=lambda: state_label.config(text="On" if var.get() else "Off"))
        switch.grid(column=1, row=row, sticky='w', pady=config['GUI']['h_spacing'])
        state_label.config(text="On" if var.get() else "Off")
        state_label.grid(column=2, row=row, sticky='w', padx=(2, config['GUI']['v_spacing']))

        master.rowconfigure(row, weight=1)

        return var

    @staticmethod
    def settings_slider_line(master: ttk.Frame, config: Dict[str, Dict[str, Any]], row: int, label: str,
                             value: float, from_: float, to: float, resolution: float = 1,
                             unit: str = "") -> tk.DoubleVar:
        """Settings line with a slider snapping to the given resolution."""

        var = tk.DoubleVar(master, value=min(max(float(value), from_), to))
        label = ttk.Label(master, text=label)
        label.grid(column=0, row=row, sticky=tk.W, padx=config['GUI']['v_spacing'])

        def text() -> str:
            val = var.get()
            return (str(int(val)) if float(resolution).is_integer() else str(round(val, 2))) + " " + unit

        value_label = ttk.Label(master, text=text(), width=10)

        def snap(val: str) -> None:
            var.set(from_ + round((float(val) - from_) / resolution) * resolution)
            value_label.config(text=text())

        scale = ttk.Scale(master, from_=from_, to=to, orient=tk.HORIZONTAL, variable=var, command=snap)
        scale.grid(column=1, row=row, sticky='n,s,w,e', pady=config['GUI']['h_spacing'])
        value_label.grid(column=2, row=row, sticky='w', padx=(2, config['GUI']['v_spacing']))

        master.rowconfigure(row, weight=1)
        master.columnconfigure(1, weight=1)

        return var

    @staticmethod
    def settings_combobox_line(master: ttk.Frame, config: Dict[str, Dict[str, Any]], row: int, label: str,
                               value: str, values: List[str]) -> tk.StringVar:
        """Settings line with a read-only dropdown."""

        var = tk.StringVar(master, value=value if value in values else values[0])
        label = ttk.Label(master, text=label)
        label.grid(column=0, row=row, sticky=tk.W, padx=config['GUI']['v_spacing'])
        combobox = ttk.Combobox(master, textvariable=var, values=values, state='readonly')
        combobox.grid(column=1, row=row, sticky='n,s,w,e', pady=config['GUI']['h_spacing'])

        master.rowconfigure(row, weight=1)

        return var

    @staticmethod
    def vector2_input(master: ttk.LabelFrame, config: Dict[str, Dict[str, Any]], col: int, row: int, width: int,
                      label: str, unit: str = "") -> list:
        label = ttk.Label(master, text=label)
        label.grid(column=col, row=row, sticky='w', padx=config['GUI']['v_spacing'])
        x_entry = ttk.Entry(master, width=width, justify='right')
        x_entry.grid(column=col + 1, row=row, sticky='n,s,w,e', padx=1, pady=config['GUI']['h_spacing'])
        y_entry = ttk.Entry(master, width=width, justify='right')
        y_entry.grid(column=col + 2, row=row, sticky='n,s,w,e', padx=1, pady=config['GUI']['h_spacing'])
        unit = ttk.Label(master, text=unit)
        unit.grid(column=col + 3, row=row, sticky='w', padx=(2, config['GUI']['v_spacing']))

        return [x_entry, y_entry]

    @staticmethod
    def vector3_input(master: ttk.LabelFrame, config: Dict[str, Dict[str, Any]], col: int, column_span: int, row: int,
                      head_label: str, entry_labels: list) -> list:
        frame = GUIElements.label_frame(master, config, col, row, column_span, 1, head_label)
        frame.grid(column=col, columnspan=column_span, row=row, sticky='n,w,s,e')
        for i in range(0, 6):
            frame.columnconfigure(i, weight=1, minsize=config['GUI']['entry_width'])
        frame.rowconfigure(1, weight=0, minsize=7)

        x_label = ttk.Label(frame, text=entry_labels[0])
        x_label.grid(column=0, row=0)
        x_entry = ttk.Entry(frame, width=5, justify='center')
        x_entry.grid(column=1, row=0)
        y_label = ttk.Label(frame, text=entry_labels[1])
        y_label.grid(column=2, row=0)
        y_entry = ttk.Entry(frame, width=5, justify='center')
        y_entry.grid(column=3, row=0)
        z_label = ttk.Label(frame, text=entry_labels[2])
        z_label.grid(column=4, row=0)
        z_entry = ttk.Entry(frame, width=5, justify='center')
        z_entry.grid(column=5, row=0)

        return [x_entry, y_entry, z_entry]

    @staticmethod
    def vector6_input(master: ttk.LabelFrame, config: Dict[str, Dict[str, Any]], col: int, column_span: int, row: int,
                      head_label: str) -> list:
        frame = GUIElements.label_frame(master, config, col, row, column_span, 1, head_label)
        frame.grid(column=col, columnspan=column_span, row=row, sticky='n,w,s,e')
        for i in range(1, 4):
            frame.columnconfigure(i, weight=1)
        frame.columnconfigure(0, weight=0, minsize=7)
        frame.columnconfigure(4, weight=0, minsize=7)
        frame.rowconfigure(3, weight=0, minsize=7)

        master.columnconfigure(col, weight=1)
        master.rowconfigure(row, weight=1)

        x_label = ttk.Label(master=frame, text='x:')
        x_label.grid(column=1, row=0, sticky='w', padx=1, pady=1)

        x0_entry = ttk.Entry(master=frame, justify='right')
        x0_entry.grid(column=2, row=0, sticky='n,w,s,e', padx=1, pady=1)

        x1_entry = ttk.Entry(master=frame, justify='right')
        x1_entry.grid(column=3, row=0, sticky='n,w,s,e', padx=1, pady=1)

        y_label = ttk.Label(master=frame, text='y:')
        y_label.grid(column=1, row=1, sticky='w', padx=1, pady=1)

        y0_entry = ttk.Entry(master=frame, justify='right')
        y0_entry.grid(column=2, row=1, sticky='n,w,s,e', padx=1, pady=1)

        y1_entry = ttk.Entry(master=frame, justify='right')
        y1_entry.grid(column=3, row=1, sticky='n,w,s,e', padx=1, pady=1)

        z_label = ttk.Label(master=frame, text='z:')
        z_label.grid(column=1, row=2, sticky='w', padx=1, pady=1)

        z0_entry = ttk.Entry(master=frame, justify='right')
        z0_entry.grid(column=2, row=2, sticky='n,w,s,e', padx=1, pady=1)

        z1_entry = ttk.Entry(master=frame, justify='right')
        z1_entry.grid(column=3, row=2, sticky='n,w,s,e', padx=1, pady=1)

        return [[x0_entry, y0_entry, z0_entry], [x1_entry, y1_entry, z1_entry]]

    @staticmethod
    def vector8_input(master: ttk.LabelFrame, config: Dict[str, Dict[str, Any]], col: int, column_span: int, row: int,
                      head_label: str, entry_labels: list) -> list:
        frame = GUIElements.label_frame(master, config, col, row, column_span, 1, head_label)
        frame.grid(column=col, columnspan=column_span, row=row, sticky='n,w,s,e')
        frame.columnconfigure(0, weight=0, minsize=7)
        frame.columnconfigure(5, weight=0, minsize=7)
        frame.rowconfigure(4, weight=0, minsize=7)
        for i in range(1, 5):
            frame.columnconfigure(i, weight=1)

        x1_label = ttk.Label(frame, text=entry_labels[0])
        x1_label.grid(column=1, row=0)

        x1_entry = ttk.Entry(frame, width=9, justify='center')
        x1_entry.grid(column=1, row=1, sticky='n,w,s,e', padx=1)

        x2_label = ttk.Label(frame, text=entry_labels[1])
        x2_label.grid(column=2, row=0)

        x2_entry = ttk.Entry(frame, width=9, justify='center')
        x2_entry.grid(column=2, row=1, sticky='n,w,s,e', padx=1)

        x3_label = ttk.Label(frame, text=entry_labels[2])
        x3_label.grid(column=3, row=0)

        x3_entry = ttk.Entry(frame, width=9, justify='center')
        x3_entry.grid(column=3, row=1, sticky='n,w,s,e', padx=1)

        x4_label = ttk.Label(frame, text=entry_labels[3])
        x4_label.grid(column=4, row=0)

        x4_entry = ttk.Entry(frame, width=9, justify='center')
        x4_entry.grid(column=4, row=1, sticky='n,w,s,e', padx=1)

        x5_label = ttk.Label(frame, text=entry_labels[4])
        x5_label.grid(column=1, row=2)

        x5_entry = ttk.Entry(frame, width=9, justify='center')
        x5_entry.grid(column=1, row=3, sticky='n,w,s,e', padx=1)

        x6_label = ttk.Label(frame, text=entry_labels[5])
        x6_label.grid(column=2, row=2)

        x6_entry = ttk.Entry(frame, width=9, justify='center')
        x6_entry.grid(column=2, row=3, sticky='n,w,s,e', padx=1)

        x7_label = ttk.Label(frame, text=entry_labels[6])
        x7_label.grid(column=3, row=2)

        x7_entry = ttk.Entry(frame, width=9, justify='center')
        x7_entry.grid(column=3, row=3, sticky='n,w,s,e', padx=1)

        x8_label = ttk.Label(frame, text=entry_labels[7])
        x8_label.grid(column=4, row=2)

        x8_entry = ttk.Entry(frame, width=9, justify='center')
        x8_entry.grid(column=4, row=3, sticky='n,w,s,e', padx=1)

        return [x1_entry, x2_entry, x3_entry, x4_entry, x5_entry, x6_entry, x7_entry, x8_entry]

    @staticmethod
    def dropdown_menu(master: ttk.LabelFrame, config: Dict[str, Dict[str, Any]], col: int, row: int,
                      architecture_list: list) -> tk.StringVar:
        variable = tk.StringVar(master)
        variable.set(architecture_list[0])
        label = ttk.Label(master, text='Sensor Presets:')
        label.grid(column=col, row=row, sticky='w', padx=config['GUI']['padding'])
        sensor_menu = ttk.OptionMenu(master, variable, *architecture_list)
        sensor_menu.grid(column=col + 1, row=row, sticky='n,w,s')

        return variable

    @staticmethod
    def check_box(master: Union[ttk.LabelFrame, ttk.Frame], config: Dict[str, Dict[str, Any]], col: int, row: int,
                  label: str) -> tk.BooleanVar:
        var = tk.BooleanVar()
        checkbutton = ttk.Checkbutton(master=master, text=label, variable=var, onvalue=1, offvalue=0)
        checkbutton.grid(column=col, row=row, sticky='n,w,s,e', padx=config['GUI']['v_spacing'],
                         pady=config['GUI']['h_spacing'])

        return var

    @staticmethod
    def extract(entries: Dict[str, Union[ttk.Entry, List[ttk.Entry], tk.IntVar, tk.BooleanVar]]) -> Dict[str, Any]:
        entries_dict: Dict[str, Union[float, np.ndarray]] = dict()
        for key, value in entries.items():
            if isinstance(value, list):
                if isinstance(value[0], list):
                    entries_dict[key] = np.array([[float(val.get()) for val in value[0]],
                                                  [float(val.get()) for val in value[1]]])
                else:
                    entries_dict[key] = np.array([float(val.get()) for val in value])
            elif isinstance(value, tk.IntVar) or isinstance(value, tk.BooleanVar):
                entries_dict[key] = value.get()
            else:
                val: Any = value.get()
                if isinstance(val, str):
                    if val.isdigit():
                        entries_dict[key] = int(val)
                    else:
                        entries_dict[key] = float(val)
                else:
                    entries_dict[key] = val

        return entries_dict

    @staticmethod
    def insert(entries: Dict[str, Union[ttk.Entry, List[Union[ttk.Entry, List[ttk.Entry]]], tk.IntVar,
                                        tk.BooleanVar]], sim_object: Any) -> None:
        for key, entry in entries.items():
            value = getattr(sim_object, key)
            if isinstance(entry, list):
                for i, item in enumerate(entry):
                    if isinstance(item, list):
                        for j, sub_item in enumerate(item):
                            sub_item.delete(0, 'end')
                            sub_item.insert(0, value[i][j])
                    else:
                        item.delete(0, 'end')
                        item.insert(0, value[i])
            elif isinstance(entry, tk.BooleanVar):
                entry.set(bool(value))
            elif isinstance(entry, tk.IntVar):
                entry.set(value)
            else:
                entry.delete(0, 'end')
                entry.insert(0, value)

    @staticmethod
    def button_frame(master: ttk.LabelFrame, config: Dict[str, Dict[str, Any]]) -> ttk.Frame:
        button_frame = ttk.Frame(master=master)
        button_frame.pack(side="top", fill="both", expand=True, padx=(3, 3 + int(config['GUI']['arrow_size'])), pady=2)

        return button_frame

    @staticmethod
    def init_style(master: tk.Tk, config: Dict[str, Dict[str, Any]]) -> None:
        base_res = files("libs") / "resources" / "themes" / "awthemes-10.4.0"
        with as_file(base_res) as base_dir:
            master.tk.call("set", "base_theme_dir", str(base_dir))
            master.tk.eval(r"""
                        set base_theme_dir [file normalize $base_theme_dir]
                        package ifneeded awthemes 10.4.0 \
                            [list source [file join $base_theme_dir awthemes.tcl]]
                        package ifneeded awlight 7.10 \
                            [list source [file join $base_theme_dir awlight.tcl]]
                        package ifneeded awdark 7.12 \
                            [list source [file join $base_theme_dir awdark.tcl]]
                    """)
            master.tk.call('package', 'require', 'awdark')
            master.tk.call('package', 'require', 'awlight')
            style = ttk.Style(master)

        if config['GUI']['theme'] in style.theme_names():
            style.theme_use(config['GUI']['theme'])
        else:
            style.theme_use('vista')

        style.configure('TFrame',
                        bg=style.lookup('TFrame', 'background'),
                        highlightbackground=style.lookup('TFrame', 'background'),
                        padding=(config['GUI']['padding']),
                        relief=tk.FLAT)
        style.configure('TLabelFrame',
                        bg=style.lookup('TFrame', 'background'),
                        highlightbackground=style.lookup('TFrame', 'background'),
                        padding=(config['GUI']['padding']),
                        relief=tk.FLAT)
        style.configure('Vertical.TScrollbar', arrowsize=config['GUI']['arrow_size'])
        style.configure('Horizontal.TScrollbar', arrowsize=config['GUI']['arrow_size'])
        style.configure('TRadiobutton', padding=(config['GUI']['padding']))

    @staticmethod
    def scrollable_frame(master: ttk.LabelFrame, config: Dict[str, Dict[str, Any]]) -> ttk.Frame:

        scrolled_frame = ScrolledFrame(master=master,
                                       scrollbars='both',
                                       use_ttk=True,
                                       relief=tk.FLAT,
                                       background=ttk.Style().lookup('TFrame', 'background'),
                                       width=config['GUI']['column_width'],
                                       height=config['GUI']['height'])
        scrolled_frame.pack(side="top", expand=1, fill="both")

        inner_frame = scrolled_frame.display_widget(ttk.Frame)

        inner_frame.configure(padding=(config['GUI']['padding'],
                                       config['GUI']['padding'],
                                       int(config['GUI']['arrow_size']) + int(config['GUI']['padding']),
                                       config['GUI']['padding']))

        scrolled_frame.canvas.create_window((0, 0),
                                            window=inner_frame,
                                            anchor="nw",
                                            width=int(config['GUI']['column_width']) + int(config['GUI']['arrow_size']))

        return inner_frame

    @staticmethod
    def screen_size() -> Tuple[int, int]:
        window = tk.Tk()
        window.attributes("-alpha", 0)
        try:
            window.state("zoomed")
        except tk.TclError:
            window.state("normal")
        window.update()
        usable_width = window.winfo_width()
        usable_height = window.winfo_height()
        window.destroy()

        return usable_width, usable_height

    @staticmethod
    def auto_frame_size(root: tk.Tk, inner_frame: ttk.Frame, config: Dict[str, Dict[str, Any]],
                        screen_width: int, screen_height: int):
        """Function determines the size of the window by comparing ideal size of the root frame and
        the size of the screen"""

        inner_frame.update()
        window_w = inner_frame.winfo_width() + int(config['GUI']['arrow_size'])
        window_h = inner_frame.winfo_height() + int(config['GUI']['arrow_size']) + 20

        if screen_width >= window_w and screen_height >= window_h:
            root.geometry(f"{window_w}x{window_h}+0+0")
        else:
            try:
                root.state("zoomed")
            except tk.TclError:
                root.state("normal")
