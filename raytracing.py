import math

class Surface():
    # superclass containing different types of surface
    # i.e. planes, circles, squares, etc.

    # ADD MORE INHERITANCE -- i.e. implement more generalized surface stuff
    # see emailed attachment for more information
    
    # ideally, make it so a meaningful Surface object can be created
    # rather than only XPlane, YPlane, Circle objects

    
    def dist_to_collision(self, x_input, y_input, x_col, y_col):
        return ((x_input - x_col)**2 + (y_input - y_col)**2)**0.5
    
    def dist_to_boundary(self, x_input, y_input, direction):
        if self.find_collision_point(x_input, y_input, direction) == None:
            return None
        x_col, y_col = self.find_collision_point(x_input, y_input, direction)
        return self.dist_to_collision(x_input, y_input, x_col, y_col)
        

# for an x-plane (a plane at a given x-val), the sense test checks
# to see if the x-coordinate is greater than the plane's x-val
class XPlane(Surface):
    def __init__(self, x_val):
        self.x_val = x_val
    def getX(self):
        return self.x_val
    def __lt__(self, xplane):
        assert isinstance(xplane, XPlane)
        return self.getX() < xplane.getX()
    def __gt__(self, xplane):
        assert isinstance(xplane, XPlane)
        return self.getX() > xplane.getX()
    def __eq__(self, xplane):
        if not isinstance(xplane, XPlane):
            return False
        return self.getX() == xplane.getX()
    def sense(self, x_input, y_input, direction):
        # direction is measured in degrees
        # CCW from positive x-axis
        if x_input != self.getX():
            return x_input > self.getX()
        elif direction != 90 and direction != 270:
            x_new = x_input + 0.0001*math.cos(math.radians(direction))
            return x_new > self.getX()
        else:
            # if the direction is directly along the plane,
            # consider this case to be positive/"to the right"
            return True
    def find_collision_point(self, x_input, y_input, direction):
        """Returns the (x,y) location of the collision point in current direction."""
        if self.getX() == x_input:
            # it is already on the boundary
            return (x_input, y_input)
        elif self.sense(x_input, y_input, direction) and math.cos(math.radians(direction)) > 0:
            # this means it will never cross the boundary
            # so it returns None, meaning infinity
            return None
        elif not self.sense(x_input, y_input, direction) and math.cos(math.radians(direction)) < 0:
            # this means it will never cross the boundary
            # so it returns None, meaning infinity
            return None
        elif math.cos(math.radians(direction)) == 0:
            # this means it is moving parallel to the plane and will never reach it
            return None
        else:
            # hypotenuse = adj/cos
            # absolute value for distance
            x_col = self.getX()
            y_col = y_input + (self.getX() - x_input)*math.tan(math.radians(direction))
            return (x_col, y_col)

# this block is now unnecessary
        
##    def dist_to_boundary(self, x_input, y_input, direction):
##        if self.getX() == x_input:
##            return 0
##        elif self.sense(x_input, y_input, direction) and math.cos(math.radians(direction)) > 0:
##            # this means it will never cross the boundary
##            # so it returns None, meaning infinity
##            return None
##        elif not self.sense(x_input, y_input, direction) and math.cos(math.radians(direction)) < 0:
##            # this means it will never cross the boundary
##            # so it returns None, meaning infinity
##            return None
##        elif math.cos(math.radians(direction)) == 0:
##            # this means it is moving parallel to the plane and will never reach it
##            return None
##        else:
##            # hypotenuse = adj/cos
##            # absolute value for distance
##            return abs((x_input - self.getX())/math.cos(math.radians(direction)))

##    def dist_to_boundary(self, x_input, y_input, direction):
##        if self.find_collision_point(x_input, y_input, direction) == None:
##            return None
##        x_col, y_col = self.find_collision_point(x_input, y_input, direction)
##        return self.dist_to_collision(x_input, y_input, x_col, y_col)


class YPlane(Surface):
    def __init__(self, y_val):
        self.y_val = y_val
    def getY(self):
        return self.y_val
    def __lt__(self, yplane):
        assert isinstance(yplane, YPlane)
        return self.getY() < yplane.getY()
    def __gt__(self, yplane):
        assert isinstance(yplane, YPlane)
        return self.getY() > yplane.getY()
    def __eq__(self, yplane):
        if not isinstance(yplane, YPlane):
            return False
        return self.getY() == yplane.getY()
    def sense(self, x_input, y_input, direction):
        if y_input != self.getY():
            return y_input > self.getY()
        elif direction != 0 and direction != 180:
            y_new = y_input + 0.0001*math.sin(math.radians(direction))
            return y_new > self.getY()
        else:
            # if the direction is directly along the plane,
            # consider this case to be positive/"to the right"
            return True

    def find_collision_point(self, x_input, y_input, direction):
        """Returns the (x,y) location of the collision point in current direction."""
        if self.getY() == y_input:
            # it is already on the boundary
            return (x_input, y_input)
        
        if self.sense(x_input, y_input, direction) and math.sin(math.radians(direction)) > 0:
            # this means it will never cross the boundary
            # so it returns None, meaning infinity
            return None
        
        elif not self.sense(x_input, y_input, direction) and math.sin(math.radians(direction)) < 0:
            # this means it will never cross the boundary
            # so it returns None, meaning infinity
            return None
        
        elif math.sin(math.radians(direction)) == 0:
            # this means it is moving parallel to the plane and will never reach it
            return None
        
        else:
            # using trig to find the collision point with the known Y-value
            x_col = x_input + (self.getY() - y_input)/math.tan(math.radians(direction))
            y_col = self.getY()
            return (x_col, y_col)

    
##    def dist_to_boundary(self, x_input, y_input, direction):
##        if self.getY() == y_input:
##            return 0
##        if self.sense(x_input, y_input, direction) and math.sin(math.radians(direction)) > 0:
##            # this means it will never cross the boundary
##            # so it returns None, meaning infinity
##            return None
##        elif not self.sense(x_input, y_input, direction) and math.sin(math.radians(direction)) < 0:
##            # this means it will never cross the boundary
##            # so it returns None, meaning infinity
##            return None
##        elif math.sin(math.radians(direction)) == 0:
##            # this means it is moving parallel to the plane and will never reach it
##            return None
##        else:
##            # hypotenuse = opp/sin
##            # absolute value for distance
##            return abs((y_input - self.getY())/math.sin(math.radians(direction)))
##

class Circle(Surface):
    def __init__(self, x_0, y_0, r):
        self.x_0 = x_0
        self.y_0 = y_0
        self.radius = r
        self.center = (x_0, y_0)
    def getX(self):
        return self.x_0
    def getY(self):
        return self.y_0
    def get_rad(self):
        return self.radius
    def get_center(self):
        return self.center
    def sense(self, x_input, y_input, direction):
        """Returns whether or not the point is inside the circle. If the point is on the boundary of the circle,
            its sense depends on whether it's moving into or out of the circle. If the path is tangent to the circle,
            it is considered within the circle and returns True."""
        
        # first: determine the slope at the point, in case it's a boundary case.
        # doing this here so it doesn't confuse the if/elif/else block later.

        if (self.get_rad()**2 - (x_input-self.getX())**2) < 0:
            return False
            # this means it is outside of the circle.
        elif (self.get_rad()**2 - (x_input-self.getX())**2) == 0:
            slope_at_point = None
            # this means it has a vertical slope at the point (so one of the two sides)
        else:
            slope_at_point = (self.getX()-x_input)/(self.get_rad()**2 - (x_input-self.getX())**2)**0.5           

        # first case: it is NOT along the edges
        if (x_input - self.getX())**2 + (y_input - self.getY())**2 != self.get_rad()**2:
            return (x_input - self.getX())**2 + (y_input - self.getY())**2 < self.get_rad()**2
            # just return if it's within or outside the circle

        # next case: the circle has a vertical slope at (x,y), which matches the direction it is moving - special case of tangency.
        elif slope_at_point == None and math.radians(direction) == math.pi/2 or slope_at_point == None and math.radians(direction) == 3*math.pi/2:
            #it's tangent, with a vertical slope
            return True

        # need to check for tangency again here or else we get false negatives
        elif type(slope_at_point) == float and math.atan(slope_at_point) == math.radians(direction):
            # this means it is tangent to the circle
            return True

        # final case: the slope exists (is not infinite). check to see what happens if we move it over a little.
        else:
            x_new = x_input + 0.0001*math.cos(math.radians(direction))
            y_new = y_input + 0.0001*math.sin(math.radians(direction))
            return self.sense(x_new, y_new, direction)
            # recursive call but only once

    def find_collision_point(self, x_input, y_input, direction):


        # on boundary: return point
        if (x_input - self.getX())**2 + (y_input - self.getY())**2 == self.get_rad()**2:
            return (x_input, y_input)

        # just to clean things up
        dir_rad = math.radians(direction)
        x_0 = self.getX()
        y_0 = self.getY()
        r = self.get_rad()

        # equation to find d:
        # d^2 + 2d(xcos + ysin - hcos - ksin) + (x-h)^2 + (y-k)^2 - r^2 = 0

        a = 1
        b = 2*(x_input*math.cos(dir_rad) + y_input*math.sin(dir_rad) - x_0*math.cos(dir_rad) - y_0*math.sin(dir_rad))
        c = (x_input - x_0)**2 + (y_input - y_0)**2 - r**2

        if (b**2 - 4*c) < 0:
            # no collision
            #print 'quadratic showed no collisions'
            return None

        d_plus = (-b + (b**2 - 4*c)**0.5)/2
        d_minus = (-b - (b**2 - 4*c)**0.5)/2

        if d_minus > 0:
            return (x_input + d_minus*math.cos(dir_rad), y_input + d_minus*math.sin(dir_rad))
            # since that would be the first collision, shorter distance
            
        elif d_plus > 0:
            return (x_input + d_plus*math.cos(dir_rad), y_input + d_plus*math.sin(dir_rad))
            # check to make sure it's a positive distance
            
        else:
            #print 'all collisions were negative direction'
            return None
                
##    def dist_to_boundary(self, x_input, y_input, direction):
##
##        # on boundary: 0
##        if (x_input - self.getX())**2 + (y_input - self.getY())**2 == self.get_rad()**2:
##            return 0
##
##        # next case: starting within the circle
##        elif (x_input - self.getX())**2 + (y_input - self.getY())**2 < self.get_rad()**2:
##            slope = math.tan(math.radians(direction))
##            b = y_input - slope*x_input
##            # referring to y = mx + b


        # steps to accomplish:
        #   1. finding the x,y coords of the point on the circle's edge that is
        #      along the trajectory of the ray
        #           (this means: following direction, using y = mx + b, etc.
        #           to find a point that fits the circle equation and the
        #           linear equation (found using direction))
        #   2. finding the distance between the given point and the target point


        # add function : find collision point, then just find distance to that point (could be inherited)
            
            

        # next case: starting outside the circle, but crossing it
            # SOME CONDITION THAT TELLS IF IT CROSSES THE CIRCLE 

        # next case: starting outside the circle, and tangential

        # next: starting outside circle, missing it
            # this will probably be "else"

class Cell(): # don't have it inherit
    """Takes one surface as initial input, the rest have to be added.

        Currently assumes the shape is a circle or rectangle.

        Surfaces are stored in a list of self.surfaces."""
    def __init__(self, surface):
        self.surfaces = [surface]
    def add_surface(self,new_surface, sense):
        """sense: -1 for left / inside, 1 for right / outside"""
        self.surfaces.append(new_surface, sense)
        
    def get_surfaces(self):
        return self.surfaces
    def am_i_in_cell(self, x, y, direction):

        # circle cell:
        if len(self.get_surfaces()) == 1:            
            # if the cell only has one surface, just return
            # whether or not its 'sense' of that is positive.
            # this is really only meaningful for circles.
            return self.get_surfaces()[0].sense(x, y, direction)
        
        else:
            
            # right now this only supports rectangles (2 XPlanes and 2 YPlanes) and circles
            surface_dict = {'min_x':None, 'max_x':None, 'min_y':None, 'max_y':None, 'circle':None}
            
            for surface in self.get_surfaces():
                if isinstance(surface, XPlane):
                    if surface_dict.get('min_x') == None:
                        surface_dict['min_x'] = surface
                    elif surface < surface_dict.get('min_x'):
                        surface_dict['max_x'] = surface_dict['min_x']
                        surface_dict['min_x'] = surface
                    else:
                        surface_dict['max_x'] = surface
                        
                if isinstance(surface, YPlane):
                    if surface_dict.get('min_y') == None:
                        surface_dict['min_y'] = surface
                    elif surface < surface_dict.get('min_y'):
                        surface_dict['max_y'] = surface_dict['min_y']
                        surface_dict['min_y'] = surface
                    else:
                        surface_dict['max_y'] = surface
                if isinstance(surface, Circle):
                    surface_dict['circle'] = surface

            xmax = surface_dict['max_x']
            xmin = surface_dict['min_x']
            ymax = surface_dict['max_y']
            ymin = surface_dict['min_y']
            circle = surface_dict['circle']


            # plain rectangle case
            if circle == None:
                # return true only if sense passes for the minimums AND fails for the maximums.
                return xmin.sense(x, y, direction) and ymin.sense(x, y, direction) and not xmax.sense(x, y, direction) and not ymax.sense(x, y, direction)
                            

            # rectangle outside a circle
            else:

                # this is for debugging
##                print 'xmin:',xmin.getX(), '; xmin sense', xmin.sense(x, y, direction)
##                print 'ymin:',ymin.getY(), '; ymin sense', ymin.sense(x, y, direction)
##                print 'xmax:',xmax.getX(), '; xmax sense', xmax.sense(x, y, direction)
##                print 'ymax:',ymax.getY(), '; ymax sense', ymax.sense(x, y, direction)
##                print 'circle sense', circle.sense(x, y, direction)
                return xmin.sense(x, y, direction) and ymin.sense(x, y, direction) and not xmax.sense(x, y, direction) and not ymax.sense(x, y, direction) and not circle.sense(x, y, direction)

            # TO DO:

            # generalize Surface so it could actually be used
            # generalize cells (squares in circles, curved sides? etc.)
            # basically just generalize and clean up

            # also plotting. use matplotlib.

            # also read up on unittest vs nose

            # cells don't have to be closed (i.e. everything outside a circle, or everythign outside 3 planes
            # adding surface splits things into half space
            # in_cell: check each surface (check all constraints)
            
            # ADD SURFACE SHOULD INCLUDE DESIRED SENSE (duh)
            # distance to each surface - take min

            # give it a series of surfaces, 
