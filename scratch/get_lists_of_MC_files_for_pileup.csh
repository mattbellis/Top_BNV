# 2017 and 2018
foreach dataset( "TTToHadronic_TuneCP5_13TeV" "TTTo2L2Nu_TuneCP5_13TeV" "TTToSemiLeptonic_TuneCP5_13TeV" )
# 2016
#foreach dataset( "TTToHadronic_TuneCP5_PSweights_13TeV" "TTTo2L2Nu_TuneCP5_PSweights_13TeV" "TTToSemiLeptonic_TuneCP5_PSweights_13TeV" )

                                                
                                                echo $dataset
                                                
                                                # 2016
                                                # Just run command down below
                                                #dasgoclient --query="file dataset=/$dataset-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM" --format plain --limit=100 > LIST_OF_SOME_MC_XROOTD_FOR_PILEUP_"$dataset"_2016.txt
                                                #/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM

                                                # 2017
                                                if ( $dataset == "TTToSemiLeptonic_TuneCP5_13TeV" ) then
                                                    dasgoclient --query="file dataset=/$dataset-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM" --format plain --limit=100 > LIST_OF_SOME_MC_XROOTD_FOR_PILEUP_"$dataset"_2017.txt
                                                    else
                                                    dasgoclient --query="file dataset=/$dataset-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM" --format plain --limit=100 > LIST_OF_SOME_MC_XROOTD_FOR_PILEUP_"$dataset"_2017.txt
                                                    endif

                                                # 2018
                                                #dasgoclient --query="file dataset=/$dataset-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM" --format plain --limit=100 > LIST_OF_SOME_MC_XROOTD_FOR_PILEUP_"$dataset"_2018.txt
                                                
                                                end

#set dataset="/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM"
#echo $dataset
#dasgoclient --query="file dataset=/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM" --format plain --limit=100 > LIST_OF_SOME_MC_XROOTD_FOR_PILEUP_TT_Tune_2016.txt
