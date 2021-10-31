# From here
# https://root.cern.ch/root/html/tutorials/tree/copytree3.C.htm
import gc
import ROOT

import sys

infile = sys.argv[1]
outfile = infile.split('.root')[0] + '_SMALL_1k.root'
#outfile = infile.split('.root')[0] + '_SMALL_100k.root'

# Get old file, old tree and set top branch address
oldfile = ROOT.TFile.Open(infile)
oldfile.ls()
oldtree = oldfile.Get("Events");
nentries = oldtree.GetEntries();
#Event *event   = 0;
#oldtree.SetBranchAddress("event",&event);

# Create a new file + a clone of old tree in new file
newfile = ROOT.TFile(outfile,"recreate");
newtree = oldtree.CloneTree(0);

for i in range(nentries):
    if i%10000==0:
        print(i)

    #if i>=100000:
    if i>=1000:
        break

    oldtree.GetEntry(i);

    newtree.Fill();
    
newtree.Print();
newtree.Write();
#newtree.AutoSave();
oldfile.Close()
newfile.Close()

#delete oldfile;
#delete newfile;

gc.collect()
