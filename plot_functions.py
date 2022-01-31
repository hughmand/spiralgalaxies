import numpy as np
import matplotlib.pyplot as plt
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
"""
Contains functions used for creating plots
"""

def plotter(massive_objects, time_given):
    """Produces plot of the positions of all masses in the system, given a massive_objects and a time (float)"""
    position_to_plot_x = []
    position_to_plot_y = []

    for i in range(len(massive_objects)):
        for j in range(len(massive_objects[i].test_masses)):
            position_to_plot_x.append(massive_objects[i].test_masses[j].position[0])
            position_to_plot_y.append(massive_objects[i].test_masses[j].position[1])
    
    figure, axes = plt.subplots()
    axes.scatter(position_to_plot_x, position_to_plot_y, marker = '.', s = 5, linewidths=0.5, label = "Test mass")
    
    position_to_plot_x = []
    position_to_plot_y = []
    for i in range(len(massive_objects)):
            position_to_plot_x.append(massive_objects[i].position[0])
            position_to_plot_y.append(massive_objects[i].position[1])

    axes.scatter(position_to_plot_x, position_to_plot_y, marker = '.', color = 'red', linewidths=0.5, label = "Massive object")
    axes.set_xlabel(r"x coordinate / $\widetilde{m}$")
    axes.set_ylabel(r"y coordinate / $\widetilde{m}$")
    axes.set_title("x-y plane at " + str("{:.0f}".format(time_given)) + "s")
    y_lower, y_upper = massive_objects[0].position[1]-20, massive_objects[0].position[1]+20
    x_lower, x_upper = massive_objects[0].position[0]-20, massive_objects[0].position[0]+20
    plt.ylim([y_lower, y_upper])
    plt.xlim([x_lower, x_upper])
    plt.gca().set_aspect('equal', adjustable='box')
    axes.legend(loc="upper right",bbox_to_anchor=(1, 1), fontsize='xx-small')
    title = "x-y plane at " + str("{:.2f}".format(time_given)) + ".jpg"
    figure.savefig(title,  bbox_inches="tight", dpi=300)
    return None


def energy_against_time(energy, time):
    """Produces plot of energy against time"""
    figure, axes = plt.subplots()
    axes.plot(time, energy)
    axes.set_title("Energy of test masses \n against time")
    axes.set_xlabel("time / s")
    axes.set_ylabel("Energy / Modified Joules")
    figure.savefig('energy_against_time_for_single_orbit.jpg',  bbox_inches="tight", dpi=300)


def tidal_length_against_time(length, time):
    """Produces plot of tidal tail length against time"""
    figure, axes = plt.subplots()
    axes.plot(time, length)
    axes.set_title("Average distance of test masses in tail against time")
    axes.set_xlabel("time / s")
    axes.set_ylabel(r"Distance / $\widetilde{m}$")
    figure.savefig('tidal_length_against_time.jpg',  bbox_inches="tight", dpi=300)

def plot_order(n, times):
    """Produces plot of time to compute against number of test masses"""
    figure, axes = plt.subplots()
    axes.plot(n, times)
    axes.set_title("Time to compute against number of test masses")
    axes.set_xlabel("n")
    axes.set_ylabel("time / s")
    figure.savefig('order.jpg',  bbox_inches="tight", dpi=300)