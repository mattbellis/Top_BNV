import ROOT, sys
import numpy as np
import matplotlib.pylab as plt
import lichen.lichen as lch
from PttoXYZ import PTtoXYZ

def invmass(p4s):
     tot = np.array([0.,0.,0.,0.])
     for p4 in p4s:
         tot += p4
     m2 = tot[0]**2 - tot[1]**2 - tot[2]**2 - tot[3]**2
     m = -999
     if m2 >= 0:
         mp = np.sqrt(m2)
     else:
         m = -np.sqrt(np.abs(m2))
     return m

f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

nentries = tree.GetEntries()

for i in range(nentries):
	if i % 100 == 0:
		print(i)
		
	#Jets
	jets = []
	btagJets = []
	wCandidatesH = []
	topCandidatesH = []

	njets = tree.njet
	btag = tree.jetbtag
	jetpt = tree.jetpt
	jete = tree.jete
	jeteta = tree.jeteta
	jetphi = tree.jetphi

	for j in range(njets):
		jetx, jety, jetz = PTtoXYZ(jetpt[j],jeteta[j],jetphi[j])
		jet = [jete[j],jetx,jety,jetz]
		if btag[j] >= .84:
			btagJets.append(jet)
		else:
			jets.append(jet)
	
	# At least 3 jets, including a btag
	if njets >= 3 and len(btagJets) >= 1:
		for j1 in range(0,len(jets)-1):
			for j2 in range(1,len(jets)):
				W = invmass([jets[j1],jets[j2]])
				if W >= 65 and W <= 95:
					for b in btagJets:
						top = invmass([jets[j1],jets[j2],b])
						if top >= 160 and top <= 190:
							topCandidatesH.append([jets[j1],jets[j2],b])
							wCandidatesH.append([jets[j1],jets[j2]])
							
	wCandidatesM = []
	topCandidatesM = []
	wCandidatesE = []
	topCandidatesE = []
	
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
	iso = tree.electronTkIso
	isoH = tree.electronHCIso
	isoE = tree.electronECIso

	# Check if there was a possible hadronic decay, then check for leptonic
	if len(topCandidates) >= 1:
		# Leptonic decay needs an isolated lepton, btag jet and missing ET
		# Missing ET and lepton should be a wCandidate							
		metx,mety,metz = PTtoXYZ(metpt,meteta,metphi)
		MET = [mete,metx,mety,metz]

		for m in range(nmuons):
			muonpt = float(muonpt[m])
			iso = (muonsumchhadpt[m]+muonsumnhadpt[m]+muonsumphotet[m])/muonpt
			muonx,muony,muonz = PTtoXYZ(muonpt[m],muoneta[m],muonphi[m])
			muon = [muone[m],muonx,muony,muonz]
			if iso >= .84:
				W = invmass([MET,muon])
				if W >= 65 and W <= 95:
					for b in btagJets:
						top = invmass([MET,muon,b])
						if top >= 160 and top <= 190:
							topCandidatesM.append([MET,muon,b])
							wCandidatesM.append([MET,muon])
								
		for e in range(nelectrons):
			elecpt = float(elecpt[e])
			isovarE = (iso[e]+isoH[e]+isoE[e])/elecpt
			isovarB = (iso[e]+isoH[e]+max(0.,isoE[e]-1))/elecpt 
			
			elecx,elecy,elecz = PTtoXYZ(elecpt,eleceta[e],elecphi[e])
			electron = [elece[e],elecx,elecy,elecz]
			
			# What should this value actually be cut at?
			if isovarE >= 0 and isovarB >= 0:
				W = invmass([MET,electron])
				if W >= 65 and W <= 95:
					for b in btagJets:
						top = invmass([MET,electron,b])
						if top >= 160 and top <= 190:
							topCandidatesE.append([MET,electron,b])
							wCandidatesE.append([MET,electron])

Hmasses = []
Mmasses = []
Emasses = []


for i in range(len(topCandidatesH)):
	Hmasses.append(invmass(topCandidatesH[i]))

for i in range(len(topCandidatesE)):
	Emasses.append(invmass(topCandidatesE[i]))

for i in range(len(topCandidatesM)):
	Mmasses.append(invmass(topCandidatesM[i]))


plt.figure()
lch.hist_err(topCandidatesH,bins = 100, color = 'red', label = 'Hadronic')
lch.hist_err(topCandidatesM, bins = 100, color = 'blue', label = 'Semileptonic Muon')
lch.hist_err(topCandidatesE, bins = 100, color = 'black', label = 'Semileptonic Electron')
plt.legend()
plt.show()
