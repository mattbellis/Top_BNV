# From here
# https://root.cern.ch/root/html/tutorials/tree/copytree3.C.htm
import gc
import ROOT

import sys

tag = sys.argv[1]
year = sys.argv[2]
infile = sys.argv[3]
infile = "root://cmsxrootd.fnal.gov//"+infile

#outfile = "root://cmseos.fnal.gov//store/user/mbellis/small_skims_1k/"+infile.split('/')[-1].split('.root')[0] + '_SMALL_1k.root'
outfile = "root://cmseos.fnal.gov//store/user/mbellis/small_skims_1k/"+tag+"_"+year+"_SMALL_1k.root"

print("Opening...")
print(infile)

print("\nWriting to....")
print(outfile)

#exit()

# Get old file, old tree and set top branch address
oldfile = ROOT.TFile.Open(infile)
oldfile.ls()
oldtree = oldfile.Get("Events");
nentries = oldtree.GetEntries();
print("\nNentries: "+str(nentries)+"\n\n")
#Event *event   = 0;
#oldtree.SetBranchAddress("event",&event);

# Create a new file + a clone of old tree in new file
newfile = ROOT.TFile.Open(outfile,"recreate");
newtree = oldtree.CloneTree(0);

for i in range(nentries):
    if i%10000==0:
        print(i)

    #if i>=100000:
    if i>=1000:
        break

    oldtree.GetEntry(i);

    newtree.Fill();
    
#newtree.Print();
newtree.Write();
#newtree.AutoSave();
oldfile.Close()
newfile.Close()

#delete oldfile;
#delete newfile;

gc.collect()
