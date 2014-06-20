    # TO DO:

    # test cases for Surface (generalized)
        # could add more (just tested plotting)
    # more testing with plotting
    
    # also read up on unittest vs nose ********

    # geometry: holds multiple cells
        # add cell
        # force it to have a bounding box (give it a rectangular surface that bounds the entire thing)
        # we're going to use bounding box for ray tracing
        # use bottom + left sides to start doing ray tracing
    # make tracks routine in geometry - lays down tracks (x, y, direction) <- x,y muxt be on bounding box
        # trace until it hits other end of bounding box
        # dist to next surface: find out cell you're in, dist to next surface in cell
        # angle and track spacing (TRACK SPACING = parallel distance)
    # Track class: x_0, y_0, x_1, y_1 (start, endpt), array of segments (which make up the track)
        # tracks should have IDs as well
        # and the number of segments
    # Segment class: x_0, y_0... (start, endpt), also has region ID
        # add IDs to the cells
    # plot tracks routine: make lines, show diff colors in diff regions
            
