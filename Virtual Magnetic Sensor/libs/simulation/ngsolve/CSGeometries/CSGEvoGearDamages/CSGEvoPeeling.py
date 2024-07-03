from libs.elements.components.EvoGear import EvoGear
from libs.simulation.ngsolve.CSGeometries.CSGEvoGear import CSGEvoGear
import netgen.csg as csg
import numpy as np


class CSGEvoPeeling:
    """Generate the geometry for a evogear with peeling damage in the simulation using netgen.csg.CSGeometry elements.

    Args:
        CSGEvoGear_cls(CSGEvoGear): EvoGear Class is being used to generate all the teeth without damage.
        body(csg.Solid):  Netgen.csg.CSGeometry representation of the gear damage which is being used for the simulation.

    Raises:
        Exception: The correct tooth side must be indicated "left" or "right".
        ValueError: Informs the user that the give tooth number is not being rendered and should be changed to get correct results. 
    """

    CSGEvoGear_cls: CSGEvoGear
    body: csg.Solid

    def __init__(self,
                 EvoTooth_ini: EvoGear) -> None:
        """Initalize the peeling gear geometry using the netgen.csg.CSGeometry elements. 

        Args:
            EvoTooth_ini (EvoGear): Class is being used to calculated all the parameters for the tooth damage.
            tooth_number (int): On which tooth the damage is being placed, begining with the horizonal tooth zero at the right side and counting in a counterclockwise direction. 
            tooth_side (str): On whiche tooth side the damage is being placed the available options are: left or right.
            diameter (list): Indicates the peeling surface area.
            c (float): Peeling depth indicated in millimeter.

        """
        self.CSGEvoGear_cls = CSGEvoGear(EvoTooth_ini)
        self.body = self.build_evopeeling(EvoTooth_ini.involute_points,
                                          EvoTooth_ini.damage_parameter_dict["tooth_number"],
                                          EvoTooth_ini.damage_parameter_dict["tooth_side"],
                                          EvoTooth_ini.damage_parameter_dict["diameter"],
                                          EvoTooth_ini.damage_parameter_dict["c"])

    def build_evopeeling(self, involute_points: int, tooth_number: int, tooth_side: str, diameter: list, c: float) -> csg.Solid:
        """Method to generate the Netgen.csg.CSGeometry for peeling damage.

        Args:
            involute_points (int): The points which are being used to calculate the involute-function.
            tooth_number (int): On which tooth the damage is being placed, begining with the horizonal tooth zero at the right side and counting in a counterclockwise direction. 
            tooth_side (str): On whiche tooth side the damage is being placed the avaialable options are: left or right.
            diameter (list): Indicates the peeling surface area.
            c (float): Peeling depth indicated in millimeter.

        Returns:
            csg.Solid: Returns the csg.Solid geometry for peeling damage.
        """
        # Retrieve Extrude List
        extrude_list = self.evopeeling_extrude_list(
            involute_points, tooth_number, tooth_side, diameter, c)
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
        if self.CSGEvoGear_cls.EvoTooth_ini.diameter[0] != 0:
            gearbody = csg.Cylinder(csg.Pnt(self.CSGEvoGear_cls.EvoTooth_ini.pos[0], self.CSGEvoGear_cls.EvoTooth_ini.pos[1],self.CSGEvoGear_cls.EvoTooth_ini.pos[2]),
                                    csg.Pnt(self.CSGEvoGear_cls.EvoTooth_ini.pos[0], self.CSGEvoGear_cls.EvoTooth_ini.pos[1],self.CSGEvoGear_cls.EvoTooth_ini.pos[2]+ (-1)*self.CSGEvoGear_cls.EvoTooth_ini.length),
                                    self.CSGEvoGear_cls.EvoTooth_ini.d_f/2) \
                - csg.Cylinder(csg.Pnt(self.CSGEvoGear_cls.EvoTooth_ini.pos[0], self.CSGEvoGear_cls.EvoTooth_ini.pos[1],self.CSGEvoGear_cls.EvoTooth_ini.pos[2]),
                               csg.Pnt(self.CSGEvoGear_cls.EvoTooth_ini.pos[0], self.CSGEvoGear_cls.EvoTooth_ini.pos[1],self.CSGEvoGear_cls.EvoTooth_ini.pos[2]+(-1)*self.CSGEvoGear_cls.EvoTooth_ini.length),
                               self.CSGEvoGear_cls.EvoTooth_ini.diameter[0])
        else:
            gearbody = csg.Cylinder(csg.Pnt(self.CSGEvoGear_cls.EvoTooth_ini.pos[0], self.CSGEvoGear_cls.EvoTooth_ini.pos[1],self.CSGEvoGear_cls.EvoTooth_ini.pos[2]),
                                    csg.Pnt(self.CSGEvoGear_cls.EvoTooth_ini.pos[0], self.CSGEvoGear_cls.EvoTooth_ini.pos[1],self.CSGEvoGear_cls.EvoTooth_ini.pos[2]+ (-1)*self.CSGEvoGear_cls.EvoTooth_ini.length),
                                    self.CSGEvoGear_cls.EvoTooth_ini.d_f/2)
            
        return (csg_evotooth+gearbody)*front*back

    def evopeeling_2dpoint_array(self, involute_points: int, tooth_side: str, diameter: list, c: float) -> np.array:
        """Method to generate the 2d spline of peeling damage.

        Args:
            involute_points (int): The points which are being used to calculate the involute-function.
            tooth_number (int): On which tooth the damage is being placed, begining with the horizonal tooth zero at the right side and counting in a counterclockwise direction. 
            tooth_side (str): On whiche tooth side the damage is being placed the available options are: left or right.
            diameter (list): Indicates the peeling surface area.
            c (float): Peeling depth indicated in millimeter.

        Raises:
            Exception: The correct tooth side must be indicated "left" or "right".

        Returns:
            np.array: Array of 2d points.
        """
        end_diameter = min(diameter)
        start_diameter = max(diameter)
        match tooth_side:
            case "left":
                tooth_side_coord = self.CSGEvoGear_cls.evotooth_2dpoint_array(involute_points)[
                    1]
                tooth_side_coord = tooth_side_coord[::-1, :]
            case "right":
                tooth_side_coord = self.CSGEvoGear_cls.evotooth_2dpoint_array(involute_points)[
                    2]
                tooth_side_coord = tooth_side_coord[::-1, :]
            case _: raise Exception('Input for tooth_side must be "left" or "right"')
        # Adding d_f to tooth_side_coord
        d_f = np.array(
            [tooth_side_coord[-1, 0], self.CSGEvoGear_cls.EvoTooth_ini.d_f*0.5*0.99])
        d_f = np.reshape(d_f, (1, 2))
        tooth_side_coord = np.vstack((tooth_side_coord, d_f))
        # np.VStack Diameter to Tooth_Side_Coord
        diameter_of_tsc = np.sqrt(
            np.power(tooth_side_coord[::, 0], 2)+np.power(tooth_side_coord[::, 1], 2))
        diameter_of_tsc = np.reshape(
            diameter_of_tsc, (diameter_of_tsc.shape[0], 1))
        tooth_side_coord = np.hstack((tooth_side_coord, diameter_of_tsc))
        # Insert Diameter into toopth_side_coord
        a = self.find_diameter_coordinates(
            tooth_side_coord, tooth_side, start_diameter/2)
        b = self.find_diameter_coordinates(a[0], tooth_side, end_diameter/2)
        tooth_side_coord = b[0][::, [0, 1]]
        # Reverse if left
        if tooth_side == "left":
            tooth_side_coord = tooth_side_coord[::-1, ::]

        # Identify minimum and maximum entry points
        j = sorted([a[1], b[1]])

        # Copy coord entry from j
        if tooth_side == "right":
            min_j_entry_array = np.copy(tooth_side_coord[j[0]])
            max_j_entry_array = np.copy(tooth_side_coord[j[1]])
            p = j[1]+2
        else:
            min_j_entry_array = np.copy(tooth_side_coord[j[0]])
            max_j_entry_array = np.copy(tooth_side_coord[j[1]+1])
            p = j[1]+3

        # Update coordinates based on range argument (the magic happens in this mess)
        for i in range(j[0]+1, p):  # left j[2]+2
            v = np.reshape(tooth_side_coord[i]-tooth_side_coord[i-1], (1, 2))
            v = c*(1/np.sqrt(np.power(v[0, 0], 2)+np.power(v[0, 1], 2)))*v
            v_ = np.dot(v, self.CSGEvoGear_cls.EvoTooth_ini.rotation_matrix(
                np.radians(+90))[0:2, 0:2])
            tooth_side_coord[i-1] = tooth_side_coord[i-1]+v_

        # Insert min and max entry points
        if tooth_side == "right":
            tooth_side_coord = np.insert(
                tooth_side_coord, j[1]+1, max_j_entry_array, axis=0)
            tooth_side_coord = np.insert(
                tooth_side_coord, j[0], min_j_entry_array, axis=0)
        else:
            tooth_side_coord = np.insert(
                tooth_side_coord, j[1]+2, max_j_entry_array, axis=0)
            tooth_side_coord = np.insert(
                tooth_side_coord, j[0], min_j_entry_array, axis=0)

        match tooth_side:
            case "left":
                tooth_side_coord = np.vstack(
                    (tooth_side_coord, self.CSGEvoGear_cls.evotooth_2dpoint_array(involute_points)[2][::-1, ::]))
                tooth_side_coord = np.append(tooth_side_coord, np.reshape(
                    np.array([tooth_side_coord[-1, 0], tooth_side_coord[0, 1]]), (1, 2)), axis=0)
                return tooth_side_coord
            case "right":
                tooth_side_coord = np.vstack(
                    (self.CSGEvoGear_cls.evotooth_2dpoint_array(involute_points)[1], tooth_side_coord))
                tooth_side_coord = np.append(tooth_side_coord, np.reshape(
                    np.array([(-1)*tooth_side_coord[-1, 0], tooth_side_coord[-1, 1]]), (1, 2)), axis=0)
                return tooth_side_coord

    def find_diameter_coordinates(self, tooth_side_coord: np.array, tooth_side: str, diameter: float) -> tuple:
        """Method to find the coordinates of a given diameter on the tooth flank.

        Args:
            tooth_side_coord (np.array): Array of the tooth flank coordinates.
            tooth_side (str): On whiche tooth side the damage is being placed the available options are: left or right.
            diameter (list): Indicates the peeling surface area.

        Returns:
            tuple: Returns a tuple consisting of the tooth flank coordinates and the index where the diameter was found.
        """
        # Find Diameter Postion in the Array & Inserting Empty Array
        i = np.argmax(tooth_side_coord[::, 2] <= diameter)
        # Interpolation
        if tooth_side == "left":
            tooth_side_coord = tooth_side_coord[::-1, ::]
            i = tooth_side_coord.shape[0] - i
            if i <= 1:
                x = tooth_side_coord[0, 0]
                y = np.sqrt(np.power(diameter, 2)-np.power(x, 2))

                i_array = np.array([x, y, diameter])
                i_array = np.reshape(i_array, (1, 3))
                tooth_side_coord = np.insert(
                    tooth_side_coord, i, i_array, axis=0)

                return tooth_side_coord[::-1, ::], i

            else:
                m = (tooth_side_coord[i, 1]-tooth_side_coord[i-1, 1]) / \
                    (tooth_side_coord[i, 0]-tooth_side_coord[i-1, 0])
                a = 1+m
                b = 2*m*(tooth_side_coord[i-1, 1]-tooth_side_coord[i-1, 0])
                c = -2*tooth_side_coord[i-1, 1]*tooth_side_coord[i-1, 0]*m+np.power(
                    tooth_side_coord[i-1, 0], 2)*m+np.power(tooth_side_coord[i-1, 1], 2)-np.power(diameter, 2)
                x = ((-b+np.sqrt(np.power(b, 2)-4*a*c))/(2*a),
                     (-b-np.sqrt(np.power(b, 2)-4*a*c))/(2*a))

                if tooth_side_coord[i-1, 0] <= x[0] <= tooth_side_coord[i, 0]:
                    x = x[0]
                else:
                    x = x[1]

                y = m*(x-tooth_side_coord[i-1, 0])+tooth_side_coord[i-1, 1]

                i_array = np.array([x, y, diameter])
                i_array = np.reshape(i_array, (1, 3))
                tooth_side_coord = np.insert(
                    tooth_side_coord, i, i_array, axis=0)

                return tooth_side_coord[::-1, ::], i

        elif tooth_side == "right":
            if i == tooth_side_coord.shape[0]-1:
                x = tooth_side_coord[-1, 0]
                y = np.sqrt(np.power(diameter, 2)-np.power(x, 2))

                i_array = np.array([x, y, diameter])
                i_array = np.reshape(i_array, (1, 3))
                tooth_side_coord = np.insert(
                    tooth_side_coord, i, i_array, axis=0)

                return tooth_side_coord, i

            else:
                m = (tooth_side_coord[i, 1]-tooth_side_coord[i-1, 1]) / \
                    (tooth_side_coord[i, 0]-tooth_side_coord[i-1, 0])
                a = 1+m
                b = 2*m*(tooth_side_coord[i-1, 1]-tooth_side_coord[i-1, 0])
                c = -2*tooth_side_coord[i-1, 1]*tooth_side_coord[i-1, 0]*m+np.power(
                    tooth_side_coord[i-1, 0], 2)*m+np.power(tooth_side_coord[i-1, 1], 2)-np.power(diameter, 2)
                x = ((-b+np.sqrt(np.power(b, 2)-4*a*c))/(2*a),
                     (-b-np.sqrt(np.power(b, 2)-4*a*c))/(2*a))

                if tooth_side_coord[i-1, 0] <= x[0] <= tooth_side_coord[i, 0]:
                    x = x[0]
                else:
                    x = x[1]

                y = m*(x-tooth_side_coord[i-1, 0])+tooth_side_coord[i-1, 1]

                i_array = np.array([x, y, diameter])
                i_array = np.reshape(i_array, (1, 3))
                tooth_side_coord = np.insert(
                    tooth_side_coord, i, i_array, axis=0)

            return tooth_side_coord, i

    def evopeeling_extrude_list(self, involute_points: int, tooth_number: int, tooth_side: str, diameter: list, c: float) -> list:
        """Method to put the peeling damage in the list which indicates what every tooth is and clearly defines it's position.

        Args:
            involute_points (int): The points which are being used to calculate the involute-function.
            tooth_number (int): On which tooth the damage is being placed, begining with the horizonal tooth zero at the right side and counting in a counterclockwise direction. 
            tooth_side (str): On whiche tooth side the damage is being placed the available options are: left or right.
            diameter (list): Indicates the peeling surface area.
            c (float): Peeling depth indicated in millimeter.

        Raises:
            ValueError: Informs the user that the give tooth number is not being rendered and should be changed to get correct results. 

        Returns:
            list: Returns all teeth 
        """
        
        # Retrieve extrude_list
        extrude_list = self.CSGEvoGear_cls.evotooth_extrude_list(
            involute_points=involute_points)
        # Deploying Spline and Path
        evopeeling_spline_array = self.evopeeling_2dpoint_array(
            involute_points, tooth_side, diameter, c)
        evopeeling_spline_list = []
        evopeeling_spline_segements_list = []

        peeling_spline = csg.SplineCurve2d()
        peeling_path = csg.SplineCurve3d()

        # Sorting tooth_spline points & segments
        for i in range(evopeeling_spline_array.shape[0]):
            evopeeling_spline_list.append(
                (evopeeling_spline_array[i, 0], evopeeling_spline_array[i, 1]))
            evopeeling_spline_segements_list.append((i, i+1))
        evopeeling_spline_segements_list[-1] = (
            evopeeling_spline_array.shape[0]-1, 0)

        # self.pnts_2d=evopeeling_spline_list

        # Deploying Segs&Points to tooth_spline
        for pnt in evopeeling_spline_list:
            peeling_spline.AddPoint(*pnt)
        for seg in evopeeling_spline_segements_list:
            peeling_spline.AddSegment(*seg)
        # Deploying Segs&points to tooth_path
        for pnt in self.CSGEvoGear_cls.path_list()[0]:
            peeling_path.AddPoint(*pnt)
        for seg in self.CSGEvoGear_cls.path_list()[1]:
            peeling_path.AddSegment(*seg)

        for i in range(len(extrude_list)):
            for j in range(len(extrude_list[i])):
                if "evotooth "+str(tooth_number) == extrude_list[i][0]:
                    extrude_list[i][0] = "evopeeling "+str(tooth_number)
                    extrude_list[i][1] = peeling_path
                    extrude_list[i][2] = peeling_spline
                    break
        return extrude_list
