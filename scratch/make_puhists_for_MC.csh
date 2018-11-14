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
                ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1 \
                ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1 \
                ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1 \
)

echo $dataset

    python makepu_fwlite.py --files LIST_OF_SOME_MC_XROOTD_FOR_PILEUP_"$dataset".txt --maxevents 500000 --outname pumc_"$dataset".root
    

end
