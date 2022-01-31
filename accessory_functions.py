import numpy as np
from global_constants import GRAVITATIONAL_CONSTANT
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
"""
Self-contained small numeric functions, and functions used in testing the stability of the program.


Methods:

    circular_oribit_velocity(float, float) --> float (No Side-effects)

    position_polar_to_cartesian(float[]) --> float[] (No Side-effects)

    field_polar_to_cartesian(float[], float[]) --> float[] (No Side-effects)

    distance(float[], float[]) --> float[] (No Side-effects)

    energy_of_massive_objects(Mass[]) --> float (No Side-effects)

    energy_of_test_masses(Mass[]) --> float (No Side-effects)
    
"""

def circular_orbit_velocity(radius, mass):
    """
    Finds the velocity at which test masses need to orbit to stay in a circular orbit around their massive object.

    Keyword arguments:
    radius -- float, distance at which test mass is orbiting from massive object
    mass --  float, mass of the massive object

    Return value:
    -- float, the speed (magnitude, not a vector) for cicular orbit
    """

    return np.sqrt(GRAVITATIONAL_CONSTANT*mass/radius)

def position_polar_to_cartesian(position):
    """
    Turns a 3 position vector in cylindrical polar coordinates into cartesians

    Keywords arguments:
    position -- array of floats, [r, theta, z]

    Return value:
    -- array of floats, cartesian coordinates[x, y, z]
    """

    coordinate_change = np.array([[np.cos(position[1]), 0, 0], [np.sin(position[1]), 0, 0], [0, 0, 1]] ) #matrix to change basis

    return np.dot(coordinate_change, position) 
  
def field_polar_to_cartesian(position, vector):
    """
    Turns a vector field in cylindrical polar coordinates into cartesians

    Keywords arguments:
    position -- array of floats, [r, theta, z], denoting the position of the vector
    vector -- array of floats, [r, theta, z], denoting the direction of the vector field at positon

    Return value:
    -- array of floats, cartesian coordinates [x, y, z] the cartesian direction in which the vector is pointing
    """

    coordinate_change = np.array([[np.cos(position[1]), -np.sin(position[1]), 0], [np.sin(position[1]), np.cos(position[1]), 0], [0, 0, 1]] ) #matrix to change basis
    return np.dot(coordinate_change, vector)

def distance(vector_1, vector_2):
    """
    Finds the displacement vector between two position vectors

    Keyword arguments;
    vector_1 -- array of floats, [x, y, z]
    vector_2 --  array of floats, [x,y, z]

    Return value:
    -- array of floats, [x, y, z]
    """

    vector_1 = np.array(vector_1)
    vector_2 = np.array(vector_2)
    return vector_2 - vector_1

def energy_of_massive_objects(massive_objects):
    """Returns a float of the total energy of the massive objects in the system, excludes test masses"""
    energy = [] 
    for i in range(len(massive_objects)):
        velocity = np.linalg.norm(massive_objects[i].velocity)
        kinetic_energy = 0.5*massive_objects[i].mass*(velocity**2) 
        gpe = 0
        for j in range(len(massive_objects)): #loop over all massive objects to find potential energy
            if i == j: #to avoid self gravitation
                pass
            else:
                r_vector = distance(massive_objects[i].position, massive_objects[j].position)
                gpe += (-1)*(massive_objects[j].mass)*(massive_objects[i].mass)/abs((np.linalg.norm(r_vector)))   #calculation of GPE
        energy.append(gpe+kinetic_energy)
    return np.sum(energy)

def energy_of_test_masses(massive_objects):
    """Returns a float of the total energy of the test masses orbiting the massive objects in the system"""
    energy = []
    for j in range(len(massive_objects)):
        for i in range(len(massive_objects[j].test_masses)): #loop over all massive objects to find potential energy
            velocity = np.linalg.norm(massive_objects[j].test_masses[i].velocity)
            kinetic_energy = 0.5*velocity**2
            r_vector = distance(massive_objects[j].position, massive_objects[0].test_masses[i].position)
            gpe = -massive_objects[j].mass/(np.linalg.norm(r_vector))
            energy.append(kinetic_energy+gpe)
    return np.sum(energy)
