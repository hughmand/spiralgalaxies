import numpy as np
import accessory_functions as af
import scipy.integrate as syi
from global_constants import GRAVITATIONAL_CONSTANT, STEP_SIZE
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

"""
Methods for integrating the differential equations and changing the format of data 

For methods involving vector algebra and other minor numerical calculations, see accessory_functions.py

Methods:

    stacker(Mass[]) --> (float[], string[], float[]) (No side-effects)

    separate_stack(float[], string[]) --> (float[], float[]) (No side-effects)

    destacker(float[], string[], Mass[]) --> None (Side-effects: modifies attributes of Mass[])

    forcing_function_massive_object(float[], float[], int, int) --> float (No Side-effects)

    forcing_function_test_mass(float[], float[], int, float[]) --> float (No Side-effects)

    derivative_assignment(float, float[], string[], float[]) --> float[] (No Side-effects)

    integrate(float[], string[], float[], float, float) --> float[] (No Side-effects)

"""





def stacker(massive_objects):
    """
    Creates a one dimensional array of all the positions and velocities of masses and test masses in massive_objects
    The structure of stack is:
        Massive object 1
            position
                x, y, z
            velocity
                x, y, z
        Massive object 2
        ...
        Test mass 1 of Massive object 1
            position
                x, y, z
            velocity
                x, y, z 
        ...
    For more information see accompanying report.

    Keyword arguments:
    massive_objects -- array of class Mass

    Return values:
    stack -- array of floats, structure described above
    stack_info -- array of strings, contains information about what the values in stack correspond to
    masses -- array of floats, the masses of the massive objects 
    """


    stack = []
    stack_info = []
    masses = []

    number_of_massive_objects = len(massive_objects)


    #loop for massive objects
    for i in range(number_of_massive_objects):
        masses.append(massive_objects[i].mass)
        for k in range(3):
            stack.append(massive_objects[i].position[k])
            stack_info.append(("position", "mass"))
        for k in range(3):
            stack.append(massive_objects[i].velocity[k])
            stack_info.append(("velocity", "mass"))


    #loop for test masses
    for i in range(number_of_massive_objects):
        for j in range(massive_objects[i].number_of_test_masses):
            for k in range(3):
                stack.append(massive_objects[i].test_masses[j].position[k])
                stack_info.append(("position", "test_mass"))
            for k in range(3):
                stack.append(massive_objects[i].test_masses[j].velocity[k])
                stack_info.append(("velocity", "test_mass"))
    stack_info = np.array(stack_info)



    return (stack, stack_info, masses)







def separate_stack(stack, stack_info):
    """
    Separates stack into arrays corresponding to position for massive objects and test masses

    Keyword arguments:
    stack -- array of floats, see stacker() method for more information
    stack_info -- array of strings, contains information about what the values in stack correspond to

    Return values:
    positions_of_massive_objects -- 2D array of floats, [ x y z, ...] for the positions of massive objects
    positions_of_test_masses -- 2D array of floats, [ x y z, ...] for the positions of test masses
    """


    positions_of_massive_objects = []
    positions_of_test_masses = []
    i = 0
    while i < len(stack) - 1: 
        if stack_info[i, 1] == "mass":
            #assigns x, y and z coordinates
            positions_of_massive_objects.append([stack[i], stack[i+1], stack[i+2]]) 
            i += 6
        else:
            positions_of_test_masses.append([stack[i], stack[i+1], stack[i+2]])
            i += 6


        

    return (positions_of_massive_objects, positions_of_test_masses)







def destacker(stack, stack_info, massive_objects):
    """
    Updates the position and velocity in massive_objects, for massive objects and test masses, given a stack

    Keyword arguments:
    stack -- array of floats, see stacker() method for more information
    stack_info -- array of strings, contains information about what the values in stack correspond to
    massive_objects -- array of class Mass

    Return value:
    None, changes attributes of massive_objects (pass by reference)
    """
    number_of_masses = len(massive_objects)
    positions_of_massive_objects = []
    velocities_of_massive_objects = []
    positions_of_test_masses = []
    velocities_of_test_masses = []
    number_of_test_masses_completed = 0
    i = 0

    #looping over entire stack
    while i < len(stack) - 1:
        if stack_info[i, 1] == "mass":
            #assigns x, y and z coordinates
            positions_of_massive_objects.append([stack[i], stack[i+1], stack[i+2]]) 
            #assigns x, y and z velocities
            velocities_of_massive_objects.append([stack[i+3], stack[i+4], stack[i+5]]) 
            i += 6
        else:
            positions_of_test_masses.append([stack[i], stack[i+1], stack[i+2]])
            velocities_of_test_masses.append([stack[i+3], stack[i+4], stack[i+5]])
            i += 6
    for a in range(number_of_masses):
        massive_objects[a].position = positions_of_massive_objects[a]
        massive_objects[a].velocity = velocities_of_massive_objects[a]
        for b in range(massive_objects[a].number_of_test_masses):
            massive_objects[a].test_masses[b].position = positions_of_test_masses[number_of_test_masses_completed]
            massive_objects[a].test_masses[b].velocity = velocities_of_test_masses[number_of_test_masses_completed]
            number_of_test_masses_completed += 1

  
  
    return None








def forcing_function_massive_object(positions_of_massive_objects, masses, axis, massive_object_number):
    """
    Finds the force acting on massive_object_number in massive_objects array along a particular axis

    Keyword arguments:
    positions_of_massive_objects -- 2D array of floats, [ x y z, ...] positions of all the masses
    masses -- array of floats, masses of each of the massive_objects
    axis -- float, range 0-2 corresponding to x, y, z
    massive_object_number -- the row number of positions_of_massive_objects of the mass 

    Return values:
    force -- float, the force acting on the object along (axis)
    """
    number_of_massive_objects = len(masses)
    force = 0
    for i in range(number_of_massive_objects): #loop over massive objects
        if i == massive_object_number:
            pass #so the mass doesn't exert a force on itself
        else:
            #finding the separation vector
            r_vector = af.distance(positions_of_massive_objects[massive_object_number], positions_of_massive_objects[i])
            r_vector = np.array(r_vector)
            #adds the force due to this mass to the total force
            force += r_vector[axis]*masses[i]*GRAVITATIONAL_CONSTANT/(np.linalg.norm(r_vector)**3) 
    
    
    
    return force







def forcing_function_test_mass(positions_of_massive_objects, masses, axis, position_of_test_mass):
    """
    Finds the force acting on a test mass along a particular axis due to the massive objects

    Keyword arguments:
    positions_of_massive_objects -- 2D array of floats, [ x y z, x y z, ...] positions of all the masses
    masses -- array of floats, masses of each of the massive_objects
    axis -- float, range 0-2 corresponding to x, y, z
    position_of_test_mass -- the position of the test mass on which the force will act

    Return values:
    force -- float, the force acting on the object along (axis)
    """
    force = 0
    for i in range(len(positions_of_massive_objects)):  
        #finding the separation vector
        r_vector = af.distance(position_of_test_mass, positions_of_massive_objects[i]) 
        r_vector = np.array(r_vector)
        #adds the force due to this mass to the total force
        force += r_vector[axis]*masses[i]*GRAVITATIONAL_CONSTANT/(np.linalg.norm(r_vector)**3) 


    return force






def derivative_assignment(time, stack, stack_info, masses): 
    """
    Create and return the values of the derivatives at time, in the same format as stack.

    Keyword arguments:
    time -- float, time at which derivatives are to be evaluated. 
    stack -- array of floats, see stacker() method for more information
    stack_info -- array of strings, contains information about what the values in stack correspond to
    masses -- array of floats, masses of each of the massive_objects

    Return values:
    derivative_stack -- array of floats, of the derivatives to be assigned at time
    """


    derivative_stack = [] #return object

    length_of_stack = len(stack)
    stack = np.array(stack)

    #keeps track of which number mass is being assigned in the separated arrays
    number_of_massive_objects_compelted = 0 
    number_of_test_masses_completed = 0

    i = 0 #counter for each element in stack 

    (positions_of_massive_objects, positions_of_test_masses) = separate_stack(stack, stack_info)
    while i < length_of_stack:  #looping over stack
        if stack_info[i, 1] == "mass":
            for axis in range(3):
                derivative_stack.append(stack[i+3+axis])
            i += 3 #advances to next set of three velocities
            for axis in range(3):
                derivative_stack.append(forcing_function_massive_object(positions_of_massive_objects, masses, axis, number_of_massive_objects_compelted))
            number_of_massive_objects_compelted += 1
            i += 3 #advances to next set of three position coordinates
        else:
            for axis in range(3):
                derivative_stack.append(stack[i+3+axis])
            i += 3
            for axis in range(3):
                derivative_stack.append(forcing_function_test_mass(positions_of_massive_objects, masses, axis, positions_of_test_masses[number_of_test_masses_completed])) 
            number_of_test_masses_completed += 1  
            i += 3



    return derivative_stack





def integrate(stack, stack_info, masses, time, delta_time):
    """
    Takes arguments and passes them to scipy.integrate.solve_ivp()

    Keyword arguments:
    stack -- array of floats, see stacker() method for more information
    stack_info -- array of strings, contains information about what the values in stack correspond to
    masses -- array of floats, masses of each of the massive_objects
    time -- float, the start time from which the system should be solved
    delta_time --  float, the interval over which the system should be solved

    Return values:
    new_stack -- array of floats, the stack at a later time having been integrated
    """


    result = syi.solve_ivp(derivative_assignment, (time, time + delta_time), stack, 'RK45', vectorized = False, args = (stack_info, masses), max_step = STEP_SIZE)
    
    
    return result





    