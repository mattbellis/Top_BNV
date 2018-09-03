"""
========================================================
Building histograms using Rectangles and PolyCollections
========================================================

Using a path patch to draw rectangles.
The technique of using lots of Rectangle instances, or
the faster method of using PolyCollections, were implemented before we
had proper paths with moveto/lineto, closepoly etc in mpl.  Now that
we have them, we can draw collections of regularly shaped objects with
homogeneous properties more efficiently with a PathCollection.  This
example makes a histogram -- its more work to set up the vertex arrays
at the outset, but it should be much faster for large numbers of
objects
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path

###################################################
# Hist from heights
###################################################
def hh(heights, bins, ax=None,color='blue',alpha=1.0): 

    # get the corners of the rectangles for the histogram
    left = np.array(bins[:-1])
    right = np.array(bins[1:])
    bottom = np.zeros(len(left))
    top = bottom + heights

    # we need a (numrects x numsides x 2) numpy array for the path helper
    # function to build a compound path
    XY = np.array([[left, left, right, right], [bottom, top, top, bottom]]).T

    # get the Path object
    barpath = path.Path.make_compound_path_from_polys(XY)

    # make a patch out of it
    patch = patches.PathPatch(barpath,color=color,linewidth=0.0,alpha=alpha)
    ax.add_patch(patch)

    # update the view limits
    ax.set_xlim(left[0], right[-1])
    ax.set_ylim(bottom.min(), top.max())

###################################################
# Stacked ist from heights
###################################################
def shh(heights, bins, ax=None,color='blue',alpha=1.0): 

    bottom_ref = np.zeros(len(heights[0]))

    for h,b,c in zip(heights,bins,color):

        # get the corners of the rectangles for the histogram
        left = np.array(b[:-1])
        right = np.array(b[1:])
        bottom = bottom_ref.copy()
        top = bottom + h
        #print(bottom[20:23],top[20:23])

        bottom_ref = top

        # we need a (numrects x numsides x 2) numpy array for the path helper
        # function to build a compound path
        XY = np.array([[left, left, right, right], [bottom, top, top, bottom]]).T

        # get the Path object
        barpath = path.Path.make_compound_path_from_polys(XY)

        # make a patch out of it
        patch = patches.PathPatch(barpath,color=c,alpha=alpha)
        ax.add_patch(patch)

        # update the view limits
        #print("HERE")
        #print(left)
        ax.set_xlim(left[0], right[-1])
        ax.set_ylim(bottom.min(), 1.1*top.max())

