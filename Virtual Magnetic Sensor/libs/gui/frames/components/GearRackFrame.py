import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from typing import Callable

from libs.gui.frames.ObjectFrame import ObjectFrame
from libs.gui.GUIElements import GUIElements as Gui
from libs.gui.GUIHandler import GUIHandler

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler


class GearRackFrame(ObjectFrame):
    """description of class"""

    def __init__(self,
                 master: ttk.Frame,
                 data_handler: DataHandler,
                 config_handler: ConfigHandler,
                 gui_handler: GUIHandler,
                 remove_gear_rack: Callable) -> None:
        super().__init__(master=master, title="Gear Rack", data_handler=data_handler, config_handler=config_handler,
                         gui_handler=gui_handler, remove=remove_gear_rack)

        self.entries['pos'] = Gui.vector3_input(master=self, config=config_handler.config,
                                                head_label="Center x in mm",
                                                col=0, row=0, column_span=3, entry_labels=["x: ", "y: ", "z: "])
        self.entries['rot'] = Gui.vector3_input(master=self, config=config_handler.config,
                                                head_label="Rotation θ in °", col=0, row=1, column_span=3,
                                                entry_labels=["x:", "y:", "z:"])

        self.body_frame = Gui.label_frame(master=self, config=config_handler.config, col=0, row=2,
                                          column_span=3,
                                          row_span=1, label="Gear Rack Body")

        self.entries['dim'] = Gui.vector3_input(master=self.body_frame, config=config_handler.config,
                                                head_label="Size b in mm", col=0, row=0, column_span=4,
                                                entry_labels=["x: ", "y: ", "z: "])
        self.entries['mu_r'] = Gui.input_line(master=self.body_frame, config=config_handler.config, col=0, row=1,
                                              label=u'Relative Permeability µ\u1D63:', col_shift=0)

        self.teeth_frame = Gui.label_frame(master=self, config=config_handler.config, col=0, row=3,
                                           column_span=3, row_span=1, label="Gear Rack Teeth")

        self.entries['tooth_height'] = Gui.input_line(master=self.teeth_frame, config=config_handler.config,
                                                      col=0, row=0, label=u'Tooth Height h\u209A:', unit="mm")
        self.entries['tooth_width'] = Gui.input_line(master=self.teeth_frame, config=config_handler.config,
                                                     col=0, row=1, label=u'Tooth Width s\u209A:', unit="mm")
        self.entries['tooth_pitch'] = Gui.input_line(master=self.teeth_frame, config=config_handler.config,
                                                     col=0, row=2, label=u'Pitch p:', unit="mm")
        self.entries['tooth_flank_angle'] = Gui.input_line(master=self.teeth_frame, config=config_handler.config, col=0,
                                                           row=3,
                                                           label=u'Tooth Flank Angle α\u209A:', unit="°")
        # Not fully implemented yet
        """self.entries['chamfer_depth'] = Gui.input_line(master=self.teeth_frame, config=data_handler.config,
                                                       col=0, row=4, label="Chamfer Depth t:", unit="µm")
        self.entries['chamfer_angle'] = Gui.input_line(master=self.teeth_frame, config=data_handler.config,
                                                       col=0, row=5, label=u'Chamfer Angle \u0398:', unit="Deg")"""
        self.entries['chamfer_depth'] = tk.Entry()
        self.entries['chamfer_depth'].insert(0, "0")
        self.entries['chamfer_angle'] = tk.Entry()
        self.entries['chamfer_angle'].insert(0, "45")
        # Not fully implemented yet

        self.sim_params_frame = Gui.label_frame(master=self, config=config_handler.config, col=0, row=4,
                                                column_span=3, row_span=1, label="Simulation Parameters")

        self.entries['velocity'] = Gui.vector3_input(master=self.sim_params_frame, config=config_handler.config,
                                                     head_label="Velocity v in mm/s", col=0, row=0, column_span=4,
                                                     entry_labels=["x: ", "y: ", "z: "])
        self.entries['maxh'] = Gui.input_line(master=self.sim_params_frame, config=config_handler.config, col=0, row=1,
                                              label="Max Mesh Size:", unit="mm", col_shift=1)

        self.info_button = ttk.Button(master=self.button_frame, text="?", width=3, command=InfoFrame)
        self.info_button.pack(side="right", anchor="ne", padx=(1, config_handler.config['GUI']['padding']),
                              pady=config_handler.config['GUI']['h_spacing'])
        self.buttons.append(self.info_button)
        gui_handler.buttons.append(self.info_button)

        self.button_frame.grid(column=0, row=5, columnspan=3, rowspan=1, sticky='s,w,e')


class InfoFrame:

    def __init__(self) -> None:
        self.frame = tk.Toplevel()
        self.frame.title("Info")
        self.frame.protocol("WM_DELETE_WINDOW", self.destroy)

        img = (Image.open(r"resources/images/GearRack.png"))
        image_width = int(1.0 * img.width)
        image_height = int(1.0 * img.height)
        self.resized_img = ImageTk.PhotoImage(img.resize((image_width, image_height), Image.Resampling.LANCZOS))
        self.frame.geometry(f"{image_width}x{image_height}+{100}+{100}")

        image_frame = ttk.Label(master=self.frame, image=self.resized_img)
        image_frame.pack(expand=True, fill="both", side="top", anchor="center")

    def destroy(self):
        self.frame.destroy()
