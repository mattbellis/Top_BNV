dasgoclient --query="dataset=/*/*RunIISummer19UL17GEN*/*" --format plain --limit=30
dasgoclient --query="dataset=/*/*RunIISummer19UL16GEN*/*" --format plain --limit=30


dasgoclient --query="dataset=/*/*RunIISummer19UL16*/NANOAODSIM" --format plain --limit=30

dasgoclient --query="dataset=/*/*RunIISummer19UL17*/NANOAODSIM" --format plain --limit=30
dasgoclient --query="dataset=/TT*/*RunIISummer19UL17*/NANOAODSIM" --format plain --limit=30


# Data
dasgoclient --query="dataset=/SingleMuon/*UL*/NANOAOD" --format plain --limit=30
#/SingleMuon/Run2017B-UL2017_02Dec2019-v1/NANOAOD
#/SingleMuon/Run2017C-UL2017_02Dec2019-v1/NANOAOD
#/SingleMuon/Run2017D-UL2017_02Dec2019-v1/NANOAOD
#/SingleMuon/Run2017E-UL2017_02Dec2019-v1/NANOAOD
#/SingleMuon/Run2017F-UL2017_02Dec2019-v1/NANOAOD

dasgoclient --query="dataset=/SingleMuon/*UL*16*/MINIAOD" --format plain --limit=100
dasgoclient --query="dataset=/TTTo*TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL17NanoAOD-106X_mc2017_realistic_v6-v*/NANOAODSIM" --format plain --limit=100
dasgoclient --query="dataset=/TT*Jet*/*UL*/NANOAODSIM" --format plain --limit=100

dasgoclient --query="dataset=/TT*BNV*/*UL*/NANOAODSIM" --format plain --limit=100

#dasgoclient -query="file dataset=/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM | sum(file.nevents)"


# From here
# https://hypernews.cern.ch/HyperNews/CMS/get/computing-tools/6072/1/2/1/1.html
curl -k -O https://raw.githubusercontent.com/dmwm/DASMaps/master/js/das_maps_dbs_prod.js
dasgoclient -dasmaps ./das_maps_dbs_prod.js --query="file dataset=/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAOD-106X_upgrade2018_realistic_v11_L1v1-v1/NANOAODSIM" --format plain

# Helpful. Dumps some summary output to a json-esqe output. Dictionary?
dasgoclient -query="summary dataset=/ZMM/Summer11-DESIGN42_V11_428_SLHC1-v1/GEN-SIM"

# Get all the info about datasets, including files and file entries
dasgoclient -dasmaps ./das_maps_dbs_prod.js -query="file dataset=/ZMM/Summer11-DESIGN42_V11_428_SLHC1-v1/GEN-SIM" -json

dasgoclient -dasmaps ./das_maps_dbs_prod.js -query=file dataset=/QCD_Pt_50to80_TuneCP5_13TeV_pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM -json
