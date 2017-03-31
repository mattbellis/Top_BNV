import ROOT
import sys

import numpy as np
import matplotlib.pylab as plt


f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

#print("In the file...")
#f.ls()
#print("In the TTree...")
#tree.Print()
#exit()

nentries = tree.GetEntries()

topPT = []
genPDG = []

#ngen = tree.ngen
for i in range(nentries):
	tree.GetEntry(i)
	ngen = tree.ngen
	genpt = tree.genpt
	genpdg = tree.genpdg
	for i in range(ngen):
		#print(genpdg[i])
		genPDG.append(genpdg[i])

		#print(genpt[i])
		topPT.append(genpt[i])

print(genPDG[1])
