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
        """Asserts that direction is between 0 and 360 degrees. [0, 360]
        Track spacing is measured across parallel."""
        assert direction >= 0
        assert direction <= 360
        rad_dir = math.radians(direction)

        # directions treated as "positive angles"
        # includes 0 and 180 (and 360)
        if rad_dir >= 0 and rad_dir < math.pi*0.5 or direction == 360:
            # moving up + right
            x_init = self.get_xmin()
            pos_ang = True
        elif rad_dir >= math.pi and rad_dir < 1.5*math.pi:
            # moving down + left: flip direction
            direction = direction - 180
            rad_dir = math.radians(direction)
            x_init = self.get_xmin()
            pos_ang = True

        # directions treated as "negative angles"
        # includes 90 and 270
        elif rad_dir >= 1.5*math.pi and rad_dir < 2*math.pi:
            # moving down + right: flip direction
            direction = direction - 180
            rad_dir = math.radians(direction)
            x_init = self.get_xmax()
            pos_ang = False
            
        elif rad_dir >= math.pi*0.5 and rad_dir < math.pi:
            # moving left + up
            x_init = self.get_xmax()
            pos_ang = False
    
        # set spacing along sides and bottom
        x_spacing = 0
        y_spacing = 0
        
        if direction%90 != 0:
            y_spacing = abs(float(track_spacing)/math.cos(rad_dir))
            x_spacing = abs(float(track_spacing)/math.sin(rad_dir))

        elif direction%180 == 0:
            y_spacing = abs(float(track_spacing)/math.cos(rad_dir))

        elif direction%90 == 0:
            x_spacing = abs(float(track_spacing)/math.sin(rad_dir))
        
        # begin laying down tracks along one side, starting from top
        # (but first moving down one full trackspacing - no point in having
        # a track move upwards from the top)
        yval = self.get_ymax() - y_spacing

        if direction == 90 or direction == 270:
            # only need to make tracks across
            xval = self.get_xmin()+float(track_spacing)
            while xval < self.get_xmax():
                self.make_single_track(xval, self.get_ymin(), 90)
                xval += x_spacing

        elif direction == 0 or direction == 180 or direction == 360:
            # only need to make tracks going down
            yval = (self.get_ymax())-float(track_spacing)
            while yval > self.get_ymin():
                self.make_single_track(self.get_xmin(), yval, direction)
                yval -= y_spacing

        else:
            # if positive angle, start at left; negative, start at right
            while yval >= self.get_ymin():
                self.make_single_track(x_init, yval, direction)
                yval -= y_spacing
                # yval should now be below the edge of the bounding box                

            # YPlane representing minimum y value (bounding box)
            min_y_plane = self.get_edges()[2][0]

            # if pos: move left to right across bottom
            if pos_ang:
                # ignore horizontal case (no need to make additional tracks)
                if direction % 180 != 0:
                    # find collision point along the ray from yval (the ray that would start below the bounding box)
                    x_start = min_y_plane.find_collision_point(self.get_xmin(), yval, direction)
                    xval = x_start[0]
                    while xval < self.get_xmax():
                        self.make_single_track(xval, self.get_ymin(), direction)
                        xval += x_spacing

            # if neg: move right to left across bottom
            if not pos_ang:
                # find collision point along the ray from yval (the ray that would start below the bounding box)
                x_start = min_y_plane.find_collision_point(self.get_xmax(), yval, direction)
                xval = x_start[0]
                # starting point for the tracks being laid across bottom
                while xval > self.get_xmin():
                    self.make_single_track(xval, self.get_ymin(), direction)
                    xval -= x_spacing
                    
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
        if len(endpts) == 0:
            return
        length, endpt = min(endpts), endpts[min(endpts)]
        x_1, y_1 = endpt

        # generate ID for this track
        ID = self.generate_ID('next_track_ID')

        # create track
        new_track = Track(x_0, y_0, x_1, y_1, direction, ID)

        # add to dictionary of tracks
        self.tracks[ID] = new_track

        # still need to determine segments!!
        self.generate_segments(new_track, x_0, y_0, direction)

    def generate_segments(self, track, x_0, y_0, direction):
        """Determines segments, creates Segment instances, and
        adds them to the Track instance"""

        # Takes a long time to run if it's on a boundary (horizontal/vertical case)
        
        tiny_x_step = 0.00001*math.cos(math.radians(direction))
        tiny_y_step = 0.00001*math.sin(math.radians(direction))
        temp_x, temp_y = x_0+tiny_x_step, y_0+tiny_y_step
        # just so it doesn't return the boundary it starts on
        collision_point = 'start'
        while True:
            if not self.in_geometry(temp_x, temp_y, direction):
                break
            current_cell = self.which_cell(temp_x, temp_y, direction)[1]
            collision_point = current_cell.find_collision_point(temp_x, temp_y, direction)
            x_col, y_col = collision_point
            ID = self.generate_ID('next_segment_ID')
            segment = Segment(temp_x - tiny_x_step, temp_y - tiny_y_step, x_col, y_col, ID)
            temp_x, temp_y = x_col+tiny_x_step, y_col+tiny_y_step
            track.add_segment(ID, segment)
    
    def get_tracks(self):
        return self.tracks

class Track():
    def __init__(self, x_0, y_0, x_1, y_1, direction, ID):
        self.start = (x_0, y_0)
        self.endpt = (x_1, y_1)
        self.ID = ID
        self.segments = {}
        self.direction = direction
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
    def get_direction(self):
        return self.direction
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
