import numpy as np
import awkward as ak
import uproot as uproot

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

jets = events.Jet


print("------ Looking for W stuff ---------")
#for event in events:
#    for p in event.GenPart.pdgId:
#        print(p)
any_quark_mask =((abs(events.GenPart.pdgId)==1) |  \
       (abs(events.GenPart.pdgId)==2) |  \
       (abs(events.GenPart.pdgId)==3) |  \
       (abs(events.GenPart.pdgId)==4) |  \
       (abs(events.GenPart.pdgId)==5)) & \
       (events.GenPart.hasFlags(['isPrompt','isLastCopy']))

from_Wp_from_t = (events.GenPart.distinctParent.pdgId==24) & (events.GenPart.distinctParent.distinctParent.pdgId==6) 
from_Wm_from_tbar = (events.GenPart.distinctParent.pdgId==-24) &  (events.GenPart.distinctParent.distinctParent.pdgId==-6) 

bquark_from_t = (events.GenPart.pdgId==5) & \
                (events.GenPart.hasFlags(['isPrompt','isLastCopy'])) & \
                (events.GenPart.distinctParent.pdgId==6) 

bbarquark_from_tbar = (events.GenPart.pdgId==-5) & \
                (events.GenPart.hasFlags(['isPrompt','isLastCopy'])) & \
                (events.GenPart.distinctParent.pdgId==-6) 

#print(mask)
#parent_pdgId = events.GenPart[mask].distinctParent.pdgId
#print("pdgId of parent")
#print(parent_pdgId)
#print(pdgId)
#mask2 = (pdgId==24)

#pt = events.GenPart[mask].distinctParent.pt

#mask = any_quark_mask & from_Wp_from_t
mask = any_quark_mask & from_Wm_from_tbar
#mask = from_Wp_from_t
#mask = bquark_from_t | bbarquark_from_tbar 

pdgId = events.GenPart[mask].pdgId
pt = events.GenPart[mask].pt
eta = events.GenPart[mask].eta
phi = events.GenPart[mask].phi
parent = events.GenPart[mask].distinctParent.pdgId

bjet_partons = events.GenPart[mask]

print("pt")
print(pt)
for a,b,c,d,e in zip(pdgId,pt,eta,phi,parent):
    print("-------")
    #print(a)
    #print(b)
    for i,j,k,l,m in zip(a,b,c,d,e):
        if i is None:
            continue
        print(f"{i:3d} {j:6.3f} {k:6.3f} {l:6.3f} {m:3d}")
#print("pt with W parent")
##print(pt[mask2])
#pt = events.GenPart[mask].pt
#for p in pt[mask2]:
    #print(p)
#
#eta = events.GenPart[mask].distinctParent.eta
#phi = events.GenPart[mask].distinctParent.phi


for partons,jets_in_event in zip(bjet_partons,jets):
    print("Event --------------------------------------------")
    if partons is None:
        continue
    print(partons)
    for parton in partons:
        print("Parton ============")
        if parton is None:
            continue
        print(parton.pt)
        x = parton.delta_r(jets_in_event)
        y = parton.pt - jets_in_event.pt
        print(x)
        print(y)
        print(jets_in_event.btagDeepB)
        print(ak.min(x))
        print(ak.min(abs(y)))
#dR = jets[:].delta_r(bjet_partons)

print(dR)
