import numpy as np
import awkward as ak
import uproot as uproot

import matplotlib.pylab as plt

import sys

from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import nanoaod_analysis_tools as nat

import time

# https://coffeateam.github.io/coffea/api/coffea.nanoevents.methods.nanoaod.GenParticle.html

# This might be helpful
# https://github.com/CoffeaTeam/coffea/blob/master/binder/nanoevents.ipynb

infilename = sys.argv[1]

# Topology = t/tbar
topology = ["had","had"]

print("Reading in {0}".format(infilename))

events = NanoEventsFactory.from_root(infilename, schemaclass=NanoAODSchema).events()
print(len(events))

events = events[0:100]

jets = events.Jet
genpart = events.GenPart
print("Calculating Cartesian 4-vectors...")
jets['px'],jets['py'],jets['pz'] = nat.etaphipt2xyz(jets)
jets['e'] = nat.energyfrommasspxpypz(jets)

genpart['px'],genpart['py'],genpart['pz'] = nat.etaphipt2xyz(genpart)
#print(genpart.fields)
genpart['e'] = nat.energyfrommasspxpypz(genpart)

print("Calculated Cartesian 4-vectors!")

print("------ Looking for W stuff ---------")
# Get the quarks that are quark 1-5
any_quark_mask =((abs(genpart.pdgId)==1) |  \
       (abs(genpart.pdgId)==2) |  \
       (abs(genpart.pdgId)==3) |  \
       (abs(genpart.pdgId)==4) |  \
       (abs(genpart.pdgId)==5)) & \
       (genpart.hasFlags(['isPrompt','isLastCopy']))

# Quarks from W+ that comes from a top
from_Wp_from_t = (genpart.distinctParent.pdgId==24) & (genpart.distinctParent.distinctParent.pdgId==6) 
# Quarks from W- that comes from an antitop
from_Wm_from_tbar = (genpart.distinctParent.pdgId==-24) &  (genpart.distinctParent.distinctParent.pdgId==-6) 

# b quark from a t
bquark_from_t = (genpart.pdgId==5) & \
                (genpart.hasFlags(['isPrompt','isLastCopy'])) & \
                (genpart.distinctParent.pdgId==6) 

# bbar from a tbar
bbarquark_from_tbar = (genpart.pdgId==-5) & \
                (genpart.hasFlags(['isPrompt','isLastCopy'])) & \
                (genpart.distinctParent.pdgId==-6) 

t_mask = None
tbar_mask = None

if topology[0] == 'had':
    # Identifies quarks from W+ from top *and* a b quark from same t
    t_mask =    (any_quark_mask & from_Wp_from_t) | (bquark_from_t)
if topology[1] == 'had':
    # Identifies quarks from W- from antitop *and* a antib quark from same antit
    tbar_mask = (any_quark_mask & from_Wm_from_tbar) | (bbarquark_from_tbar)

##########################################################################
# Testing t_mask or tbar_mask
# The below works for hadronic ttbar MC
##########################################################################
e = events[0]
print("Quarks from t --> W+ b")
for i in e.GenPart[t_mask[0]].pdgId:
    print(i)

print("Quarks from tbar --> W- bbar")
for i in e.GenPart[tbar_mask[0]].pdgId:
    print(i)

print("Quarks from either t or tbar hadronic decay")
for i in e.GenPart[tbar_mask[0] | t_mask[0]].pdgId:
    print(i)
##########################################################################


#print(mask)
#parent_pdgId = genpart[mask].distinctParent.pdgId
#print("pdgId of parent")
#print(parent_pdgId)
#print(pdgId)
#mask2 = (pdgId==24)

#pt = genpart[mask].distinctParent.pt

#mask = any_quark_mask & from_Wp_from_t
#mask = any_quark_mask & from_Wm_from_tbar
#mask = (any_quark_mask & from_Wm_from_tbar) | ( any_quark_mask & from_Wp_from_t)
#mask = from_Wp_from_t
#mask = bquark_from_t | bbarquark_from_tbar 
mask = t_mask | tbar_mask

pdgId = genpart[mask].pdgId
pt = genpart[mask].pt
eta = genpart[mask].eta
phi = genpart[mask].phi
parent = genpart[mask].distinctParent.pdgId

# This is a jagged array of GenParticles that correspond to the
# quarks that come from the masked decays
quark_partons = genpart[mask]

#print(quark_partons)

#exit()

#print("pt")
#print(pt)
total = 0

# Loop over the gen particles at the event level 
for a,b,c,d,e in zip(pdgId,pt,eta,phi,parent):
    for i,j,k,l,m in zip(a,b,c,d,e):
        if i is None:
            continue
        #print(f"pdgID: {i:3d}\tpT: {j:6.3f}\teta: {k:6.3f}\tphi: {l:6.3f}\tparent pdgId: {m:3d}")
        total += 1
print(f"{total} quarks")


'''
for jet in jets:
    for j in jet:
        print(f"pT: {j.pt:6.3f}\teta: {j.eta:6.3f}\tphi: {j.phi:6.3f}\tbtagDeepB: {j.btagDeepB:.5f}")
'''


# Using this for guidance on matching
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePATMCMatching
# 
# deltaPtRel = deltaPt/Pt
maxdR = 0.4
#maxdpTRel = 3.0
maxdpTRel = 4.0

nmatched_partons = 0
nmatched_events = 0
tmass = []
tbarmass = []
wmmass = []
wpmass = []
icount = 0

for partons,jets_in_event in zip(quark_partons,jets):

    if icount%100==0:
        print(icount)

    b1,b2 = None,None
    q1 = []
    q2 = []

    event_p4s = []
    nmatched_partons_in_event = 0
    #print("Event --------------------------------------------------------------------------")
    #print(partons.pt)
    #print(jets_in_event.pt)
    if partons is None:
        continue
    #print(partons)
    for parton in partons:
        if parton is None:
            continue
        #print("Parton ======== ", parton.pdgId)
        #print('parton pT', parton.pt)
        dR_between_parton_and_all_jets = parton.delta_r(jets_in_event)
        pT_between_parton_and_all_jets = parton.pt - jets_in_event.pt
        mindR,mindpTRel,minJetIdx = 1e6, 1e6,-1
        for i,(dR,dpT) in enumerate(zip(dR_between_parton_and_all_jets,pT_between_parton_and_all_jets)):
            dpT = np.abs(dpT)
            #print(i,dR,dpT,dpT/parton.pt,dpT/jets_in_event[i].pt)
            if mindR > dR:
                mindR = dR
                mindpTRel = dpT/parton.pt
                minJetIdx = i
        #print(f"best match: mindR: {mindR:.3f} \tmindpTRel: {mindpTRel:.3f}")
        #print(f"pdgID: {parton.pdgId:3d}\tpT: {parton.pt:6.3f}\teta: {parton.eta:6.3f}\tphi: {parton.phi:6.3f}\tparent pdgId: {parton.distinctParent.pdgId:3d}")
        j = jets_in_event[minJetIdx]
        #print(f"\t\tpT: {j.pt:6.3f}\teta: {j.eta:6.3f}\tphi: {j.phi:6.3f}\tbtagDeepB: {j.btagDeepB:.5f}")

        mindR = ak.min(dR_between_parton_and_all_jets)
        mindpT = ak.min(abs(pT_between_parton_and_all_jets))
        mindpTRel = ak.min(abs(pT_between_parton_and_all_jets))/parton.pt
        #print('min of dR : ',mindR)
        #print('min of dPt: ',mindpT)
        #print('min of dPtRel: ',mindpTRel)

        if mindR<=maxdR and mindpTRel<=maxdpTRel:
            nmatched_partons += 1
            nmatched_partons_in_event += 1
            #p4 = nat.massptetaphi2epxpypz(jets_in_event[minJetIdx])
            p4 = (jets_in_event[minJetIdx]['e'], jets_in_event[minJetIdx]['px'],jets_in_event[minJetIdx]['py'],jets_in_event[minJetIdx]['pz'])
            if parton.distinctParent.pdgId == 6:
                b1 = p4
            elif parton.distinctParent.pdgId == -6:
                b2 = p4
            elif parton.distinctParent.pdgId == 24:
                q1.append(p4)
            elif parton.distinctParent.pdgId == -24:
                q2.append(p4)


    if nmatched_partons_in_event==6:
        nmatched_events += 1

        if b1 is None or b2 is None:
            continue

        wm = nat.invmass(q1)
        wpmass.append(wm)
        wm = nat.invmass(q2)
        wmmass.append(wm)
        tm = nat.invmass([b1]+q1)
        tmass.append(tm)
        tm = nat.invmass([b2]+q2)
        tbarmass.append(tm)

    icount += 1

print(f"Matched partons: {nmatched_partons}")
print(f"Matched events:  {nmatched_events}")
#dR = jets[:].delta_r(quark_partons)

#print(dR)

plt.figure()
plt.subplot(2,2,1)
plt.hist(wpmass,bins=50,range=(0,150))

plt.subplot(2,2,2)
plt.hist(wmmass,bins=50,range=(0,150))

plt.subplot(2,2,3)
plt.hist(tmass,bins=50,range=(0,300))

plt.subplot(2,2,4)
plt.hist(tbarmass,bins=50,range=(0,300))

0

plt.show()
