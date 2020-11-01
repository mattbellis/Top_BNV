import numpy as np
import awkward1 as awkward
import uproot4 as uproot
import matplotlib.pylab as plt

import sys

import nanoaod_analysis_tools as nat

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

jets = events.Jet
print(len(jets))
events[mask]

jets = events[mask].Jet
muons = events[mask].Muon
print(len(jets))
print(len(muons))

mask_jet = jets.btagDeepB > 0.5

jets[mask_jet].pt

jets[3][0].pt

jets.counts

'''
for jet,muon in zip(jets,muons):
    print(len(jet))
    print(jet)
    print(len(muon))
    print(muons)
    
'''

# Learning truth matching
print("Calculating the jet mask...")
alljets = events.Jet
jet_mask = nat.jet_mask(alljets,ptcut=20)

print(len(alljets))
print(len(alljets[jet_mask]))

alljets['px'],alljets['py'],alljets['pz'] = nat.etaphipt2xyz(alljets)
alljets['e'] = nat.energyfrommasspxpypz(alljets)

print("------ Gen Particles ----------")
print(events.GenPart.columns)
# Find the tops
events.GenPart.pdgId == 6

#nat.truth_matching_TESTING(events)
tm,atm, lowest_momentum_parton, bparton_momenta, all_parton_momenta, ntruths = nat.truth_matching(events,max_events=2000000)

print("Number of truth matched events")
print(len(tm[0]),len(atm[0]))

bins = [100,100,100,100]
ranges = [(0,400), (0,250), (0,250), (0,250)]
xlabels = [r'M($t/\overline{t}$ candidate) [GeV/c$^2$]',
           r'M($j_1$ + $j_b$) [GeV/c$^2$]',
           r'M($j_2$ + $j_b$) [GeV/c$^2$]',
           r'M($j_1$ + $j_1$) [GeV/c$^2$]']

plt.figure()
for i in range(0,4):
    plt.subplot(2,2,i+1)
    plt.hist(tm[i],bins=bins[i],range=ranges[i])
    plt.xlabel(xlabels[i])
plt.tight_layout()
plt.savefig('truthmatched_top_masses.png')

plt.figure()
for i in range(0,4):
    plt.subplot(2,2,i+1)
    plt.hist(atm[i],bins=bins[i],range=ranges[i])
    plt.xlabel(xlabels[i])
plt.tight_layout()
plt.savefig('truthmatched_antitop_masses.png')

plt.figure()#figsize=(12,3))
plt.subplot(2,2,1)
plt.hist(lowest_momentum_parton,bins=100)

plt.subplot(2,2,2)
plt.hist(bparton_momenta,bins=100)

plt.subplot(2,2,3)
plt.hist(all_parton_momenta,bins=100)

# See what percent have low momentum jet
ptcut = []
pct = []
nentries = len(lowest_momentum_parton)
lowest_momentum_parton = np.array(lowest_momentum_parton)
for i in range(0,50,5):
    ptcut.append(i)
    y = len(lowest_momentum_parton[lowest_momentum_parton>i])
    pct.append(y/float(nentries))

plt.subplot(2,2,4)
plt.plot(ptcut,pct,'o')

plt.savefig('partons_momenta.png')

plt.figure()
plt.hist(ntruths,bins=7,range=(-0.5,6.5))

#plt.show()
