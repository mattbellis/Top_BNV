## import skeleton process
import FWCore.ParameterSet.Config as cms

process = cms.Process("DAS")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
            #'root://cmseos.fnal.gov//store/user/cmsdas/2017/pre_exercises/DYJetsToLL.root'
            # This is a sample MC
            #'root://cmsxrootd.fnal.gov///store/mc/RunIISummer16MiniAODv2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/18E31463-B3BE-E611-B6A3-0CC47A4D7678.root'
            'root://cmsxrootd.fnal.gov////store/mc/RunIISummer16MiniAODv2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/0693E0E7-97BE-E611-B32F-0CC47A78A3D8.root'
            # This is a sample data
            #'root://cmsxrootd.fnal.gov///store/data/Run2016B/SingleMuon/MINIAOD/23Sep2016-v3/00000/00AE0629-1F98-E611-921A-008CFA1112CC.root'
            #'file:///uscms/home/mbellis/eos_store/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/crab_bellis_top_slim_MC/170112_192558/0000/top_slimmmed_files_MC_ttbar_1.root'
            )
        )


process.out = cms.OutputModule("PoolOutputModule",
        fileName = cms.untracked.string('top_slimmmed_files_MC_ttbar_NOTLOCAL_FOR_TESTING.root'),
        #fileName = cms.untracked.string('top_slimmmed_files_DATA_ttbar.root'),
        #fileName = cms.untracked.string('/uscms/home/mbellis/eos_store/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/crab_bellis_top_slim_MC/170112_192558/0000/top_slimmmed_files_MC_ttbar_TESTLARGE.root'),
        #outputCommands = cms.untracked.vstring(['drop *', 'keep *_slimmedMuons__*', 'keep *_slimmedElectrons__*', 'keep *_slimmedJets__*', 'keep *_slimmedMETs__*'])
        outputCommands = cms.untracked.vstring(['drop *', \
                'keep *_slimmedMuons__*', \
                'keep *_slimmedElectrons__*', \
                'keep *_reducedEgamma_*_*', # need for electron cuts? \
                'keep *_slimmedPhotons__*', \
                'keep *_slimmedJets__*', \
                'keep *_slimmedJetsPuppi__*', \
                'keep *_slimmedJetsAK8__*', # This is for top-tagged (boosted?) I think\
                'keep *_slimmedMETs__*', \
                'keep *_slimmedTaus__*', \
                'keep *_offlineBeamSpot__*', # maybe needed for electron \
                'keep *_ConversionCollection__*', # maybe needed for electron \
                'keep *_slimmedAddPileupInfo__*', \
                'keep *_offlineSlimmedPrimaryVertices__*', \
                'keep *_prunedGenParticles__*',  # This will be Feynman-level particles. Not jets. \
                #'keep *_packedGenParticles__*',  # This will be Feynman-level particles. MAYBE? \
                'keep *_slimmedGenJets__*',  # Generated jets. \
                'keep *_generator__*',  # Used for event weights \
                'keep *_TriggerResults__*', \
                'keep *_fixedGridRhoAll__*', # Needed for isolation \
                'keep *_fixedGridRhoFastjetAll__*',  # Needed for cutbased e cuts?

                ])
        )

process.end = cms.EndPath(process.out)
