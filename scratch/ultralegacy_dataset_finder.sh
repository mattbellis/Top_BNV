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

