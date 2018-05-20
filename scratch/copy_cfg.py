import FWCore.ParameterSet.Config as cms

# Run with
# cmsRun <THISSCRIPT>

# Getting this example from 
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookDataSamples
#infilename = "/store/mc/RunIISummer16MiniAODv2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/7C8A67E6-9ABE-E611-B3E7-0242AC130004.root"
infilename = "/store/mc/RunIISummer16MiniAODv2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/0693E0E7-97BE-E611-B32F-0CC47A78A3D8.root"

outdir = "/eos/uscms/store/user/mbellis/MINIAOD"
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
