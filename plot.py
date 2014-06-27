from raytracing import *
from surfaces import *
from cells import *
from geometry import *

import math
import numpy
import matplotlib.pyplot as plt


def plot(cell, direction, xmin, xmax, ymin, ymax, step):
    """Takes in the cell, the direction of the particles (uniform here), the limits of the plot,
        and the step size between points (same for x and y)."""
    
    to_plot_red = []
    # this is for things that are not in the cell
    to_plot_blue = []
    # this is for things that ARE in the cell

    # create test points
    x = []
    x_current = xmin
    while x_current < xmax:
        x.append(x_current)
        x_current += step

    y = []
    y_current = ymin
    while y_current < ymax:
        y.append(y_current)
        y_current += step

    for x_val in x:
        for y_val in y:
            point = (x_val, y_val)
            in_cell = cell.in_cell(x_val, y_val, direction)
            if in_cell:
                to_plot_blue.append([x_val, y_val])
            else:
                to_plot_red.append([x_val, y_val])

    # splits the list of points into x and y lists for plt
    x_red = [x for [x, y] in to_plot_red]
    y_red = [y for [x, y] in to_plot_red]
    # splits the list of points into x and y lists for plt
    x_blue = [x for [x, y] in to_plot_blue]
    y_blue = [y for [x, y] in to_plot_blue]

    # make plots
    plt.plot(x_red, y_red, marker='.', color='r', linestyle='None')
    plt.plot(x_blue, y_blue, marker='.',color='b', linestyle='None')
    plt.show()

def simple_plot(cell, direction):
    """Takes in cell and direction, plots on a graph of -5 to 5 for
        both x and y. Step size is 0.1"""
    plot(cell, direction, -5, 5, -5, 5, 0.1)    

def make_and_plot_tracks(geometry, directions, track_spacing):
    """Takes in a geometry (with cells), a list of direction, and track spacing.
    directions = list of directions to lay tracks
    Creates tracks for all directions and plots them."""

    num_dir = len(directions)
    for i in xrange(num_dir):
        geometry.make_tracks(directions[i], track_spacing)
    plot_tracks(geometry)
    
def plot_tracks(geometry):
    colors = ['b', 'r', 'c', 'm', 'y', 'g', 'k', 'pink']
    num_tracks = len(geometry.get_tracks())
    for j in xrange(1, num_tracks+1):
        track = geometry.get_tracks()[j]
        # look at each track
        for k in track.get_segments():
            segment = track.get_segments()[k]
            # look at each segment
            direction = track.get_direction()
            x_step = 0.0001*math.cos(math.radians(direction))
            y_step = 0.0001*math.sin(math.radians(direction))
            # using x_step and y_step fixes boundary problems
            x_0 = segment.get_start()[0] + x_step
            y_0 = segment.get_start()[1] + y_step
            x_f = segment.get_endpt()[0] - x_step
            y_f = segment.get_endpt()[1] - y_step
            cell_ID = geometry.which_cell(x_0, y_0, track.get_direction())[0]
            # cell ID determines color of segment
            plt.plot([x_0, x_f], [y_0, y_f], color=colors[cell_ID-1])
            
    plt.show()
