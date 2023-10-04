import netgen.csg as csg
from typing import List

from libs.elements.Magnet import Magnet

from libs.elements.magnets.CuboidMagnet import CuboidMagnet
from libs.elements.magnets.RodMagnet import RodMagnet

from libs.simulation.ngsolve.CSGeometries.CSGCuboidMagnet import CSGCuboidMagnet
from libs.simulation.ngsolve.CSGeometries.CSGRodMagnet import CSGRodMagnet


class CSGMagnets:
    """Wrapper class to determine the type of the magnet and initiate an object of the specific class to build the
        geometry with netgen.csg.CSGeometry elements.

    :param magnets: List of magnets parameters.
    :type magnets: List[Magnet]
    """

    magnets: List[Magnet]
    bodies: List[csg.Solid]

    def __init__(self,
                 magnets: List[Magnet]) -> None:
        """Constructor method."""

        self.magnets = magnets
        self.bodies: List[csg.Solid] = list()
        for magnet in self.magnets:
            self.bodies.append(self.build_magnet_body(magnet))

    @staticmethod
    def build_magnet_body(magnet: Magnet) -> csg.Solid:
        """Method to generate the geometry of a magnet with the parameters specified in the committed component
            object.

        :param magnet: Magnet parameters.
        :type magnet: Magnet
        :return: Magnet geometry.
        :rtype: netgen.csg.Solid
        """

        magnet_geometry = csg.Solid
        if isinstance(magnet, CuboidMagnet):
            magnet_geometry = CSGCuboidMagnet(magnet)
        elif isinstance(magnet, RodMagnet):
            magnet_geometry = CSGRodMagnet(magnet)

        return magnet_geometry.body
