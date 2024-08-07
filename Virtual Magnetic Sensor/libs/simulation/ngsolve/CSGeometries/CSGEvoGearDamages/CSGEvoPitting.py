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

                if np.isnan(rnd_x) or np.isnan(coord[1]) or np.isnan(rnd_z) or np.isnan(rnd_radius):
                    raise ValueError(f"NaN detected in generated values: rnd_x={rnd_x}, coord[1]={coord[1]}, rnd_z={rnd_z}, rnd_radius={rnd_radius}")

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
            
            #print(f'new_sphere:{new_sphere}')
            
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
        delta_alpha=2*(np.pi/self.CSGEvoGear_cls.EvoTooth_ini.n)
        
        rot_mat = self.CSGEvoGear_cls.EvoTooth_ini.rotation_matrix(((tooth_number-1) * delta_alpha + self.CSGEvoGear_cls.EvoTooth_ini.theta) - np.radians(90))[0:2,0:2]
        
        left=self.CSGEvoGear_cls.evotooth_2dpoint_array(self.CSGEvoGear_cls.EvoTooth_ini.involute_points)[1]
        right=self.CSGEvoGear_cls.evotooth_2dpoint_array(self.CSGEvoGear_cls.EvoTooth_ini.involute_points)[2][::-1]
        
        lft_trafo=np.dot(left,rot_mat)
        lft_rdus=np.sqrt(np.power(lft_trafo[::,0], 2)+np.power(lft_trafo[::,1], 2))
        lft_rdus=np.reshape(lft_rdus,(self.CSGEvoGear_cls.EvoTooth_ini.involute_points,1))
        lft_trafo=np.hstack((lft_trafo,lft_rdus))
        
        rgt_trafo=np.dot(right,rot_mat)
        rgt_rdus=np.sqrt(np.power(rgt_trafo[::,0], 2)+np.power(rgt_trafo[::,1], 2))
        rgt_rdus=np.reshape(rgt_rdus,(self.CSGEvoGear_cls.EvoTooth_ini.involute_points,1))
        rgt_trafo=np.hstack((rgt_trafo,rgt_rdus))
        
        if np.any(np.isnan(lft_trafo)) or np.any(np.isnan(rgt_trafo)):
            raise ValueError(f"NaN detected in result: {lft_trafo} or {rgt_trafo}")
        
        return [np.transpose(lft_trafo),np.transpose(rgt_trafo)]
    
    def find_coordinates_of_diameter(self, tooth_number: int, tooth_side: str, diameter: float) -> np.ndarray:
        """Find the coordinates [x, y, r] of a diameter on a given tooth number.

        Args:
            tooth_number (int): The tooth number, starting with 0 on the right and counting counterclockwise.
            tooth_side (str): The tooth side ('left' or 'right').
            diameter (float): The diameter to find on the tooth flank.

        Raises:
            ValueError: If tooth_side is invalid or diameter is out of range.

        Returns:
            np.ndarray: A 3x1 array of [x, y, r] coordinates.
        """
        try:
            surface_coordinates = self.tooth_surface_coordinate(tooth_number)[0 if tooth_side == "left" else 1]
        except IndexError:
            raise ValueError(f"Invalid tooth_side: {tooth_side}. Must be 'left' or 'right'.")

        radius = diameter / 2
        z_coords = surface_coordinates[2]
        if radius < z_coords[0] or radius > z_coords[-1]:
            raise ValueError(f"Diameter must be between {z_coords[0]*2} and {z_coords[-1]*2}")

        i = np.searchsorted(z_coords, radius)
        
        if i == 0 or i == len(z_coords):
            raise ValueError(f"Radius {radius} not found within the tooth surface coordinates")

        x = surface_coordinates[0, i-1:i+1]
        y = surface_coordinates[1, i-1:i+1]

        t = (radius - z_coords[i-1]) / (z_coords[i] - z_coords[i-1])
        interpolated_x = x[0] + t * (x[1] - x[0])
        interpolated_y = y[0] + t * (y[1] - y[0])

        result = np.array([[interpolated_x], [interpolated_y], [radius]])

        if np.any(np.isnan(result)):
            raise ValueError(f"NaN detected in result: {result}")

        return result
