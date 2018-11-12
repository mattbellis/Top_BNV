# Following instructions here
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial

from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

datasets = ['/SingleElectron/Run2016B-03Feb2017_ver2-v2/MINIAOD',
        '/SingleElectron/Run2016C-03Feb2017-v1/MINIAOD',
        '/SingleElectron/Run2016D-03Feb2017-v1/MINIAOD',
        '/SingleElectron/Run2016E-03Feb2017-v1/MINIAOD',
        '/SingleElectron/Run2016F-03Feb2017-v1/MINIAOD',
        '/SingleElectron/Run2016G-03Feb2017-v1/MINIAOD',
        '/SingleElectron/Run2016H-03Feb2017_ver2-v1/MINIAOD',
        '/SingleElectron/Run2016H-03Feb2017_ver3-v1/MINIAOD'
        ]


dataset = datasets[NUMBERTORUN]

request_name = "bellis_SingleElectron_%s" % (dataset.split('/')[2])

#config.General.requestName = 'bellis_topbnv_TT_TUNE'
#config.General.requestName = 'bellis_topbnv_RSGluonToTT'
config.General.requestName = request_name
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'

config.Data.inputDataset = dataset
#config.Data.inputDataset = '/RSGluonToTT_M-3000_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM'
#config.Data.inputDataset = '/GenericTTbar/HC-CMSSW_5_3_1_START53_V5-v1/GEN-SIM-RECO'
#config.Data.inputDataset = '/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
#config.Data.inputDataset = '/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'

config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 1

# FOr 2016
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCrabFaq
# https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/
# Submitting from CERN
#config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
# Submitting from FNAL
config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'

config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())

# This selecting some of the data
config.Data.publication = False

config.Site.storageSite = 'T3_US_FNALLPC'

config.JobType.scriptExe = 'execute_for_crab_data.sh'

config.JobType.outputFiles = ['output.root']
config.JobType.sendExternalFolder = True

# We need that FrameworkJobReport.xml file for the output.
config.JobType.inputFiles = ['execute_for_crab_data.py', 'topbnv_fwlite.py', 'FrameworkJobReport.xml','JECs']

