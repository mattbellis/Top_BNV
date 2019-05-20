# https://twiki.cern.ch/twiki/bin/view/CMS/StandardModelCrossSectionsat13TeVInclusive
#
#
# https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO
#
# https://twiki.cern.ch/twiki/bin/view/CMS/TopMonteCarlo
#
#
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
                    ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1
                    RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM
                        /ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM

                    )

    echo 
    dasgoclient --query="dataset=/$dataset*/*Summer16*/MINIAODSIM" --format plain --limit=30
    echo 

end


# Data
# dasgoclient --query="dataset=/SingleMuon/Run2016*03Feb2017*/MINIAOD" --format plain --limit=30
#
# Get a listing of filenames
# dasgoclient --query="file dataset=/SingleMuon/Run2016B-03Feb2017*/MINIAOD" --format plain --limit=30
#
# FOR USE WITH 9_4_X 
# dasgoclient --query="file dataset=/SingleMuon/Run2016B-17Jul2018*/MINIAOD" --format plain --limit=30
#dasgoclient --query="dataset=/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8*/*RunIISummer16MiniAODv3*/MINIAODSIM" --format plain --limit=30
