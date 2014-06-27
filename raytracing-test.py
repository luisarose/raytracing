from raytracing import *
from surfaces import *
from cells import *
from plot import *
from geometry import *

import numpy
import matplotlib.pyplot as plt

def testSurface():
    S1 = Surface(0, 0, 0, 3, 0, -3) # XPlane(1)
    S2 = Surface(0, 0, 0, 0, 2, 1)  # YPlane(-0.5)
    S3 = Surface(0, 0, 0, 1, 1, 0)  # angled plane
    S4 = Surface(1, 2, 0, 0, 0, -3)  # ellipse!!

    cell = Cell()
    cell.add_surface(S4, True)
    simple_plot(cell, 0)
    plot(cell, 0, -2, 2, -2, 2, 0.1)

    # this is good enough for me

def testXPlane():
    # create 3 x-planes to test on
    XP1, XP2, XP3 = XPlane(0), XPlane(2), XPlane(-2)
    
    # test the x-value assignments and getter
    assert XP1.getX() == 0
    assert XP2.getX() == 2
    assert XP3.getX() == -2
    
    # test the sense function for non-boundary cases
    # direction is not important here
    assert not XP1.sense(-0.01, 0, 0)
    assert XP1.sense(0.00001, 0, 0)
    assert not XP2.sense(1.9, 0, 0)
    assert XP2.sense(2.01, 0, 0)
    assert not XP3.sense(-2.01, 0, 0)
    assert XP3.sense(-1.99, 0, 0)

    # test sense function for boundary cases with
    # a direction that is NOT vertical (should depend
    # on if the point is traveling left or right)

    # XP1
    assert XP1.sense(0, 0, -89)
    assert XP1.sense(0, 0, 89)
    assert not XP1.sense(0, 0, 90.1)
    assert not XP1.sense(0, 0, -91)

    # XP2
    assert XP2.sense(2, 0, -89)
    assert XP2.sense(2, 0, 89.99)
    assert not XP2.sense(2, 0, 90.001)
    assert not XP2.sense(2, 0, -91)

    # XP3
    assert XP3.sense(-2, 0, -89)
    assert XP3.sense(-2, 0, 89)
    assert not XP3.sense(-2, 0, 91)
    assert not XP3.sense(-2, 0, -91)

    # test sense function on boundary with direction
    # directly along plane (direction = 90 or 270)

    assert XP1.sense(0, 0, 90)
    assert XP1.sense(0, 0, 270)
    assert XP2.sense(2, 0, 90)
    assert XP2.sense(2, 0, 270)
    assert XP3.sense(-2, 0, 90)
    assert XP3.sense(-2, 0, 270)

    # test dist_to_boundary

    assert XP1.dist_to_boundary(1, 0, 180) == 1
    assert XP1.dist_to_boundary(1, 0, 0) == None
    assert XP1.dist_to_boundary(1, 0, 150) > 1
    assert XP1.dist_to_boundary(-2, 0, 0) == 2

    assert XP2.dist_to_boundary(1, 0, 180) == None
    assert XP2.dist_to_boundary(1, 0, 0) == 1
    assert XP2.dist_to_boundary(1, 0, 30) > 1
    assert XP2.dist_to_boundary(-2, 0, 0) == 4

    assert XP3.dist_to_boundary(1, 0, 180) == 3
    assert XP3.dist_to_boundary(1, 0, 0) == None
    assert XP3.dist_to_boundary(1, 0, 150) > 3
    assert XP3.dist_to_boundary(-2, 0, 180) == 0

def testYPlane():
    
    # create 3 y-planes to test on
    YP1, YP2, YP3 = YPlane(0), YPlane(2), YPlane(-2)
    
    # test the y-value assignments and getter
    assert YP1.getY() == 0
    assert YP2.getY() == 2
    assert YP3.getY() == -2
    
    # test the sense function for non-boundary cases
    # direction is not important here
    assert not YP1.sense(0, -0.01, 0)
    assert YP1.sense(0, 0.00001, 0)
    assert not YP2.sense(0, 1.9, 0)
    assert YP2.sense(0, 2.01, 0)
    assert not YP3.sense(0, -2.01, 0)
    assert YP3.sense(0, -1.99, 0)

    # test sense function for boundary cases with
    # a direction that is NOT vertical (should depend
    # on if the point is traveling up or down)

    # YP1
    assert YP1.sense(0, 0, 0.1)
    assert YP1.sense(0, 0, 179.9)
    assert not YP1.sense(0, 0, -1)
    assert not YP1.sense(0, 0, -179)

    # YP2
    assert YP2.sense(0, 2, 0.1)
    assert YP2.sense(0, 2, 179.99)
    assert not YP2.sense(0, 2, -0.01)
    assert not YP2.sense(0, 2, -179)

    # YP3
    assert YP3.sense(0, -2, 0.1)
    assert YP3.sense(0, -2, 179.9)
    assert not YP3.sense(0, -2, -0.01)
    assert not YP3.sense(0, -2, -179)

    # test sense function on boundary with direction
    # directly along plane (direction = 0 or 180)

    assert YP1.sense(0, 0, 0)
    assert YP1.sense(0, 0, 180)
    assert YP2.sense(0, 2, 0)
    assert YP2.sense(0, 2, 180)
    assert YP3.sense(0, -2, 0)
    assert YP3.sense(0, -2, 180)

    # test dist_to_boundary

    assert YP1.dist_to_boundary(0, 1, 270) == 1
    assert YP1.dist_to_boundary(0, 1, 0) == None
    assert YP1.dist_to_boundary(0, 1, -20) > 1
    assert YP1.dist_to_boundary(0, -2, 90) == 2

    assert YP2.dist_to_boundary(0, 1, 90) == 1
    assert YP2.dist_to_boundary(0, 1, -90) == None
    assert YP2.dist_to_boundary(0, 1, 30) > 1
    assert YP2.dist_to_boundary(0, -2, 90) == 4

    assert YP3.dist_to_boundary(0, 1, 180) == None
    assert YP3.dist_to_boundary(0, 1, 0) == None
    assert YP3.dist_to_boundary(0, 1, -30) > 3
    assert YP3.dist_to_boundary(0, -2, 90) == 0

def testRectangle():
    
    R1 = Rectangle(0,0,1,1)
    R2 = Rectangle(-1,2,3,4)
    R3 = Rectangle(0,0,4,6)

    #assert R1.sense(2, 2, 0)
    #assert R2.sense(-3, 0, 0)
    #assert R3.sense(-2, -5, 0)

    assert not R1.sense(0,0,0)
    assert not R1.sense(0,0.5,-90)
    assert not R2.sense(-1,2,3)
    assert not R2.sense(-2.5,2,0)
    assert not R3.sense(0,0,0)
    assert not R3.sense(0,-3,90)

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
    assert not C1.sense(0, 0, 0)
    assert not C1.sense(0, 0.75, 0)
    assert not C1.sense (0.99, 0, 0)
    assert not C1.sense(0.5, -0.5, 0)

    assert not C2.sense(1, 4, 0)
    assert not C2.sense(2.5, 4, 0)
    assert not C2.sense(1, 5.9, 0)
    assert not C2.sense(2, 3, 0)
    
    assert not C3.sense(-1, 10, 0)
    assert not C3.sense(-1, 8, 0)
    assert not C3.sense(1.8, 10, 0)
    assert not C3.sense(1, 9, 0)

    # test sense for points that are outside the circle
    assert C1.sense(0, 5, 0)
    assert C1.sense(2, 2, 0)
    assert C1.sense (0.99, 1.1, 0)

    assert C2.sense(-1, 5, 0)
    assert C2.sense(0, 1, 0)
    assert C2.sense(3, 3, 0)

    assert C3.sense(4, 1, 0)
    assert C3.sense(2, 0, 0)
    assert C3.sense(1.8, 6, 0)

    # test sense for cases on the edge - dependent on motion
    # these test cases are either entering or exiting.

    assert not C1.sense(1, 0, 180)
    assert not C2.sense(1, 6, -90)
    assert not C3.sense(-4, 10, 0)


    assert C1.sense(1, 0, 0)
    assert C2.sense(3, 4, 20)
    assert C3.sense(2, 10, 45)

    # test sense for cases with tangent lines - should be
    # considered to be FALSE

    assert not C1.sense(1, 0, 90)
    assert not C2.sense(-1, 4, 270)
    assert not C3.sense(-1, 13, 0)
        

    # test dist_to_boundary

    assert C1.dist_to_boundary(0, 0, 0) == 1
    assert C1.dist_to_boundary(2, 0, 180) == 1
    assert C1.dist_to_boundary(0, 2, 0) == None
    assert C1.dist_to_boundary(0, 0, 38) == 1

    assert C2.dist_to_boundary(1, 4, 280) == 2
    assert C2.dist_to_boundary(2, 4, 0) == 1
    assert C2.dist_to_boundary(1, 6, 200) == 0
    assert C2.dist_to_boundary(1, 5, 90) == 1

    # good enough for me! it works.

def testCell():

    # create testable cells

    # Cell1: circle
    Cell1 = Cell()
    Cell1.add_surface(Circle(0,0,1), False)

    # Cell2: square
    Cell2 = Cell()
    Cell2.add_surface(XPlane(-1), True)
    Cell2.add_surface(YPlane(-1), True)
    Cell2.add_surface(XPlane(1), False)
    Cell2.add_surface(YPlane(1), False)

    # Cell3: circle in a square
    Cell3 = Cell()
    Cell3.add_surface(Circle(1,1,2), True)
    Cell3.add_surface(XPlane(-2), True)
    Cell3.add_surface(XPlane(4), False)
    Cell3.add_surface(YPlane(-2), True)
    Cell3.add_surface(YPlane(4), False)

    # Cell4: 3 planes (X = -1, X = 1, Y = -1) and the curved edge of a circle with r = 1, center (0, 1)
    Cell4 = Cell()
    Cell4.add_surface(XPlane(-1), True)
    Cell4.add_surface(XPlane(1),False)
    Cell4.add_surface(YPlane(-1),True)
    Cell4.add_surface(Circle(0,1,1),False)

    # test get_surfaces (worked as expected)
##    print Cell1.get_surfaces()
##    print Cell2.get_surfaces()
##    print Cell3.get_surfaces()

    # test in_cell

    # Cell1: just a circle
    assert Cell1.in_cell(0, 0, 0)
    assert Cell1.in_cell(0, 0.5, 90)
    assert Cell1.in_cell(1, 0, 180)
    assert not Cell1.in_cell(1, 0, 0)
    assert not Cell1.in_cell(2, 2, 90)

    # Cell2: square, len 2, centered at (0,0)
    assert Cell2.in_cell(0, 0, 180)
    assert Cell2.in_cell(-1,-1,45)
    assert not Cell2.in_cell(-2, -1, 0)
    assert not Cell2.in_cell(-1,-1,-5)

    # Cell3: square of len 6 centered at (1,1) with a circle cutout (rad 2, center (1,1)).
    assert not Cell3.in_cell(1,1,0)
    assert not Cell3.in_cell(1,3,-90)
    assert not Cell3.in_cell(1,3,0) # tangent to circle = circle sense True = am_i_in False
    assert Cell3.in_cell(1,3.1,0)

    # Cell4: 3 planes (X = -1, X = 1, Y = -1) and the curved edge of a circle with r = 1, center (0, 1)
    assert Cell4.in_cell(0,0,0)
    assert Cell4.in_cell(-1,1,0)
    assert Cell4.in_cell(0,2,0)
    assert not Cell4.in_cell(0,3,0)
    assert not Cell4.in_cell(0,2,90)

def test_plot():

    # create test cells
    test_cell1 = Cell()
    test_cell1.add_surface(Circle(0,0,2), False) # inside a circle (r = 2)
    test_cell1.add_surface(Rectangle(0, 0, 0.5, 0.5), True) # outside a square (l = 1)

    test_cell2 = Cell()
    test_cell2.add_surface(Circle(1,1,2), True) # outside a circle
    test_cell2.add_surface(Circle(0,0,4), False) # inside a larger circle

    test_cell3 = Cell()
    test_cell3.add_surface(Rectangle(0,0,2,2), False) # inside a rectangle
    test_cell3.add_surface(Circle(0,0,1), True) # outside a circle

    test_cell4 = Cell()
    test_cell4.add_surface(Rectangle(0,0,5,5),False)
    test_cell4.add_surface(Rectangle(0,0,3,3), True)

    # call simple_plot or plot
    simple_plot(test_cell1, 0)
    simple_plot(test_cell2, 0)
    simple_plot(test_cell3, 0)
    simple_plot(test_cell4, 0)

    plot(test_cell1, 0, -5, 10, -5, 5, 0.1)

def testGeometry():

    # generate geometry: circle cell inside a square cell (w/ circle cutout)
    box = Rectangle(0,0,10,10)
    print 'made box'
    G = Geometry(box)
    print 'made geometry'
    cell1 = Cell()
    cell1.add_surface(Circle(0,0,4),False)
    cell2 = Cell()
    cell2.add_surface(Circle(0,0,4),True)
    cell2.add_surface(box,False)

    cell1_id = G.generate_ID('next_cell_ID')
    cell2_id = G.generate_ID('next_cell_ID')
    G.add_cell(cell1, cell1_id)
    G.add_cell(cell2, cell2_id)

##    G.make_tracks(45, 0.2)
##    G.make_tracks(90, .2)
##    G.make_tracks(0, .2)
##    G.make_tracks(22.5, 0.2)
##    G.make_tracks(67.5, 0.2)

    tracks = G.get_tracks()


def testPlotTracks():
    """Test plotting tracks"""

    # make geometry: circle inside a square
    box = Rectangle(0,0,10,10)
    G = Geometry(box)
    cell1 = Cell()
    cell1.add_surface(Circle(0,0,4),False)
    cell1.add_surface(Circle(0,0,1),True)
    cell2 = Cell()
    cell2.add_surface(Circle(0,0,4),True)
    cell2.add_surface(box,False)
    cell3 = Cell()
    cell3.add_surface(Circle(0,0,1),False)

    cell1_id = G.generate_ID('next_cell_ID')
    cell2_id = G.generate_ID('next_cell_ID')
    cell3_id = G.generate_ID('next_cell_ID')
    G.add_cell(cell1, cell1_id)
    G.add_cell(cell2, cell2_id)
    G.add_cell(cell3, cell3_id)

    # complicated geometry: has 7 cells
    G2 = Geometry(box)
    XP1 = XPlane(0)
    
    cell1a = Cell()
    cell1a.add_surface(Circle(0,0,4),False)
    cell1a.add_surface(Circle(0,0,1),True)
    cell1a.add_surface(XP1, True)
    
    cell1b = Cell()
    cell1b.add_surface(Circle(0,0,4),False)
    cell1b.add_surface(Circle(0,0,1),True)
    cell1b.add_surface(XP1, False)
    
    cell2a = Cell()
    cell2a.add_surface(Circle(0,0,4),True)
    cell2a.add_surface(box,False)
    cell2a.add_surface(XP1,True)
    cell2a.add_surface(Rectangle(0,0,8,8),False)
    
    cell2b = Cell()
    cell2b.add_surface(Circle(0,0,4),True)
    cell2b.add_surface(box,False)
    cell2b.add_surface(XP1,False)
    cell2b.add_surface(Rectangle(0,0,8,8),False)


    cell3a = Cell()
    cell3a.add_surface(Circle(0,0,1),False)
    cell3a.add_surface(XP1,False)
    
    cell3b = Cell()
    cell3b.add_surface(Circle(0,0,1),False)
    cell3b.add_surface(XP1,True)

    cell4 = Cell()
    cell4.add_surface(Rectangle(0,0,8,8),True)
    cell4.add_surface(box, False)

    cell1a_id = G2.generate_ID('next_cell_ID')
    cell1b_id = G2.generate_ID('next_cell_ID')
    cell2a_id = G2.generate_ID('next_cell_ID')
    cell2b_id = G2.generate_ID('next_cell_ID')
    cell3a_id = G2.generate_ID('next_cell_ID')
    cell3b_id = G2.generate_ID('next_cell_ID')
    cell4_id = G2.generate_ID('next_cell_ID')
    G2.add_cell(cell1a, cell1a_id)
    G2.add_cell(cell1b, cell1b_id)
    G2.add_cell(cell2a, cell2a_id)
    G2.add_cell(cell2b, cell2b_id)
    G2.add_cell(cell3a, cell3a_id)
    G2.add_cell(cell3b, cell3b_id)
    G2.add_cell(cell4, cell4_id)

    # make list of directions to plot
    dir_list = [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165]
    dir_list2 = []
    tempdir = 0

    while tempdir < 180:
        dir_list2.append(tempdir)
        tempdir += 10

    print 'about to plot G with dir_list and 0.3 spacing'
    make_and_plot_tracks(G, dir_list, 0.3)
    print 'done'


#### 0 and 90 cause infinite loops.. current solution is just to move them over .0001 ####

    print 'about to plot G2 with dir_list2 and 0.5 spacing'
    make_and_plot_tracks(G2, dir_list2, 0.5)
    print 'done'
    

##testSurface()
##testXPlane()
##print "all x-plane tests passed"
##testYPlane()
##print "all y-plane tests passed"
##testRectangle()
##print "all rectangle tests passed"
##testCircle()
##print "all circle tests passed"
##testCell()
##print "all cell tests passed"
##test_plot()
##print "done plotting"
testPlotTracks()
