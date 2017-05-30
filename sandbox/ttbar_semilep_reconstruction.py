
import ROOT

import sys

import numpy as np
import matplotlib.pylab as plt

# Might need to comment this if lichen is not installed
import lichen.lichen as lch


f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

# Uncomment this if you just want to see what is stored
# in the file.
'''
print("In the file...")
f.ls()
print("In the TTree....")
tree.Print()
exit()
'''

################################################################################
def invmass(p4s):
    tot = np.array([0.0, 0.0, 0.0, 0.0])
    #print("-------------")
    for p4 in p4s:
        #print(p4)
        tot += p4

    m2 = tot[0]**2 - (tot[1]**2 + tot[2]**2 + tot[3]**2)
    if m2>=0:
        return np.sqrt(m2)
    else:
        return -np.sqrt(-m2)
################################################################################

nentries = tree.GetEntries()

metpt = []
muonpt = []
jetbtag = []
jet3mass = []
jet2mass = []

btagcut = 0.84

for nentry in range(nentries):

    jets = []
    bjets = []

    if nentry%100==0:
        print(nentry)

    output = "Event: %d\n" % (nentry)
    tree.GetEntry(nentry)

    nmuon = tree.nmuon
    njet = tree.njet

    metpt.append(tree.metpt)

    onegood_muon = False
    for i in range(nmuon):
        muonpt.append(tree.muonpt[i])
        if nmuon==1 and tree.muonpt[i]>50:
            onegood_muon = True

    if onegood_muon == False:
        continue 

    for i in range(njet):
        jetbtag.append(tree.jetbtag[i])
        if tree.jetbtag[i] > btagcut:
            if tree.jetpt[i]>10:
                bjets.append(np.array([tree.jete[i], tree.jetpx[i], tree.jetpy[i], tree.jetpz[i]]))
        else:
            if tree.jetpt[i]>10:
                jets.append(np.array([tree.jete[i], tree.jetpx[i], tree.jetpy[i], tree.jetpz[i]]))

    if len(bjets)>1 and len(jets)>1:
        #print(len(bjets),len(jets))
        for bjet in bjets:
            for i in range(0,len(jets)-1):
                for j in range(i+1,len(jets)):
                    p4s = []
                    p4s.append(bjet)
                    p4s.append(jets[i])
                    p4s.append(jets[j])
                    m = invmass(p4s)
                    #print("mass: ",m)
                    jet3mass.append(m)
                    jet2mass.append(invmass([jets[i],jets[j]]))



muonpt = np.array(muonpt)
metpt = np.array(metpt)
jetbtag = np.array(jetbtag)
jet3mass = np.array(jet3mass)
jet2mass = np.array(jet2mass)

plt.figure()
lch.hist_err(metpt[metpt<500])
plt.xlabel(r'$mising E_T$')

plt.figure()
lch.hist_err(muonpt[(muonpt<200)*(muonpt>30)])
plt.xlabel(r'$p_T \mu$')

plt.figure()
lch.hist_err(jetbtag[jetbtag>=0])
plt.xlabel(r'jets b-tagging')

plt.figure()
lch.hist_err(jet3mass[jet3mass<400])
plt.xlabel(r'3-jets mass')

plt.figure()
lch.hist_err(jet2mass[jet2mass<400])
plt.xlabel(r'2-jets mass')

plt.figure()
lch.hist_err(jet3mass[(jet3mass<400)*(jet2mass>60)*(jet2mass<120)])
plt.xlabel(r'3-jets mass')



plt.show()

