from raytracing import *

def testXPlane():
    # create 3 x-planes to test on
    XP1, XP2, XP3 = XPlane(0), XPlane(2), XPlane(-2)
    
    # test the x-value assignments and getter
    assert XP1.getX() == 0
    assert XP2.getX() == 2
    assert XP3.getX() == -2
    
    # test the sense function for non-boundary cases
    # direction is not important here
    assert not XP1.sense(-0.01, 0)
    assert XP1.sense(0.00001, 0)
    assert not XP2.sense(1.9, 0)
    assert XP2.sense(2.01, 0)
    assert not XP3.sense(-2.01, 0)
    assert XP3.sense(-1.99, 0)

    # test sense function for boundary cases with
    # a direction that is NOT vertical (should depend
    # on if the point is traveling left or right)

    # XP1
    assert XP1.sense(0, -89)
    assert XP1.sense(0, 89)
    assert not XP1.sense(0, 90.1)
    assert not XP1.sense(0, -91)

    # XP2
    assert XP2.sense(2, -89)
    assert XP2.sense(2, 89.99)
    assert not XP2.sense(2, 90.001)
    assert not XP2.sense(2, -91)

    # XP3
    assert XP3.sense(-2, -89)
    assert XP3.sense(-2, 89)
    assert not XP3.sense(-2, 91)
    assert not XP3.sense(-2, -91)

    # test sense function on boundary with direction
    # directly along plane (direction = 90 or 270)

    assert XP1.sense(0, 90)
    assert XP1.sense(0, 270)
    assert XP2.sense(2, 90)
    assert XP2.sense(2, 270)
    assert XP3.sense(-2, 90)
    assert XP3.sense(-2, 270)

    # test dist_to_boundary

    assert XP1.dist_to_boundary(1, 180) == 1
    assert XP1.dist_to_boundary(1, 0) == None
    assert XP1.dist_to_boundary(1, 150) > 1
    assert XP1.dist_to_boundary(-2, 0) == 2

    assert XP2.dist_to_boundary(1, 180) == None
    assert XP2.dist_to_boundary(1, 0) == 1
    assert XP2.dist_to_boundary(1, 30) > 1
    assert XP2.dist_to_boundary(-2, 0) == 4

    assert XP3.dist_to_boundary(1, 180) == 3
    assert XP3.dist_to_boundary(1, 0) == None
    assert XP3.dist_to_boundary(1, 150) > 3
    assert XP3.dist_to_boundary(-2, 180) == 0

def testYPlane():
    
    # create 3 y-planes to test on
    YP1, YP2, YP3 = YPlane(0), YPlane(2), YPlane(-2)
    
    # test the y-value assignments and getter
    assert YP1.getY() == 0
    assert YP2.getY() == 2
    assert YP3.getY() == -2
    
    # test the sense function for non-boundary cases
    # direction is not important here
    assert not YP1.sense(-0.01, 0)
    assert YP1.sense(0.00001, 0)
    assert not YP2.sense(1.9, 0)
    assert YP2.sense(2.01, 0)
    assert not YP3.sense(-2.01, 0)
    assert YP3.sense(-1.99, 0)

    # test sense function for boundary cases with
    # a direction that is NOT vertical (should depend
    # on if the point is traveling up or down)

    # YP1
    assert YP1.sense(0, 0.1)
    assert YP1.sense(0, 179.9)
    assert not YP1.sense(0, -1)
    assert not YP1.sense(0, -179)

    # YP2
    assert YP2.sense(2, 0.1)
    assert YP2.sense(2, 179.99)
    assert not YP2.sense(2, -0.01)
    assert not YP2.sense(2, -179)

    # YP3
    assert YP3.sense(-2, 0.1)
    assert YP3.sense(-2, 179.9)
    assert not YP3.sense(-2, -0.01)
    assert not YP3.sense(-2, -179)

    # test sense function on boundary with direction
    # directly along plane (direction = 0 or 180)

    assert YP1.sense(0, 0)
    assert YP1.sense(0, 180)
    assert YP2.sense(2, 0)
    assert YP2.sense(2, 180)
    assert YP3.sense(-2, 0)
    assert YP3.sense(-2, 180)

    # test dist_to_boundary

    assert YP1.dist_to_boundary(1, 270) == 1
    assert YP1.dist_to_boundary(1, 0) == None
    assert YP1.dist_to_boundary(1, -20) > 1
    assert YP1.dist_to_boundary(-2, 90) == 2

    assert YP2.dist_to_boundary(1, 90) == 1
    assert YP2.dist_to_boundary(1, -90) == None
    assert YP2.dist_to_boundary(1, 30) > 1
    assert YP2.dist_to_boundary(-2, 90) == 4

    assert YP3.dist_to_boundary(1, 180) == None
    assert YP3.dist_to_boundary(1, 0) == None
    assert YP3.dist_to_boundary(1, -30) > 3
    assert YP3.dist_to_boundary(-2, 90) == 0


def testCircle():

    # create test cases
    C1, C2, C3 = Circle(0, 0, 1), Circle(1,4,2), Circle(-1, 10, 3)
    
    # test assignments and getters
    assert C1.getX() == 0
    assert C1.getY() == 0
    assert C1.get_center() == (0,0)
    assert C1.get_rad() == 1

    assert C2.getX() == 1
    assert C2.getY() == 4
    assert C2.get_center() == (1,4)
    assert C2.get_rad() == 2

    assert C3.getX() == -1
    assert C3.getY() == 10
    assert C3.get_center() == (-1, 10)
    assert C3.get_rad() == 3

    # test sense for points that are inside the circle
    assert C1.sense(0, 0, 0)
    assert C1.sense(0, 0.75, 0)
    assert C1.sense (0.99, 0, 0)
    assert C1.sense(0.5, -0.5, 0)

    assert C2.sense(1, 4, 0)
    assert C2.sense(2.5, 4, 0)
    assert C2.sense(1, 5.9, 0)
    assert C2.sense(2, 3, 0)
    
    assert C3.sense(-1, 10, 0)
    assert C3.sense(-1, 8, 0)
    assert C3.sense(1.8, 10, 0)
    assert C3.sense(1, 9, 0)

    # test sense for points that are outside the circle
    assert not C1.sense(0, 5, 0)
    assert not C1.sense(2, 2, 0)
    assert not C1.sense (0.99, 1.1, 0)

    assert not C2.sense(-1, 5, 0)
    assert not C2.sense(0, 1, 0)
    assert not C2.sense(3, 3, 0)

    assert not C3.sense(4, 10)
    assert not C3.sense(2, 0)
    assert not C3.sense(1.8, 6)

    # test sense for cases on the edge - dependent on motion
    # these test cases are either entering or exiting.
    
    assert not C1.sense(1, 0)
        

    # test dist_to_boundary

def testCell():

    # create testable cells

    # Cell1: circle
    Cell1 = Cell(Circle(0,0,1))

    # Cell2: square
    Cell2 = Cell(XPlane(-1))
    Cell2.add_surface(YPlane(-1))
    Cell2.add_surface(XPlane(1))
    Cell2.add_surface(YPlane(1))
    
    
testXPlane()
print "all x-plane tests passed"
testYPlane()
print "all y-plane tests passed"
testCircle()
print "all circle tests passed"