from libs.elements.components.EvoGear import EvoGear
from libs.simulation.ngsolve.CSGeometries.CSGEvoGear import CSGEvoGear
import netgen.csg as csg
import numpy as np


class CSGEvoWF:
    """Generate the geometry for a evogear with warm flow damage in the simulation using netgen.csg.CSGeometry elements.

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
        """Initalize the warm flow gear geometry using the netgen.csg.CSGeometry elements. 

        Args:
            EvoTooth_ini (EvoTooth): _description_
            tooth_number (int): On which tooth the damage is being placed, begining with the horizonal tooth zero at the right side and counting in a counterclockwise direction. 
            s (float): Warm flow multiplier s=]-∞,+∞[ , default value is s=1
        """

        self.CSGEvoGear_cls = CSGEvoGear(EvoTooth_ini)
        self.body = self.build_evowf(EvoTooth_ini.involute_points,
                                     EvoTooth_ini.damage_parameter_dict["tooth_number"],
                                     EvoTooth_ini.damage_parameter_dict["s"])

    def build_evowf(self, involute_points: int, tooth_number: int, s: float) -> csg.Solid:
        """Method to generate the Netgen.csg.CSGeometry for warm flow  damage.

        Args:
            involute_points (int): The points which are being used to calculate the involute-function.
            tooth_number (int): On which tooth the damage is being placed, begining with the horizonal tooth zero at the right side and counting in a counterclockwise direction. 
            s (float): Warm flow multiplier s=]-∞,+∞[ , default value is s=1

        Returns:
            csg.Solid: Returns the csg.Solid geometry for warm flow damage.
        """
        # Retrieve Extrude List
        extrude_list = self.evowf_extrude_list(
            involute_points, tooth_number, s)
        # Front & Back Plane
        back = csg.Plane(
            csg.Pnt(self.CSGEvoGear_cls.EvoTooth_ini.pos[0], self.CSGEvoGear_cls.EvoTooth_ini.pos[1],self.CSGEvoGear_cls.EvoTooth_ini.pos[2]+(-1)*self.CSGEvoGear_cls.EvoTooth_ini.length), csg.Vec(0, 0, -1))
        front = csg.Plane(csg.Pnt(self.CSGEvoGear_cls.EvoTooth_ini.pos[0], self.CSGEvoGear_cls.EvoTooth_ini.pos[1],self.CSGEvoGear_cls.EvoTooth_ini.pos[2]), csg.Vec(0, 0, 1))
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
        if self.CSGEvoGear_cls.EvoTooth_ini.diameter[0] != 0:
            gearbody = csg.Cylinder(csg.Pnt(self.CSGEvoGear_cls.EvoTooth_ini.pos[0], self.CSGEvoGear_cls.EvoTooth_ini.pos[1],self.CSGEvoGear_cls.EvoTooth_ini.pos[2]),
                                    csg.Pnt(
                                        self.CSGEvoGear_cls.EvoTooth_ini.pos[0], self.CSGEvoGear_cls.EvoTooth_ini.pos[1],self.CSGEvoGear_cls.EvoTooth_ini.pos[2]+(-1)*self.CSGEvoGear_cls.EvoTooth_ini.length),
                                    self.CSGEvoGear_cls.EvoTooth_ini.d_f/2) \
                - csg.Cylinder(csg.Pnt(self.CSGEvoGear_cls.EvoTooth_ini.pos[0], self.CSGEvoGear_cls.EvoTooth_ini.pos[1],self.CSGEvoGear_cls.EvoTooth_ini.pos[2]),
                               csg.Pnt(self.CSGEvoGear_cls.EvoTooth_ini.pos[0], self.CSGEvoGear_cls.EvoTooth_ini.pos[1],self.CSGEvoGear_cls.EvoTooth_ini.pos[2]+(-1)*self.CSGEvoGear_cls.EvoTooth_ini.length),
                               self.CSGEvoGear_cls.EvoTooth_ini.diameter[0])
        else:
            gearbody = csg.Cylinder(csg.Pnt(self.CSGEvoGear_cls.EvoTooth_ini.pos[0], self.CSGEvoGear_cls.EvoTooth_ini.pos[1],self.CSGEvoGear_cls.EvoTooth_ini.pos[2]),
                                    csg.Pnt(
                                        self.CSGEvoGear_cls.EvoTooth_ini.pos[0], self.CSGEvoGear_cls.EvoTooth_ini.pos[1],self.CSGEvoGear_cls.EvoTooth_ini.pos[2]+(-1)*self.CSGEvoGear_cls.EvoTooth_ini.length),
                                    self.CSGEvoGear_cls.EvoTooth_ini.d_f/2)
        return (csg_evotooth+gearbody)*front*back

    def evowf_2d_point_array(self, involute_points: int, s: float) -> np.array:
        """Method to generate the 2d spline of warm flow damage.

        Args:
            involute_points (int): The points which are being used to calculate the involute-function.
            s (float): Warm flow multiplier s=]-∞,+∞[ , default value is s=1

        Returns:
            np.array: Array of 2d points.
        """
        # Retrieve Coordinates
        tooth_side_coord = self.CSGEvoGear_cls.evotooth_2dpoint_array(involute_points)[
            0].T
        gsa = self.get_surface_area(tooth_side_coord)
        tooth_side_coord = np.append(tooth_side_coord, np.ones(
            (1, tooth_side_coord.shape[1])), axis=0)
        scal_mat = np.array(
            [[s, 0, 0], [0, (1/s), 0], [0, 0, 1]])  # 3x3 Matrix
        trans_mat = np.array([[1, 0, gsa[0]], [0, 1, gsa[1]], [0, 0, 1]])

        tooth_side_coord = np.dot(np.linalg.inv(trans_mat), tooth_side_coord)
        tooth_side_coord = np.dot(scal_mat, tooth_side_coord)
        tooth_side_coord = np.dot(trans_mat, tooth_side_coord)

        tooth_side_coord = tooth_side_coord[[0, 1], ::]

        tooth_side_coord = np.transpose(tooth_side_coord)

        return tooth_side_coord

    def get_surface_area(self, tooth_side_coord: np.array) -> tuple:
        """Method to calculate the surface area of a gear tooth.

        Args:
            tooth_side_coord (np.array): The spline array of the tooth.

        Returns:
            tuple: Returns a tuple of coordinates and the surface area
        """

        last = np.array([[tooth_side_coord[0, -1]],
                        [tooth_side_coord[0, -2]], [tooth_side_coord[1, -1]]]).T

        # Input toot_side_coord 2xN array, output tooth_side_coord Nx3 -x,x,y
        temp_1 = np.transpose(
            tooth_side_coord[::, :(tooth_side_coord.shape[1]-2)//2])
        temp_1 = temp_1[::-1, ::]
        temp_2 = np.transpose(
            tooth_side_coord[::, (tooth_side_coord.shape[1]-2)//2:-2])
        tooth_side_coord = np.hstack((temp_1, temp_2))
        tooth_side_coord = tooth_side_coord[::, [0, 2, 3]]

        tooth_side_coord = np.vstack((tooth_side_coord, last))

        # Return an array containing [a,b,h,A,ys,xs] from top of the tooth to the bottem of the edge
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
                               0.5*(tooth_side_coord[-2, 2] -
                                    tooth_side_coord[-1, 2]),
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
        return (cog_xs, cog_ys+tooth_side_coord[-1, 2], cog_area)

    def evowf_extrude_list(self, involute_points: int, tooth_number: int, s: float) -> list:
        """Method to put the cold flow damage in the list which indicates what every tooth is and clearly defines it's position.

        Args:
            involute_points (int): The points which are being used to calculate the involute-function.
            tooth_number (int): On which tooth the damage is being placed, begining with the horizonal tooth zero at the right side and counting in a counterclockwise direction. 
            s (float): Warm flow multiplier s=]-∞,+∞[ , default value is s=1

        Raises:
            ValueError: Informs the user that the give tooth number is not being rendered and should be changed to get correct results. 

        Returns:
            list: Returns a list of all teeth 
        """
        # Retrieve extrude_list
        extrude_list = self.CSGEvoGear_cls.evotooth_extrude_list(
            involute_points=involute_points)
        # Deploying Spline and Path
        evowf_spline_array = self.evowf_2d_point_array(involute_points, s)
        evowf_spline_list = []
        evowf_spline_segements_list = []

        wf_spline = csg.SplineCurve2d()
        wf_path = csg.SplineCurve3d()

        # Sorting tooth_spline points & segments
        for i in range(evowf_spline_array.shape[0]):
            evowf_spline_list.append(
                (evowf_spline_array[i, 0], evowf_spline_array[i, 1]))
            evowf_spline_segements_list.append((i, i+1))
        evowf_spline_segements_list[-1] = (evowf_spline_array.shape[0]-1, 0)

        # Deploying Segs&Points to tooth_spline
        for pnt in evowf_spline_list:
            wf_spline.AddPoint(*pnt)
        for seg in evowf_spline_segements_list:
            wf_spline.AddSegment(*seg)
        # Deploying Segs&points to tooth_path
        for pnt in self.CSGEvoGear_cls.path_list()[0]:
            wf_path.AddPoint(*pnt)
        for seg in self.CSGEvoGear_cls.path_list()[1]:
            wf_path.AddSegment(*seg)

        for i in range(len(extrude_list)):
            for j in range(len(extrude_list[i])):
                if "evotooth "+str(tooth_number) == extrude_list[i][0]:
                    extrude_list[i][0] = "evowf "+str(tooth_number)
                    extrude_list[i][1] = wf_path
                    extrude_list[i][2] = wf_spline
                    break
        return extrude_list
