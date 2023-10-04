import netgen.csg as csg
from typing import List

from libs.elements.Component import Component

from libs.elements.components.Gear import Gear
from libs.elements.components.Shaft import Shaft
from libs.elements.components.GearRack import GearRack

from libs.simulation.ngsolve.CSGeometries.CSGGear import CSGGear
from libs.simulation.ngsolve.CSGeometries.CSGShaft import CSGShaft
from libs.simulation.ngsolve.CSGeometries.CSGGearRack import CSGGearRack


class CSGComponents:
    """Wrapper class to determine the type of the component and initiate an object of the specific class to build the
        geometry with netgen.csg.CSGeometry elements.

    :param components: List of components parameters.
    :type components: List[Component]
    """

    components: List[Component]
    bodies: List[csg.Solid]

    def __init__(self,
                 components: List[Component]) -> None:
        """Constructor method."""

        self.components = components
        self.bodies: List[csg.Solid] = list()
        for component in self.components:
            self.bodies.append(self.build_component_body(component))

    @staticmethod
    def build_component_body(component: Component) -> csg.Solid:
        """Method to generate the geometry of a component with the parameters specified in the committed component
            object.

        :param component: Component parameters.
        :type component: Component
        :return: Component geometry.
        :rtype: netgen.csg.Solid
        """

        component_geometry = csg.Solid
        if isinstance(component, Gear):
            component_geometry = CSGGear(component)
        elif isinstance(component, Shaft):
            component_geometry = CSGShaft(component)
        elif isinstance(component, GearRack):
            component_geometry = CSGGearRack(component)

        return component_geometry.body
