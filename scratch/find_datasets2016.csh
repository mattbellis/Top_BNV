# https://twiki.cern.ch/twiki/bin/view/CMS/StandardModelCrossSectionsat13TeVInclusive
#
#
# https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO
#
# https://twiki.cern.ch/twiki/bin/view/CMS/TopMonteCarlo
#
#

set fileName = "datasets2016.csv"
set MCTag = "RunIISummer16MiniAODv3"
set globalTag = "94X_mcRun2_asymptotic_v3"
set under = "_"

echo > $fileName

foreach dataset(DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8 \
        DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8 \
        WW_TuneCUETP8M1_13TeV-pythia8 \
        ZZ_TuneCUETP8M1_13TeV-pythia8 \
        WZ_TuneCUETP8M1_13TeV-pythia8 \
        TT_TuneCUETP8M2T4_13TeV-powheg-pythia8 \
        TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8 \
        WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8 \
        ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1 \
        ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1 \
        ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1 \
        ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1 \
        QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8 \
        QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8 \
        QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8 \
        QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8 \
        QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8 \
        QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8 \
        QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8 \
        QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8 \
        QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8 \
        QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8 \
        QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8 \
        QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8 \
        QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8 \
        QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8 \
        QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8 \
        QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8 \
        QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8 \
        QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8 \
        QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8 \
        )
        echo $dataset
#dasgoclient --query="dataset=/$dataset*/*Summer16*/MINIAODSIM" --format plain --limit=30
        dasgoclient --query="dataset=/$dataset/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3*/MINIAODSIM" --format plain --limit=30 >> $fileName
        dasgoclient --query="dataset=/$dataset/RunIISummer16MiniAODv3_94X_mcRun2_asymptotic_v3*/MINIAODSIM" --format plain --limit=30 >> $fileName


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
