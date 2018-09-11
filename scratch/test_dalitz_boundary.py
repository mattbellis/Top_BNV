import ROOT
import sys

import topbnv_tools as tbt

import numpy as np
import math
import matplotlib.pylab as plt

import pickle

import argparse

from array import array

from collections import OrderedDict


################################################################################
def main():

    M = 173
    m1 = 5.1
    m2 = 1
    m3 = 1

    x,y0,y1 = tbt.draw_dalitz_boundary(M,m1,m2,m3,npts=10000)

    plt.figure()
    plt.plot(x,y0)
    plt.plot(x,y1)

    plt.show()


################################################################################
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Process some files for top BNV search.')
    #parser.add_argument('--outfile', dest='outfile', default=None, help='Name of output file.')
    #parser.add_argument('infiles', action='append', nargs='*', help='Input file name(s)')
    args = parser.parse_args()

    print(args)

    main()
