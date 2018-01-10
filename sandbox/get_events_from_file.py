import ROOT

import sys

f = ROOT.TFile.Open(sys.argv[1])

t0 = f.Get('meta')
t0.GetEntry(0)

t0.Print()

vals = t0.nEventsRaw,t0.nEventsStored,t0.globalTag
print(vals)
nRuns = t0.nRuns,

for n in nRuns:
    print(n)

t1 = f.Get('IIHEAnalysis')
nentries = t1.GetEntries()

print(nentries)

