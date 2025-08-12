from __future__ import annotations
from tkinter import ttk
from tkinter import X
from typing import Union

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler

from libs.elements.magnets.CuboidMagnet import CuboidMagnet
from libs.elements.magnets.RodMagnet import RodMagnet
from libs.elements.magnets.UniField import UniField

from libs.gui.GUIHandler import GUIHandler
from libs.gui.frames.magnets.CuboidMagnetFrame import CuboidMagnetFrame
from libs.gui.frames.magnets.RodMagnetFrame import RodMagnetFrame
from libs.gui.frames.magnets.UniFieldFrame import UniFieldFrame
from libs.gui.buttons.SubFrameButtons import AddButton
from libs.gui.GUIElements import GUIElements as Gui


class MagnetsFrame(ttk.LabelFrame):

    def __init__(self,
                 master: ttk.Frame,
                 side: str,
                 data_handler: DataHandler,
                 config_handler: ConfigHandler,
                 gui_handler: GUIHandler) -> None:

        self.sub_frames = list()

        super().__init__(master=master, text="Magnets", width=config_handler.config['GUI']['column_width'])
        self.pack(side=side, fill=X, padx=config_handler.config['GUI']['padding'],
                  pady=config_handler.config['GUI']['padding'])
        self.button_frame = Gui.button_frame(self, config_handler.config)

        self.scrollable_frame = Gui.scrollable_frame(self, config_handler.config)

        self.brick_mag_button = AddButton(master=self.button_frame, label="+ Cuboid", gui_handler=gui_handler,
                                          command=lambda: self.add_brick_magnet(
                                              data_handler, config_handler, gui_handler))
        self.cyl_mag_button = AddButton(master=self.button_frame, label="+ Rod", gui_handler=gui_handler,
                                        command=lambda: self.add_cylinder_magnet(
                                            data_handler, config_handler, gui_handler))
        self.uni_field_button = AddButton(master=self.button_frame, label="+ Uniform Field", gui_handler=gui_handler,
                                          command=lambda: self.add_uniform_field(
                                              data_handler, config_handler, gui_handler))
        self.update_sub_frames(data_handler, config_handler, gui_handler)

    def add_brick_magnet(self, data_handler: DataHandler, config_handler: ConfigHandler, gui_handler: GUIHandler):
        self.sub_frames.append(CuboidMagnetFrame(master=self.scrollable_frame, data_handler=data_handler,
                                                 config_handler=config_handler, gui_handler=gui_handler,
                                                 remove_magnet=self.remove_magnet))
        self.sub_frames[-1].refresh(CuboidMagnet.template())

    def add_cylinder_magnet(self, data_handler: DataHandler, config_handler: ConfigHandler, gui_handler: GUIHandler):
        self.sub_frames.append(RodMagnetFrame(master=self.scrollable_frame, data_handler=data_handler,
                                              config_handler=config_handler, gui_handler=gui_handler,
                                              remove_magnet=self.remove_magnet))
        self.sub_frames[-1].refresh(RodMagnet.template())

    def add_uniform_field(self, data_handler: DataHandler, config_handler: ConfigHandler, gui_handler: GUIHandler):
        self.sub_frames.append(UniFieldFrame(master=self.scrollable_frame, data_handler=data_handler,
                                             config_handler=config_handler, gui_handler=gui_handler,
                                             remove_magnet=self.remove_magnet))
        self.sub_frames[-1].refresh(UniField.template())

    def erase_sub_frames(self, gui_handler: GUIHandler):
        for frame in reversed(self.sub_frames):
            frame.remove_frame(gui_handler)

    def update_sub_frames(self, data_handler: DataHandler, config_handler: ConfigHandler, gui_handler: GUIHandler):
        for magnet in data_handler.magnets():
            if isinstance(magnet, CuboidMagnet):
                self.sub_frames.append(CuboidMagnetFrame(master=self.scrollable_frame, data_handler=data_handler,
                                                         config_handler=config_handler, gui_handler=gui_handler,
                                                         remove_magnet=self.remove_magnet))
            elif isinstance(magnet, RodMagnet):
                self.sub_frames.append(RodMagnetFrame(master=self.scrollable_frame, data_handler=data_handler,
                                                      config_handler=config_handler, gui_handler=gui_handler,
                                                      remove_magnet=self.remove_magnet))
            elif isinstance(magnet, UniField):
                self.sub_frames.append(UniFieldFrame(master=self.scrollable_frame, data_handler=data_handler,
                                                     config_handler=config_handler, gui_handler=gui_handler,
                                                     remove_magnet=self.remove_magnet))

    def remove_magnet(self, obj: Union[CuboidMagnetFrame, RodMagnetFrame, UniFieldFrame]):
        self.sub_frames.remove(obj)
        self.update_idletasks()

    def refresh(self, data_handler: DataHandler, config_handler: ConfigHandler, gui_handler: GUIHandler):
        self.erase_sub_frames(gui_handler)
        self.update_sub_frames(data_handler, config_handler, gui_handler)
        for num, frame in enumerate(self.sub_frames):
            if hasattr(frame, "refresh"):
                frame.refresh(data_handler.magnets()[num])
