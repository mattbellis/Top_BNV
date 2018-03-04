Referencing B2G list of MC

https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GAnaEDMNTuples80X


When using das_client, need 3 things within the slashes dataset query. 

    das_client --query="dataset=/WJetsToQQ*/*/*" --format=plain --limit=30

    das_client --query="dataset=/WJetsToQQ*/*Summer16*/MINIAODSIM" --format=plain --limit=30

    das_client --query="dataset=/WW_TuneCUETP8M1_13TeV-pythia8/*Summer16*/MINIAODSIM" --format plain

    das_client --query="dataset=/WW_TuneCUETP8M1_13TeV-pythia8/*Summer16*/MINIAODSIM" --format plain
    
    das_client --query="dataset=/ZW_TuneCUETP8M1_13TeV-pythia8/*Summer16*/MINIAODSIM" --format plain

Some of the above queries will produce collections with what looks like the exact same string, except for a "ext1" addition. 
That just refers to an extension of the dataset, that is, additional Monte Carlo. 



To find the root files in case we want to look at them.

    das_client --query="file dataset=/WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" --format=plain --limit=30


If we wanted to look at one of these files, we would do

        root -l "root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/70000/007F0D37-9ABE-E611-9EE6-002590E3A212.root"
        
'Commands for our MC'
* W + jets
     das_client --query="dataset=/WJetsToLNu*TuneCUETP8M1*13TeV-madgraphMLM-pythia8/*Summer16*/MINIAODSIM" --format plain --limit=30
** /WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM

* Drell-Yan
    das_client --query="dataset=/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*Summer16*/MINIAODSIM" --format plain --limit=30
** /DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM
** /DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM

* Single top
    das_client --query="dataset=/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/*Summer16*/MINIAODSIM" --format plain --limit=30
** /ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM



Here's how I found a ttbar file to run on. 

        das_client --query="file dataset=/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" --format=plain


** And some others

dasgoclient --query="dataset=/TTJets*/*Summer16*/MINIAODSIM" --format plain --limit=30


** To get numbers of events

dasgoclient --query="dataset=/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM | grep dataset.nevents" --format=json

dasgoclient --query="dataset=/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM | grep dataset.nevents" --format=json
