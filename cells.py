from surfaces import *

import math    

class Cell():
    """Takes one surface as initial input, the rest have to be added.
        Surfaces are stored in a list of self.surfaces."""
    def __init__(self):
        self.surfaces = []
    def add_surface(self, new_surface, sense):
        """sense: False for left/inside, True for right/outside"""
        if isinstance(new_surface, Rectangle) and not sense:
            for surface in new_surface.get_surfaces():
                self.surfaces.append((surface[0], surface[1]))
        else:
            self.surfaces.append((new_surface, sense))
    def get_surfaces(self):
        return self.surfaces
    def in_cell(self, x, y, direction):
        surfaces = self.get_surfaces()
        for surface in surfaces:
##            if isinstance(surface, Rectangle) and sense:
##                surface.sense(x,y,direction)
            if surface[0].sense(x, y, direction) != surface[1]:
                return False
        return True
    def dist_to_boundary(self, x, y, direction):
        list_of_distances = []
        surfaces = self.get_surfaces()
        for surface in surfaces:
            dist = surface[0].dist_to_boundary(x, y, direction)
            print dist
            if dist != None:
                list_of_distances.append(dist)
        return min(list_of_distances)
    def find_collision_point(self, x, y, direction):
        dict_of_distances = {}
        surfaces = self.get_surfaces()
        for surface in surfaces:
            dist = surface[0].dist_to_boundary(x, y, direction)
            if dist != None:
                dict_of_distances[dist] = surface[0].find_collision_point(x, y, direction)
#        if dict_of_distances == {}:
            # debugging
##            print "STOP AND READ THIS"
##            print "******************"
##            print x, y
##            print "why would that have no distances?"
##            print self.in_cell(x,y,direction)
##            print self.dist_to_boundary(x, y, direction)
        return dict_of_distances[min(dict_of_distances)]
