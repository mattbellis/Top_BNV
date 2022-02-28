# From here
# https://root.cern.ch/root/html/tutorials/tree/copytree3.C.htm
import gc
import ROOT

import sys

infile = sys.argv[1]
infile = "root://cmsxrootd.fnal.gov//"+infile

#outfile = infile.split('/')[-1].split('.root')[0] + '_SMALL_1k.root'
#outfile = "root://cmseos.fnal.gov//store/user/mbellis/test/"+infile.split('/')[-1].split('.root')[0] + '_SMALL_1k.root'

# Write it here
outfile = infile.split('/')[-1].split('.root')[0] + '_SMALL_10k.root'

#outfile = infile.split('.root')[0] + '_SMALL_1k.root'
#outfile = infile.split('.root')[0] + '_SMALL_100k.root'

print(infile)
print(outfile)

#exit()

# Get old file, old tree and set top branch address
oldfile = ROOT.TFile.Open(infile)
oldfile.ls()
oldtree = oldfile.Get("Events");
oldtree1 = oldfile.Get("LuminosityBlocks");
oldtree2 = oldfile.Get("Runs");
oldtree3 = oldfile.Get("MetaData");
#oldtree4 = oldfile.Get("ParameterSets");
#Event *event   = 0;
#oldtree.SetBranchAddress("event",&event);
print("nentries: "+str(nentries))

# Create a new file + a clone of old tree in new file
newfile = ROOT.TFile.Open(outfile,"recreate");
newtree = oldtree.CloneTree(0);
newtree1 = oldtree1.CloneTree(0);
newtree2 = oldtree2.CloneTree(0);
newtree3 = oldtree3.CloneTree(0);

nentries = oldtree.GetEntries();
for i in range(nentries):
    if i%10000==0:
        print(i)

    #if i>=100000:
    if i>=10000:
        break

    oldtree.GetEntry(i);

    newtree.Fill();
    
   
# The others
nentries = oldtree1.GetEntries();
for i in range(nentries):
    oldtree1.GetEntry(i);
    newtree1.Fill();

nentries = oldtree2.GetEntries();
for i in range(nentries):
    oldtree2.GetEntry(i);
    newtree2.Fill();

nentries = oldtree3.GetEntries();
for i in range(nentries):
    oldtree3.GetEntry(i);
    newtree3.Fill();

#newtree.Print();
newtree.Write();
newtree1.Write();
newtrea2.Write();
newtree3.Write();

#newtree.AutoSave();
oldfile.Close()
newfile.Close()

#delete oldfile;
#delete newfile;

gc.collect()
