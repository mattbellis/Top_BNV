from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'bellis_ttbar'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'

#config.Data.inputDataset = '/RSGluonToTT_M-3000_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM'
config.Data.inputDataset = '/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
#config.Data.userInputFiles = open('/uscms/homes/m/mbellis/CMSSW_8_0_26/src/Analysis/Top_BNV/test/filesToProcess_FOR_CRAB_TTBAR_SMALL.txt').readlines()
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/mbellis/'
#config.Data.ignoreLocality = True # DO I NEED THIS BECAUSE IT IS AT FNAL?
#config.Site.whitelist = ["T2_US*"] # DO I NEED THIS BECAUSE IT IS AT FNAL?
config.Data.publication = False

config.Site.storageSite = 'T3_US_FNALLPC'

config.JobType.scriptExe = 'execute_for_crab.sh'
config.JobType.outputFiles = ['output.root']
config.JobType.sendExternalFolder = True
#config.JobType.inputFiles = ['execute_for_crab.py', 'topbnv_fwlite.py', 'filesToProcess_FOR_CRAB_TTBAR_SMALL.txt', 'JECs', 'egammaEffi.txt_SF2D.root', 'MuonID_Z_RunBCD_prompt80X_7p65.root', 'general_tracks_and_early_general_tracks_corr_ratio.root' ]
config.JobType.inputFiles = ['execute_for_crab.py', 'topbnv_fwlite.py', 'JECs', 'egammaEffi.txt_SF2D.root', 'MuonID_Z_RunBCD_prompt80X_7p65.root', 'general_tracks_and_early_general_tracks_corr_ratio.root' ]
