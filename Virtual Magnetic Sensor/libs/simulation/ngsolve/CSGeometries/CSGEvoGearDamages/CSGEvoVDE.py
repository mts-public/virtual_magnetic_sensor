from libs.elements.components.EvoGear import EvoGear
from libs.simulation.ngsolve.CSGeometries.CSGEvoGear import CSGEvoGear
import netgen.csg as csg
import numpy as np


class CSGEvoVDE:
    """Generate the geometry for a evogear with wear and tear due to interference damage in the simulation using netgen.csg.CSGeometry elements.

    Args:
        CSGEvoGear_cls(CSGEvoGear): EvoGear Class is being used to generate all the teeth without damage.
        body(csg.Solid):  Netgen.csg.CSGeometry representation of the gear damage which is being used for the simulation.

    Raises:
        ValueError: The correct thoot side must be indicated available options: "left", "right", "both"
        ValueError: Informs the user that the give tooth number is not being rendered and should be changed to get correct results. 
    """

    CSGEvoGear_cls: CSGEvoGear
    body: csg.Solid

    def __init__(self,
                 EvoTooth_ini: EvoGear) -> None:
        """Initalize the wear and tear due to interference damage gear geometry using the netgen.csg.CSGeometry elements.

        Args:
            EvoTooth_ini (EvoTooth): Class is being used to calculated all the parameters for the tooth damage.
            tooth_number (int): On which tooth the damage is being placed, begining with the horizonal tooth zero at the right side and counting in a counterclockwise direction. 
            tooth_side (str): On whiche tooth side the damage is being placed the available options are: left, right or both sides.
            radius (float): Rounding radius of the tooth head indicated in millimeters.
        """

        self.CSGEvoGear_cls = CSGEvoGear(EvoTooth_ini)
        self.body = self.build_evovde(EvoTooth_ini.involute_points,
                                      EvoTooth_ini.damage_parameter_dict["tooth_number"],
                                      EvoTooth_ini.damage_parameter_dict["tooth_side"],
                                      EvoTooth_ini.damage_parameter_dict["radius"])

    def build_evovde(self, involute_points: int, tooth_number: int, tooth_side: str, r: float) -> csg.Solid:
        """Method to generate the Netgen.csg.CSGeometry for wear and tear due to interference damage.

        Args:
            involute_points (int): The points which are being used to calculate the involute-function.
            tooth_number (int): On which tooth the damage is being placed, begining with the horizonal tooth zero at the right side and counting in a counterclockwise direction. 
            tooth_side (str): On whiche tooth side the damage is being placed the available options are: left, right or both sides.
            radius (float): Rounding radius of the tooth head indicated in millimeters.

        Returns:
            csg.Solid: csg.Solid: Returns the csg.Solid geometry for cold flow damage.
        """
        # Retrieve Extrude List
        extrude_list = self.evovde_extrude_list(
            involute_points, tooth_number, tooth_side, r)
        # Front & Back Plane
        back = csg.Plane(
            csg.Pnt(0, 0, (-1)*self.CSGEvoGear_cls.EvoTooth_ini.length), csg.Vec(0, 0, -1))
        front = csg.Plane(csg.Pnt(0, 0, 0), csg.Vec(0, 0, 1))
        # Buidling teeth
        for i in range(len(extrude_list)):
            if i == 0:
                csg_evotooth = csg.Extrusion(extrude_list[i][1],
                                             extrude_list[i][2],
                                             csg.Vec(extrude_list[i][3]))
            else:
                csg_evotooth += csg.Extrusion(extrude_list[i][1],
                                              extrude_list[i][2],
                                              csg.Vec(extrude_list[i][3]))
        # Building GearBody
        gearbody = csg.Cylinder(csg.Pnt(0, 0, 0),
                                csg.Pnt(
                                    0, 0, (-1)*self.CSGEvoGear_cls.EvoTooth_ini.length),
                                self.CSGEvoGear_cls.EvoTooth_ini.d_f/2)-csg.Cylinder(csg.Pnt(0, 0, 0),
                                                                                     csg.Pnt(
                                                                                         0, 0, (-1)*self.CSGEvoGear_cls.EvoTooth_ini.length),
                                                                                     self.CSGEvoGear_cls.EvoTooth_ini.diameter[0])
        return (csg_evotooth+gearbody)*front*back

    def evovde_2d_point_array(self, r: float, tooth_side: str, involute_points: int) -> np.array:
        """Method to generate the 2d spline of wear and tear due to interference damage.

        Args:
            r (float): Rounding radius of the tooth head indicated in millimeters.
            tooth_side (str): On whiche tooth side the damage is being placed the available options are: left, right or both sides.
            involute_points (int): The points which are being used to calculate the involute-function.

        Raises:
            ValueError: The correct thoot side must be indicated available options: "left", "right", "both"

        Returns:
            np.array: Array of 2d points.
        """
        tooth_side_coord = self.CSGEvoGear_cls.evotooth_2dpoint_array(involute_points)[
            2][::-1, :]

        m = (tooth_side_coord[1, 1]-tooth_side_coord[0, 1]) / \
            (tooth_side_coord[1, 0]-tooth_side_coord[0, 0])
        a = np.array([tooth_side_coord[0, 0], tooth_side_coord[0, 1]])
        b = np.array([(-r/m)+tooth_side_coord[0, 0], tooth_side_coord[0, 1]-r])
        ab = b-a
        ab_lenght = np.sqrt(np.power(ab[0], 2)+np.power(ab[1], 2))

        s_1 = np.array([b[0]-ab_lenght, a[1]])
        s_2 = np.array([r*np.cos((np.pi/2)-np.arcsin((a[1]-b[1])/ab_lenght))+(b[0]-ab_lenght),
                       r*np.sin((np.pi/2)-np.arcsin((a[1]-b[1])/ab_lenght))+b[1]])

        theta_start = (np.pi/2)-np.arcsin((a[1]-b[1])/ab_lenght)
        theta_end = np.radians(90)
        num_points = involute_points

        theta = np.linspace(theta_end, theta_start, num_points)
        x = r * np.cos(theta) + (b[0]-ab_lenght)
        y = r * np.sin(theta) + b[1]

        # Hei nach drun schaffen
        tooth_side_coord = np.delete(tooth_side_coord, 0, axis=0)
        tooth_side_coord = np.vstack((np.vstack((x, y)).T, tooth_side_coord))

        match tooth_side:
            case "left":
                tooth_side_coord[::, 0] = tooth_side_coord[::, 0]*(-1)
                tooth_side_coord = np.vstack((tooth_side_coord[::-1], self.CSGEvoGear_cls.evotooth_2dpoint_array(
                    involute_points)[2][::-1]))
            case "right":
                tooth_side_coord = np.vstack((self.CSGEvoGear_cls.evotooth_2dpoint_array(
                    involute_points)[1], tooth_side_coord))
            case "both":
                invert_tooth_side_coord = np.copy(tooth_side_coord)
                invert_tooth_side_coord[::,
                                        0] = invert_tooth_side_coord[::, 0]*(-1)
                invert_tooth_side_coord = invert_tooth_side_coord[::-1]
                tooth_side_coord = np.vstack(
                    (invert_tooth_side_coord, tooth_side_coord))
            case _:
                print("choose left,right or both")
                raise ValueError("This is not possible")

        tooth_side_coord = np.append(tooth_side_coord, np.array(
            [[tooth_side_coord[-1, 0]], [self.CSGEvoGear_cls.EvoTooth_ini.d_f/2*0.99]]).T, axis=0)
        tooth_side_coord = np.append(tooth_side_coord, np.array(
            [[(-1)*tooth_side_coord[-1, 0]], [self.CSGEvoGear_cls.EvoTooth_ini.d_f/2*0.99]]).T, axis=0)

        return tooth_side_coord

    def evovde_extrude_list(self, involute_points: int, tooth_number: int, tooth_side: str, r: float) -> list:
        """Method to put the cold flow damage in the list which indicates what every tooth is and clearly defines it's position.

        Args:
            involute_points (int): _description_
            tooth_number (int): _description_

        Raises:
            ValueError: Informs the user that the give tooth number is not being rendered and should be changed to get correct results. 

        Returns:
            list: Returns a list of all teeth 
        """

        # Retrieve extrude_list
        extrude_list = self.CSGEvoGear_cls.evotooth_extrude_list(
            involute_points=involute_points)
        # Deploying Spline and Path
        evovde_spline_array = self.evovde_2d_point_array(
            r, tooth_side, involute_points)
        evovde_spline_list = []
        evovde_spline_segements_list = []

        vde_spline = csg.SplineCurve2d()
        vde_path = csg.SplineCurve3d()

        # Sorting tooth_spline points & segments
        for i in range(evovde_spline_array.shape[0]):
            evovde_spline_list.append(
                (evovde_spline_array[i, 0], evovde_spline_array[i, 1]))
            evovde_spline_segements_list.append((i, i+1))
        evovde_spline_segements_list[-1] = (evovde_spline_array.shape[0]-1, 0)

        # Deploying Segs&Points to tooth_spline
        for pnt in evovde_spline_list:
            vde_spline.AddPoint(*pnt)
        for seg in evovde_spline_segements_list:
            vde_spline.AddSegment(*seg)
        # Deploying Segs&points to tooth_path
        for pnt in self.CSGEvoGear_cls.path_list()[0]:
            vde_path.AddPoint(*pnt)
        for seg in self.CSGEvoGear_cls.path_list()[1]:
            vde_path.AddSegment(*seg)

        for i in range(len(extrude_list)):
            for j in range(len(extrude_list[i])):
                if "evotooth "+str(tooth_number) == extrude_list[i][0]:
                    extrude_list[i][0] = "evovde "+str(tooth_number)
                    extrude_list[i][1] = vde_path
                    extrude_list[i][2] = vde_spline
                    break

        return extrude_list
