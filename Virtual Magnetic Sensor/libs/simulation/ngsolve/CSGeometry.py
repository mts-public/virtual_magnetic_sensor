import netgen.csg as csg
from typing import Dict, List

from libs.DataHandler import DataHandler

from libs.simulation.ngsolve.CSGeometries.CSGComponents import CSGComponents
from libs.simulation.ngsolve.CSGeometries.CSGMagnets import CSGMagnets
from libs.simulation.ngsolve.CSGeometries.CSGEnvironment import CSGEnvironment
from libs.simulation.ngsolve.CSGeometries.CSGSensors import CSGSensors


class CSGeometry:
    """Generates the CSGeometries for the objects in the scenery and composes them to the overall geometry including all
        elements of the simulation.

    :param data_handler: Object of the Data class containing all simulation relevant data.
    :type data_handler: DataHandler
    """

    data_handler: DataHandler
    materials: Dict[str, str]

    def __init__(self,
                 data_handler: DataHandler) -> None:
        """Constructor method."""

        self.data_handler = data_handler

        self.materials = {
            "component": "iron",
            "magnet": "magnet",
            "sensor": "air",
            "outer": "air"
        }

        self.border_geometry = CSGEnvironment(self.data_handler.sim_params())
        self.components_geometries = CSGComponents(self.data_handler.components())
        self.magnet_geometries = CSGMagnets(self.data_handler.physical_magnets())
        self.sensor_geometries = CSGSensors(self.data_handler.physical_sensors())

        self.geometry = self.init_geometry()
        self.geometry.Draw()

    def init_geometry(self) -> csg.CSGeometry:
        """Creates the overall geometry of all elements of the simulation. Result can be displayed in the netgen gui.

        :return: Geometry of the whole scenery.
        :rtype: netgen.csg.CSGeometry
        """

        geometry: csg.CSGeometry = csg.CSGeometry()
        bodies_list: List[csg.Solid] = list()

        for num, magnet_body in enumerate(self.magnet_geometries.bodies):
            for body in bodies_list:
                magnet_body -= body
            bodies_list.append(magnet_body)
            geometry.Add(magnet_body.mat(self.materials["magnet"] + str(num)),
                         maxh=self.data_handler.physical_magnets()[num].maxh,
                         col=(0.5, 0.5, 0.5))

        for num, component_body in enumerate(self.components_geometries.bodies):
            for body in bodies_list:
                component_body -= body
            bodies_list.append(component_body)
            geometry.Add(component_body.mat(self.materials["component"] + str(num)),
                         maxh=self.data_handler.components()[num].maxh, col=(0.9, 0.9, 0.9))

        for num, sensor_body in enumerate(self.sensor_geometries.bodies):
            for body in bodies_list:
                sensor_body -= body
            bodies_list.append(sensor_body)
            geometry.Add(sensor_body.mat(self.materials["sensor"]), maxh=self.data_handler.physical_sensors()[num].maxh,
                         col=(0.2, 0.2, 0.2))

        outer_body = self.border_geometry.body
        for body in bodies_list:
            outer_body -= body
        geometry.Add(outer_body.mat(self.materials["outer"]), maxh=self.data_handler.sim_params().maxh_global,
                     transparent=True)

        return geometry
