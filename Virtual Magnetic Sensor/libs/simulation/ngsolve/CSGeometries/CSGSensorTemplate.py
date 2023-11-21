import netgen.csg as csg

from libs.elements.sensors.SensorTemplate import SensorTemplate


class CSGSensorTemplate:
    """Generates the geometry for a shaft in the simulation with netgen.csg.CSGeometry elements.

    :param template: Object of the SensorTemplate class.
    :type template: SensorTemplate
    """

    template: SensorTemplate
    body: csg.Solid

    def __init__(self,
                 template: SensorTemplate) -> None:
        """Constructor method."""

        self.template = template

        self.body = self.build_body()

    def build_body(self) -> csg.Solid:
        """Builds the geometry of the template with netgen.csg.CSGeometry elements.

        :return: Template geometry.
        :type: netgen.csg.Solid
        """

        """The geometry of the new element is designed here.
        1. Import the element class.
        2. Rename this class. The class name must match the elements class name with a prefixed 'CSG'. For example:
        A class called 'NewSensor' expects a class called 'CSGNewSensor'.
        3. Design the geometry (-> https://docu.ngsolve.org/nightly/i-tutorials/unit-4.2-csg/csg.html) and return it.
        """

        body = csg.Solid()

        return body
