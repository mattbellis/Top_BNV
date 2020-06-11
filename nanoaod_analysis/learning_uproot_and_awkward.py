import numpy as np
import awkward1 as awkward
import uproot4 as uproot
import matplotlib.pylab as plt

import sys

# https://github.com/CoffeaTeam/coffea/blob/9a29fe47fc690051be50773d262ee74e805a2f60/binder/nanoevents.ipynb
from coffea.nanoaod import NanoEvents

infilename = sys.argv[1]

# UPROOT AND AWKWARD
#data = uproot.open(infilename)
#events = events['Events']
#
#n = events.num_entries
#
#print(n)
#
#
#cms_dict_ak1 = events.arrays(events.keys())

events = NanoEvents.from_file(infilename)

a = awkward.flatten(events.Jet.pt)

print(events.Jet.columns)

a = awkward.flatten(events.Jet.pt[events.Jet.pt>15])

mask = events.L1.SingleMu22==True

events[mask]


