import numpy as np
import awkward as ak
import uproot as uproot

import matplotlib.pylab as plt

import sys

from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import nanoaod_analysis_tools as nat

import time

# Info about scale factors and reweighting
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD

# https://coffeateam.github.io/coffea/api/coffea.nanoevents.methods.nanoaod.GenParticle.html

infilename = sys.argv[1]
tag = infilename
if tag.find('/')>=0:
    tag = tag.split('/')[-1].split('.root')[0]
tag = tag.split('.root')[0]

print(tag)


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
 #'GenVtx',
 'GenDressedLepton',
 #'GenIsolatedPhoton',
 'GenJet',
 'GenVisTau',
 'PSWeight',
 'LHEPdfWeight',
 'genWeight',
 'GenPart',
 ]

plot_range = {'LHEScaleWeight': (0,2.5), 
              'PSWeight': (0,4), 
              'LHEPdfWeight': (0.5,2)
              }

print(events.fields)
plt.figure(figsize=(12,4))
subfigure_count = 1
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
            elif field.find('LHEReweightingWeight')>=0:
                continue
            #print(ak.size(events[field]))
            plt.subplot(1,3,subfigure_count)
            x = ak.to_numpy(ak.flatten(events[field]))
            print(x[0:10])
            #x = ak.to_numpy(events[field])
            plt.hist(x,range=plot_range[field],bins=100)
            plt.title(field)

            subfigure_count += 1

plt.tight_layout()
plt.savefig(f'{tag}_SYSTEMATICS.png')

#plt.show()





