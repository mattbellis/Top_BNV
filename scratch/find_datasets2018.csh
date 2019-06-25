# https://twiki.cern.ch/twiki/bin/view/CMS/StandardModelCrossSectionsat13TeVInclusive
#
#
# https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO
#
# https://twiki.cern.ch/twiki/bin/view/CMS/TopMonteCarlo
#
#

set fileName = "datasets2018.csv"
set MCTag = "RunIIAutumn18MiniAOD"
set globalTag = "102X_upgrade2018_realistic_v"
set under = "_"
set Tune = "TuneCP5_13"
echo > $fileName

foreach dataset(DYJetsToLL_M-50_TuneCP5_13\
                    DYJetsToLL_M-10to50_TuneCP5_13\
                    WW_TuneCP5_13\
                    ZZ_TuneCP5_13\
                    WZ_TuneCP5_13\
                    TT\
                    TTGJets\
                    WJetsToLNu\
                    ST_t-channel\
                    ST_tW\
                    QCD\
                    )
    echo $dataset
    dasgoclient --query="dataset=/$dataset*/$MCTag$under$globalTag*/MINIAODSIM" --format plain --limit=30 >> $fileName


end

python make_short_name.py $fileName


# Data
# dasgoclient --query="dataset=/SingleMuon/Run2016*03Feb2017*/MINIAOD" --format plain --limit=30
#
# Get a listing of filenames
# dasgoclient --query="file dataset=/SingleMuon/Run2016B-03Feb2017*/MINIAOD" --format plain --limit=30
#
# FOR USE WITH 9_4_X 
# dasgoclient --query="file dataset=/SingleMuon/Run2016B-17Jul2018*/MINIAOD" --format plain --limit=30
#dasgoclient --query="dataset=/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8*/*RunIISummer16MiniAODv3*/MINIAODSIM" --format plain --limit=30
