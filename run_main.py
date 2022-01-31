import numpy as np
from core_functions import *
import accessory_functions as af
from core_classes import *
from plot_functions import *
import time
from global_constants import *
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
"""
Script with different intial conditions used to produce the tidal tail results. 
Changes to the initial conditions made in global_constants.py
"""




#generate the arrays of objects:
massive_objects = [Mass([0,0,0], [0, 0, 0], 1), Mass(GALAXY_POSITION, GALAXY_VELOCITY, GALAXY_MASS)]
massive_objects[0].generate_test_masses()



start = time.time() #timing the run

plotter(massive_objects, 0) #plot initial condition

sim_time = [] #array to store the values of time in the simulation
length_of_tidal_tail = [] #array to store the average length of the tidal tail
closest_approach = 100 #float to store value fo closest approach



for i in range(NUMBER_OF_SNAPSHOTS):
    print("Calculating snapshot number: " + str(i))

    #main integration steps
    (stack, stack_info, masses) = stacker(massive_objects)
    result = integrate(stack, stack_info, masses, 0, DELTA_TIME)
    destacker(result.y[:, -1], stack_info, massive_objects)



    plotter(massive_objects, DELTA_TIME*(i+1)) #produces snapshot image of system
    sim_time.append(DELTA_TIME*(i+1))
    

    #checks approach of the perturbing system, and records the closest distance only.
    approach = np.linalg.norm(af.distance(massive_objects[0].position, massive_objects[1].position))
    if closest_approach > approach:
        closest_approach = approach
    
    #finds massses in tidal tail and their average distance from galaxy centre
    distances_of_masses_in_tail = [] #temporary storage for distances 
    for i in range(massive_objects[0].number_of_test_masses):
        distance = np.linalg.norm(af.distance(massive_objects[0].position, massive_objects[0].test_masses[i].position))
        if 10 < distance: 
            #exlude captured masses
            if 10 < np.linalg.norm(af.distance(massive_objects[1].position, massive_objects[0].test_masses[i].position)):
                distances_of_masses_in_tail.append(distance)
    if len(distances_of_masses_in_tail) == 0: #catches cases where there is no tail
        length_of_tidal_tail.append(0)
    else:
        length_of_tidal_tail.append(np.mean(distances_of_masses_in_tail)) #appends average length for this time




end = time.time() #stop timing
time_difference = end - start #subtracting two floats, caution
print("The results were produced in: " + str(time_difference) + " seconds")



print("The closest approach was: " + str(closest_approach))


#creates tidal length plot
tidal_length_against_time(length_of_tidal_tail, sim_time)
#excludes early on snapshots from mean
print("The mean tidal tail length was: " + str(np.mean(length_of_tidal_tail[10:])))



#The following code is to obtain an estimate of the number of capture masses by the perturbing galaxy.
count = 0
for i in range(massive_objects[0].number_of_test_masses):
    if 10 > np.linalg.norm(af.distance(massive_objects[1].position, massive_objects[0].test_masses[i].position)):
        count += 1 
fraction = count / massive_objects[0].number_of_test_masses


print(str(count) + " test masses were captured by the perturbing galaxy, " + str(fraction) + " of the total")









#def run(n): 


#n = range(1, 50)
#times = [run(i) for i in n]

#plot_order(n, times)

