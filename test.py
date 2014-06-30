from raytracing import *
from surfaces import *
from cells import *
from plot import *
from geometry import *
import unittest

class surface_tests(unittest.TestCase):

    def setUp(self):
        """Creates surface instances for use in this set of test cases."""
        self.XP1 = XPlane(0)
        self.XP2 = XPlane(2)
        self.XP3 = XPlane(-2)

        self.YP1 = YPlane(0)
        self.YP2 = YPlane(2)
        self.YP3 = YPlane(-2)

        self.R1 = Rectangle(0,0,1,1)
        self.R2 = Rectangle(-1,2,3,4)
        self.R3 = Rectangle(0,0,4,6)

        self.C1 = Circle(0,0,1)
        self.C2 = Circle(1,4,2)
        self.C3 = Circle(-1,10,3)

    def test_xplane_getters(self):
        """Tests the getX method of XPlane."""
        self.failUnless(self.XP1.getX() == 0 and self.XP2.getX() == 2 and self.XP3.getX() == -2)
        
    def test_xplane_sense_simple(self):
        """Simple cases, where the point is either to the right
        or to the left of the XPlane. Direction doesn't matter.
        False = to the left
        True = to the right"""
        self.assertTrue(self.XP1.sense(0.00001, 0, 0))
        self.assertTrue(self.XP2.sense(2.01, 0, 0))
        self.assertTrue(self.XP3.sense(-1.99, 0, 0))
        
        self.assertFalse(self.XP1.sense(-0.01, 0, 0))
        self.assertFalse(self.XP2.sense(1.9, 0, 0))
        self.assertFalse(self.XP3.sense(-2.01, 0, 0))

    def test_xplane_sense_boundary(self):
        """Cases where the point is on the XPlane and is either moving
        to the right or left. Direction (left/right) determines sense.
        False = moving left
        True = moving right"""
        self.assertTrue(self.XP1.sense(0, 0, -89))
        self.assertTrue(self.XP1.sense(0, 0, 89))
        self.assertTrue(self.XP2.sense(2, 0, -89))
        self.assertTrue(self.XP2.sense(2, 0, 89.99))
        self.assertTrue(self.XP3.sense(-2, 0, -89))
        self.assertTrue(self.XP3.sense(-2, 0, 89))
        
        self.assertFalse(self.XP1.sense(0,0,90.1))
        self.assertFalse(self.XP1.sense(0,0,-91))
        self.assertFalse(self.XP2.sense(2.0, 0, 91))
        self.assertFalse(self.XP2.sense(2.0, 0, -91))
        self.assertFalse(self.XP3.sense(-2.0, 0, 91))
        self.assertFalse(self.XP3.sense(-2.0, 0, -90.1))

    def test_xplane_sense_boundary2(self):
        """Cases where the point is on the XPlane and is traveling
        directly along the plane. Returns True."""
        self.assertTrue(self.XP1.sense(0, 0, 90))
        self.assertTrue(self.XP1.sense(0, 0, 270))
        self.assertTrue(self.XP2.sense(2, 0, 90))
        self.assertTrue(self.XP2.sense(2, 0, 270))
        self.assertTrue(self.XP3.sense(-2, 0, 90))
        self.assertTrue(self.XP3.sense(-2, 0, 270))
        
        
    def test_xplane_dist_to_boundary(self):
        """Takes the point x, y and the direction of motion.
        Returns None if the path doesn't collide with the XPlane."""
        self.assertEqual(self.XP1.dist_to_boundary(1, 0, 180),1)
        self.assertEqual(self.XP1.dist_to_boundary(1, 0, 0), None)
        self.assertTrue(self.XP1.dist_to_boundary(1, 0, 150) > 1)
        self.assertEqual(self.XP1.dist_to_boundary(-2, 0, 0), 2)

        self.assertEqual(self.XP2.dist_to_boundary(1, 0, 180), None)
        self.assertEqual(self.XP2.dist_to_boundary(1, 0, 0),1)
        self.assertTrue(self.XP2.dist_to_boundary(1, 0, 30) > 1)
        self.assertEqual(self.XP2.dist_to_boundary(-2, 0, 0), 4)

        self.assertEqual(self.XP3.dist_to_boundary(1, 0, 180),3)
        self.assertEqual(self.XP3.dist_to_boundary(1, 0, 0), None)
        self.assertTrue(self.XP3.dist_to_boundary(1, 0, 150) > 3)
        self.assertEqual(self.XP3.dist_to_boundary(-2, 0, 180),0)


    def test_yplane_getters(self):
        """Tests the getY method of YPlane."""
        self.failUnless(self.YP1.getY() == 0 and self.YP2.getY() == 2 and self.YP3.getY() == -2)
        
    def test_yplane_sense_simple(self):
        """Simple cases: where the point is either above or below the YPlane.
        Direction doesn't matter; position determines sense.
        False = below / True = above"""
        self.assertTrue(self.YP1.sense(0, 0.00001, 0))
        self.assertTrue(self.YP2.sense(0, 2.01, 0))
        self.assertTrue(self.YP3.sense(0, -1.99, 0))
        
        self.assertFalse(self.YP1.sense(0, -0.01, 0))
        self.assertFalse(self.YP2.sense(0, 1.9, 0))
        self.assertFalse(self.YP3.sense(0, -2.01, 0))

    def test_yplane_sense_boundary(self):
        """Cases where the point is on the YPlane and is either moving up or down.
        Direction determines sense. False = moving down / True = moving up"""
        self.assertTrue(self.YP1.sense(0, 0, 0.1))
        self.assertTrue(self.YP1.sense(0, 0, 179.9))
        self.assertTrue(self.YP2.sense(0, 2, 0.1))
        self.assertTrue(self.YP2.sense(0, 2, 179.9))
        self.assertTrue(self.YP3.sense(0, -2, 0.1))
        self.assertTrue(self.YP3.sense(0, -2, 179.9))
        
        self.assertFalse(self.YP1.sense(0, 0, -1))
        self.assertFalse(self.YP1.sense(0, 0, -179))
        self.assertFalse(self.YP2.sense(0, 2, -0.01))
        self.assertFalse(self.YP2.sense(0, 2, -179))
        self.assertFalse(self.YP3.sense(0, -2, -0.01))
        self.assertFalse(self.YP3.sense(0, -2, -179))

    def test_yplane_sense_boundary2(self):
        """Cases where the point is on the YPlane and is traveling
        directly along the plane. Returns True."""
        self.assertTrue(self.YP1.sense(0, 0, 0))
        self.assertTrue(self.YP1.sense(0, 0, 180))
        self.assertTrue(self.YP2.sense(0, 2, 0))
        self.assertTrue(self.YP2.sense(0, 2, 180))
        self.assertTrue(self.YP3.sense(0, -2, 0))
        self.assertTrue(self.YP3.sense(0, -2, 180))
        
        
    def test_yplane_dist_to_boundary(self):
        """Takes the point x, y and the direction of motion.
        Returns None if the path doesn't collide with the YPlane."""
        self.assertEqual(self.YP1.dist_to_boundary(0, 1, 270),1)
        self.assertEqual(self.YP1.dist_to_boundary(0, 1, 0), None)
        self.assertTrue(self.YP1.dist_to_boundary(0, 1, -20) > 1)
        self.assertEqual(self.YP1.dist_to_boundary(0, -2, 90), 2)

        self.assertEqual(self.YP2.dist_to_boundary(0, 1, 90), 1)
        self.assertEqual(self.YP2.dist_to_boundary(0, 1, -90),None)
        self.assertTrue(self.YP2.dist_to_boundary(0, 1, 30) > 1)
        self.assertEqual(self.YP2.dist_to_boundary(0,-2, 90), 4)

        self.assertEqual(self.YP3.dist_to_boundary(0, 1, 180),None)
        self.assertEqual(self.YP3.dist_to_boundary(0, 1, 0), None)
        self.assertTrue(self.YP3.dist_to_boundary(0, 1, -30) > 3)
        self.assertEqual(self.YP3.dist_to_boundary(0, -2, 90),0)

    def test_rectangle_sense(self):
        """Tests the sense method for Rectangle objects (subclass of Surface).
        Same sense rules apply as with 4 individual planes"""
        self.assertTrue(self.R1.sense(2, 2, 0))
        self.assertTrue(self.R2.sense(-3, 0, 0))
        self.assertTrue(self.R3.sense(-2, -5, 0))

        self.assertFalse(self.R1.sense(0,0,0))
        self.assertFalse(self.R1.sense(0,0.5,-90))
        self.assertFalse(self.R2.sense(-1,2,3))
        self.assertFalse(self.R2.sense(-2.5,2,0))
        self.assertFalse(self.R3.sense(0,0,0))
        self.assertFalse(self.R3.sense(0,-3,90))

    def test_circle_getters(self):
        """Tests the getX, getY, get_center, and get_rad methods."""
        self.assertEqual(self.C1.getX(),0)
        self.assertEqual(self.C1.getY(),0)
        self.assertEqual(self.C1.get_center(),(0,0))
        self.assertEqual(self.C1.get_rad(),1)

        self.assertEqual(self.C2.getX(),1)
        self.assertEqual(self.C2.getY(),4)
        self.assertEqual(self.C2.get_center(),(1,4))
        self.assertEqual(self.C2.get_rad(),2)

        self.assertEqual(self.C3.getX(),-1)
        self.assertEqual(self.C3.getY(),10)
        self.assertEqual(self.C3.get_center(),(-1,10))
        self.assertEqual(self.C3.get_rad(),3)

    def test_circle_sense_false(self):
        """Tests sense for points that are inside the circle.
        Direction doesn't matter. All should return False."""
        self.assertFalse(self.C1.sense(0, 0, 0))
        self.assertFalse(self.C1.sense(0, 0.75, 0))
        self.assertFalse(self.C1.sense (0.99, 0, 0))
        self.assertFalse(self.C1.sense(0.5, -0.5, 0))

        self.assertFalse(self.C2.sense(1, 4, 0))
        self.assertFalse(self.C2.sense(2.5, 4, 0))
        self.assertFalse(self.C2.sense(1, 5.9, 0))
        self.assertFalse(self.C2.sense(2, 3, 0))
        
        self.assertFalse(self.C3.sense(-1, 10, 0))
        self.assertFalse(self.C3.sense(-1, 8, 0))
        self.assertFalse(self.C3.sense(1.8, 10, 0))
        self.assertFalse(self.C3.sense(1, 9, 0))

    def test_circle_sense_true(self):
        """Tests sense for points that are outside the circle.
        Direction doesn't matter. All should return True."""
        self.assertTrue(self.C1.sense(0, 5, 0))
        self.assertTrue(self.C1.sense(2, 2, 0))
        self.assertTrue(self.C1.sense (0.99, 1.1, 0))

        self.assertTrue(self.C2.sense(-1, 5, 0))
        self.assertTrue(self.C2.sense(0, 1, 0))
        self.assertTrue(self.C2.sense(3, 3, 0))

        self.assertTrue(self.C3.sense(4, 1, 0))
        self.assertTrue(self.C3.sense(2, 0, 0))
        self.assertTrue(self.C3.sense(1.8, 6, 0))

    def test_circle_sense_boundary(self):
        """Tests sense for points that are on the boundary and traveling
        into or out of the circle. Moving in = False / moving out = True"""
        self.assertTrue(self.C1.sense(1,0,0))
        self.assertTrue(self.C2.sense(3,4,20))
        self.assertTrue(self.C3.sense(2,10,45))

        self.assertFalse(self.C1.sense(1,0,180))
        self.assertFalse(self.C2.sense(1,6,-90))
        self.assertFalse(self.C3.sense(-4,10,0))

    def test_circle_sense_tangent(self):
        """Tests sense for points that are on the boundary and moving
        tangent to the circle at that point. Should return False."""
        self.assertFalse(self.C1.sense(1,0,90))
        self.assertFalse(self.C2.sense(-1,4,270))
        self.assertFalse(self.C3.sense(-1,13,0))

    def test_circle_dist_to_boundary(self):
        """Tests distance to circle boundary. Returns None if the
        current point and direction would not cross the circle. Otherwise,
        returns shortest distance (since there can be two)."""

        self.assertEqual(self.C1.dist_to_boundary(0, 0, 0),1)
        self.assertEqual(self.C1.dist_to_boundary(2, 0, 180),1)
        self.assertEqual(self.C1.dist_to_boundary(0, 2, 0),None)
        self.assertEqual(self.C1.dist_to_boundary(0, 0, 38),1)

        self.assertEqual(self.C2.dist_to_boundary(1, 4, 280),2)
        self.assertEqual(self.C2.dist_to_boundary(2, 4, 0),1)
        self.assertEqual(self.C2.dist_to_boundary(1, 6, 200),0)
        self.assertEqual(self.C2.dist_to_boundary(1, 5, 90),1)


class cell_geometry_tests(unittest.TestCase):

    def setUp(self):
        """Creates instances of Cells and Geometry used for testing and plotting."""
        
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

        # G: 10x10 box with 2 cells inside (circle inside a square)
        box = Rectangle(0,0,10,10)
        G = Geometry(box)
        cell1 = Cell()
        cell1.add_surface(Circle(0,0,4),False)
        cell2 = Cell()
        cell2.add_surface(Circle(0,0,4),True)
        cell2.add_surface(box,False)

        G.add_cell(cell1, 1)
        G.add_cell(cell2, 2)

        # add all generated cells/geometries to the TestFixture
        self.Cell1 = Cell1
        self.Cell2 = Cell2
        self.Cell3 = Cell3
        self.Cell4 = Cell4
        self.G = G

    def test_in_cell_1(self):

        self.assertTrue(self.Cell1.in_cell(0,0,0))
        self.assertTrue(self.Cell1.in_cell(0,0.5,90))
        self.assertTrue(self.Cell1.in_cell(1,0,180))
        self.assertFalse(self.Cell1.in_cell(1,0,0))
        self.assertFalse(self.Cell1.in_cell(2,2,90))


    def test_in_cell_2(self):

        self.assertTrue(self.Cell2.in_cell(0,0,180))
        self.assertTrue(self.Cell2.in_cell(-1,-1,45))
        self.assertFalse(self.Cell2.in_cell(-2,-1,0))
        self.assertFalse(self.Cell2.in_cell(-1,-1,-5))

    def test_in_cell_3(self):

        self.assertTrue(self.Cell3.in_cell(1,3.1,0))
        self.assertFalse(self.Cell3.in_cell(1,1,0))
        self.assertFalse(self.Cell3.in_cell(1,3,-90))
        self.assertFalse(self.Cell3.in_cell(1,3,0))

    def test_in_cell_4(self):

        self.assertTrue(self.Cell4.in_cell(0,0,0))
        self.assertTrue(self.Cell4.in_cell(-1,1,0))
        self.assertTrue(self.Cell4.in_cell(0,2,0))
        self.assertFalse(self.Cell4.in_cell(0,3,0))
        self.assertFalse(self.Cell4.in_cell(0,2,90))

    def test_geometry(self):

        self.assertEqual(len(self.G.get_cells()), 2)

if __name__ == '__main__':
    unittest.main()
