import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from typing import Callable

from libs.gui.frames.ObjectFrame import ObjectFrame
from libs.gui.GUIElements import GUIElements as Gui
from libs.gui.GUIHandler import GUIHandler

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler


class CuboidMagnetFrame(ObjectFrame):
    """description of class"""

    def __init__(self,
                 master: ttk.Frame,
                 data_handler: DataHandler,
                 config_handler: ConfigHandler,
                 gui_handler: GUIHandler,
                 remove_magnet: Callable) -> None:
        super().__init__(master=master, title="Cuboid", data_handler=data_handler, config_handler=config_handler,
                         gui_handler=gui_handler, remove=remove_magnet)

        self.entries['pos'] = Gui.vector3_input(master=self, config=config_handler.config,
                                                head_label="Center x in mm",
                                                col=0, row=0, column_span=3, entry_labels=["x:", "y:", "z:"])
        self.entries['dim'] = Gui.vector3_input(master=self, config=config_handler.config,
                                                head_label="Size b in mm", col=0, row=1, column_span=3,
                                                entry_labels=["x:", "y:", "z:"])
        self.entries['rot'] = Gui.vector3_input(master=self, config=config_handler.config,
                                                head_label="Rotation θ in °", col=0, row=2, column_span=3,
                                                entry_labels=["x:", "y:", "z:"])
        self.entries['direction'] = Gui.vector3_input(master=self, config=config_handler.config,
                                                      head_label="Magnetisation Direction n\u2098", col=0, row=3,
                                                      column_span=3,
                                                      entry_labels=["x:", "y:", "z:"])
        self.entries['m'] = Gui.input_line(master=self, config=config_handler.config, col=0, row=4,
                                           label=u'Magnetisation M\u2080:', unit="kA/m")
        self.entries['mu_r'] = Gui.input_line(master=self, config=config_handler.config, col=0, row=5,
                                              label=u'Relative Permeability µ\u1D63:')
        self.entries['temperature'] = Gui.input_line(master=self, config=config_handler.config, col=0, row=6,
                                                     label=u'Operating Temperature T\u2080:', unit="°C")
        self.entries['tk'] = Gui.input_line(master=self, config=config_handler.config, col=0, row=7,
                                            label="Rev. Temp. -Coeff TK:", unit="%/K")
        self.entries['maxh'] = Gui.input_line(master=self, config=config_handler.config, col=0, row=8,
                                              label="Max Mesh Size:", unit="mm")

        self.info_button = ttk.Button(master=self.button_frame, text="?", width=3, command=InfoFrame)
        self.info_button.pack(side="right", anchor="ne", padx=(1, config_handler.config['GUI']['padding']),
                              pady=config_handler.config['GUI']['h_spacing'])
        self.buttons.append(self.info_button)
        gui_handler.buttons.append(self.info_button)

        self.button_frame.grid(column=0, row=9, columnspan=3, rowspan=1, sticky='s,w,e')


class InfoFrame:

    def __init__(self) -> None:
        self.frame = tk.Toplevel()
        self.frame.title("Info")
        self.frame.protocol("WM_DELETE_WINDOW", self.destroy)

        img = (Image.open(r"resources/images/CuboidMagnet.png"))
        image_width = int(1.0 * img.width)
        image_height = int(1.0 * img.height)
        self.resized_img = ImageTk.PhotoImage(img.resize((image_width, image_height), Image.ANTIALIAS))
        self.frame.geometry(f"{image_width}x{image_height}+{100}+{100}")

        image_frame = ttk.Label(master=self.frame, image=self.resized_img)
        image_frame.pack(expand=True, fill="both", side="top", anchor="center")

    def destroy(self):
        self.frame.destroy()

