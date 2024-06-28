from libs.elements.components.EvoGear import EvoGear
from libs.simulation.ngsolve.CSGeometries.CSGEvoGear import CSGEvoGear
import netgen.csg as csg
import numpy as np


class CSGEvoSD:
    """Generate the geometry for a evogear with switching damage in the simulation using netgen.csg.CSGeometry elements.

    Args:
        CSGEvoGear_cls(CSGEvoGear): EvoGear Class is being used to generate all the teeth without damage.
        body(csg.Solid):  Netgen.csg.CSGeometry representation of the gear damage which is being used for the simulation.

    Raises:
        ValueError: Informs the user that the give tooth number is not being rendered and should be changed to get correct results. 
    """

    CSGEvoGear_cls: CSGEvoGear
    body: csg.Solid

    def __init__(self,
                 EvoTooth_ini: EvoGear) -> None:
        """Initalize the switching damage gear geometry using the netgen.csg.CSGeometry elements.

        Args:
            EvoTooth_ini (EvoTooth): Class is being used to calculated all the parameters for the tooth damage.
            angle (float): Angle (in Degrees) by which the tooth is being rotated.
            tooth_number (int): On which tooth the damage is being placed, begining with the horizonal tooth zero at the right side and counting in a counterclockwise direction. 
        """
        self.CSGEvoGear_cls = CSGEvoGear(EvoTooth_ini)
        self.body = self.build_evosd(EvoTooth_ini.involute_points,
                                     EvoTooth_ini.damage_parameter_dict["angle"],
                                     EvoTooth_ini.damage_parameter_dict["tooth_number"])

    def build_evosd(self, involute_points: int, angle: float, tooth_number: int) -> csg.Solid:
        """Method to generate the Netgen.csg.CSGeometry for switching damage.

        Args:
            involute_points (int): The points which are being used to calculate the involute-function.
            angle (float): Angle (in degrees) by which the tooth is being rotated.
            tooth_number (int): On which tooth the damage is being placed, begining with the horizonal tooth zero at the right side and counting in a counterclockwise direction. 

        Returns:
            csg.Soild: Returns the csg.Solid geometry for switching damage
        """
        # Retrieve Extrude List
        extrude_list = self.evosd_extrude_list(
            involute_points, angle, tooth_number)
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
        """ gearbody = csg.Cylinder(csg.Pnt(0, 0, 0),
                                csg.Pnt(0, 0, (-1)*self.CSGEvoGear_cls.EvoTooth_ini.length),
                                self.CSGEvoGear_cls.EvoTooth_ini.d_f/2)-csg.Cylinder(csg.Pnt(0, 0, 0),
                                                                                     csg.Pnt(
                                                                                         0, 0, (-1)*self.CSGEvoGear_cls.EvoTooth_ini.length),
                                                                                     self.CSGEvoGear_cls.EvoTooth_ini.diameter[0]) """
        if self.CSGEvoGear_cls.EvoTooth_ini.diameter[0] != 0:
            gearbody = csg.Cylinder(csg.Pnt(0, 0, 0),
                                    csg.Pnt(
                                        0, 0, (-1)*self.CSGEvoGear_cls.EvoTooth_ini.length),
                                    self.CSGEvoGear_cls.EvoTooth_ini.d_f/2) \
                - csg.Cylinder(csg.Pnt(0, 0, 0),
                               csg.Pnt(0, 0, (-1)*self.CSGEvoGear_cls.EvoTooth_ini.length),
                               self.CSGEvoGear_cls.EvoTooth_ini.diameter[0])
        else:
            gearbody = csg.Cylinder(csg.Pnt(0, 0, 0),
                                    csg.Pnt(
                                        0, 0, (-1)*self.CSGEvoGear_cls.EvoTooth_ini.length),
                                    self.CSGEvoGear_cls.EvoTooth_ini.d_f/2)
                                
        return (csg_evotooth+gearbody)*front*back

    def evosd_2dpoint_array(self, involute_points: int, angle: float) -> np.array:
        """Method to generate the 2d spline of switching damage.

        Args:
            involute_points (int): The points which are being used to calculate the involute-function.
            angle (float): Angle by which the tooth is being rotated.

        Returns:
            np.array: Array of 2d points. 
        """
        # Retrieve CSGEvoGear 2D Points
        tooth_side_coord = self.CSGEvoGear_cls.evotooth_2dpoint_array(involute_points)[0].T
        # Rotation Matrix
        rot_mat = self.CSGEvoGear_cls.EvoTooth_ini.rotation_matrix(np.radians(angle))[0:2, 0:2]
        zp = tooth_side_coord-np.array([self.get_cog(involute_points=7)]).T
        zp = np.dot(rot_mat, zp)
        zp = zp+np.array([self.get_cog(involute_points=7)]).T
        return zp.T

    def get_cog(self, involute_points: int) -> tuple:
        """Method to calculate the center of gravity.

        Args:
            involute_points (int): The points which are being used to calculate the involute-function.

        Returns:
            tuple: tuple consisting of the cog coordinates
        """
        # Sorting coord array
        left = self.CSGEvoGear_cls.evotooth_2dpoint_array(involute_points)[
            1][::-1, :]
        right = self.CSGEvoGear_cls.evotooth_2dpoint_array(involute_points)[
            2][::-1, :]

        tooth_side_coord = np.hstack((left, right))
        tooth_side_coord = tooth_side_coord[:, [0, 2, 3]]
        last = np.array([[self.CSGEvoGear_cls.evotooth_2dpoint_array(involute_points)[0][-1, 0]],
                        [self.CSGEvoGear_cls.evotooth_2dpoint_array(involute_points)[
                            0][-2, 0]],
                         [self.CSGEvoGear_cls.evotooth_2dpoint_array(involute_points)[0][-2, 1]]]).T
        tooth_side_coord = np.vstack((tooth_side_coord, last))

        # Return a list containing [a,b,h,A,ys,xs] from top of the tooth to the bottem of the edge
        parameter_list = []
        for i in range(tooth_side_coord.shape[0]-2):
            a = tooth_side_coord[i+1, 1]-tooth_side_coord[i+1, 0]
            b = tooth_side_coord[i, 1]-tooth_side_coord[i, 0]
            h = tooth_side_coord[i, 2]-tooth_side_coord[i+1, 2]
            A = h*0.5*(a+b)
            ys = (h/3)*((a+2*b)/(a+b))
            xs = 0
            parameter_list.append([a, b, h, A, ys, xs])

        parameter_list.append([2*tooth_side_coord[-1, 1],
                               0,
                               tooth_side_coord[-2, 2]-tooth_side_coord[-1, 2],
                               2*tooth_side_coord[-1, 1]*(tooth_side_coord[-2, 2]-tooth_side_coord[-1, 2]),
                               0.5*(tooth_side_coord[-2, 2] -tooth_side_coord[-1, 2]),
                               0])

        parameter_array = np.array(parameter_list)
        cog_area = np.sum(parameter_array[:, 3], axis=0)

        cog_xs = 0
        cog_ys = 0

        for i in range(parameter_array.shape[0]):
            cog_xs += (parameter_array[i, 5]*parameter_array[i, 3])
            cog_ys += (parameter_array[i, 4]*parameter_array[i, 3])

        cog_xs /= cog_area
        cog_ys /= cog_area

        # COG  Coordinates return tuple
        return (cog_xs, cog_ys+tooth_side_coord[-1, 2])

    def evosd_extrude_list(self, involute_points: int, angle: float, tooth_number: int) -> list:
        """Method to put the switching damage in the list which indicates what every tooth is and clearly defines it's position.

        Args:
            involute_points (int): _description_
            angle (float): Angle (in degrees) by which the tooth is being rotated.
            tooth_number (int): _description_

        Raises:
            ValueError: Informs the user that the give tooth number is not being rendered and should be changed to get correct results. 

        Returns:
            list: Returns all teeth 
        """

        # Retrieve extrude_list
        extrude_list = self.CSGEvoGear_cls.evotooth_extrude_list(
            involute_points=involute_points)
        # Deploying Spline and Path
        evosd_spline_array = self.evosd_2dpoint_array(involute_points, angle)
        evosd_spline_list = []
        evosd_spline_segements_list = []

        sd_spline = csg.SplineCurve2d()
        sd_path = csg.SplineCurve3d()

        # Sorting tooth_spline points & segments
        for i in range(evosd_spline_array.shape[0]):
            evosd_spline_list.append(
                (evosd_spline_array[i, 0], evosd_spline_array[i, 1]))
            evosd_spline_segements_list.append((i, i+1))
        evosd_spline_segements_list[-1] = (evosd_spline_array.shape[0]-1, 0)

        # Deploying Segs&Points to tooth_spline
        for pnt in evosd_spline_list:
            sd_spline.AddPoint(*pnt)
        for seg in evosd_spline_segements_list:
            sd_spline.AddSegment(*seg)
        # Deploying Segs&points to tooth_path
        for pnt in self.CSGEvoGear_cls.path_list()[0]:
            sd_path.AddPoint(*pnt)
        for seg in self.CSGEvoGear_cls.path_list()[1]:
            sd_path.AddSegment(*seg)

        for i in range(len(extrude_list)):
            for j in range(len(extrude_list[i])):
                if "evotooth "+str(tooth_number) == extrude_list[i][0]:
                    extrude_list[i][0] = "evosd "+str(tooth_number)
                    extrude_list[i][1] = sd_path
                    extrude_list[i][2] = sd_spline
                    break

        return extrude_list
