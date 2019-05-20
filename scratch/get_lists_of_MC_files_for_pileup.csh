set miniaod = "RunIISummer16MiniAODv3"
set pileup = '-PUMoriond17_'
set global_tag = "94X_mcRun2_asymptotic_v3"

set tag = `printf "%s%s%s" $miniaod $pileup $global_tag`
echo

#echo $miniaod '*' $global_tag '*' | awk '{print $1$2$3$4}'
#set tag = `echo $miniaod $global_tag '*' | awk '{print $1$2$3$4}'`
echo $tag

foreach dataset( #DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8 \
    #WW_TuneCUETP8M1_13TeV-pythia8 \
    #ZZ_TuneCUETP8M1_13TeV-pythia8 \
    #WZ_TuneCUETP8M1_13TeV-pythia8 \
    TT_TuneCUETP8M2T4_13TeV-powheg-pythia8 \
    #TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8 \
    #WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8 \
    #DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8 \
    #DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8 \
    #ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1 \
    #ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1 \
    #ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1 \
    )
                                                
                                                echo $dataset
                                                echo $tag
                                                
                                                dasgoclient --query="file dataset=/$dataset/$tag*/MINIAODSIM" --format plain --limit=30 > LIST_OF_SOME_MC_XROOTD_FOR_PILEUP_"$dataset".txt
                                                
                                                end

#set dataset="/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM"
#echo $dataset
#dasgoclient --query="file dataset=$dataset" --format plain --limit=30 > "LIST_OF_SOME_MC_XROOTD_FOR_PILEUP_"`echo $dataset | awk -F'/' '{print $2}'`.txt
