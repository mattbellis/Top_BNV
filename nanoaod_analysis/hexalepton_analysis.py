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

#print("Calculating number of electrons...")
#nelectrons = awkward.num(electrons)
#print("Calculating number of muons...")
#nmuons = awkward.num(muons)
#print(len(electrons))
#print(len(muons))

#nlep = nelectrons + nmuons

#plt.figure(figsize=(12,6))
#plt.subplot(3,1,1)
#plt.hist(nlep,bins=10,range=(0,10))

#plt.subplot(3,1,2)
#plt.hist(nelectrons,bins=10,range=(0,10))

#plt.subplot(3,1,3)
#plt.hist(nmuons,bins=10,range=(0,10))

#mask = nlep>=6

#allmuons = events[mask].Muon
#allelectrons = events[mask].Electron

allmuons = events.Muon
allelectrons = events.Electron

print("Calculating Cartesian 4-vectors for muons...")
allmuons['px'],allmuons['py'],allmuons['pz'] = nat.etaphipt2xyz(allmuons)
allmuons['e'] = nat.energyfrommasspxpypz(allmuons)

print("Calculating Cartesian 4-vectors for electrons...")
allelectrons['px'],allelectrons['py'],allelectrons['pz'] = nat.etaphipt2xyz(allelectrons)
allelectrons['e'] = nat.energyfrommasspxpypz(allelectrons)

################################################################################

#mask = allelectrons['matched_jet'] == None
#print(mask)
#allelectrons[mask] = allelectrons

#nelectrons = awkward.num(allelectrons)
#nmuons = awkward.num(allmuons)

#nlep = nelectrons + nmuons

# nlep = 2
# +/-2 mumu mue ee
#  0   mumu mue ee

# nlep = 3
# +/-3 mumumu  mumue  muee    eee
# +/-1 mumumu  ++-    ++-     eee
# +/-1         +-+    +-+         

# nlep = 4
# +/-4 mumumumu  mumumue  mumuee   mueee  eeee
# +/-2 +++-      +++-     +++-     +++-   +++-
# +/-2           ++-+     ++-+     ++-+        
#    0 +-+-      +-+-     +-+-     +-+-   +-+-       
#    0                    ++--                       

tags = ['nm0']
tags = [['nm2_ne0_qtot2_qm2_qe0',
         'nm2_ne0_qtot0_qm0_qe0',
         'nm0_ne2_qtot0_qm0_qe0',
         'nm0_ne2_qtot2_qm0_qe2',
         'nm1_ne1_qtot2_qm1_qe1',
         'nm1_ne1_qtot0_qm1_qe1',
        ],
        ['nm3_ne0_qtot3_qm3_qe0',
         'nm0_ne3_qtot3_qm0_qe3',
         'nm3_ne0_qtot1_qm1_qe0',
         'nm0_ne3_qtot1_qm0_qe1',
         'nm2_ne1_qtot3_qm1_qe2',
         'nm1_ne2_qtot3_qm2_qe1',
         'nm2_ne1_qtot3_qm2_qe1',
         'nm1_ne2_qtot3_qm1_qe2',
         'nm2_ne1_qtot1_qm1_qe2',
         'nm2_ne1_qtot1_qm2_qe1',
         'nm1_ne2_qtot1_qm2_qe1',
         'nm1_ne2_qtot1_qm1_qe2',
         'nm2_ne1_qtot1_qm1_qe0',
         'nm1_ne2_qtot1_qm0_qe1',
         'nm2_ne1_qtot1_qm0_qe1',
         'nm1_ne2_qtot1_qm1_qe0',
        ],
        ['nm4_ne0_qtot4_qm4_qe0',
         'nm3_ne1_qtot4_qm3_qe1',
         'nm2_ne2_qtot4_qm2_qe2',
         'nm1_ne3_qtot4_qm1_qe3',
         'nm0_ne4_qtot4_qm0_qe4',
         'nm4_ne0_qtot2_qm2_qe0',
         'nm3_ne1_qtot2_qm3_qe1',
         'nm2_ne2_qtot2_qm2_qe0',
         'nm1_ne3_qtot2_qm1_qe1',
         'nm0_ne4_qtot2_qm0_qe2',
         'nm3_ne1_qtot2_qm1_qe1',
         'nm2_ne2_qtot2_qm0_qe2',
         'nm1_ne3_qtot2_qm1_qe1',
         'nm4_ne0_qtot0_qm0_qe0',
         'nm3_ne1_qtot0_qm1_qe1',
         'nm2_ne2_qtot0_qm0_qe0',
         'nm1_ne3_qtot0_qm1_qe1',
         'nm0_ne4_qtot0_qm0_qe0',
         'nm2_ne2_qtot0_qm2_qe2',
         ]
        ]


nmasses = 5
masses = []
for i in range(2,nmasses):
    masses.append({})
    for tag in tags[i-2]:
        masses[i-2][tag] = []

for m in masses:
    print(masses)
#exit()

'''
qms = [+1, -1]
qes = [+1, -1]
nmasses = 10
masses = []
for i in range(2,nmasses):
    masses.append([])

    print("------")
    for j in range(i+1):
        nm = i-j
        ne = j
        tag0 = "nm{0}_ne{1}".format(nm,ne)
        print(tag0)
        qm,qe=0,0
        for knm in range(nm):
            for qm in qms:
                for kne in range(ne):
                    for qe in qes:
                        print(qm,qe,qe+qm)
                        #tag1 = "qm{0}_qe{1}".format(i-j,j)
                        #masses.append([])

'''
#exit()
nevents = len(allmuons)

#for nm,ne,muons,electrons in zip(nmuons,nelectrons,allmuons,allelectrons):
for icount,(muons,electrons) in enumerate(zip(allmuons,allelectrons)):

    if icount%1000==0:
        print(icount,nevents)
    
    tempmuons = []
    tempelectrons = []

    for muon in muons:
        if muon.matched_jet is None:
            tempmuons.append(muon)

    for electron in electrons:
        if electron.matched_jet is None:
            tempelectrons.append(electron)

    nmuons = len(tempmuons)
    nelectrons = len(tempelectrons)

    #total_leptons = nm + ne
    total_leptons = nmuons + nelectrons
    if total_leptons>2:
        print("total_leptons: ",total_leptons)

    if total_leptons<2:
        continue

    if total_leptons>=10:
        continue

    for nbody in range(2,total_leptons+1):
        for indices in combinations(np.arange(total_leptons), nbody):
            p4s = []

            #print("----------")
            #print(total_leptons,nbody)
            #print(indices)
            #print(nmuons,nelectrons)

            qm = 0
            qe = 0
            nm = 0
            ne = 0
            npassed = 0
            for idx in indices:
                # Grab the muons
                if idx<nmuons:
                    n = idx
                    #print("muons: ",idx,n,nmuons)
                    p4s.append(tempmuons[n])
                    qm += tempmuons[n].charge
                    nm += 1

                # Then the electrons
                else:
                    n = idx-nmuons
                    #print("electrons: ",idx,n,nelectrons)
                    p4s.append(tempelectrons[n])
                    qe += tempelectrons[n].charge
                    ne += 1

            tag = 'nm{0}_ne{1}_qtot{2}_qm{3}_qe{4}'.format(nm, ne, int(abs(qe+qm)), int(abs(qm)), int(abs(qe)))
            print(tag)
            #print("npassed: ",total_leptons)
            if nbody>0:
                mass = nat.invmass(p4s)
                #print(mass)
                if nbody<nmasses-1:
                    masses[nbody-2][tag].append(mass)

for i in range(nmasses-2):
    plt.figure(figsize=(14,8))
    print(i)
    for j,key in enumerate(masses[i].keys()):
        print("{0} {3}: {1}    # masses: {2}".format(i, key, len(masses[i][key]),j))
        plt.subplot(4,5,j+1)
        plt.hist(masses[i][key],bins=100,label=key)
        #plt.title(key,fontsize=10)
        plt.legend(fontsize=6)
    plt.tight_layout()
    plt.savefig('hexamasses_{0}.png'.format(i))


plt.show()
