import netgen.csg as csg
import numpy as np
from libs.elements.components.EvoGear import EvoGear


class CSGEvoGear:
    """Generate the geometry for a evogear in the simulation using netgen.csg.CSGeometry elements.

    :param EvoTooth_ini: Object of the EvoTooth which is used to calculate the coordinates of the evotooth
    :type EvoTooth_ini: EvoTooth

    :param body: CSG object representing the involute gear
    :type body: csg.Solid

    :param pnts_2d: 2D Points List
    :type pnts_2d: list

    :param segs_2d: 2D Segments List
    :type segs_2d: list

    :param delta_alpha: Gear pitch angle
    :type delta_alpha: float

    :param involute_points: n Points to calculate the involute function n=7 is sufficiant
    :type involute_points: int
    """

    EvoTooth_ini: EvoGear
    body: csg.Solid
    pnts_2d: list
    segs_2d: list
    involute_points: int

    def __init__(self, EvoTooth_ini: EvoGear) -> None:
        """Constructor method."""

        self.EvoTooth_ini = EvoTooth_ini
        self.body = self.build_evogear(EvoTooth_ini.involute_points)

    def build_evogear(self, involute_points: int) -> csg.Solid:
        """Builds the geometry of the evogear with netgen.csg.CSGeometry elements.

        :param involute_points: Points to calculate the involute
        :type involute_points:

        :return: EvoGear geometry.
        :type: netgen.csg.Solid
        """

        # Retrieve extrude_list
        extrude_list = self.evotooth_extrude_list(involute_points)
        # Front & Back Plane
        back = csg.Plane(
            csg.Pnt(0, 0, (-1)*self.EvoTooth_ini.length), csg.Vec(0, 0, -1))
        front = csg.Plane(csg.Pnt(0, 0, 0), csg.Vec(0, 0, 1))
        # Building teeth
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
        if self.EvoTooth_ini.diameter[0] != 0:
            gearbody = csg.Cylinder(csg.Pnt(0, 0, 0),
                                    csg.Pnt(
                                        0, 0, (-1)*self.EvoTooth_ini.length),
                                    self.EvoTooth_ini.d_f/2) \
                - csg.Cylinder(csg.Pnt(0, 0, 0),
                               csg.Pnt(0, 0, (-1)*self.EvoTooth_ini.length),
                               self.EvoTooth_ini.diameter[0])
        else:
            gearbody = csg.Cylinder(csg.Pnt(0, 0, 0),
                                    csg.Pnt(
                                        0, 0, (-1)*self.EvoTooth_ini.length),
                                    self.EvoTooth_ini.d_f/2)

        print("Theta: ", np.degrees(self.EvoTooth_ini.theta))

        return (csg_evotooth+gearbody)*front*back

    def evotooth_2dpoint_array(self, involute_points: int) -> tuple:
        """Generate 2D coordinates representing points on the EvoTooth profile.

        :param involute_points: Points to calculate the involute function
        :type: int 

        :return:tuple consisting of the whole 2D point list of the involute tooth, 
                2nd & 3rd entrie are the point lists of the left & right 2D point list of the involute tooth.
        :rtype: tuple
        """

        coordinate_2d = self.EvoTooth_ini.coordinates(involute_points)
        temp = coordinate_2d[:, [0, 2]]
        temp = temp[::-1, [0, 1]]
        coordinate_2d = coordinate_2d[:, [1, 2]]

        left = coordinate_2d
        right = temp[::-1, [0, 1]]

        coordinate_2d = np.vstack((coordinate_2d, temp))
        coordinate_2d = np.vstack(
            (coordinate_2d, [temp[-1, 0], self.EvoTooth_ini.d_f/2*0.8]))
        coordinate_2d = np.vstack(
            (coordinate_2d, [(-1)*temp[-1, 0], self.EvoTooth_ini.d_f/2*0.8]))

        return coordinate_2d, left, right

    def dirvec_array(self) -> np.array:
        """Generate an array of direction vectors for EvoTooth geometry.

        :return: An array of direction vectors representing the orientation of each EvoTooth.
        :rtype: np.array
        """

        delta_alpha = 2*self.EvoTooth_ini.m*np.pi * \
            np.cos(self.EvoTooth_ini.alpha)/self.EvoTooth_ini.d_b
        rotation_angle = np.radians(0)
        dirvec_list = []

        for i in range(self.EvoTooth_ini.n):  # self.EvoTooth_ini.n-1
            if i > 0:
                rotation_angle += delta_alpha
            if self.EvoTooth_ini.display_teeth_angle[0] <= rotation_angle <= self.EvoTooth_ini.display_teeth_angle[1]:
                dirvec_list.append(((self.EvoTooth_ini.d_b/2)*np.cos(rotation_angle+self.EvoTooth_ini.theta),
                                    (self.EvoTooth_ini.d_b/2)*np.sin(rotation_angle+self.EvoTooth_ini.theta), 0))
                print("Tooth Nr.", i+1, " Total Angle:",
                      np.degrees(rotation_angle+self.EvoTooth_ini.theta))
                print("x:", (self.EvoTooth_ini.d_b/2) *
                      np.cos(rotation_angle+self.EvoTooth_ini.theta))
                print("y:", (self.EvoTooth_ini.d_b/2) *
                      np.sin(rotation_angle+self.EvoTooth_ini.theta))

        return np.array(dirvec_list)

    def path_list(self) -> tuple:
        """The path along which the spline geometry is being extruded

        :return: tuple consisting of lists
        :rtype: tuple
        """

        pnts_3d = [(0, 0, 0),
                   (0, 0, (-1)*self.EvoTooth_ini.length)]
        segs_3d = [(0, 1)]

        return pnts_3d, segs_3d

    def evotooth_extrude_list(self, involute_points: int) -> list:
        """Generate a list of extrusion parameters for creating EvoTooth geometry.

        :param involute_points: Points to calculate the involute function
        :type: int 

        :return: Puts every gear tooth in an easy acessible list,
        :rtype: list
        """
        evotooth_spline_array = self.evotooth_2dpoint_array(involute_points)[0]
        evotooth_spline_list = []
        evotooth_spline_segements_list = []

        extrude_list = []

        tooth_spline = csg.SplineCurve2d()
        tooth_path = csg.SplineCurve3d()

        # Sorting tooth_spline points & segments
        for i in range(evotooth_spline_array.shape[0]):
            evotooth_spline_list.append(
                (evotooth_spline_array[i, 0], evotooth_spline_array[i, 1]))
            evotooth_spline_segements_list.append((i, i+1))
        evotooth_spline_segements_list[-1] = (
            evotooth_spline_array.shape[0]-1, 0)

        self.pnts_2d = evotooth_spline_list

        # Deploying Segs&Points to tooth_spline
        for pnt in evotooth_spline_list:
            tooth_spline.AddPoint(*pnt)
        for seg in evotooth_spline_segements_list:
            tooth_spline.AddSegment(*seg)
        # Deploying Segs&points to tooth_path
        for pnt in self.path_list()[0]:
            tooth_path.AddPoint(*pnt)
        for seg in self.path_list()[1]:
            tooth_path.AddSegment(*seg)

        # Adding entries to extrude list, dont forget to add a Front and Back Plane
        dir_vec_arr = self.dirvec_array()
        for i in range(dir_vec_arr.shape[0]):
            extrude_list.append(["evotooth "+str(i+1), tooth_path, tooth_spline,
                                (dir_vec_arr[i, 0], dir_vec_arr[i, 1], dir_vec_arr[i, 2])])

        return extrude_list
