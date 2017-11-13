import numpy as np
import matplotlib.pylab as plt
import ROOT

import sys

import topbnv_tools as tbt



f = ROOT.TFile.Open(sys.argv[1])

t = f.Get("IIHEAnalysis")

nevents = t.GetEntries()

ebnv = []
esm = []

anti = 1
if sys.argv[1].find("aT2")>=0:
    anti = -1

for i in range(nevents):

    t.GetEntry(i)

    if i%1000==0:
        print(i)

    nparticles = len(t.LHE_pdgid)

    #print("--------")
    bnvmuon = []
    bnvtop = []

    smmuon = []
    smtop = []

    Mt = 173.

    for j in range(nparticles):
        pid = t.LHE_pdgid[j]
        #print(pid)
        #'''
        if pid==-13 * anti:
            px,py,pz = tbt.etaphiTOxyz(t.LHE_Pt[j], t.LHE_Eta[j], t.LHE_Phi[j])
            bnvmuon = [t.LHE_E[j], px,py,pz]

        elif pid==13 * anti or pid==11 * anti:
            px,py,pz = tbt.etaphiTOxyz(t.LHE_Pt[j], t.LHE_Eta[j], t.LHE_Phi[j])
            smmuon = [t.LHE_E[j], px,py,pz]

        elif pid==6 * anti:
            px,py,pz = tbt.etaphiTOxyz(t.LHE_Pt[j], t.LHE_Eta[j], t.LHE_Phi[j])
            bnvtop = [t.LHE_E[j], px,py,pz]

        elif pid==-6 * anti:
            px,py,pz = tbt.etaphiTOxyz(t.LHE_Pt[j], t.LHE_Eta[j], t.LHE_Phi[j])
            smtop = [t.LHE_E[j], px,py,pz]

    if len(bnvmuon)==4 and len(bnvtop)==4:
        boosted = tbt.lorentz_boost(bnvmuon,bnvtop)
        Ee = boosted.item(0,0)
        ebnv.append(2*Ee/Mt)

    if len(smmuon)==4 and len(smtop)==4:
        boosted = tbt.lorentz_boost(smmuon,smtop)
        Ee = boosted.item(0,0)
        esm.append(2*Ee/Mt)




#'''
print(len(ebnv))
print(len(esm))
plt.figure()
plt.hist(ebnv,bins=50,range=(0,1),linewidth=3,fill=False,histtype='step',label='BNV',normed=True,color='r')
plt.hist(esm,bins=50,range=(0,1),linewidth=3,fill=False,histtype='step',label='SM',normed=True,color='b')
plt.xlabel(r'$2E_{\ell}/m_t$',fontsize=18)
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig('Fig1_from_paper.png')
plt.show()
#'''
