# Notes on file access

edmFileUtil -d /store/mc/RunIISummer20UL16NanoAODv9/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_v17-v1/280000/52C47220-8299-4F4F-BCF4-87C6D32CF79A.root

edmProvDump /store/mc/RunIISummer20UL16NanoAODv9/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_v17-v1/280000/52C47220-8299-4F4F-BCF4-87C6D32CF79A.root



# Accessing files in ROOT
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookXrootdService#OpenwithRoot
Open a file using ROOT
If you are using bare ROOT, you can open files in the xrootd service just like you would any other file:

TFile *f =TFile::Open("root://cmsxrootd.fnal.gov///store/mc/SAM/GenericTTbar/GEN-SIM-RECO/CMSSW_5_3_1_START53_V5-v1/0013/CE4D66EB-5AAE-E111-96D6-003048D37524.root");
Note the prefix of the root://cmsxrootd.fnal.gov/ (or any other redirector name name) in front of your LFN. This returns a TFile object, and you can proceed normally. The same is true for FWLite environment.

BEWARE: do not use the apparently equivalent syntax, which is known not to work :

TFile("root://cmsxrootd.fnal.gov//store/foo/bar")
BEWARE: This syntax also will fail a large percentage of the time for files accessed through xrootd:
root root://cmsxrootd.fnal.gov//store/foo/bar


# Getting extra data out of ROOT files
# https://uproot.readthedocs.io/en/latest/basic.html#inspecting-a-tbranches-of-a-ttree
t = uproot.open('/home/bellis/top_data/NANOAOD/small_skims_10k/TT_TToBCE_TuneCP5_BNV_2018_SMALL_10k.root')
 t['Runs']['genEventCount'].array()[0]
