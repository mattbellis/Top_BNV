import ROOT
import sys

import numpy as np
import matplotlib.pylab as plt

from PttoXYZ import PTtoXYZ

def invmass(p4):

    m2 = p4[0]**2 - p4[1]**2- p4[2]**2- p4[3]**2

    m = -999
    if m2>=0:
        m = np.sqrt(m2)
    else:
        m = -np.sqrt(np.abs(m2))

    return m


f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

#print("In the file...")
#f.ls()
#print("In the TTree...")
#tree.Print()
#exit()

nentries = tree.GetEntries()

topPT = []
muonPT = []
tbarPT = []
#genPDG = []

top = np.array([0., 0., 0., 0.])
W = np.array([0., 0., 0., 0.])
b = np.array([0., 0., 0., 0.])
WChild1 = np.array([0., 0., 0., 0.,0])
WChild2 = np.array([0., 0., 0., 0.,0])

tbar = np.array([0., 0., 0., 0.])
Wm = np.array([0., 0., 0., 0.])
bbar = np.array([0., 0., 0., 0.])
WmChild1 = np.array([0., 0., 0., 0.,0])
WmChild2 = np.array([0., 0., 0., 0.,0])


diffs = []
diffsBar = []
for i in range(4):
    diffs.append([])
    diffsBar.append([])
Wdiffs = []
WdiffsM = []
for i in range(4):
    Wdiffs.append([])
    WdiffsM.append([])
masses = []
for i in range(6):
    masses.append([])

decayProducts = []
for i in range(3):
    decayProducts.append([])
numBoosted = 0
muonCount = 0
electronCount = 0
tauCount = 0
#ngen = tree.ngen
for i in range(nentries):

        #print(" ---------------- ")
        tree.GetEntry(i)
        ngen = tree.ngen
        genpt = tree.genpt
        genpdg = tree.genpdg

        top[0] = tree.gene[0]
        top[1] = tree.genpt[0]
        top[2] = tree.geneta[0]
        top[3] = tree.genphi[0]
        
        tbar[0] = tree.gene[5]
        tbar[1] = tree.genpt[5]
        tbar[2] = tree.geneta[5]
        tbar[3] = tree.genphi[5]

        #print(top)
        topPT.append(top[1])
        tbarPT.append(tbar[1])
        if (top[1]>= 400 or tbar[1]>=400):
            numBoosted += 1
        #if(tbar[1]>=400):
        #    numBoosted += 1
        top[1],top[2],top[3] = PTtoXYZ(top[1],top[2],top[3])
        tbar[1],tbar[2],tbar[3] = PTtoXYZ(tbar[1],tbar[2],tbar[3])

        #print(top)

        W[0] = tree.gene[2]
        W[1] = tree.genpt[2]
        W[2] = tree.geneta[2]
        W[3] = tree.genphi[2]
        W[1],W[2],W[3] = PTtoXYZ(W[1],W[2],W[3])

        b[0] = tree.gene[1]
        b[1] = tree.genpt[1]
        b[2] = tree.geneta[1]
        b[3] = tree.genphi[1]
        b[1],b[2],b[3] = PTtoXYZ(b[1],b[2],b[3])
        
        Wm[0] = tree.gene[7]
        Wm[1] = tree.genpt[7]
        Wm[2] = tree.geneta[7]
        Wm[3] = tree.genphi[7]
        Wm[1],Wm[2],Wm[3] = PTtoXYZ(Wm[1],Wm[2],Wm[3])

        bbar[0] = tree.gene[6]
        bbar[1] = tree.genpt[6]
        bbar[2] = tree.geneta[6]
        bbar[3] = tree.genphi[6]
        bbar[1],bbar[2],bbar[3] = PTtoXYZ(bbar[1],bbar[2],bbar[3])

        WChild1[0] = tree.gene[4]
        WChild1[1] = tree.genpt[4]
        WChild1[2] = tree.geneta[4]
        WChild1[3] = tree.genphi[4]
        WChild1[4] = tree.genpdg[4]
        WChild1[1],WChild1[2],WChild1[3] = PTtoXYZ(WChild1[1],WChild1[2],WChild1[3])
    
        WChild2[0] = tree.gene[3]
        WChild2[1] = tree.genpt[3]
        WChild2[2] = tree.geneta[3]
        WChild2[3] = tree.genphi[3]
        WChild2[4] = tree.genpdg[3]
        WChild2[1],WChild2[2],WChild2[3] = PTtoXYZ(WChild2[1],WChild2[2],WChild2[2]) 
        
        WmChild1[0] = tree.gene[8]
        WmChild1[1] = tree.genpt[8]
        WmChild1[2] = tree.geneta[8]
        WmChild1[3] = tree.genphi[8]
        WmChild1[4] = tree.genpdg[8]
        WmChild1[1],WmChild1[2],WmChild1[3] = PTtoXYZ(WmChild1[1],WmChild1[2],WmChild1[3])
        
        WmChild2[0] = tree.gene[9]
        WmChild2[1] = tree.genpt[9]
        WmChild2[2] = tree.geneta[9]
        WmChild2[3] = tree.genphi[9]
        WmChild2[4] = tree.genpdg[9]
        WmChild2[1],WmChild2[2],WmChild2[3] = PTtoXYZ(WmChild2[1],WmChild2[2],WmChild2[3])
        
        if(WChild1[4] == 13):
            muonPT.append(WChild1[1])
        if(WChild2[4] == 13):
            muonPT.append(WChild2[1])
        if(WmChild1[4] == 13):
            muonPT.append(WmChild1[1])
        if(WmChild2[4] == 13):
            muonPT.append(WmChild2[1])

        #print(WChild1[4])
        #print(WChild2[4])
        if(WChild1[4] == -13.0 or WChild2[4] == -13.0):
            muonCount += 1
        elif(WChild1[4] == -11.0 or WChild2[4] == -11.0):
            electronCount += 1
        elif(WChild1[4] == -15.0 or WChild2[4] == -15.0):
            tauCount += 1        
        if(WmChild1[4] == 13.0 or WmChild2[4] == 13.0):
            muonCount += 1
        elif(WmChild1[4] == 11.0 or WmChild2[4] == 11.0):
            electronCount += 1
        elif(WmChild1[4] == 15.0 or WmChild2[4] == 15.0):
            tauCount += 1 

        #print(invmass(top))
        diff = top-W-b
        diffBar = tbar-Wm-bbar
        for j in range(4):
            diffs[j].append(diff[j])
            diffsBar[j].append(diffBar[j])
        
        Wdiff = [0.,0.,0.,0.]
        WdiffM = [0.,0.,0.,0.]

        Wdiff[0] = W[0]-WChild1[0]-WChild2[0]
        Wdiff[1] = W[1]-WChild1[1]-WChild2[1]
        Wdiff[2] = W[2]-WChild1[2]-WChild2[2]
        Wdiff[3] = W[3]-WChild1[3]-WChild2[3]

       
        WdiffM[0] = Wm[0]-WmChild1[0]-WmChild2[0]
        WdiffM[1] = Wm[1]-WmChild1[1]-WmChild2[1]
        WdiffM[2] = Wm[2]-WmChild1[2]-WmChild2[2]
        WdiffM[3] = Wm[3]-WmChild1[3]-WmChild2[3]

        
        
        for j in range(4):
            Wdiffs[j].append(Wdiff[j])
            WdiffsM[j].append(WdiffM[j])

        masses[0].append(invmass(top))
        masses[1].append(invmass(W))
        masses[2].append(invmass(b))
        masses[3].append(invmass(tbar))
        masses[4].append(invmass(Wm))
        masses[5].append(invmass(bbar))
        
        '''
	for i in range(ngen):
		#print(genpdg[i])
		genPDG.append(genpdg[i])

		#print(genpt[i])
		topPT.append(genpt[i])
        '''
print("The percent of boosted tops is: ", numBoosted/nentries*100)
print("The percent of muon decays is: ", muonCount/nentries*100)
print("The percent of electron decays is: ", electronCount/nentries*100)
print("The percent of tau decays is: ", tauCount/nentries*100)


pltTitles = ["E","px","py","pz"]
plt.figure()
for j in range(0,4):
    plt.subplot(2,2,j+1)
    plt.title(pltTitles[j])
    plt.hist(diffs[j],bins=125,range=(-50,50))
plt.tight_layout()

plt.figure()
for j in range(0,4):
    plt.subplot(2,2,j+1)
    plt.title(pltTitles[j] + " tbar")
    plt.hist(diffsBar[j],bins=25,range=(-50,50))
plt.tight_layout()

pltTitles = ["W diff E","W diff px","W diff py","W diff pz"]
plt.figure()
for j in range(0,4):
    plt.subplot(2,2,j+1)
    plt.title(pltTitles[j])
    plt.hist(Wdiffs[j],bins=125,range=(-50,50))
plt.tight_layout()

plt.figure()
for j in range(0,4):
    plt.subplot(2,2,j+1)
    plt.title(pltTitles[j] + " m")
    plt.hist(WdiffsM[j],bins=25,range=(-50,50))
plt.tight_layout()



pltTitles2 = ["Mass Top", "Mass W", "Mass B"]
plt.figure()
for j in range(0,3):
    plt.subplot(2,2,j+1)
    plt.hist(masses[j],bins=25)
    plt.title(pltTitles2[j])
plt.tight_layout()

plt.figure()
for j in range(3,6):
    plt.subplot(2,2,j-2)
    plt.hist(masses[j],bins=25)
    plt.title(pltTitles2[j-3] + " tbar")
plt.tight_layout()

plt.figure()
plt.title("Top PT")
plt.hist(topPT,bins = 25)

plt.figure()
plt.title("TBar PT")
plt.hist(tbarPT,bins = 25)

plt.figure()
plt.title("Muon PT")
plt.hist(muonPT,bins = 25)


plt.show()


