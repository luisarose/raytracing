import math

class Geometry():
    """Holds multiple cells. Must have a bounding box, passed in as a Rectangle."""
    def __init__(self, bound_box):
        self.bound_box = bound_box
        self.edges = bound_box.get_surfaces()
        self.cells = {}
        self.next_cell_ID = 0
        self.next_track_ID = 0
        self.next_segment_ID = 0
        self.tracks = {}
        self.segments = {}
        self.cell_list = []
        self.x_min = self.edges[0][0].getX()
        self.x_max = self.edges[1][0].getX()
        self.y_min = self.edges[2][0].getY()
        self.y_max = self.edges[3][0].getY()
    def __str__(self):
        # just something I can print easily
        x_min = self.get_edges()[0][0].getX()
        x_max = self.get_edges()[1][0].getX()
        y_min = self.get_edges()[2][0].getY()
        y_max = self.get_edges()[3][0].getY()
        return "Geometry bounded with xmin "+str(x_min)+", xmax "+str(x_max)+", ymin "+str(y_min)+", and ymax "+str(y_max)+". Total cells: "+str(len(self.get_cells()))
    def get_edges(self):
        return self.edges
    def get_xmax(self):
        return self.x_max
    def get_xmin(self):
        return self.x_min
    def get_ymax(self):
        return self.y_max
    def get_ymin(self):
        return self.y_min
    def get_bounding_box(self):
        return self.bound_box
    def add_cell(self, cell, ID):
        """ID is an identifier for the cell. Goes into a dictionary
        of cells."""
        self.cells[ID] = cell
        self.cell_list.append((ID, cell))
    def generate_ID(self, ID_type):
        """IDs are integers in numerical order as
        cells are added. ID_type is one of these:
        next_cell_ID, next_track_ID, or next_segment_ID"""
        if ID_type == 'next_cell_ID':
            self.next_cell_ID += 1
            return self.next_cell_ID
        elif ID_type == 'next_track_ID':
            self.next_track_ID += 1
            return self.next_track_ID
        elif ID_type == 'next_segment_ID':
            self.next_segment_ID += 1
            return self.next_segment_ID
    def get_cells(self):
        return self.cell_list
    def in_geometry(self, x, y, direction):
        """Returns True if the point is in the geometry."""
        return not self.get_bounding_box().sense(x, y, direction)
    def which_cell(self, x, y, direction):
        """Determines which cell the point is in."""
        for cell in self.get_cells():
            if cell[1].in_cell(x, y, direction):
                return cell
        # is it possible to not be in a cell? probably.
        return None
    def dist_to_boundary(self, x, y, direction):
        current_cell = self.which_cell(x, y, direction)
        dist_to_edges = []
        for edge in self.get_edges():
            dist = edge.dist_to_boundary(x, y, direction)
            if dist != None:
                dist_to_edges.append(dist)
        dist_to_edge = min(dist_to_edges)
        return min(dist_to_edge, current_cell.dist_to_boundary(x, y, direction))    
    def make_tracks(self, direction, track_spacing):
        pass
    
        # TO BE ADDED
        
    def make_single_track(self, x_0, y_0, direction):
        """Takes in direction (angle in degrees) and start point (x,y)."""

        # first must find the endpoint of the track (on the far edge of bounding box)
        endpts = {}
        for edge in self.get_edges():
            potential_endpt = edge[0].find_collision_point(x_0, y_0, direction)
            if potential_endpt != None and potential_endpt != (x_0, y_0):
                pot_x, pot_y = potential_endpt
                dist = edge[0].dist_to_collision(x_0, y_0, pot_x, pot_y)
                endpts[dist] = potential_endpt
        length, endpt = min(endpts), endpts[min(endpts)]
        x_1, y_1 = endpt

        # generate ID for this track
        ID = self.generate_ID('next_track_ID')

        # create track
        new_track = Track(x_0, y_0, x_1, y_1, ID)

        # add to dictionary of tracks
        self.tracks[ID] = new_track

        # still need to determine segments!!
        self.generate_segments(new_track, x_0, y_0, direction)

    def generate_segments(self, new_track, x_0, y_0, direction):
        """Determines segments, creates Segment instances, and
        adds them to the Track instance"""
        segments = []
        num_segments = 0

        # determine how many segments there are: count collisisions
        temp_x = x_0
        temp_y = y_0
        current_cell = self.which_cell(x_0, y_0, direction)[1]
        while temp_x <= self.get_xmax() and temp_y <= self.get_ymax() and temp_x >= self.get_xmin() and temp_y >= self.get_ymin():
            temp_x += 0.0001*math.cos(math.radians(direction))
            temp_y += 0.0001*math.sin(math.radians(direction))
            if not current_cell.in_cell(temp_x, temp_y, direction):
                num_segments += 1
                current_cell = self.which_cell(temp_x, temp_y, direction)
                if current_cell == None and not self.in_geometry(temp_x, temp_y, direction):
                    break
                else:
                    current_cell = current_cell[1]

        # now we know how many segments there are - must find exact points

        # setting starting point for the first segment
        x_i, y_i = x_0+0.0001*math.cos(math.radians(direction)), y_0+0.0001*math.sin(math.radians(direction))

        # generate Segments and add them to the Track
        for num in xrange(num_segments):
            current_cell = self.which_cell(x_i, y_i, direction)[1]
            ID = self.generate_ID('next_segment_ID')
            x_f, y_f = current_cell.find_collision_point(x_i, y_i, direction)
            segment = Segment(x_i, y_i, x_f, y_f, ID)
            new_track.add_segment(ID, segment)
            x_i, y_i = x_f+0.0001*math.cos(math.radians(direction)), y_f+0.0001*math.cos(math.radians(direction))
        
    def get_tracks(self):
        return self.tracks

class Track():
    def __init__(self, x_0, y_0, x_1, y_1, ID):
        self.start = (x_0, y_0)
        self.endpt = (x_1, y_1)
        self.ID = ID
        self.segments = {}
    def get_start(self):
        return self.start
    def get_endpt(self):
        return self.endpt
    def get_ID(self):
        return self.ID
    def add_segment(self, ID, segment):
        self.segments[ID] = segment
    def get_segments(self):
        return self.segments
    def num_segments(self):
        return len(self.segments)

class Segment(Track):
    def __init__(self, x_0, y_0, x_1, y_1, ID):
        self.start = (x_0, y_0)
        self.endpt = (x_1, y_1)
        self.ID = ID
    def get_start(self):
        return self.start
    def get_endpt(self):
        return self.endpt
    def get_ID(self):
        return self.ID
