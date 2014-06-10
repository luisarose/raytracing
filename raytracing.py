import math

class Surface():
    # superclass containing different types of surface
    # i.e. planes, circles, squares, etc.
    pass        
        

# for an x-plane (a plane at a given x-val), the sense test checks
# to see if the x-coordinate is greater than the plane's x-val
class XPlane(Surface):
    def __init__(self, x_val):
        self.x_val = x_val
    def getX(self):
        return self.x_val
    def sense(self, x_input, direction):
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
    def dist_to_boundary(self, x_input, direction):
        if self.getX() == x_input:
            return 0
        elif self.sense(x_input, direction) and math.cos(math.radians(direction)) > 0:
            # this means it will never cross the boundary
            # so it returns None, meaning infinity
            return None
        elif not self.sense(x_input, direction) and math.cos(math.radians(direction)) < 0:
            # this means it will never cross the boundary
            # so it returns None, meaning infinity
            return None
        elif math.cos(math.radians(direction)) == 0:
            # this means it is moving parallel to the plane and will never reach it
            return None
        else:
            # hypotenuse = adj/cos
            # absolute value for distance
            return abs((x_input - self.getX())/math.cos(math.radians(direction)))
        

# for a y-plane, the sense test checks to see if the y-coordinate
# is greater than the plane's y-value
class YPlane(Surface):
    def __init__(self, y_val):
        self.y_val = y_val
    def getY(self):
        return self.y_val
    def sense(self, y_input, direction):
        if y_input != self.getY():
            return y_input > self.getY()
        elif direction != 0 and direction != 180:
            y_new = y_input + 0.0001*math.sin(math.radians(direction))
            return y_new > self.getY()
        else:
            # if the direction is directly along the plane,
            # consider this case to be positive/"to the right"
            return True
    def dist_to_boundary(self, y_input, direction):
        if self.getY() == y_input:
            return 0
        if self.sense(y_input, direction) and math.sin(math.radians(direction)) > 0:
            # this means it will never cross the boundary
            # so it returns None, meaning infinity
            return None
        elif not self.sense(y_input, direction) and math.sin(math.radians(direction)) < 0:
            # this means it will never cross the boundary
            # so it returns None, meaning infinity
            return None
        elif math.sin(math.radians(direction)) == 0:
            # this means it is moving parallel to the plane and will never reach it
            return None
        else:
            # hypotenuse = opp/sin
            # absolute value for distance
            return abs((y_input - self.getY())/math.sin(math.radians(direction)))


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
        if (x_input - self.getX())**2 + (y_input - self.getY())**2 != self.get_rad()**2:
            return (x_input - self.getX())**2 + (y_input - self.getY())**2 < self.get_rad()**2
    
class Cell(Surface):
    def __init__(self, surface):
        self.surfaces = list(surface)
    def add_surface(new_surface):
        self.surfaces.append(new_surface)
    def get_surfaces():
        return self.surfaces
    def am_i_in_cell(self, x, y):
        if len(self.get_surfaces()) == 1:
            return self.get_surfaces()[0].sense(x,y)
        else:
            pass
