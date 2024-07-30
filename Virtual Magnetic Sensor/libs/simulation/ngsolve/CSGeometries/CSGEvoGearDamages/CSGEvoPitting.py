from libs.elements.components.EvoGear import EvoGear
from libs.simulation.ngsolve.CSGeometries.CSGEvoGear import CSGEvoGear
import netgen.csg as csg
import numpy as np


class CSGEvoPitting:
    """Generate the geometry for a evogear with pitting damage in the simulation using netgen.csg.CSGeometry elements.

    Args:
        CSGEvoGear_cls(CSGEvoGear): EvoGear Class is being used to generate all the teeth without damage.
        body(csg.Solid):  Netgen.csg.CSGeometry representation of the gear damage which is being used for the simulation.

    Raises:
        Exception: The correct tooth side must be indicated "left" or "right".
        Exception: The correct diameter must be indicated. 
    """

    CSGEvoGear_cls: CSGEvoGear
    body: csg.Solid

    def __init__(self,
                 EvoTooth_ini: EvoGear) -> None:
        """Initialize pitting damage on an EvoGear given the tooth number and an INI file to generate the involute points.

        Args:
            EvoTooth_ini (EvoGear): Class is being used to calculated all the parameters for the tooth damage.
            pitting_count (int): Amount of pitting spheres that are being placed and calculated in the simualtion.
            pitting_radius (float): Mean pitting sphere radius.
            tooth_number (int): On which tooth the damage is being placed, begining with the horizonal tooth zero at the right side and counting in a counterclockwise direction. 
            tooth_side (str): On whiche tooth side the damage is being placed the avaialable options are: left or right.
            seed (int): The seed is being used to reproduce the same sequence of geometry results.
            standart_deviation (float): Standart Deviation is being used to get random pitting radius. Default 0.05.
        """

        self.CSGEvoGear_cls = CSGEvoGear(EvoTooth_ini)
        self.body = self.build_evopitting(EvoTooth_ini.damage_parameter_dict["pitting_count"],
                                          EvoTooth_ini.damage_parameter_dict["pitting_radius"],
                                          EvoTooth_ini.damage_parameter_dict["tooth_number"],
                                          EvoTooth_ini.damage_parameter_dict["tooth_side"],
                                          EvoTooth_ini.damage_parameter_dict["seed"],
                                          EvoTooth_ini.damage_parameter_dict["sd_r"],
                                          EvoTooth_ini.damage_parameter_dict["sd_d"])

    def build_evopitting_old(self, pitting_count: int, pitting_radius: float, tooth_number: int, tooth_side: str, seed: int, standart_deviation: float) -> csg.Solid:
        """Method to generate the Netgen.csg.CSGeometry for pitting damage.

        Args:
            pitting_count (int): Amount of pitting spheres that are being placed and calculated in the simualtion.
            pitting_radius (float): Mean pitting sphere radius.
            tooth_number (int): On which tooth the damage is being placed, begining with the horizonal tooth zero at the right side and counting in a counterclockwise direction. 
            tooth_side (str): On whiche tooth side the damage is being placed the avaialable options are: left or right.
            seed (int): The seed is being used to reproduce the same sequence of geometry results.
            standart_deviation (float): Standart Deviation is being used to get random pitting radius. Default 0.05.

        Returns:
            csg.Solid: The EvoGear with pitting damage.
        """

        csg_pitting: csg.Solid

        print('d',self.CSGEvoGear_cls.EvoTooth_ini.d)
        for i in range(pitting_count):
            generator_seed = np.random.Generator(np.random.PCG64(seed))
            
            rnd_d=np.random.Generator.normal(generator_seed, loc=self.CSGEvoGear_cls.EvoTooth_ini.d, scale=0.05, size=None)
            print('rnd_d',rnd_d)
            
            coord = self.find_coordinates_of_diameter(tooth_number,tooth_side,rnd_d)
            #coord = self.find_coordinates_of_diameter(tooth_number,tooth_side,self.CSGEvoGear_cls.EvoTooth_ini.d)
            
            rnd_x = np.random.Generator.normal(generator_seed, loc=coord[0], scale=0.05, size=None)
            print('x',rnd_x)
            
            rnd_z = np.random.Generator.uniform(generator_seed, -self.CSGEvoGear_cls.EvoTooth_ini.length, 0)
            rnd_radius = np.random.Generator.normal(generator_seed, loc=pitting_radius, scale=standart_deviation, size=None)
            rnd_radius = np.absolute(rnd_radius)

            if i == 0:
                csg_pitting = csg.Sphere(csg.Pnt(rnd_x+self.CSGEvoGear_cls.EvoTooth_ini.pos[0], coord[1]+self.CSGEvoGear_cls.EvoTooth_ini.pos[1], rnd_z+self.CSGEvoGear_cls.EvoTooth_ini.pos[2]), rnd_radius)
            else:
                csg_pitting += csg.Sphere(csg.Pnt(rnd_x+self.CSGEvoGear_cls.EvoTooth_ini.pos[0],coord[1]+self.CSGEvoGear_cls.EvoTooth_ini.pos[1], rnd_z+self.CSGEvoGear_cls.EvoTooth_ini.pos[2]), rnd_radius)

            seed += 1

        return (self.CSGEvoGear_cls.body-csg_pitting)
    
    def build_evopitting(self, pitting_count: int, pitting_radius: float, tooth_number: int, tooth_side: str, seed: int, sd_r: float, sd_d:float) -> csg.Solid:
        """Method to generate the Netgen.csg.CSGeometry for pitting damage.

        Args:
            pitting_count (int): Amount of pitting spheres that are being placed and calculated in the simulation.
            pitting_radius (float): Mean pitting sphere radius.
            tooth_number (int): On which tooth the damage is being placed, beginning with the horizontal tooth zero at the right side and counting in a counterclockwise direction. 
            tooth_side (str): On which tooth side the damage is being placed the available options are: left or right.
            seed (int): The seed is being used to reproduce the same sequence of geometry results.
            standart_deviation (float): Standard Deviation is being used to get random pitting radius. Default 0.05.

        Returns:
            csg.Solid: The EvoGear with pitting damage.
        """

        csg_pitting: csg.Solid = None
        generator_seed = np.random.Generator(np.random.PCG64(seed))
        pitting_spheres = []

        for i in range(pitting_count):
            overlap = True
            attempts = 0
            max_attempts = 100

            while overlap and attempts < max_attempts:
                rnd_d = generator_seed.normal(loc=self.CSGEvoGear_cls.EvoTooth_ini.d, scale=sd_d)
                coord = self.find_coordinates_of_diameter(tooth_number, tooth_side, rnd_d)
                #rnd_x = generator_seed.normal(loc=coord[0], scale=0.05)
                rnd_x = coord[0]
                
                rnd_z = generator_seed.uniform(-self.CSGEvoGear_cls.EvoTooth_ini.length, 0)
                rnd_radius = abs(generator_seed.normal(loc=pitting_radius, scale=sd_r))

                overlap = False
                for sphere in pitting_spheres:
                    distance = np.sqrt((rnd_x - sphere[0])**2 + (coord[1] - sphere[1])**2 + (rnd_z - sphere[2])**2)
                    if distance < (rnd_radius + sphere[3]):
                        overlap = True
                        break

                attempts += 1

            if attempts == max_attempts:
                print(f"Warning: Could not place non-overlapping sphere after {max_attempts} attempts.")
                continue

            # Add the new sphere to the list
            pitting_spheres.append((rnd_x, coord[1], rnd_z, rnd_radius))
            #print(pitting_spheres[-1])

            # Create or update the CSG object
            new_sphere = csg.Sphere(csg.Pnt(rnd_x + self.CSGEvoGear_cls.EvoTooth_ini.pos[0],
                                            coord[1] + self.CSGEvoGear_cls.EvoTooth_ini.pos[1],
                                            rnd_z + self.CSGEvoGear_cls.EvoTooth_ini.pos[2]),
                                    rnd_radius)
            
            if csg_pitting is None:
                csg_pitting = new_sphere
            else:
                csg_pitting += new_sphere

        if csg_pitting is None:
            return self.CSGEvoGear_cls.body
        else:
            return (self.CSGEvoGear_cls.body - csg_pitting)

    def tooth_surface_coordinate(self, tooth_number: int) -> list:
        """Returns a list containing two arrays which contain the (x, y) coordinates of the EvoTooth flanks.
        The array list[0] contains the coordinates of the left flank. 
        The array list[1] contains the coordinates of the right flank.
        Known Bug: Tooth 0 & last tooth are the same 

        Args:
            tooth_number (int): On which tooth the damage is being placed, begining with the horizonal tooth zero at the right side and counting in a counterclockwise direction.

        Returns:
            list: _description_
        """
        delta_alpha = 2*self.CSGEvoGear_cls.EvoTooth_ini.m*np.pi * \
            np.cos(self.CSGEvoGear_cls.EvoTooth_ini.alpha) / \
            self.CSGEvoGear_cls.EvoTooth_ini.d_b
        points_2d = np.array(self.CSGEvoGear_cls.pnts_2d).T
        points_2d = np.vstack([points_2d, np.zeros((1, points_2d.shape[1]))])

        # Rotation matrix<
        rot_mat = self.CSGEvoGear_cls.EvoTooth_ini.rotation_matrix(((tooth_number-1) * delta_alpha + self.CSGEvoGear_cls.EvoTooth_ini.theta) - np.radians(90))

        # Transform points_2d /w rot_mat
        transformed_points_2d = np.dot(rot_mat, points_2d)
        transformed_points_2d[2] = np.sqrt(np.power(
            transformed_points_2d[0, ::], 2)+np.power(transformed_points_2d[1, ::], 2))

        # Separate left and right flanks
        num_points = transformed_points_2d.shape[1]-2
        mid = num_points // 2
        left = transformed_points_2d[:, :mid]
        right = transformed_points_2d[:, mid:transformed_points_2d.shape[1]-2]

        # Reverse the order of the right flank
        right = right[:, ::-1]

        # Append the last point of the original tooth to both left and right flanks
        left = np.insert(
            left, 0, transformed_points_2d[:, transformed_points_2d.shape[1]-1], axis=1)
        right = np.insert(
            right, 0, transformed_points_2d[:, transformed_points_2d.shape[1]-2], axis=1)

        return [left, right]

    def find_coordinates_of_diameter(self, tooth_number: int, tooth_side: str, diameter: float) -> np.array:
        """Find the interval coordinates [x2, x1] of a (to be found) diameter on a given tooth number.

        Args:
            tooth_number (int): On which tooth the damage is being placed, begining with the horizonal tooth zero at the right side and counting in a counterclockwise direction.
            tooth_side (str): On which tooth side the damage is being placed the avaialable options are: left or right.
            diameter (float): Find the diameter on the tooth flank.

        Raises:
            Exception: The correct tooth side must be indicated "left" or "right".
            Exception: The correct diamter must be indicated. 

        Returns:
            tuple: Intervall represented as a list where the first entry is the second coordinate and the second entry is the first coordinate
        """

        match tooth_side:
            case "left": surface_coordinates = self.tooth_surface_coordinate(tooth_number)[0]
            case "right": surface_coordinates = self.tooth_surface_coordinate(tooth_number)[1]
            case _: raise Exception('Input for toot0,1h_side must be "left" or "right"')
        if ((diameter/2) > surface_coordinates[2, surface_coordinates.shape[1]-1]) or (diameter/2) < surface_coordinates[2, 0]:
            raise Exception('Diameter must be inbetween ['+str(surface_coordinates[2, 0])+','+str(
                surface_coordinates[2, surface_coordinates.shape[1]-1]*2)+']')
        else:
            i=0
            while (surface_coordinates[2, i] < (diameter/2)):
                i += 1
            else:
                x = np.array([(surface_coordinates[0, i-1], surface_coordinates[1, i-1]),
                                  (surface_coordinates[0, i], surface_coordinates[1, i])]).T
                
        m = (x[1, 1]-x[1, 0])/(x[0, 1]-x[0, 0])
        a = 1+m
        b = 2*m*(x[1, 0]-x[0, 0])
        c = -2*x[1, 0]*x[0, 0]*m + \
            np.power(x[0, 0], 2)*m+np.power(x[1, 0], 2)-np.power(diameter/2, 2)
        s = ((-b+np.sqrt(np.power(b, 2)-4*a*c))/(2*a),
             (-b-np.sqrt(np.power(b, 2)-4*a*c))/(2*a))
        if x[0, 0] < s[0] < x[0, 1] or x[0, 1] > s[0] > x[0, 0]:
            s = s[0]
        else:
            s = s[1]
        y = m*(s-x[0, 0])+x[1, 0]

        return np.array([[s], [y], [diameter/2]])
