from surfaces import *

import math    

class Cell():
    """Takes one surface as initial input, the rest have to be added.
        Surfaces are stored in a list of self.surfaces."""
    def __init__(self):
        self.surfaces = []
    def add_surface(self, new_surface, sense):
        """Takes in the surface and the sense for that surface.
        sense: False for left/inside, True for right/outside."""
        self.surfaces.append((new_surface, sense))
    def get_surfaces(self):
        return self.surfaces
    
    def in_cell(self, x, y, direction):
        """Returns True if point is within cell.""" 
        surfaces = self.get_surfaces()
        for surface in surfaces:
            if surface[0].sense(x, y, direction) != surface[1]:
                return False
        return True
    
    def dist_to_boundary(self, x, y, direction):
        """Finds shortest distance to the boundary of the cell."""
        list_of_distances = []
        surfaces = self.get_surfaces()
        for surface in surfaces:
            dist = surface[0].dist_to_boundary(x, y, direction)
            print dist
            if dist != None:
                list_of_distances.append(dist)
        return min(list_of_distances)
    
    def find_collision_point(self, x, y, direction):
        """Finds collision point with edge of cell in given direction."""
        dict_of_distances = {}
        surfaces = self.get_surfaces()
        for surface in surfaces:
            dist = surface[0].dist_to_boundary(x, y, direction)
            if dist != None:
                dict_of_distances[dist] = surface[0].find_collision_point(x, y, direction)
        return dict_of_distances[min(dict_of_distances)]
