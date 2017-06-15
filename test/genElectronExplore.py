import ROOT, sys, math
import matplotlib.pylab as plt
import numpy as np

f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

nent = tree.GetEntries()
genpts = []
genetas = []
electronpts = []
electronetas = []

count = 0
total = 0 
electrons = 0

for i in range(nent):
    if i % 1000 == 0:
        print(i)

    tree.GetEntry(i)

# Get all the tree items you will need
    # Jets
    njets = tree.njet
    btag = tree.jetbtag
    jetpt = tree.jetjecpt
    jete = tree.jetjece
    jeteta = tree.jetjeceta
    jetphi = tree.jetjecphi
    
    # MET
    metpt = tree.metpt
    mete = tree.mete
    meteta = tree.meteta
    metphi = tree.metphi
    
    # Muons
    muonpt = tree.muonpt
    muone = tree.muone
    muoneta = tree.muoneta
    muonphi = tree.muonphi
    nmuons = tree.nmuon
    muonsumnhadpt = tree.muonsumnhadpt
    muonsumchhadpt = tree.muonsumchhadpt
    muonsumphotet = tree.muonsumphotEt

    # Electrons
    elecpt = tree.electronpt
    elece = tree.electrone
    eleceta = tree.electroneta
    elecphi = tree.electronphi
    nelectrons = tree.nelectron
    eleciso = tree.electronTkIso
    isoH = tree.electronHCIso
    isoE = tree.electronECIso

    # MC Truth
    b = [0.,0.,0.,0.]
    bb = [0.,0.,0.,0.]
    wc1 = [0.,0.,0.,0.]
    wc2 = [0.,0.,0.,0.]
    wc1m = [0.,0.,0.,0.]
    wc2m = [0.,0.,0.,0.]

    b[0] = tree.gene[1]
    b[1] = tree.genpt[1]
    b[2] = tree.geneta[1]
    b[3] = tree.genphi[1]
    #b[1],b[2],b[3] = PTtoXYZ(b[1],b[2],b[3])

    bb[0] = tree.gene[6]
    bb[1] = tree.genpt[6]
    bb[2] = tree.geneta[6]
    bb[3] = tree.genphi[6]
    #bb[1],bb[2],bb[3] = PTtoXYZ(bb[1],bb[2],bb[3])

    wc1[0] = tree.gene[4]
    wc1[1] = tree.genpt[4]
    wc1[2] = tree.geneta[4]
    wc1[3] = tree.genphi[4]
    wc1pdg = tree.genpdg[4] 
    #wc1[1],wc1[2],wc1[3] = PTtoXYZ(wc1[1],wc1[2],wc1[3])
    
    wc2[0] = tree.gene[3]
    wc2[1] = tree.genpt[3]
    wc2[2] = tree.geneta[3]
    wc2[3] = tree.genphi[3]
    wc2pdg = tree.genpdg[3] 
    #wc2[1],wc2[2],wc2[3] = PTtoXYZ(wc2[1],wc2[2],wc2[3])

    wc1m[0] = tree.gene[9]
    wc1m[1] = tree.genpt[9]
    wc1m[2] = tree.geneta[9]
    wc1m[3] = tree.genphi[9]
    wc1mpdg = tree.genpdg[9] 
    #wc1m[1],wc1m[2],wc1m[3] = PTtoXYZ(wc1m[1],wc1m[2],wc1m[3])

    wc2m[0] = tree.gene[8]
    wc2m[1] = tree.genpt[8]
    wc2m[2] = tree.geneta[8]
    wc2m[3] = tree.genphi[8]
    wc2mpdg = tree.genpdg[8] 
    #wc2m[1],wc2m[2],wc2m[3] = PTtoXYZ(wc2m[1],wc2m[2],wc2m[3])

    Wchildren = [[wc1pdg,wc1],[wc1mpdg,wc1m],[wc2pdg,wc2],[wc2mpdg,wc2m]]


    for j in range(0,3):
        if abs(Wchildren[j][0]) == 11:
            genpt = Wchildren[j][1][1]
            genpts.append(genpt)
            geneta = Wchildren[j][1][2]
            genetas.append(Wchildren[j][1][2])
            total += 1
            if(genpt > 45 and abs(geneta) < 2.494):
                count += 1

    for j in range(nelectrons):
        electronpt = elecpt[j]
        electronpts.append(electronpt)
        electroneta = eleceta[j]
        electronetas.append(electroneta)
        electrons += 1

print(min(electronetas),max(electronetas))
print(min(electronpts))
print('Gen > 45 and -2.49 < eta < 2.49: ', count)
print('Gen lost', total - count)
print('Total gen electrons', total)
print('Total electrons', electrons)
plt.figure()
plt.hist(genpts, bins=100, color = 'red', alpha = 0.2, normed = True, label = 'Gen')
plt.hist(electronpts, bins=100, color = 'blue', alpha = 0.2, normed = True, label = 'Reconstructed')
#plt.hist(genpts, bins=100, color = 'red', label = 'Gen')
#plt.hist(electronpts, bins=100, color = 'blue', label = 'Reconstructed')
plt.xlabel('pt')
plt.legend()

plt.figure()
plt.hist(electronetas, bins=100, color = 'blue', alpha = 0.2, normed = True, label = 'Reconstructed')
plt.hist(genetas, bins=100, color = 'red', alpha = 0.2, normed = True, label = 'Gen')
plt.xlabel('eta')
plt.legend()

plt.show()
