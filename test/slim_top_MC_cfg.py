## import skeleton process
import FWCore.ParameterSet.Config as cms

process = cms.Process("DAS")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
            #'root://cmseos.fnal.gov//store/user/cmsdas/2017/pre_exercises/DYJetsToLL.root'
            '/store/mc/RunIISpring15DR74/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/30000/101C5701-2141-E511-B832-00259073E532.root'
            #'file:///uscms/home/mbellis/eos_store/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/crab_bellis_top_slim_MC/170112_192558/0000/top_slimmmed_files_MC_ttbar_1.root'
            )
        )


process.out = cms.OutputModule("PoolOutputModule",
        fileName = cms.untracked.string('top_slimmmed_files_MC_ttbar.root'),
        #fileName = cms.untracked.string('/uscms/home/mbellis/eos_store/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/crab_bellis_top_slim_MC/170112_192558/0000/top_slimmmed_files_MC_ttbar_TESTLARGE.root'),
        #outputCommands = cms.untracked.vstring(['drop *', 'keep *_slimmedMuons__*', 'keep *_slimmedElectrons__*', 'keep *_slimmedJets__*', 'keep *_slimmedMETs__*'])
        outputCommands = cms.untracked.vstring(['drop *', \
                'keep *_slimmedMuons__*', \
                'keep *_slimmedElectrons__*', \
                'keep *_slimmedPhotons__*', \
                'keep *_slimmedJets__*', \
                'keep *_slimmedJetsPuppi__*', \
                'keep *_slimmedJetsAK8__*', # This is for top-tagged (boosted?) I think\
                'keep *_slimmedMETs__*', \
                'keep *_slimmedTaus__*', \
                'keep *_slimmedAddPileupInfo__*', \
                'keep *_offlineSlimmedPrimaryVertices__*', \
                'keep *_prunedGenParticles__*', \
                'keep *_generator__*', \
                'keep *_TriggerResults__*', \
                'keep *_fixedGridRhoAll__*', \

                ])
        )

process.end = cms.EndPath(process.out)
