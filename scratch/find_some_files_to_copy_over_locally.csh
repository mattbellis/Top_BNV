# https://twiki.cern.ch/twiki/bin/view/CMS/StandardModelCrossSectionsat13TeVInclusive
#
#
# https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO
#
# https://twiki.cern.ch/twiki/bin/view/CMS/TopMonteCarlo
#
#

set GTdata = "94X_dataRun2_v11"
set data_date = "31Mar2018"

#set MCtag = "RunIIFal17MiniAODv2"
#set GTMC = "94X_mc2017_realistic_v14"
# 2017
set tag = "RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14" 
# 2018
#set tag = "RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15"

foreach dataset( ZZ_Tune \
                    ZZ_Tune \
                    WZ_Tune \
                    TT_Tune \
                    TTGJets_Tune \
                    DYJetsToLL_M-10to50_Tune \
                    DYJetsToLL_M-50_Tune \
                    ST_ \
                    QCD_ \
                    )
    echo "\n----------------------------"
    echo $dataset
    echo $tag
    #dasgoclient --query="dataset=/$dataset*/*Summer16*/MINIAODSIM" --format plain --limit=30
    #dasgoclient --query="dataset=/$dataset/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3*/MINIAODSIM" --format plain --limit=30 >> $1
    #dasgoclient --query="dataset=/$dataset/RunIISummer16MiniAODv3_94X_mcRun2_asymptotic_v3*/MINIAODSIM" --format plain --limit=30 >> $1
    dasgoclient --query="dataset=/$dataset*/$tag*/MINIAODSIM" --format plain --limit=30 


end


# Data
# 2016
# dasgoclient --query="dataset=/SingleMuon/Run2016B-17Jul2018*/MINIAOD" --format plain --limit=30
# To find a listing of files
# dasgoclient --query="file dataset=/SingleMuon/Run2016B-17Jul2018*/MINIAOD" --format plain --limit=30
# 2017
# dasgoclient --query="dataset=/SingleMuon/*Run2017*31Mar2018*/MINIAOD" --format plain --limit=30
# dasgoclient --query="dataset=/SingleElectron/*Run2017*31Mar2018*/MINIAOD" --format plain --limit=30
# 2018
# dasgoclient --query="dataset=/SingleMuon/*Run2018*17Sep2018*/MINIAOD" --format plain --limit=30
# dasgoclient --query="dataset=/SingleMuon/*Run2018*2019*/MINIAOD" --format plain --limit=30
#
# dasgoclient --query="dataset=/EGamma/*Run2018*17Sep2018*/MINIAOD" --format plain --limit=30
# dasgoclient --query="dataset=/EGamma/*Run2018*2019*/MINIAOD" --format plain --limit=30

