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
                    DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8 \
                    DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8 \
                    ST_t-channel_top_4f_inclusiveDecays_13TeV-powheg \
                    ST_tW_tugFCNC_leptonDecays_Madgraph \
                    ST_tW_tcgFCNC_leptonDecays_Madgraph \
                    ST_s-channel_4f_InclusiveDecays_13TeV-amcatnlo-pythia8 \
                    ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8 \
                    ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1 \
                    )

    echo 
    dasgoclient --query="dataset=/$dataset*/*Summer16*/MINIAODSIM" --format plain --limit=30
    echo 

end
