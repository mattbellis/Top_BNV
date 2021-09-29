# Following instructions here
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial

from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

import sys
sys.path.append('Datasets')
import datasets_DATA

year = "YEARGOESHERE"
trigger = "TRIGGERGOESHERE"
print(trigger)
print(year)

dataset = datasets_DATA.datasets[year][NUMBERTORUN]
dataset = dataset.replace('TRIGGER',trigger)

print("DATASET!")
print(dataset)

#request_name = "bellis_SingleMuon_%s" % (dataset.split('/')[2])
request_name = "bellis_{0}_{1}_{2}".format(year,trigger,dataset.split('/')[2])

#config.General.requestName = 'bellis_topbnv_TT_TUNE'
#config.General.requestName = 'bellis_topbnv_RSGluonToTT'
config.General.requestName = request_name
config.General.workArea = 'crab_projects/Data/{0}'.format(year)
#config.General.workArea = '/uscms_data/d3/mbellis/crab_projects/Data/{0}'.format(year)
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
lumiMaskFiles = {'2016':
'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt', 
                 '2017':
'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt',
                 '2018':
'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'
}
config.Data.lumiMask = lumiMaskFiles[year]
print(config.Data.lumiMask)
#config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'

#config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.outLFNDirBase = '/store/user/{0}/Data/{1}/{2}'.format(getUsernameFromSiteDB(), year, trigger)


# This selecting some of the data
config.Data.publication = False

config.Site.storageSite = 'T3_US_FNALLPC'

config.JobType.scriptExe = 'execute_for_crab_data.sh'
config.JobType.scriptArgs = ['year={0}'.format(year), 'trigger={0}'.format(trigger)]

config.JobType.outputFiles = ['output.root']
config.JobType.sendExternalFolder = True

# We need that FrameworkJobReport.xml file for the output.
config.JobType.inputFiles = ['execute_for_crab_data.py', 'topbnv_fwlite.py', 'FrameworkJobReport.xml','JECs', 'fwlite_tools.py']

