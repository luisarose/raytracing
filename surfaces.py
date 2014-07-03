import math

# direction = angle in degrees, on interval [0, 360], measured CCW from pos x-axis.

class Surface():
    """Superclass containing other types of Surface: XPlane, YPlane,
    Circle, Rectangle. Can also be initialized with 6 variables (a,
    b, f, p, q, d)."""
    def __init__(self, a, b, f, p,q, d):

        self.a = a
        # a is the coefficient for x^2
        
        self.b = b
        # b is the coefficient for y^2

        self.f = f
        # f is the coefficient for xy

        self.p = p
        # p is the coefficient for x
        
        self.q = q
        # q is the coefficient for y

        self.d = d
        # d is the number added to get 0

        # full equation of a quadratic surface:
        # a*x**2 + b*y**2 + f*x*y + p*x + q*y + d = 0
        
    def get_a(self):
        return self.a
    def get_b(self):
        return self.b
    def get_f(self):
        return self.f
    def get_p(self):
        return self.p
    def get_q(self):
        return self.q
    def get_d(self):
        return self.d
    def sense(self, x, y, direction):
        a = self.get_a()
        b = self.get_b()
        d = self.get_d()
        f = self.get_f()
        p = self.get_p()
        q = self.get_q()
        d = self.get_d()

        value = a*x**2 + b*y**2 + f*x*y + p*x + q*y + d

        if value != 0:
            return value > 0
        else:
            rad_dir = math.radians(direction)
            new_x = x + math.cos(rad_dir)*0.0001
            new_y = x + math.cos(rad_dir)*0.0001
            return sense(self, new_x, new_y, direction)
        
            # this DOES NOT work for cases where the
            # path is directly along a plane (infinite loop)
            
    def dist_to_collision(self, x_input, y_input, x_col, y_col):
        return ((x_input - x_col)**2 + (y_input - y_col)**2)**0.5
    
    def dist_to_boundary(self, x_input, y_input, direction):
        if self.find_collision_point(x_input, y_input, direction) == None:
            return None
        x_col, y_col = self.find_collision_point(x_input, y_input, direction)
        return self.dist_to_collision(x_input, y_input, x_col, y_col)




class XPlane(Surface):
    """Subclass of Surface. Takes the x value as parameter.
    Sense test checks to see if the point is to the right."""
    def __init__(self, x_val):
        self.x_val = x_val
    def getX(self):
        return self.x_val
    
    def sense(self, x_input, y_input, direction):
        if x_input != self.getX():
            return x_input > self.getX()
        elif direction != 90 and direction != 270:
            x_new = x_input + 0.0001*math.cos(math.radians(direction))
            return x_new > self.getX()
        else:
            # moving directly along plane = True
            return True
        
    def find_collision_point(self, x_input, y_input, direction):
        """Returns the (x,y) location of the collision point in current direction."""
        if self.getX() == x_input:
            # it is already on the boundary
            return (x_input, y_input)
        elif self.sense(x_input, y_input, direction) and math.cos(math.radians(direction)) > 0:
            # to the right and traveling right
            # this means it will never cross the boundary
            return None
        elif not self.sense(x_input, y_input, direction) and math.cos(math.radians(direction)) < 0:
            # to the left and traveling left
            # this means it will never cross the boundary
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




class YPlane(Surface):
    """Subclass of Surface. Takes the y value as parameter.
    Sense test checks to see if the point is above it."""
    def __init__(self, y_val):
        self.y_val = y_val
    def getY(self):
        return self.y_val
    
    def sense(self, x_input, y_input, direction):
        if y_input != self.getY():
            return y_input > self.getY()
        elif direction != 0 and direction != 180:
            y_new = y_input + 0.0001*math.sin(math.radians(direction))
            return y_new > self.getY()
        else:
            # moving directly along plane = True
            return True

    def find_collision_point(self, x_input, y_input, direction):
        """Returns the (x,y) location of the collision point in current direction."""
        if self.getY() == y_input:
            # it is already on the boundary
            return (x_input, y_input)
        
        if self.sense(x_input, y_input, direction) and math.sin(math.radians(direction)) > 0:
            # above and moving up
            # this means it will never cross the boundary
            return None
        
        elif not self.sense(x_input, y_input, direction) and math.sin(math.radians(direction)) < 0:
            # below and moving down
            # this means it will never cross the boundary
            return None
        
        elif math.sin(math.radians(direction)) == 0:
            # this means it is moving parallel to the plane and will never reach it
            return None
        
        else:
            # using trig to find the collision point with the known Y-value
            x_col = x_input + (self.getY() - y_input)/math.tan(math.radians(direction))
            y_col = self.getY()
            return (x_col, y_col)





class Rectangle(Surface):
    """Takes in the center, its horizontal length, and vertical length.
        x_0, y_0 = center
        x_len = length across (horizontal)
        y_len = length down (vertical)

        Made up of four planes, generated when it's initialized."""
    def __init__(self, x_0, y_0, x_len, y_len):
        self.center = (x_0, y_0)
        self.surfaces = [(XPlane(x_0-(x_len*0.5)),True), (XPlane(x_0 + (x_len*0.5)),False), (YPlane(y_0 - (y_len*0.5)),True), (YPlane(y_0 + (y_len*0.5)),False)]
        self.x_len = x_len
        self.y_len = y_len
    def get_center(self):
        return self.center
    def get_xlen(self):
        return self.x_len
    def get_ylen(self):
        return self.y_len
    def get_surfaces(self):
        return self.surfaces
    
    def sense(self, x, y, direction):
        surfaces = self.get_surfaces()
        for surface in surfaces:
            if surface[0].sense(x, y, direction) != surface[1]:
            # if the point fails any of the 4 sense checks
                return True # outside
        return False
        
    def find_collision_point(self, x, y, direction):
        """Finds collision point by making dictionary of distances and collision
        points for each of the 4 boundaries. Returns the point with the minimum
        distance that is not None (meaning there is no collision)."""
        possible_points = {}
        for surface in self.get_surfaces():
            possible_point = surface[0].find_collision_point(x,y,direction)
            if possible_point != None:
                pos_x, pos_y = possible_point
                poss_dist = self.dist_to_collision(x, y, pos_x, pos_y)
                possible_points[poss_dist] = possible_point
        return possible_points[min(possible_points)]
    
    def dist_to_boundary(self, x, y, direction):
        """Similar to find_collision_point, but doesn't use dictionary since
        the points don't matter."""
        list_of_distances = []
        surfaces = self.get_surfaces()
        for surface_tup in surfaces:
            surface = surface_tup[0]
            dist = surface.dist_to_boundary(x, y, direction)
            if type(dist) == float or type(dist) == int:
                list_of_distances.append(dist)
        if len(list_of_distances) == 0:
            return None
        return min(list_of_distances)






class Circle(Surface):
    """Subclass of Surface. Takes its center coordinates and radius as parameters."""
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
        """Returns False for inside circle and True for outside. If the point is on the boundary of the circle,
            its sense depends on whether it's moving into or out of the circle. If the path is tangent to the circle,
            it is considered within the circle and returns False."""

        # simple cases first: inside or outside circle
        if self.get_rad()**2 < (x_input-self.getX())**2 + (y_input-self.getY())**2:
            return True
        elif self.get_rad()**2 > (x_input-self.getX())**2 + (y_input-self.getY())**2:
            return False
            # this means it is outside of the circle.

        # boundary cases

        elif (self.get_rad()**2 == (x_input-self.getX())**2):
            slope_at_point = None # vertical slope
        else:
            slope_at_point = (self.getX()-x_input)/(self.get_rad()**2 - (x_input-self.getX())**2)**0.5 # calculates slope          
        
        # tangent path case - vertical slope
        if slope_at_point == None and math.radians(direction) == math.pi/2 or slope_at_point == None and math.radians(direction) == 3*math.pi/2:
            return False

        # tangent path case - slope is not vertical
        elif type(slope_at_point) == float and math.atan(slope_at_point) == math.radians(direction):
            return False

        # final case: the slope exists (is not vertical), on boundary, but path is not tangent to circle
        # either entering or leaving circle - take small step and test again
        else:
            x_new = x_input + 0.0001*math.cos(math.radians(direction))
            y_new = y_input + 0.0001*math.sin(math.radians(direction))
            return self.sense(x_new, y_new, direction)

    def find_collision_point(self, x_input, y_input, direction):

        # on boundary: return point
        if abs((x_input - self.getX())**2 + (y_input - self.getY())**2 - self.get_rad()**2) < 0.0001:
            return (x_input, y_input)

        # just to clean things up
        dir_rad = math.radians(direction)
        x_0 = self.getX()
        y_0 = self.getY()
        r = self.get_rad()

        # equation to find d:
        # d^2 + 2d(xcos + ysin - hcos - ksin) + (x-h)^2 + (y-k)^2 - r^2 = 0

        # coefficients from the equation
        a = 1
        b = 2*(x_input*math.cos(dir_rad) + y_input*math.sin(dir_rad) - x_0*math.cos(dir_rad) - y_0*math.sin(dir_rad))
        c = (x_input - x_0)**2 + (y_input - y_0)**2 - r**2

        if (b**2 - 4*c) < 0:
            # no collision
            return None

        # apply quadratic formula: d_plus is the greater distance, d_minus is the lesser (could be the same value)
        d_plus = (-b + (b**2 - 4*c)**0.5)/2
        d_minus = (-b - (b**2 - 4*c)**0.5)/2

        if d_minus > 0:
            return (x_input + d_minus*math.cos(dir_rad), y_input + d_minus*math.sin(dir_rad))
            # since that would be the first collision, shorter distance
            # this would also work with a single intersection (tangent)
            
        elif d_plus > 0:
            return (x_input + d_plus*math.cos(dir_rad), y_input + d_plus*math.sin(dir_rad))
            
        else:
            return None
