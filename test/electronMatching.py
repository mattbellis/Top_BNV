import ROOT, sys
import numpy as np
import matplotlib.pylab as plt
import lichen.lichen as lch
from PttoXYZ import PTtoXYZ

def invmass(p4s):
     tot = np.array([0.,0.,0.,0.])
     for p4 in p4s:
         tot += p4
     m2 = tot[0]**2 - tot[1]**2 - tot[2]**2 - tot[3]**2
     m = -999
     if m2 >= 0:
         mp = np.sqrt(m2)
     else:
         m = -np.sqrt(np.abs(m2))
     return m

f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")


