# Adapted from Danny Noonan
# https://github.com/dnoonan08/TTGammaSemiLep_13TeV/blob/NanoAOD/Skimming/AllSamples_2018.py

#mc_type='RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1'
#mc_type['2018']='RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1'

mc_tier = 'NANOAODSIM'

mc_type = {} 
mc_type['2018'] = {} 
mc_type['2018']['Run'] = 'RunIISummer20UL18NanoAODv9'
mc_type['2018']['GT'] = '106X_upgrade2018_realistic_v16_L1v1-v1'

samples = {"MC":{}, "data":{}}

#samples['MC']['TTbarPowheg_Dilepton'] = '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/'+mc_type+'/NANOAODSIM'
#samples['MC']['TTbarPowheg_Hadronic'] = '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/'+mc_type+'/NANOAODSIM'
#samples['MC']['TTbarPowheg_Hadronic'] = '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/'+mc_type+'/NANOAODSIM'
#samples['MC']['TTbarPowheg_Semilept'] = '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/'+mc_type+'/NANOAODSIM'
samples['MC']['TTbarPowheg_Dilepton'] = '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/'
samples['MC']['TTbarPowheg_Hadronic'] = '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/'
samples['MC']['TTbarPowheg_Semilept'] = '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/'


samples['MC']['2018'] = {}

for s in samples['MC'].keys():
    #print(s)
    if s in ['2016', '2017', '2018']:
        continue 

    val = samples['MC'][s]
    samples['MC']['2018'][s] = val + mc_type['2018']['Run'] + "-" + mc_type['2018']['GT'] + "/" + mc_tier
    #print(samples['MC']['2018'][s])



