import numpy as np
"""
Contains global constants that are used throughout the program
"""

#Initial conditions:
GALAXY_POSITION = [12, 12, 0]
GALAXY_VELOCITY = [-0.5,0,0]
GALAXY_MASS = 1

#Change to plot over a different range 
STEP_SIZE = 0.1
NUMBER_OF_SNAPSHOTS = 20
DELTA_TIME = 5 #time between snapshots of system

#Change to alter the scaling of the problem
GRAVITATIONAL_CONSTANT = 1


#For the creation of test masses around massive objects
NUMBER_OF_MASSES_PER_UNIT_RADIUS = 10
MINIMUM_RADIUS = 2
RING_SPACING = 0.25
NUMBER_OF_RINGS = 20
