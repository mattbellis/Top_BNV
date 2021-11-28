import numpy as np
import awkward as ak
import uproot as uproot

import matplotlib.pylab as plt

import sys

from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import nanoaod_analysis_tools as nat

import hepfile

import time

# https://coffeateam.github.io/coffea/api/coffea.nanoevents.methods.nanoaod.GenParticle.html

# This might be helpful
# https://github.com/CoffeaTeam/coffea/blob/master/binder/nanoevents.ipynb

data = hepfile.initialize()
hepfile.create_group(data,'jet',counter='njet')
hepfile.create_dataset(data,['e','px','py','pz','btag'],group='jet',dtype=float)
hepfile.create_group(data,'lepton',counter='nlepton')
hepfile.create_dataset(data,['e','px','py','pz','q'],group='lepton',dtype=float)
event = hepfile.create_single_bucket(data)


infilename = sys.argv[1]
#infilename = "~/top_data/NANOAOD/TTToHadronic_UL_2018_SMALL_1k.root"

# Topology = t/tbar
#topology = ["had","had"]
#topology = ["had","had"]
topology = ["had","TSUE"]

topology = f"{topology[0]}_{topology[1]}"

print("Reading in {0}".format(infilename))

events = NanoEventsFactory.from_root(infilename, schemaclass=NanoAODSchema).events()
print(len(events))

events = events[0:1000]

jets = events.Jet
electrons = events.Electron
genpart = events.GenPart


print("Calculating Cartesian 4-vectors...")
jets['px'],jets['py'],jets['pz'] = nat.etaphipt2xyz(jets)
jets['e'] = nat.energyfrommasspxpypz(jets)

electrons['px'],electrons['py'],electrons['pz'] = nat.etaphipt2xyz(electrons)
electrons['e'] = nat.energyfrommasspxpypz(electrons)

genpart['px'],genpart['py'],genpart['pz'] = nat.etaphipt2xyz(genpart)
#print(genpart.fields)
genpart['e'] = nat.energyfrommasspxpypz(genpart)

print("Calculated Cartesian 4-vectors!")

print("Calculating parent pdgID")
genpart['parent_pdgId'] = genpart.distinctParent.pdgId
print("Calculated parent pdgID")

#quark_partons = genpart[mask]

verbose = False

if topology=="had_had":
    b1s,q1s,b2s,q2s = nat.truth_matching_COFFEA_TOOLS(genpart,jets,topology=topology,verbose=False,maxdR=0.4,maxdpTRel=4.0)
elif topology=="had_TSUE":
    b1s,q1s,lep2s,q2s = nat.truth_matching_COFFEA_TOOLS(genpart,jets,leptons=electrons,topology=topology,verbose=verbose,maxdR=0.4,maxdpTRel=4.0)
if topology=="had_had":
    for b1,q1,b2,q2 in zip(b1s,q1s,b2s,q2s):
        #print(b1)
        # Hepfile stuff
        print("--------")
        print(b1)
        print(q1)
        print(b2)
        print(q2)
        event['jet/e'].append(b1[0])
        event['jet/px'].append(b1[1])
        event['jet/py'].append(b1[2])
        event['jet/pz'].append(b1[3])
        event['jet/btag'].append(-999)

        event['jet/e'].append(q1[0][0])
        event['jet/px'].append(q1[0][1])
        event['jet/py'].append(q1[0][2])
        event['jet/pz'].append(q1[0][3])
        event['jet/btag'].append(-999)

        event['jet/e'].append(q1[1][0])
        event['jet/px'].append(q1[1][1])
        event['jet/py'].append(q1[1][2])
        event['jet/pz'].append(q1[1][3])
        event['jet/btag'].append(-999)

        event['jet/e'].append(b2[0])
        event['jet/px'].append(b2[1])
        event['jet/py'].append(b2[2])
        event['jet/pz'].append(b2[3])
        event['jet/btag'].append(-999)

        event['jet/e'].append(q2[0][0])
        event['jet/px'].append(q2[0][1])
        event['jet/py'].append(q2[0][2])
        event['jet/pz'].append(q2[0][3])
        event['jet/btag'].append(-999)

        event['jet/e'].append(q2[1][0])
        event['jet/px'].append(q2[1][1])
        event['jet/py'].append(q2[1][2])
        event['jet/pz'].append(q2[1][3])
        event['jet/btag'].append(-999)

        #return_value = hepfile.pack(data,event,STRICT_CHECKING=True)
        return_value = hepfile.pack(data,event)
        if return_value != 0:
            exit()

elif topology=="had_TSUE":
    for b1,q1,lep2,q2 in zip(b1s,q1s,lep2s,q2s):

        if verbose:
            print("--------")
            print(b1)
            print(q1)
            print(lep2)
            print(q2)

        # Hepfile stuff
        event['jet/e'].append(b1[0])
        event['jet/px'].append(b1[1])
        event['jet/py'].append(b1[2])
        event['jet/pz'].append(b1[3])
        event['jet/btag'].append(-999)

        event['jet/e'].append(q1[0][0])
        event['jet/px'].append(q1[0][1])
        event['jet/py'].append(q1[0][2])
        event['jet/pz'].append(q1[0][3])
        event['jet/btag'].append(-999)

        event['jet/e'].append(q1[1][0])
        event['jet/px'].append(q1[1][1])
        event['jet/py'].append(q1[1][2])
        event['jet/pz'].append(q1[1][3])
        event['jet/btag'].append(-999)

        event['jet/e'].append(q2[0][0])
        event['jet/px'].append(q2[0][1])
        event['jet/py'].append(q2[0][2])
        event['jet/pz'].append(q2[0][3])
        event['jet/btag'].append(-999)

        event['jet/e'].append(q2[1][0])
        event['jet/px'].append(q2[1][1])
        event['jet/py'].append(q2[1][2])
        event['jet/pz'].append(q2[1][3])
        event['jet/btag'].append(-999)

        event['lepton/e'].append(lep2[0])
        event['lepton/px'].append(lep2[1])
        event['lepton/py'].append(lep2[2])
        event['lepton/pz'].append(lep2[3])
        event['lepton/q'].append(-999)

        #return_value = hepfile.pack(data,event,STRICT_CHECKING=True)
        return_value = hepfile.pack(data,event)
        if return_value != 0:
            exit()

outfilename = f'{infilename.split("/")[-1].split(".root")[0]}.h5'
print(f"Writing to {outfilename}")
hdfile = hepfile.write_to_file(outfilename,data,comp_type='gzip',comp_opts=9,verbose=True)


'''
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
'''
