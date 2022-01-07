# Adapted from Danny Noonan
# https://github.com/dnoonan08/TTGammaSemiLep_13TeV/blob/NanoAOD/Skimming/AllSamples_2018.py

#mc_type='RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1'
#mc_type['2018']='RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1'

mc_tier = 'NANOAODSIM'

mc_type = {} 
mc_type['2016'] = {} 
mc_type['2016']['Run'] = 'RunIISummer20UL16NanoAODv9'
mc_type['2016']['GT'] = '106X_mcRun2_asymptotic_v17-v1'
mc_type['2017'] = {} 
mc_type['2017']['Run'] = 'RunIISummer20UL17NanoAODv9'
mc_type['2017']['GT'] = '106X_mc2017_realistic_v9-v1'
mc_type['2018'] = {} 
mc_type['2018']['Run'] = 'RunIISummer20UL18NanoAODv9'
mc_type['2018']['GT'] = '106X_upgrade2018_realistic_v16_L1v1-v1'

samples = {"MC":{}, "data":{}}

samples['MC']['TTbarPowheg_Dilepton'] = '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/'
samples['MC']['TTbarPowheg_Hadronic'] = '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/'
samples['MC']['TTbarPowheg_Semilept'] = '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/'

samples['MC']['WW'] = '/WW_TuneCP5_13TeV-pythia8/'
samples['MC']['WZ'] = '/WZ_TuneCP5_13TeV-pythia8/'
samples['MC']['ZZ'] = '/ZZ_TuneCP5_13TeV-pythia8/'

samples['MC']['ST_s_channel'] = '/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8/'
samples['MC']['ST_t_channel'] = '/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/'
samples['MC']['ST_tbar_channel'] = '/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/'
samples['MC']['ST_tW_channel'] = '/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/'
samples['MC']['ST_tbarW_channel'] = '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/'


samples['MC']['2018'] = {}
samples['MC']['2017'] = {}
samples['MC']['2016'] = {}

for s in samples['MC'].keys():
    #print(s)
    if s in ['2016', '2017', '2018']:
        continue 

    val = samples['MC'][s]
    for year in ['2016','2017','2018']:
    #for year in ['2017','2018']:
        samples['MC'][year][s] = val + mc_type[year]['Run'] + "-" + mc_type[year]['GT'] + "/" + mc_tier
    #print(samples['MC']['2018'][s])



