import numpy as np
import awkward1 as awkward
import uproot4 as uproot
import matplotlib.pylab as plt

import sys

import nanoaod_analysis_tools as nat

# https://github.com/CoffeaTeam/coffea/blob/9a29fe47fc690051be50773d262ee74e805a2f60/binder/nanoevents.ipynb
from coffea.nanoaod import NanoEvents

infilename = sys.argv[1]

events = NanoEvents.from_file(infilename)

HLT = events.HLT

event_mask = nat.trigger_mask(nat.muon_triggers_of_interest['2018'], HLT)

jets = events.Jet
print(len(jets))
jets = events[event_mask].Jet
print(len(jets))

muons = events[event_mask].Muon

# Testing muons
'''
print("Muons mask")
for pt in [10,20,25,30]:
    for isoflag in range(0,7):
        for flag in ['loose','medium','tight']:
            muon_mask = nat.muon_mask(muons,ptcut=pt,isoflag=isoflag,flag=flag)

            print('{0} {1} {2} {3}'.format(pt, isoflag, flag, len(awkward.flatten(muons[muon_mask]))))
'''




