import numpy as np
import matplotlib.pylab as plt
import ROOT

import sys

import topbnv_tools as tbt



f = ROOT.TFile.Open(sys.argv[1])

t = f.Get("IIHEAnalysis")

#t.Print()
#exit()


nevents = t.GetEntries()

ebnv = []
esm = []
qpt = []
qeta = []
leppt = []
lepeta = []

cuts = []
ncuts = 5
# 0 - All hadronic decays on SM side
# 1 - lepton pt
# 2 - lepton eta
# 3 - jets pt
# 4 - jets eta

for i in range(ncuts):
    cuts.append([])

anti = 1
if sys.argv[1].find("aT2")>=0:
    anti = -1

for i in range(nevents):

    t.GetEntry(i)

    if i%1000==0:
        print(i)

    if i>1000:
        break


    nparticles = len(t.LHE_pdgid)

    #print("--------")
    bnvmuon = []
    bnvtop = []

    smmuon = []
    smtop = []

    Mt = 173.

    pass_lep_pt = True
    pass_lep_eta = True
    pass_jet_pt = True
    pass_jet_eta = True

    one_muon = True
    for j in range(nparticles):
        pid = t.LHE_pdgid[j]
        #print(pid)
        #'''
        if pid==-13 * anti:
            px,py,pz = tbt.etaphiTOxyz(t.LHE_Pt[j], t.LHE_Eta[j], t.LHE_Phi[j])
            bnvmuon = [t.LHE_E[j], px,py,pz, t.LHE_Pt[j], t.LHE_Eta[j]]
            leppt.append(t.LHE_Pt[j])
            lepeta.append(t.LHE_Eta[j])

        elif pid==13 * anti or pid==11 * anti or pid==15*anti:
            px,py,pz = tbt.etaphiTOxyz(t.LHE_Pt[j], t.LHE_Eta[j], t.LHE_Phi[j])
            smmuon = [t.LHE_E[j], px,py,pz, t.LHE_Pt[j], t.LHE_Eta[j]]
            one_muon = False

        elif pid==6 * anti:
            px,py,pz = tbt.etaphiTOxyz(t.LHE_Pt[j], t.LHE_Eta[j], t.LHE_Phi[j])
            bnvtop = [t.LHE_E[j], px,py,pz, t.LHE_Pt[j], t.LHE_Eta[j]]

        elif pid==-6 * anti:
            px,py,pz = tbt.etaphiTOxyz(t.LHE_Pt[j], t.LHE_Eta[j], t.LHE_Phi[j])
            smtop = [t.LHE_E[j], px,py,pz, t.LHE_Pt[j], t.LHE_Eta[j]]

        ########################################################################
        # Jets cuts
        ########################################################################
        if np.abs(pid) in [1,2,3,4,5]:
            pt = t.LHE_Pt[j]
            eta = t.LHE_Eta[j]

            if pt<1:
                print("--------")
                print(pt)
                print(pid)
                print(eta)

            qpt.append(pt)
            qeta.append(eta)

            if pt<30:
                pass_jet_pt = False
            if np.abs(eta)>2.5:
                pass_jet_eta = False

        ########################################################################
        # Lepton cuts
        ########################################################################
        if np.abs(pid) in [11,13,15]:
            pt = t.LHE_Pt[j]
            eta = t.LHE_Eta[j]

            if pt<25:
                pass_lep_pt = False
            if np.abs(eta)>2.5:
                pass_lep_eta = False


    if len(bnvmuon)>=4 and len(bnvtop)>=4:
        boosted = tbt.lorentz_boost(bnvmuon[0:4],bnvtop[0:4])
        Ee = boosted.item(0,0)
        ebnv.append(2*Ee/Mt)

        if one_muon:
            cuts[0].append(True)
            cuts[1].append(pass_lep_pt)
            cuts[2].append(pass_lep_eta)
            cuts[3].append(pass_jet_pt)
            cuts[4].append(pass_jet_eta)

    if len(smmuon)>=4 and len(smtop)>=4:
        boosted = tbt.lorentz_boost(smmuon[0:4],smtop[0:4])
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
#'''

plt.figure()
plt.subplot(2,2,1)
plt.hist(leppt,bins=50,range=(0,200),linewidth=3,fill=False,histtype='step',label='BNV',normed=True,color='r')
plt.subplot(2,2,2)
plt.hist(lepeta,bins=50,range=(-4,4),linewidth=3,fill=False,histtype='step',label='SM',normed=True,color='r')
plt.subplot(2,2,3)
plt.hist(qpt,bins=50,range=(0,200),linewidth=3,fill=False,histtype='step',label='BNV',normed=True,color='r')
plt.subplot(2,2,4)
plt.hist(qeta,bins=50,range=(-4,4),linewidth=3,fill=False,histtype='step',label='SM',normed=True,color='r')
#plt.xlabel(r'$2E_{\ell}/m_t$',fontsize=18)
#plt.legend(loc='upper left')
plt.tight_layout()
#plt.savefig('Fig1_from_paper.png')
plt.show()

cuts_text = ["SM hadronic: ",
             "lep pt>25: ",
             "lep abs(eta)<2.5: ",
             "jet pt>30: ",
             "jet abs(eta)<2.5: "]

print("%-28s  %5d" % ("N bnv decays: ",len(ebnv)))
indices = []
for i in range(len(cuts)):
    cuts[i] = np.array(cuts[i])
    print("%-28s  %5d" % (cuts_text[i],len(cuts[i][cuts[i]==True])))

index = cuts[0]*cuts[1]*cuts[2]
print("%-28s  %5d" % ("cut on lepton pt/eta: ", len(index[index])))
index = cuts[0]*cuts[3]*cuts[4]
print("%-28s  %5d" % ("cut on jet pt/eta: ", len(index[index])))

index = cuts[0]*cuts[1]*cuts[2]*cuts[3]*cuts[4]
print("%-28s  %5d" % ("cut on lepton/jet pt/eta: ", len(index[index])))
