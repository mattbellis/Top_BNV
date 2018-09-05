
# From here
# https://cms-pdmv.cern.ch/mcm
# Navigation -->
# In "Dataset name" enter in the 2nd entry below (the full 3-field name)
# Can also enter it in "Output dataset" in next field.
#
# "Select view" --> Completed events, generator parameters, total events, Input/Output dataset
# Click on "Dataset"
# 
# Make sure we have more than 20 records displayed!
# 
# Then need to search back through output --> input datasets to find the generator parameters.

# DYJets
# https://cms-pdmv.cern.ch/mcm/requests?dataset_name=DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8&page=0&shown=275417401471&limit=50
#
# https://cms-pdmv.cern.ch/mcm/requests?page=-1&dataset_name=DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8&shown=275417401471
#
# WW
# https://cms-pdmv.cern.ch/mcm/requests?dataset_name=WW_TuneCUETP8M1_13TeV-pythia8&page=-1&shown=275417401471



XXX = 12

mc_info = {
        'DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-v1':  
        {'dataset':'DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 
         'completed_events': 30920596,
         'total_events': 30935823.,
         'cross_section': 18610, # pb
         'filter_efficiency': 1,
         'match_efficiency': 0.61,
         'negative_weights_fraction': 0.1356
         },
        'DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-v2': #### CAN'T FIND PROPER MATCHES
        {'dataset':'DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM',
         'completed_events': 65888233.,
         'total_events': 75000000,
         'cross_section': 18610, # pb
         'filter_efficiency': 1,
         'match_efficiency': 0.61,
         'negative_weights_fraction': 0.1356 ########## CHECK THESE
         },
        'DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext1-v1': #### CAN'T FIND PROPER MATCHES
        {'dataset':'/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
         'completed_events': 40381391,
         'total_events': 40547670,
         'cross_section': 18610, # pb
         'filter_efficiency': 1,
         'match_efficiency': 0.61,
         'negative_weights_fraction': 0.1356 ########## CHECK THESE
         },
        'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-v2': ### Can't find proper values
        {'dataset':'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-BS2016_BSandPUSummer16_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM',
         'completed_events': 1364030,
         'total_events': 1394389,
         'cross_section': 6104, # pb #### THERE ARE ALSO OTHER VALUES AROUND 5900
         'filter_efficiency': 1,
         'match_efficiency': 0.3831,
         'negative_weights_fraction': 0.27 #### CHECK THIS!!!!!!!!!!!!!!!!!!!
         },
        'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext2-v1':
        {'dataset':'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM',
         'completed_events': 123925939,
         'total_events': 125000000,
         'cross_section': 6104, # pb #### THERE ARE ALSO OTHER VALUES AROUND 5900
         'filter_efficiency': 1,
         'match_efficiency': 0.3831, # CHECK THIS!!!!!!!!!!!!!!!!!!!!
         'negative_weights_fraction': 0.27
         },
        'WW_TuneCUETP8M1_13TeV-pythia8-v1':
        {'dataset':'WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
         'completed_events': 1000000,
         'total_events': 994012,
         'cross_section': 63.21, # pb
         'filter_efficiency': XXX,
         'match_efficiency': XXX,
         'negative_weights_fraction': XXX
         },
        'WW_TuneCUETP8M1_13TeV-pythia8_ext1-v1':
        {'dataset':'WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
         'completed_events': 6988168,
         'total_events': 7000000,
         'cross_section': 63.21, # pb
         'filter_efficiency': 1,
         'match_efficiency': 1,
         'negative_weights_fraction': -1
         },
        'ZZ_TuneCUETP8M1_13TeV-pythia8-v1':
        {'dataset':'ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
         'completed_events': 990064,
         'total_events': 990064,
         'cross_section': 10.32, # pb
         'filter_efficiency': XXX,
         'match_efficiency': XXX,
         'negative_weights_fraction': XXX
         },
        'ZZ_TuneCUETP8M1_13TeV-pythia8_ext1-v1':
        {'dataset':'ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
         'completed_events': 998034,
         'total_events': 1000000, # THIS DOESN'T SEEM RIGHT FOR THE NUMBER OF EVENTS SKIMMED
         'cross_section': XXX, # pb
         'filter_efficiency': XXX,
         'match_efficiency': XXX,
         'negative_weights_fraction': XXX
         },
        'WZ_TuneCUETP8M1_13TeV-pythia8-v1':
        {'dataset':'WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
         'completed_events': 1000000,
         'total_events': 1000000,
         'cross_section': 22.82, # pb
         'filter_efficiency': 1,
         'match_efficiency': 1,
         'negative_weights_fraction': 0
         },
        'WZ_TuneCUETP8M1_13TeV-pythia8_ext1-v1':
        {'dataset':'WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
         'completed_events': 2995828,
         'total_events': 3000000,
         'cross_section': 22.82, # pb
         'filter_efficiency': 1,
         'match_efficiency': 1,
         'negative_weights_fraction': 0
         },
        'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8-v1':
        {'dataset':'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
         'completed_events': 75311946,
         'total_events': 77229341,
         'cross_section': 730, # pb
         'filter_efficiency': 1,
         'match_efficiency': 1,
         'negative_weights_fraction': 0
         },
        'TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8-v1':
        {'dataset':'TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
         'completed_events': 4870911,
         'total_events': 4870911,
         'cross_section': 3.772, # pb
         'filter_efficiency': 1,
         'match_efficiency': 0.55,
         'negative_weights_fraction': 0
         },
        'TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_ext1-v1':
        {'dataset':'TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
         'completed_events': 9885348,
         'total_events': 10002949,
         'cross_section': 3.772, # pb
         'filter_efficiency': 1,
         'match_efficiency': 0.55,
         'negative_weights_fraction': 0
         },
        'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-v1':
        {'dataset':'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
         'completed_events': 24120319,
         'total_events': 24222907,
         'cross_section': 60290, # pb
         'filter_efficiency': 1,
         'match_efficiency': 0.4,
         'negative_weights_fraction': 0
         },
        'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext2-v2':
        {'dataset':'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v2/MINIAODSIM',
         'completed_events': 236107157,
         'total_events': 241749648,
         'cross_section': 60290, # pb
         'filter_efficiency': 1,
         'match_efficiency': 0.4,
         'negative_weights_fraction': 0
         },
}
