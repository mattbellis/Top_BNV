import ROOT, sys
import numpy as np
import matplotlib.pylab as plt
#import lichen.lichen as lch
import math as math
from PttoXYZ import PTtoXYZ

def invmass(p4s):
    tot = np.array([0.,0.,0.,0.])
    for p4 in p4s:
        tot += p4
    m2 = tot[0]**2 - tot[1]**2 - tot[2]**2 - tot[3]**2
    m = -999
    if m2 >= 0:
        m = np.sqrt(m2)
    else:
        m = -np.sqrt(np.abs(m2))
    return m

def XYZtoPT(x,y,z):
    pt = x**2 + y**2
    eta = -math.log(math.tan(math.atan(abs(pt/z))/2.0))
    phi = math.acos(x/pt)
    return pt,eta,phi

f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

nentries = tree.GetEntries()

wCandidatesM = []
topCandidatesM = []
wCandidatesE = []
topCandidatesE = []
wCandidatesH = []
topCandidatesH = []
topCandidatesL = []

for i in range(nentries):
    if i % 1000 == 0:
        print(i)
    
    tree.GetEntry(i)

    leptonic = False

	#Jets
    jets = []
    btagJets = []
    
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
	
    for j in range(njets):
        jetx, jety, jetz = PTtoXYZ(jetpt[j],jeteta[j],jetphi[j])
        jet = [jete[j],jetx,jety,jetz]
        if btag[j] >= .84 and jetpt[j] >= 30:
            btagJets.append(jet)
        elif jetpt[j] >= 30:
            jets.append(jet)
    
    metx,mety,metz = PTtoXYZ(metpt,meteta,metphi)
    MET = [mete,metx,mety,metz]
    
    '''
    if metpt < 30:
        for m in range(nmuons):
            if abs(muonpt[m]) > 30:
                muonptF = float(muonpt[m])
                iso = (muonsumchhadpt[m]+muonsumnhadpt[m]+muonsumphotet[m])/muonptF
                muonx,muony,muonz = PTtoXYZ(muonpt[m],muoneta[m],muonphi[m])
                muon = [muone[m],muonx,muony,muonz]
                if iso <= .12:
                    W = invmass([MET,muon])
                    if W >= 65 and W <= 95:
                        for b in btagJets:
                            top = invmass([MET,muon,b])
                            #print(top)
                            #if top >= 160 and top <= 190:
                            topCandidatesM.append([MET,muon,b])
                            wCandidatesM.append([MET,muon])
                            topCandidatesL.append([MET,muon,b])
        for e in range(nelectrons):
            elecptF = float(elecpt[e])
            if(abs(elecptF) > 30):
                isovarE = (eleciso[e]+isoH[e]+isoE[e])/elecptF
                isovarB = (eleciso[e]+isoH[e]+max(0.,isoE[e]-1))/elecptF
        			
                elecx,elecy,elecz = PTtoXYZ(elecpt[e],eleceta[e],elecphi[e])
                electron = [elece[e],elecx,elecy,elecz]
        			
                # What should this value actually be cut at?
                if isovarE <= 0.04 and isovarB <= 0.04:
                    W = invmass([MET,electron])
                    if W >= 65 and W <= 95:
                        for b in btagJets:
                            top = invmass([MET,electron,b])
                            #if top >= 160 and top <= 190:
                            topCandidatesE.append([MET,electron,b])
                            wCandidatesE.append([MET,electron])
                            topCandidatesL.append([MET,electron,b])
    '''
    for m in range(nmuons):
        if abs(muonpt[m]) > 30:
            muonptF = float(muonpt[m])
            iso = (muonsumchhadpt[m]+muonsumnhadpt[m]+muonsumphotet[m])/muonptF
            muonx,muony,muonz = PTtoXYZ(muonpt[m],muoneta[m],muonphi[m])
            muon = [muone[m],muonx,muony,muonz]
            if iso <= .12:
                W = invmass([MET,muon])
                if W >= 65 and W <= 95:
                    for b in btagJets:
                        top = invmass([MET,muon,b])
                        #print(top)
                        #if top >= 160 and top <= 190:
                        topCandidatesM.append([MET,muon,b])
                        wCandidatesM.append([MET,muon])
                        topCandidatesL.append([MET,muon,b])
                        leptonic = True
    for e in range(nelectrons):
        elecptF = float(elecpt[e])
        if(abs(elecptF) > 30):
            isovarE = (eleciso[e]+isoH[e]+isoE[e])/elecptF
            isovarB = (eleciso[e]+isoH[e]+max(0.,isoE[e]-1))/elecptF
        	
            elecx,elecy,elecz = PTtoXYZ(elecpt[e],eleceta[e],elecphi[e])
            electron = [elece[e],elecx,elecy,elecz]
        			
            # What should this value actually be cut at?
            if isovarE <= 0.04 and isovarB <= 0.04:
                W = invmass([MET,electron])
                if W >= 65 and W <= 95:
                    for b in btagJets:
                        top = invmass([MET,electron,b])
                        #if top >= 160 and top <= 190:
                        topCandidatesE.append([MET,electron,b])
                        wCandidatesE.append([MET,electron])
                        topCandidatesL.append([MET,electron,b])
                        leptonic = True
    
    
    
    ''' 
    if leptonic:        
            
        #print('btag',len(btagJets))
        #print(njets)
    
        # At least 3 jets, including a btag
        if njets >= 3 and len(btagJets) >= 1:
            #print('made it')
            for j1 in range(0,len(jets)-1):
                for j2 in range(1,len(jets)):
                    W = invmass([jets[j1],jets[j2]])
                    #print('w',W)
                    #print(j1,j2)
                    if W >= 65 and W <= 95:
                        for b in btagJets:
                            top = invmass([jets[j1],jets[j2],b])
                            #print(top)
                            #if top >= 160 and top <= 190:
                            topCandidatesH.append([jets[j1],jets[j2],b])
                            wCandidatesH.append([jets[j1],jets[j2]])
							
    '''
    
    #print('btag',len(btagJets))
    #print(njets)

    # At least 3 jets, including a btag
    if njets >= 3 and len(btagJets) >= 1:
        #print('made it')
        for j1 in range(0,len(jets)-1):
            for j2 in range(1,len(jets)):
                W = invmass([jets[j1],jets[j2]])
                #print('w',W)
                #print(j1,j2)
                if W >= 65 and W <= 95:
                    for b in btagJets:
                        top = invmass([jets[j1],jets[j2],b])
                        #print(top)
                        #if top >= 160 and top <= 190:
                        topCandidatesH.append([jets[j1],jets[j2],b])
                        wCandidatesH.append([jets[j1],jets[j2]])


    # MC Truth Info
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
   
    if wc1pdg == 11 or wc1mpdg == -11 or wc1pdg == 11 or wc2pdg == -11:
        for l in range(len(topCandidatesE)):
            electron = topCandidatesE[l][1]
            electrone, electronx, electrony, electronz = electron
            electronpt, electroneta, electronphi = XYZtoPT(electronx,electrony,electronz)
            if(abs(electronpt-wc1[1]) <= 1 or abs(electronpt - wc1m[1]) <= 1):
                print('right electron')
            if(abs(electronpt-wc2[1]) <= 1 or abs(electronpt - wc2m[1]) <= 1):
                print('right electron')
            


Hmasses = []
Mmasses = []
Emasses = []
Lmasses = []

for i in range(len(topCandidatesH)):
	Hmasses.append(invmass(topCandidatesH[i]))
#print(invmass(topCandidatesH[i]))
#print(len(Hmasses))
for i in range(len(topCandidatesE)):
	Emasses.append(invmass(topCandidatesE[i]))

for i in range(len(topCandidatesL)):
	Lmasses.append(invmass(topCandidatesL[i]))

for i in range(len(topCandidatesM)):
	Mmasses.append(invmass(topCandidatesM[i]))


plt.figure()
plt.hist(Hmasses, bins = 100, range = (150,200), color = 'red', label = 'Hadronic')
plt.hist(Lmasses, bins = 100, range = (150,200), color = 'yellow', label = 'Leptonic')
#lch.hist_err(Emasses, bins = 200, range = (150,200), color = 'blue', label = 'Semileptonic Muon')
#lch.hist_err(Mmasses, bins = 200, range = (150,200), color = 'black', label = 'Semileptonic Electron')
plt.legend()
plt.show()

