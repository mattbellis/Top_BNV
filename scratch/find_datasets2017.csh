# https://twiki.cern.ch/twiki/bin/view/CMS/StandardModelCrossSectionsat13TeVInclusive
#
#
# https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO
#
# https://twiki.cern.ch/twiki/bin/view/CMS/TopMonteCarlo
#
#

set fileName = "datasets2017.csv"
set MCTag = "RunIIFall17MiniAODv2"
set globalTag = "94X_mc2017_realistic_v14"
set Tune = "_Tune"
set var = "*"

echo > $fileName

foreach dataset( DYJetsToLL_M-10to50\
        DYJetsToLL_M-50\
        WW\
        ZZ\
        WZ\
        TT\
        TTGJets\
        WJetsToLNu\
        )
    
        
        echo $dataset
        #dasgoclient --query="dataset=/$dataset*/$MCTag-PUMoriond17_$globalTag*/MINIAODSIM" --format plain --limit=30 >> $fileName
        dasgoclient --query="dataset=/$dataset$Tune*/$MCTag-PU2017_12Apr2018_$globalTag*/MINIAODSIM" --format plain --limit=30 >> $fileName

        end


foreach dataset( ST_t-channel_antitop\
        ST_t-channel_top\
        ST_tW_top\
        ST_tW_antitop\
        )


        echo $dataset
        #dasgoclient --query="dataset=/$dataset*/$MCTag-PUMoriond17_$globalTag*/MINIAODSIM" --format plain --limit=30 >> $fileName
        dasgoclient --query="dataset=/$dataset*TuneCP5_13TeV-powheg-pythia8/$MCTag-PU2017_12Apr2018_$globalTag*/MINIAODSIM" --format plain --limit=30 >> $fileName

        end

foreach dataset( QCD_Pt-15to20_MuEnriched\
        MuEnriched\
        EMEnriched\
        )


        echo $dataset
        dasgoclient --query="dataset=/QCD*$dataset*_Tune*/$MCTag*$globalTag*/MINIAODSIM" --format plain --limit=30 >> $fileName

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
