from libs.elements.components.EvoGear import EvoGear
from libs.simulation.ngsolve.CSGeometries.CSGEvoGear import CSGEvoGear

import netgen.csg as csg
import numpy as np


class CSGEvoKF:
    """Generate the geometry for a evogear with cold flow damage in the simulation using netgen.csg.CSGeometry elements.

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
        """Initalize the cold flow gear geometry using the netgen.csg.CSGeometry elements. 

        Args:
            EvoTooth_ini (EvoTooth): Class is being used to calculated all the parameters for the tooth damage.
            tooth_number (int): On which tooth the damage is being placed, begining with the horizonal tooth zero at the right side and counting in a counterclockwise direction. 
            c (float): Cold flow depth indicated in millimeter.
            tooth_side (str): On whiche tooth side the damage is being placed the available options are: left or right.
        """

        self.CSGEvoGear_cls = CSGEvoGear(EvoTooth_ini)
        self.body = self.build_evokf(EvoTooth_ini.involute_points,
                                     EvoTooth_ini.damage_parameter_dict["tooth_number"],
                                     EvoTooth_ini.damage_parameter_dict["c"],
                                     EvoTooth_ini.damage_parameter_dict["tooth_side"])

    def build_evokf(self, involute_points: int, tooth_number: int, c: float, tooth_side: str) -> csg.Solid:
        """Method to generate the Netgen.csg.CSGeometry for cold flow damage.

        Args:
            involute_points (int): The points which are being used to calculate the involute-function.
            tooth_number (int): On which tooth the damage is being placed, begining with the horizonal tooth zero at the right side and counting in a counterclockwise direction. 
            c (float): Cold flow depth indicated in millimeter.
            tooth_side (str): On which tooth side the damage is being placed the available options are: left or right.

        Returns:
            csg.Solid: Returns the csg.Solid geometry for cold flow damage.
        """
        # Retrieve Extrude List
        extrude_list = self.evokf_extrude_list(
            involute_points, tooth_number, c, tooth_side)
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

    def evokf_2d_point_array(self, involute_points: int, c: float, tooth_side: str) -> np.array:
        """Method to generate the 2d spline of cold flow damage.

        Args:
            tooth_number (int): On which tooth the damage is being placed, begining with the horizonal tooth zero at the right side and counting in a counterclockwise direction. 
            c (float): Cold flow depth indicated in millimeter.
            tooth_side (str): On which tooth side the damage is being placed the available options are: left or right.

        Returns:
            np.array: Array of 2d points.
        """
        match tooth_side:
            case "right":
                tooth_side_coord = self.CSGEvoGear_cls.evotooth_2dpoint_array(involute_points)[
                    2][::-1, :]
                tooth_side_coord = np.append(tooth_side_coord, np.array(
                    [[tooth_side_coord[-1, 0]], [self.CSGEvoGear_cls.EvoTooth_ini.d_f/2*0.99]]).T, axis=0)

                v = np.reshape(
                    tooth_side_coord[-1]-tooth_side_coord[0], (2, 1))
                v = c*(1/(np.sqrt(np.power(v[0], 2)+np.power(v[1], 2))))*v
                v_ = np.dot(self.CSGEvoGear_cls.EvoTooth_ini.rotation_matrix(
                    np.radians(-90))[0:2, 0:2], v)
                diff = tooth_side_coord[tooth_side_coord.shape[0]//2]+v_.T
                p2 = diff+v.T
                m_c = (p2[0, 1]-diff[0, 1])/(p2[0, 0]-diff[0, 0])

                sol = []
                for i in range(1, tooth_side_coord.shape[0]):
                    if i < tooth_side_coord.shape[0]-1:
                        m_int = (tooth_side_coord[i, 1]-tooth_side_coord[i-1, 1])/(
                            tooth_side_coord[i, 0]-tooth_side_coord[i-1, 0])
                        x = (tooth_side_coord[i-1, 1]-diff[0, 1]+m_c *
                             diff[0, 0]-m_int*tooth_side_coord[i-1, 0])/(m_c-m_int)
                        if tooth_side_coord[i-1, 0] <= x <= tooth_side_coord[i, 0]:
                            y = m_c*(x-diff[0, 0])+diff[0, 1]
                            sol.append([x, y, i])
                    else:
                        y = m_c*(tooth_side_coord[-1, 0]-diff[0, 0])+diff[0, 1]
                        if tooth_side_coord[i-1, 1] >= y >= tooth_side_coord[i, 1]:
                            sol.append([tooth_side_coord[i-1, 0], y, i])
                sol = np.array(sol)
                sol = sol[::-1, :]
                indices = sol[::-1, 2].tolist()
                for i in range(sol.shape[0]):
                    tooth_side_coord = np.insert(tooth_side_coord, int(
                        sol[i, 2]), np.reshape(sol[i, [0, 1]], (1, 2)), axis=0)

                temp = tooth_side_coord[0:int(indices[0]+1), ::]
                temp_1 = tooth_side_coord[int(indices[1]+1):, ::]
                tooth_side_coord = np.vstack((temp, temp_1))

                tooth_side_coord = np.vstack((self.CSGEvoGear_cls.evotooth_2dpoint_array(
                    involute_points)[1], tooth_side_coord))

                tooth_side_coord = np.vstack((tooth_side_coord, [
                                             (-1)*tooth_side_coord[-1, 0], self.CSGEvoGear_cls.EvoTooth_ini.d_f/2*0.99]))
                return tooth_side_coord

            case "left":
                tooth_side_coord = self.CSGEvoGear_cls.evotooth_2dpoint_array(involute_points)[
                    1][::-1, :]
                tooth_side_coord = np.append(tooth_side_coord, np.array(
                    [[tooth_side_coord[-1, 0]], [self.CSGEvoGear_cls.EvoTooth_ini.d_f/2*0.99]]).T, axis=0)
                tooth_side_coord = tooth_side_coord[::-1, :]

                v = np.reshape(
                    tooth_side_coord[-1]-tooth_side_coord[0], (2, 1))
                v = c*(1/(np.sqrt(np.power(v[0], 2)+np.power(v[1], 2))))*v
                v_ = np.dot(self.CSGEvoGear_cls.EvoTooth_ini.rotation_matrix(
                    np.radians(-90))[0:2, 0:2], v)

                diff = tooth_side_coord[tooth_side_coord.shape[0]//2]+v_.T
                p2 = diff+v.T
                m_c = (p2[0, 1]-diff[0, 1])/(p2[0, 0]-diff[0, 0])

                sol = []

                for i in range(1, tooth_side_coord.shape[0]):
                    if i > 1:
                        m_int = (tooth_side_coord[i, 1]-tooth_side_coord[i-1, 1])/(
                            tooth_side_coord[i, 0]-tooth_side_coord[i-1, 0])
                        x = (tooth_side_coord[i-1, 1]-diff[0, 1]+m_c *
                             diff[0, 0]-m_int*tooth_side_coord[i-1, 0])/(m_c-m_int)
                        y = m_c*(x-diff[0, 0])+diff[0, 1]
                        if tooth_side_coord[i-1, 0] <= x <= tooth_side_coord[i, 0]:
                            sol.append([x, y, i])
                    elif i == 1:
                        y = m_c*(tooth_side_coord[0, 0]-diff[0, 0])+diff[0, 1]
                        if tooth_side_coord[i-1, 1] <= y <= tooth_side_coord[i, 1]:
                            sol.append([tooth_side_coord[0, 0], y, i])

                sol = np.array(sol)
                sol = sol[::-1, :]
                indices = sol[::-1, 2].tolist()

                for i in range(sol.shape[0]):
                    tooth_side_coord = np.insert(tooth_side_coord, int(
                        sol[i, 2]), np.reshape(sol[i, [0, 1]], (1, 2)), axis=0)

                temp = tooth_side_coord[0:int(indices[0]+1), ::]
                temp_1 = tooth_side_coord[int(indices[1]+1):, ::]
                tooth_side_coord = np.vstack((temp, temp_1))
                tooth_side_coord = np.vstack(
                    (tooth_side_coord, self.CSGEvoGear_cls.evotooth_2dpoint_array(involute_points)[2][::-1, :]))
                tooth_side_coord = np.vstack((tooth_side_coord, [
                                             tooth_side_coord[-1, 0], self.CSGEvoGear_cls.EvoTooth_ini.d_f/2*0.99]))

                return tooth_side_coord

    def evokf_extrude_list(self, involute_points: int, tooth_number: int, c: float, tooth_side: str) -> list:
        """Method to put the cold flow damage in the list which indicates what every tooth is and clearly defines it's position.

        Args:
            involute_points (int): The points which are being used to calculate the involute-function.
            tooth_number (int): On which tooth the damage is being placed, begining with the horizonal tooth zero at the right side and counting in a counterclockwise direction. 
            c (float): Cold flow depth indicated in millimeter.
            tooth_side (str): On which tooth side the damage is being placed the available options are: left or right.

        Raises:
            ValueError: Informs the user that the give tooth number is not being rendered and should be changed to get correct results. 

        Returns:
            list: Returns a list of all teeth 
        """

        # Retrieve extrude_list
        extrude_list = self.CSGEvoGear_cls.evotooth_extrude_list(
            involute_points)
        # Deploying Spline an
        evokf_spline_array = self.evokf_2d_point_array(
            involute_points, c, tooth_side)
        evokf_spline_list = []
        evokf_spline_segements_list = []

        kf_spline = csg.SplineCurve2d()
        kf_path = csg.SplineCurve3d()

        # Sorting tooth_spline points & segments
        for i in range(evokf_spline_array.shape[0]):
            evokf_spline_list.append(
                (evokf_spline_array[i, 0], evokf_spline_array[i, 1]))
            evokf_spline_segements_list.append((i, i+1))
        evokf_spline_segements_list[-1] = (evokf_spline_array.shape[0]-1, 0)

        # Deploying Segs&Points to tooth_spline
        for pnt in evokf_spline_list:
            kf_spline.AddPoint(*pnt)
        for seg in evokf_spline_segements_list:
            kf_spline.AddSegment(*seg)
        # Deploying Segs&points to tooth_path
        for pnt in self.CSGEvoGear_cls.path_list()[0]:
            kf_path.AddPoint(*pnt)
        for seg in self.CSGEvoGear_cls.path_list()[1]:
            kf_path.AddSegment(*seg)

        for i in range(len(extrude_list)):
            for j in range(len(extrude_list[i])):
                if "evotooth "+str(tooth_number) == extrude_list[i][0]:
                    extrude_list[i][0] = "evokf "+str(tooth_number)
                    extrude_list[i][1] = kf_path
                    extrude_list[i][2] = kf_spline
                    break
        return extrude_list
