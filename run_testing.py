import numpy as np
import accessory_functions as af
import core_functions as cf
from core_classes import *
import plot_functions as pf
from global_constants import *
import time
from pympler.tracker import SummaryTracker
tracker = SummaryTracker()

np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
"""Script to check the stability and performance of the program""" 


#Check stability of orbits of test masses:
massive_objects = [Mass([0,0,0], [0,0,0], 1)]
massive_objects[0].generate_test_masses()

energies  = [] #array to store energies
energies.append(af.energy_of_test_masses(massive_objects))
sim_time = [0] #array to keep track of simulation time
time_period = 0
time_period_found = False #bool to mark exit from loop

start = time.time() #timing the run

for i in range(NUMBER_OF_SNAPSHOTS):
    print("Calculating snapshot number: " + str(i))

    #main integration method
    (stack, stack_info, masses) = cf.stacker(massive_objects)
    result = cf.integrate(stack, stack_info, masses, 0, DELTA_TIME)
    cf.destacker(result.y[:, -1], stack_info, massive_objects)


    if result.success == 1: #checks if integration method worked correctly
        pass
    else:
        print(result.message) #prints out why solve_ivp exited without completing


    sim_time.append(DELTA_TIME*(i+1))


    #records energy of snapshot
    energies.append(af.energy_of_test_masses(massive_objects))
    
    #checks for whether half orbit has been completed by looking for sign change
    #works best for small DELTA_TIME
    if time_period_found == False:
        if massive_objects[0].test_masses[0].position[1] > -0.0001:
            time_period = sim_time[i+1]
        else:
            time_period_found = True
    tracker.print_diff() #outputs the difference in objects in memory since last call

end = time.time() #stop timing

time_difference = end - start #subtracting two floats, caution
print("The results were produced in: " + str(time_difference) + " seconds")

energy_difference = np.std(energies)
pf.energy_against_time(energies, sim_time)
print("The standard deviation in the energy is: " + str(energy_difference))
print("The difference from the start to the end of the energy is: " + str(energies[0] - energies[-1]))

print("The time period of the orbit is: " + str(2*time_period))
print("The system was integrated from 0 to " + str(DELTA_TIME*(NUMBER_OF_SNAPSHOTS+1)) + " seconds")







#Now for the two-body problem, much of this is repeated from above
massive_objects = [Mass([0,-5,0], [-0.2, 0 ,0], 1), Mass(GALAXY_POSITION, GALAXY_VELOCITY, GALAXY_MASS)]

sim_time = [0]
energies = [af.energy_of_massive_objects(massive_objects)]

start = time.time() #timing the run

pf.plotter(massive_objects, 0) #plot initial positions

for i in range(NUMBER_OF_SNAPSHOTS):
    

    (stack, stack_info, masses) = cf.stacker(massive_objects)
    result = cf.integrate(stack, stack_info, masses, 0, DELTA_TIME)
    cf.destacker(result.y[:, -1], stack_info, massive_objects)


    if result.success == 1: #checks if integration method worked correctly
        pass
    else:
        print(result.message) #prints out why solve_ivp exited without compeleting


    sim_time.append(DELTA_TIME*(i+1))
    energies.append(af.energy_of_massive_objects(massive_objects))
    pf.plotter(massive_objects, DELTA_TIME*(i+1))

end = time.time() #stop timing
time_difference = end - start #subtracting two floats, caution
print("The system was integrated from 0 to " + str(DELTA_TIME*(NUMBER_OF_SNAPSHOTS+1)) + " seconds")
print("The results were produced in: " + str(time_difference) + " seconds")

energy_difference = np.std(energies)
print("The standard deviation in the energy is: " + str(energy_difference))
print("The difference from the start to the end of the energy is: " + str(energies[0] - energies[-1]))
pf.energy_against_time(energies, sim_time)
