import numpy as np
import awkward as ak
import uproot as uproot

import matplotlib.pylab as plt

import sys

from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import nanoaod_analysis_tools as nat

import time

# https://coffeateam.github.io/coffea/api/coffea.nanoevents.methods.nanoaod.GenParticle.html

infilename = sys.argv[1]


# Topology = t/tbar
topology = ["had","had"]


print("Reading in {0}".format(infilename))

events = NanoEventsFactory.from_root(infilename, schemaclass=NanoAODSchema).events()
print(len(events))


#mask = (abs(events.GenPart.pdgId) == 5) & events.GenPart.hasFlags(['isPrompt', 'isLastCopy']) 
#pdgId = events.GenPart[mask].distinctParent.pdgId
#print(pdgId)
#mask2 = (pdgId==6)
#
#pt = events.GenPart[mask].distinctParent.pt
#print(pt)
#print(pt[mask2])
#
#eta = events.GenPart[mask].distinctParent.eta
#phi = events.GenPart[mask].distinctParent.phi
#print(pt)

fields = ['LHEPart',
 'LHEReweightingWeight',
 'LHEWeight',
 'LHE',
 'LHEScaleWeight',
 'GenJetAK8',
 'luminosityBlock',
 'run',
 'HTXS',
 'GenVtx',
 'GenDressedLepton',
 'GenIsolatedPhoton',
 'GenJet',
 'GenVisTau',
 'PSWeight',
 'LHEPdfWeight',
 'genWeight',
 'GenPart',
 ]

print(events.fields)
for field in fields:
    print("-------------------")
    print("-------------------")
    print(field)
    print("-------------------")
    a = events[field].fields
    if len(a)>0:
        print(a)
    else:
        if field.find('eight')>=0:
            if field.find('genWeight')>=0:
                continue
            #print(ak.size(events[field]))
            plt.figure()
            x = ak.to_numpy(ak.flatten(events[field]))
            #x = ak.to_numpy(events[field])
            plt.hist(x)
            plt.title(field)

plt.show()





