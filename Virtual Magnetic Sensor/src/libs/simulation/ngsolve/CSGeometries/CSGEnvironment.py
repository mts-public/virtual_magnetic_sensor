import netgen.csg as csg

from libs.elements.SimParams import SimParams


class CSGEnvironment:
    """Generates the geometry for the simulation boundaries with netgen.csg.CSGeometry elements.

    :param sim_params: Object of the SimParams class.
    :type sim_params: SimParams
    """

    sim_params: SimParams
    body: csg.Solid

    def __init__(self,
                 sim_params: SimParams) -> None:
        """Constructor method."""

        self.sim_params = sim_params
        self.body = self.build_body()

    def build_body(self) -> csg.Solid:
        """Builds the body of the bounding environment of the scenery.

        :return: Geometry of the bounding environment.
        :rtype: tuple
        """

        body: csg.Solid = csg.OrthoBrick(csg.Pnt(self.sim_params.boundaries[0]),
                                         csg.Pnt(self.sim_params.boundaries[1])).bc("outer")

        return body
