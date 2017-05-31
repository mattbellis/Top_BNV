import ROOT
import sys
import matplotlib.pylab as plt
import numpy as np
import lichen.lichen as lch


f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

nentries = tree.GetEntries()
btags = []
jetpt = []
for i in range(nentries):
    tree.GetEntry(i)

    jetbtag = tree.jetbtag
    jpt = tree.jetpt
    njets = tree.njet

    for j in range(njets):
        btags.append(jetbtag[j])
        jetpt.append(jpt[j])
        #print(jetbtag[j])

btags = np.array(btags)
jetpt = np.array(jetpt)
        

plt.figure()
lch.hist_err(btags,bins=100,range=(0,1.25))
plt.xlabel(r"b-tagging variable", fontsize = 18)

plt.figure()
lch.hist_err(btags[jetpt<30],bins=100,range=(0,1.25))
plt.xlabel(r"b-tagging variable", fontsize = 18)

plt.figure()
lch.hist_err(btags[jetpt>=30],bins=100,range=(0,1.25))
plt.xlabel(r"b-tagging variable", fontsize = 18)

plt.figure()
#lch.hist_err(btags, range = [0,1.25],bins=100,markersize=5)
plt.hist(btags, range = [0,1.1],bins=110)
plt.xlabel("CSV2 b-tag output",fontsize=18)
plt.tight_layout()
plt.savefig('btag.png')

plt.figure()
#plt.plot(btags[(btags>=0)*(jetpt<100)],jetpt[(btags>=0)*(jetpt<100)],'.',alpha=0.1)
lch.hist_2D(btags[(btags>=0)*(jetpt<100)],jetpt[(btags>=0)*(jetpt<100)],xbins=100,ybins=100,xrange=(0,1),yrange=(0,100))
plt.xlabel(r"b-tagging variable", fontsize = 18)

plt.show()
