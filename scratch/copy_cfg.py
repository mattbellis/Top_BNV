import FWCore.ParameterSet.Config as cms

# Run with
# cmsRun <THISSCRIPT>

# Getting this example from 
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookDataSamples

# 2016 data
#infilename = "/store/mc/RunIISummer16MiniAODv2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/7C8A67E6-9ABE-E611-B3E7-0242AC130004.root"
# MC
#infilename = "/store/mc/RunIISummer16MiniAODv2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/0693E0E7-97BE-E611-B32F-0CC47A78A3D8.root"
# Data
#infilename = "/store/data/Run2016B/SingleMuon/MINIAOD/03Feb2017_ver2-v2/100000/F2F21546-04EB-E611-9AB6-0025905B8600.root"
###################################
# CMSSW_9_4_0 data
#infilename = "/store/data/Run2016B/SingleMuon/MINIAOD/17Jul2018_ver2-v1/50000/987DBBE0-B48B-E811-8A7E-0CC47A0AD6C4.root"
# CMSSW_9_4_0 MC
#infilename = "/store/mc/RunIISummer16MiniAODv3/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/110000/B22320DB-EBBC-E811-A987-14187763B811.root"


# 2017 data
# MC
#  dasgoclient --query="file dataset=/TT_TuneCH3_13TeV-powheg-herwig7_testrun/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM" --format plain --limit=10
#infilename = "/store/mc/RunIIFall17MiniAODv2/TT_TuneCH3_13TeV-powheg-herwig7_testrun/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/30000/F87E612B-0E8A-E911-9950-AC1F6B23C7DC.root"
#infilename = "/store/mc/RunIIFall17MiniAODv2/ZZ_TuneCP5_13TeV-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/90000/BEF8F00E-DC41-E811-B90F-008CFAC93EE0.root"
# Data
# SingleMuon
#infilename = "/store/data/Run2017B/SingleMuon/MINIAOD/31Mar2018-v1/80000/54F30BE9-423C-E811-A315-0CC47A7C3410.root"
# SingleElectron
#infilename = "/store/data/Run2017B/SingleElectron/MINIAOD/31Mar2018-v1/60000/66EAEA69-3E37-E811-BC12-008CFAC91CD4.root"

# 2018
# MC
#infilename = "/store/mc/RunIIAutumn18MiniAOD/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/60000/84347EC0-60B4-5145-8F92-37F1975CA79D.root"
#infilename = "/store/mc/RunIIAutumn18MiniAOD/ZZ_TuneCP5_13TeV-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v2/110000/98E05B95-FE95-464E-89B5-01B8E09F884D.root"
# Data
# SingleMuon
#infilename = "/store/data/Run2018A/SingleMuon/MINIAOD/17Sep2018-v2/00000/11697BCC-C4AB-204B-91A9-87F952F9F2C6.root"
# SingleElectron - EGamma
infilename = "/store/data/Run2018A/EGamma/MINIAOD/17Sep2018-v2/120000/D0C18EBB-8DD7-EC4F-9C1B-CA3EAD44D993.root"




outdir = "/eos/uscms/store/user/mbellis/MINIAOD/100_events/"
names = infilename.split('/')
outname = "%s_%s_%s_%s_%s" % (names[-5], names[-6], names[-3], names[-2], names[-1])
outfilename = outdir + "/" + outname
print("\noutname:")
print(outname)
print("\noutfilename:")
print(outfilename)

# Give the process a name
process = cms.Process("PickEvent")

# Tell the process which files to use as the source
process.source = cms.Source ("PoolSource",
          #fileNames = cms.untracked.vstring ("/store/relval/CMSSW_5_3_15/RelValPyquen_ZeemumuJets_pt10_2760GeV/DQM/PU_STARTHI53V10A_TEST_feb14-v3/00000/FE0AF9FB-C196-E311-8678-0025904CF75A.root")
          fileNames = cms.untracked.vstring (infilename)

)

# tell the process to only run over 100 events (-1 would mean run over
#  everything
process.maxEvents = cms.untracked.PSet(
            input = cms.untracked.int32 (100)

)

# Tell the process what filename to use to save the output
process.Out = cms.OutputModule("PoolOutputModule",
         fileName = cms.untracked.string (outfilename)
)

# make sure everything is hooked up
process.end = cms.EndPath(process.Out)
