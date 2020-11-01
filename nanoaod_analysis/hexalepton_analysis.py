import numpy as np
import awkward1 as awkward
import uproot4 as uproot
import matplotlib.pylab as plt

import sys

import nanoaod_analysis_tools as nat

from itertools import combinations

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
print(len(events))

#mask = events.L1.SingleMu22==True

muons = events.Muon
electrons = events.Electron

print("Calculating number of electrons...")
nelectrons = awkward.num(electrons)
print("Calculating number of muons...")
nmuons = awkward.num(muons)
print(len(electrons))
print(len(muons))

nlep = nelectrons + nmuons

plt.figure(figsize=(12,6))
plt.subplot(3,1,1)
plt.hist(nlep,bins=10,range=(0,10))

plt.subplot(3,1,2)
plt.hist(nelectrons,bins=10,range=(0,10))

plt.subplot(3,1,3)
plt.hist(nmuons,bins=10,range=(0,10))

mask = nlep>=6

allmuons = events[mask].Muon
allelectrons = events[mask].Electron

print("Calculating Cartesian 4-vectors for muons...")
allmuons['px'],allmuons['py'],allmuons['pz'] = nat.etaphipt2xyz(allmuons)
allmuons['e'] = nat.energyfrommasspxpypz(allmuons)

print("Calculating Cartesian 4-vectors for electrons...")
allelectrons['px'],allelectrons['py'],allelectrons['pz'] = nat.etaphipt2xyz(allelectrons)
allelectrons['e'] = nat.energyfrommasspxpypz(allelectrons)


nelectrons = awkward.num(allelectrons)
nmuons = awkward.num(allmuons)

nlep = nelectrons + nmuons

nmasses = 10
masses = []
for i in range(nmasses):
    masses.append([])

for nm,ne,muons,electrons in zip(nmuons,nelectrons,allmuons,allelectrons):

    total_leptons = nm + ne

    for indices in combinations(np.arange(total_leptons), 6):
        p4s = []

        print(indices)
        print(nm,ne)
        npassed = 0
        for idx in indices:
            # Grab the muons
            if idx<nm:
                n = idx
                print("muons: ",idx,n,nm)
                if muons[n].matched_jet is None:
                    p4s.append(muons[n])
                    npassed += 1

            # Then the electrons
            else:
                n = idx-nm
                print("electrons: ",idx,n,ne)
                if electrons[n].matched_jet is None:
                    p4s.append(electrons[n])
                    npassed += 1

        print("npassed: ",npassed)
        if npassed>0:
            mass = nat.invmass(p4s)
            print(mass)
            if npassed<nmasses-1:
                masses[npassed].append(mass)

plt.figure(figsize=(8,8))
for i in range(nmasses):
    print("{0}: # masses: {1}".format(i, len(masses)))
    plt.subplot(3,4,i+1)
    plt.hist(masses[i],bins=100)
plt.savefig('hexamasses.png')


plt.show()
