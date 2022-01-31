import numpy as np
import accessory_functions as af
from global_constants import *
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

class Mass:
    """
    Class for massive objects.

    Attributes
    ---------
    position : float[]
        position in cartesians [a, b, c]
    velocity : float[]
        velocity in cartesians [a, b, c]
    mass : float
        mass of massive object
    test_masses : float[]
        array of TestMass objects
    number_of_test_masses : int
        length of test_masses

    Methods
    ------
    __init__(vector, vector, float) --> None  
    (Side-effects: creates position, velocity, mass, test_masses and number_of_test_masses attributes)


    generate_test_masses() --> None 
    (Side-effects: modifies test_masses and number_of_test_masses)
    """


    def __init__(self, position = [0, 0, 0], velocity = [0, 0, 0], mass = 1.0):
        """
        Assign position, velocity and mass for Mass object on initialisation
        
        Keyword arguments:
        position --- array of floats [a, b, c] (default [0, 0, 0])
        velocity -- array of floats[d, e, f] (default [0, 0, 0])
        mass -- float (default 1.0)
        """

        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.test_masses = []
        self.number_of_test_masses = 0

        return None
    
    def generate_test_masses(self):
        """Populates test_masses array with TestMass objects"""

    
        for i in range(NUMBER_OF_RINGS): #loop over the rings
            j=0 #counter for number of masses in each ring

            #the parameters in capitals have been determined in global_variables.py
            ring_radius = i*RING_SPACING + MINIMUM_RADIUS
            #rounds down to nearest integer
            number_of_masses_on_ring = int(ring_radius*NUMBER_OF_MASSES_PER_UNIT_RADIUS)
            #velocity at which masses need to orbit to stay in a circular orbit
            orbital_velocity = af.circular_orbit_velocity(ring_radius, self.mass) 

            while j < number_of_masses_on_ring:
                #spaces test masses equally around ring
                position_test = [ring_radius, j*2*np.pi/number_of_masses_on_ring, 0] 
                velocity_test = [0, orbital_velocity, 0] 
                
                #convert cylindrical polar coordinates and vector field to cartesians
                velocity_test = af.field_polar_to_cartesian(position_test, velocity_test)
                position_test = af.position_polar_to_cartesian(position_test)
                #ensures test masses are comoving with massive object they are created on
                velocity_test += self.velocity 
                position_test += self.position

                self.test_masses.append(TestMass(position_test, velocity_test))
                j += 1

            self.number_of_test_masses = len(self.test_masses)
        return None








class TestMass:
    """
    Class for test_mass objects

    Attributes
    ---------
    position : float[]
        position in cartesians [a, b, c]
    velocity : float[]
        velocity in cartesians [a, b, c]

    Methods
    ------
    __init__(vector, vector) --> None (Side-effects: creates positon, velocity attributes)
    """


    def __init__(self, position, velocity):
        """
        Assigns positon and velocity to test mass

        Keywords arguments:
        position -- position --- array of floats [a, b, c] (default [0, 0, 0])
        velocity -- array of floats[d, e, f] (default [0, 0, 0])
        """

        self.position = position
        self.velocity = velocity
  
        return None
    
