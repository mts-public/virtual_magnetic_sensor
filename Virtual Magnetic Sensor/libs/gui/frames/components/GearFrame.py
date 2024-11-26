import tkinter as tk
from tkinter import ttk
import numpy as np
from PIL import ImageTk, Image
from typing import Callable

from libs.gui.frames.ObjectFrame import ObjectFrame
from libs.gui.GUIElements import GUIElements as Gui
from libs.gui.GUIHandler import GUIHandler

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler


class GearFrame(ObjectFrame):
    """description of class"""

    def __init__(self,
                 master: ttk.Frame,
                 data_handler: DataHandler,
                 config_handler: ConfigHandler,
                 gui_handler: GUIHandler,
                 remove_gear: Callable) -> None:
        super().__init__(master=master, title="Gear", data_handler=data_handler, config_handler=config_handler,
                         gui_handler=gui_handler, remove=remove_gear)

        self.entries['pos'] = Gui.vector3_input(master=self, config=config_handler.config,
                                                head_label="Center x in mm", col=0,
                                                row=0, column_span=3, entry_labels=["x: ", "y: ", "z: "])

        self.entries['axis_0'] = Gui.vector3_input(master=self, config=config_handler.config,
                                                   head_label="Rotation Axis a", col=0, row=1, column_span=3,
                                                   entry_labels=["x: ", "y: ", "z: "])

        self.body_frame = Gui.label_frame(master=self, config=config_handler.config, col=0, row=2,
                                          column_span=3,
                                          row_span=1, label="Gear Body")

        self.entries['diameter'] = Gui.vector2_input(master=self.body_frame, config=config_handler.config, col=0, row=0,
                                                     width=10,
                                                     label='Inner/Outer Diameters d:', unit="mm")
        self.entries['length'] = Gui.input_line(master=self.body_frame, config=config_handler.config, col=0, row=1,
                                                label="Length l:",
                                                unit="mm", col_shift=1)
        self.entries['mu_r'] = Gui.input_line(master=self.body_frame, config=config_handler.config, col=0, row=2,
                                              label=u'Relative Permeability µ\u1D63:', col_shift=1)
        self.entries['eccentricity'] = Gui.input_line(master=self.body_frame, config=config_handler.config, col=0, row=3,
                                                      label="Eccentricity e :", unit="µm", col_shift=1)
        self.entries['wobble_angle'] = Gui.input_line(master=self.body_frame, config=config_handler.config, col=0, row=4,
                                                      label=u'Wobble Angle \u03D5:', unit="°", col_shift=1)

        self.teeth_frame = Gui.label_frame(master=self, config=config_handler.config, col=0, row=3,
                                           column_span=3, row_span=1, label="Gear Teeth")
        self.entries['n'] = Gui.input_line(master=self.teeth_frame, config=config_handler.config, col=0, row=0,
                                           label="Tooth Count n:")
        self.entries['tooth_height'] = Gui.input_line(master=self.teeth_frame, config=config_handler.config,
                                                      col=0, row=1, label=u'Tooth Height h\u209A:', unit="mm")
        self.entries['tooth_width'] = Gui.input_line(master=self.teeth_frame, config=config_handler.config,
                                                     col=0, row=2, label=u'Tooth Width s\u209A:', unit="mm")
        self.entries['tooth_flank_angle'] = Gui.input_line(master=self.teeth_frame, config=config_handler.config, col=0,
                                                           row=3,
                                                           label=u'Tooth Flank Angle α\u209A:', unit="°")
        self.entries['chamfer_depth'] = Gui.input_line(master=self.teeth_frame, config=config_handler.config, col=0,
                                                       row=4,
                                                       label="Chamfer Depth t:", unit="µm")
        self.entries['chamfer_angle'] = Gui.input_line(master=self.teeth_frame, config=config_handler.config, col=0,
                                                       row=5,
                                                       label=u'Chamfer Angle \u0398:', unit="°")

        self.sim_params_frame = Gui.label_frame(master=self, config=config_handler.config, col=0, row=4,
                                                column_span=3, row_span=1, label="Simulation Parameters")
        self.entries['omega'] = Gui.input_line(master=self.sim_params_frame, config=config_handler.config, col=0, row=0,
                                               label=u'Angular Velocity \u03C9:', unit="°/s", col_shift=1)
        self.entries['maxh'] = Gui.input_line(master=self.sim_params_frame, config=config_handler.config, col=0, row=1,
                                              label="Max Mesh Size:", unit="mm", col_shift=1)
        self.entries['display_teeth_angle'] = Gui.vector2_input(master=self.sim_params_frame,
                                                                config=config_handler.config, col=0, row=2,
                                                                width=10, label="Tooth Calculation Angle:", unit="°")
        self.entries['rotate_mesh'] = Gui.check_box(master=self.sim_params_frame, config=config_handler.config, col=0,
                                                    row=3,
                                                    label="Rotate Gear Mesh")
        self.entries['rotate_mesh_max_angle'] = Gui.input_line(master=self.sim_params_frame,
                                                               config=config_handler.config, col=0, row=4,
                                                               unit="°", label="Max Mesh Rotation Angle:",
                                                               col_shift=1)

        self.tooth_button = ttk.Button(master=self.button_frame, text="Tooth Defects", width=15,
                                       command=lambda: self.tooth_defect_frame(config_handler))
        self.tooth_button.pack(side="left", anchor="ne", padx=1,
                               pady=config_handler.config['GUI']['h_spacing'])
        self.buttons.append(self.tooth_button)
        gui_handler.buttons.append(self.tooth_button)
        self.info_button = ttk.Button(master=self.button_frame, text="?", width=3, command=InfoFrame)
        self.info_button.pack(side="right", anchor="ne", padx=(1, config_handler.config['GUI']['padding']),
                              pady=config_handler.config['GUI']['h_spacing'])
        self.buttons.append(self.info_button)
        gui_handler.buttons.append(self.info_button)

        self.button_frame.grid(column=0, row=5, columnspan=3, rowspan=1, sticky='s,w,e')

        self.n_devVar: int = 0
        self.devVar: np.ndarray = np.array([0, 0, 0])
        self.entries['dev_tooth_num'] = ttk.Entry(self)
        self.entries['tooth_deviations'] = [ttk.Entry(self), ttk.Entry(self),
                                            ttk.Entry(self)]
        self.entries['dev_tooth_num'].insert(0, str(self.n_devVar))
        for num, entry in enumerate(self.entries['tooth_deviations']):
            entry.insert(0, str(self.devVar[num]))

    def tooth_defect_frame(self, config_handler: ConfigHandler) -> None:
        def destroy() -> None:
            self.n_devVar = int(self.entries['dev_tooth_num'].get())
            self.devVar = np.array([float(dev.get()) for dev in self.entries['tooth_deviations']])

            self.entries['dev_tooth_num'] = ttk.Entry(self, )
            self.entries['tooth_deviations'] = [ttk.Entry(self), ttk.Entry(self),
                                                ttk.Entry(self)]

            self.entries['dev_tooth_num'].delete(0, 'end')
            self.entries['dev_tooth_num'].insert(0, str(self.n_devVar))
            for num, entry in enumerate(self.entries['tooth_deviations']):
                entry.delete(0, 'end')
                entry.insert(0, str(self.devVar[num]))

            frame.destroy()

        frame = tk.Toplevel()
        frame.title("Tooth Defects")
        frame.protocol("WM_DELETE_WINDOW", destroy)

        label_frame = Gui.label_frame(master=frame, config=config_handler.config, col=0, row=0, column_span=1,
                                      row_span=1, label="Tooth #1")
        self.entries['dev_tooth_num'] = Gui.input_line(master=label_frame, config=config_handler.config, col=0, row=0,
                                                       label="Tooth Number:", unit="")
        self.entries['tooth_deviations'] = Gui.vector3_input(master=label_frame, config=config_handler.config,
                                                             head_label="Deviation in µm", col=0, row=1, column_span=3,
                                                             entry_labels=["Left:", "Top:", "Right:"])

        self.entries['dev_tooth_num'].delete(0, 'end')
        self.entries['dev_tooth_num'].insert(0, str(self.n_devVar))
        for num, entry in enumerate(self.entries['tooth_deviations']):
            entry.delete(0, 'end')
            entry.insert(0, str(self.devVar[num]))


class InfoFrame:

    def __init__(self) -> None:
        self.frame = tk.Toplevel()
        self.frame.title("Info")
        self.frame.protocol("WM_DELETE_WINDOW", self.destroy)

        img = (Image.open(r"resources/images/Gear.png"))
        image_width = int(1.0 * img.width)
        image_height = int(1.0 * img.height)
        self.resized_img = ImageTk.PhotoImage(img.resize((image_width, image_height), Image.Resampling.LANCZOS))
        self.frame.geometry(f"{image_width}x{image_height}+{100}+{100}")

        image_frame = ttk.Label(master=self.frame, image=self.resized_img)
        image_frame.pack(expand=True, fill="both", side="top", anchor="center")

    def destroy(self):
        self.frame.destroy()
