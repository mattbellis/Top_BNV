import numpy as np
import awkward1 as awkward
import uproot4 as uproot

import sys

from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import nanoaod_analysis_tools as nat

import pandas as pd

import h5hep as hp

import time

import numba as nb

################################################################################
# Pass in x,y,z and return the pt, eta, and phi components of momentum
################################################################################
@nb.njit
def xyz2etaphi(x,y,z):

    pt = np.sqrt(x*x + y*y)
    phi = np.arctan2(y,x)
    eta = pseudorapidity(x,y,z)

    return pt,eta,phi
################################################################################

################################################################################
# Pass in mass,px,py, and pz and return energy
################################################################################
@nb.njit
def energyfrommasspxpypz(p4):

    px2 = p4.px*p4.px
    py2 = p4.py*p4.py
    pz2 = p4.pz*p4.pz
    m2 = p4.mass*p4.mass

    e2 = m2+px2+py2+pz2

    return np.sqrt(e2)

################################################################################

# https://github.com/CoffeaTeam/coffea/blob/9a29fe47fc690051be50773d262ee74e805a2f60/binder/nanoevents.ipynb
from coffea.nanoaod import NanoEvents

infilename = sys.argv[1]

print("Reading in {0}".format(infilename))

#events = NanoEvents.from_file(infilename)
events = NanoEventsFactory.from_root(infilename, schemaclass=NanoAODSchema).events()
print(len(events))



print("Applying the trigger mask and extracting jets, muons, and electrons...")
jets = events.Jet
muons = events.Muon
electrons = events.Electron
print("Extracted jets, muons, and electrons!")
print(len(jets),len(electrons),len(muons))


start = time.time()
print("Calculating Cartesian 4-vectors...")
muons['px'],muons['py'],muons['pz'] = nat.etaphipt2xyz(muons)
muons['e'] = nat.energyfrommasspxpypz(muons)
#
jets['px'],jets['py'],jets['pz'] = nat.etaphipt2xyz(jets)
jets['e'] = nat.energyfrommasspxpypz(jets)
#
electrons['px'],electrons['py'],electrons['pz'] = nat.etaphipt2xyz(electrons)
electrons['e'] = nat.energyfrommasspxpypz(electrons)
print("Calculated Cartesian 4-vectors!")

print("Time to process: {0}".format(time.time()-start))

