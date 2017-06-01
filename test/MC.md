When using das_client, need 3 things within the slashes dataset query. 

das_client --query="dataset=/WJetsToQQ*/*/*" --format=plain --limit=30

das_client --query="dataset=/WJetsToQQ*/*Summer16*/MINIAODSIM" --format=plain --limit=30


To find the root files in case we want to look at them.

    das_client --query="file dataset=/WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" --format=plain --limit=30

