import ROOT
import sys
import matplotlib.pyplot as plt
import numpy as np
import lichen.lichen as lch

import topbnv_tools as tb


f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

nentries = tree.GetEntries()
tops = []

for i in range(nentries):
    tree.GetEntry(i)

    genp = [tree.genpdg, tree.gene, tree.genpt, tree.geneta, tree.genphi]

    genmc = tb.GenParticles(genp)

    print("------------")
    genmc.pretty_print()

    dectype = genmc.decay_type()
    print(dectype)

    if "lep" in dectype:
        muons = genmc.muons()
        for m in muons:
            print(m)
