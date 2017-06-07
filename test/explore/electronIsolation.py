import ROOT
import sys
import matplotlib.pylab as plt
import lichen.lichen as lch

f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

nent = tree.GetEntries()

isoVarE = []
isoVarB = []

nelecs = 0

for i in range(nent):
    tree.GetEntry(i)

    iso = tree.electronTkIso
    isoH = tree.electronHCIso
    isoE = tree.electronECIso    
    nelec = tree.nelectron
    elecPT = tree.electronpt
    
    nelecs += nelec 

    for j in range(nelec):
        #if elecPT[j] >= 30 and elecPT[j] <= 100:
        isovarE = (iso[j]+isoH[j]+isoE[j])/elecPT[j]
        isoVarE.append(isovarE)
        isovarB = (iso[j]+isoH[j]+max(0.,isoE[j]-1))/elecPT[j]
        isoVarB.append(isovarB)
        #print('Max: ', max(0.,isoE[j]-1))
        #print(isoE[j])



print(nelecs)

plt.figure()
lch.hist_err(isoVarB,bins = 100,range=(0,1))
plt.xlabel('dr03 Barrel Electron Isolation Variable')

plt.figure()
lch.hist_err(isoVarE,bins = 100,range=(0,1))
plt.xlabel('dr03 Endcap Electron Isolation Variable')

plt.show()
