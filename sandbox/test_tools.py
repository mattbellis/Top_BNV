import numpy as np
import matplotlib.pylab as plt
import math, ROOT, sys
import topbnv_tools as tbt



f = ROOT.TFile(sys.argv[1])

tree = f.Get("IIHEAnalysis")

nentries = tree.GetEntries()

for i in range(nentries):
    if i%1000==0:
        output = "Event: %d out of %d" % (i,nentries)
        print(output)

    tree.GetEntry(i)

    E, px, py, pz, pdgId = tbt.get_gen_particles(tree.GetEntry(i), tree)

    for i in pdgId:
        print(i)
    print("--------")
