from raytracing import *
from surfaces import *
from cells import *
from plot import *
from geometry import *

import numpy
import matplotlib.pyplot as plt
import unittest

class plot_tests(unittest.TestCase):
    
    def setUp(self):
        """Sets up the two Geometry instancese we can use to plot."""
        Ellipse = Surface(1, 2, 0, 0, 0, -3)
        Angled_Plane = Surface(0, 0, 0, 1, 1, 0)

        test_cell1 = Cell()
        test_cell1.add_surface(Ellipse, True)

        test_cell2 = Cell()
        test_cell2.add_surface(Angled_Plane, True)
    
        # make geometry: circle inside a circle inside a square
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

        dir_list = [10, 20, 30, 40, 50, 60, 70, 80, 89, 100, 110, 120, 130, 140, 150, 160, 170, 179]

        self.test_cell1 = test_cell1
        self.test_cell2 = test_cell2
        
        self.G = G
        self.G2 = G2
        self.dir_list = dir_list

    def test_plot_cells(self):
        """Test plotting of cells to see shape."""
        simple_plot(self.test_cell1, 0)
        simple_plot(self.test_cell2, 0)

    def test_plot_tracks_G(self):
        
        """Test plotting tracks. Geometry: a circle (r=4) inside a square (len=10).
        Directions = 10, 20, 30, 40, 50, 60, 70, 80, 89, 100, 110, 120, 130, 140, 150, 160, 170, 179
        Track spacing: 0.5"""

        make_and_plot_tracks(self.G, self.dir_list, 0.5)

    def test_plot_tracks_G2(self):
        """Test plotting tracks. Geometry: 7 cells.
        Directions = 10, 20, 30, 40, 50, 60, 70, 80, 89, 100, 110, 120, 130, 140, 150, 160, 170, 179
        Track spacing: 0.5"""

        make_and_plot_tracks(self.G2, self.dir_list, 0.5)

if __name__ == '__main__':
    unittest.main()
