from __future__ import annotations
from tkinter import ttk
from tkinter import X
from typing import Union

from libs.DataHandler import DataHandler
from libs.ConfigHandler import ConfigHandler

from libs.elements.components.Gear import Gear
from libs.elements.components.EvoGear import EvoGear
from libs.elements.components.Shaft import Shaft
from libs.elements.components.GearRack import GearRack

from libs.gui.GUIHandler import GUIHandler
from libs.gui.GUIElements import GUIElements as Gui
from libs.gui.buttons.SubFrameButtons import AddButton
from libs.gui.frames.components.GearFrame import GearFrame
from libs.gui.frames.components.EvoGearFrame import EvoGearFrame
from libs.gui.frames.components.ShaftFrame import ShaftFrame
from libs.gui.frames.components.GearRackFrame import GearRackFrame


class ComponentsFrame(ttk.LabelFrame):

    def __init__(self,
                 master: ttk.Frame,
                 side: str,
                 data_handler: DataHandler,
                 config_handler: ConfigHandler,
                 gui_handler: GUIHandler) -> None:

        self.sub_frames = list()

        super().__init__(master=master, text="Components", width=config_handler.config['GUI']['column_width'])
        self.pack(side=side, fill=X, padx=config_handler.config['GUI']['padding'],
                  pady=config_handler.config['GUI']['padding'])
        self.button_frame = Gui.button_frame(self, config_handler.config)

        self.scrollable_frame = Gui.scrollable_frame(self, config_handler.config)

        self.gear_button = AddButton(master=self.button_frame, label="+ Gear", gui_handler=gui_handler,
                                     command=lambda: self.add_gear(data_handler, config_handler, gui_handler))
        """self.evo_gear_button = AddButton(master=self.button_frame, label="+ EvoGear", gui_handler=gui_handler,
                                         command=lambda: self.add_evo_gear(data_handler, config_handler, gui_handler))"""
        self.gear_rack_button = AddButton(master=self.button_frame, label="+ Gear Rack", gui_handler=gui_handler,
                                          command=lambda: self.add_gear_rack(data_handler, config_handler, gui_handler))
        self.shaft_button = AddButton(master=self.button_frame, label="+ Shaft", gui_handler=gui_handler,
                                      command=lambda: self.add_shaft(data_handler, config_handler, gui_handler))
        self.update_sub_frames(data_handler, config_handler, gui_handler)

    def add_gear(self, data_handler: DataHandler, config_handler: ConfigHandler, gui_handler: GUIHandler):
        self.sub_frames.append(GearFrame(master=self.scrollable_frame, data_handler=data_handler,
                                         config_handler=config_handler, gui_handler=gui_handler,
                                         remove_gear=self.remove_component))
        self.sub_frames[-1].refresh(Gear.template())
        return self.sub_frames

    def add_evo_gear(self, data_handler: DataHandler, config_handler: ConfigHandler, gui_handler: GUIHandler):
        self.sub_frames.append(EvoGearFrame(master=self.scrollable_frame, data_handler=data_handler,
                                            config_handler=config_handler, gui_handler=gui_handler,
                                            remove_gear=self.remove_component))
        self.sub_frames[-1].refresh(EvoGear.template())
        return self.sub_frames

    def add_gear_rack(self, data_handler: DataHandler, config_handler: ConfigHandler, gui_handler: GUIHandler):
        self.sub_frames.append(GearRackFrame(master=self.scrollable_frame, data_handler=data_handler,
                                             config_handler=config_handler, gui_handler=gui_handler,
                                             remove_gear_rack=self.remove_component))
        self.sub_frames[-1].refresh(GearRack.template())
        return self.sub_frames

    def add_shaft(self, data_handler: DataHandler, config_handler: ConfigHandler, gui_handler: GUIHandler):
        self.sub_frames.append(ShaftFrame(master=self.scrollable_frame, data_handler=data_handler,
                                          config_handler=config_handler, gui_handler=gui_handler,
                                          remove_shaft=self.remove_component))
        self.sub_frames[-1].refresh(Shaft.template())
        return self.sub_frames

    def erase_sub_frames(self, gui_handler: GUIHandler):
        for frame in reversed(self.sub_frames):
            frame.remove_frame(gui_handler)

    def update_sub_frames(self, data_handler: DataHandler, config_handler: ConfigHandler, gui_handler: GUIHandler):
        for component in data_handler.components():
            if isinstance(component, Gear):
                self.sub_frames.append(GearFrame(master=self.scrollable_frame, data_handler=data_handler,
                                                 config_handler=config_handler, gui_handler=gui_handler,
                                                 remove_gear=self.remove_component))
            elif isinstance(component, EvoGear):
                self.sub_frames.append(EvoGearFrame(master=self.scrollable_frame, data_handler=data_handler,
                                                    config_handler=config_handler, gui_handler=gui_handler,
                                                    remove_gear=self.remove_component))
            elif isinstance(component, GearRack):
                self.sub_frames.append(GearRackFrame(master=self.scrollable_frame, data_handler=data_handler,
                                                     config_handler=config_handler, gui_handler=gui_handler,
                                                     remove_gear_rack=self.remove_component))
            elif isinstance(component, Shaft):
                self.sub_frames.append(ShaftFrame(master=self.scrollable_frame, data_handler=data_handler,
                                                  config_handler=config_handler, gui_handler=gui_handler,
                                                  remove_shaft=self.remove_component))

    def remove_component(self, obj: Union[GearFrame, ShaftFrame]):
        self.sub_frames.remove(obj)
        self.update_idletasks()

    def refresh(self, data_handler: DataHandler, config_handler: ConfigHandler, gui_handler: GUIHandler):
        self.erase_sub_frames(gui_handler)
        self.update_sub_frames(data_handler, config_handler, gui_handler)
        for num, frame in enumerate(self.sub_frames):
            if hasattr(frame, "refresh"):
                frame.refresh(data_handler.components()[num])
