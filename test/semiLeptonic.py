# import stuff
import ROOT
import sys
import matplotlib.pyplot as plt
import numpy as np
from PttoXYZ import PTtoXYZ
# Invariant Mass function
def invmass(p4):
	m2 = p4[0]**2 - p4[1]**2 - p4[2]**2 - p4[3]**2
	m = -999
	if m2 >= 0:
		m = np.sqrt(m2)
	else:
		m = -np.sqrt(np.abs(m2))
	return m


# Set the file and tree
f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

# Number of entries
nentries = tree.GetEntries()

tMasses = []
barMasses = []
dm0 = [0.,0.,0.,0.]
dm1 = [0.,0.,0.,0.]
bb = [0.,0.,0.,0.]

# Loop over all entries for a t
for i in range(nentries):
	tree.GetEntry(i)
	leptonic = False
	hadronic = False	
	'''
	top = 0
	b = 1
	W = 2
	W daughters = 3 + 4
	tbar = 5
	bbar = 6
	Wm = 7
	Wm daughters = 8 + 9
	'''
	
	d0pdg = tree.genpdg[3]
	d1pdg = tree.genpdg[4]
	
	if(d0pdg in range(1,6) or d1pdg in range(1,6)):
		hadronic = True
	elif(d0pdg in range(-16,-11) or d1pdg in range(-16,11)):
		leptonic = True 

	
	if(leptonic):
		dm0pdg = tree.genpdg[8]
		dm1pdg = tree.genpdg[9]

		if(dm0pdg in range(-16,-11) or dm1pdg in range(-16,-11)):
			continue
		else:
			# This is a hadronic decay
			dm0[0] = tree.gene[8]
			dm0[1] = tree.genpt[8]
			dm0[2] = tree.geneta[8]
			dm0[3] = tree.genphi[8]				
			dm0[1],dm0[2],dm0[3] = PTtoXYZ(dm0[1],dm0[2],dm0[3])

			dm1[0] = tree.gene[9]
			dm1[1] = tree.genpt[9]
			dm1[2] = tree.geneta[9]
			dm1[3] = tree.genphi[9]				
			dm1[1],dm1[2],dm1[3] = PTtoXYZ(dm1[1],dm1[2],dm1[3])

			dm0mass = invmass(dm0)
			dm1mass = invmass(dm1)

			bb[0] = tree.gene[6]
			bb[1] = tree.genpt[6]
			bb[2] = tree.geneta[6]
			bb[3] = tree.genphi[6]				
			bb[1],bb[2],bb[3] = PTtoXYZ(bb[1],bb[2],bb[3])
			
			bbmass = invmass(bb)

			tb = invmass(dm0 + dm1 + bb)
			
			#print(dm0mass)
			#print(dm1mass)

			tMasses.append(tb)



plt.figure()
plt.hist(tMasses, bins = 10)
plt.show()

