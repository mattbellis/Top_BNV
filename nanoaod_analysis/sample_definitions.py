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

#### Data ######
samples['data'] = {'2016':{}, '2017':{}, '2018':{}}
for key in samples['data'].keys():
    samples['data'][key]['SingleMuon'] = {}


#/SingleMuon/Run2018A-UL2018_MiniAODv1_NanoAODv2-v3/NANOAOD
#/SingleMuon/Run2018B-UL2018_MiniAODv1_NanoAODv2-v2/NANOAOD
#/SingleMuon/Run2018C-UL2018_MiniAODv1_NanoAODv2-v2/NANOAOD
#/SingleMuon/Run2018D-UL2018_MiniAODv1_NanoAODv2-v2/NANOAOD
# Should these be NanoAODv9-v2?
samples['data']['2018']['SingleMuon']['Run2018A'] = '/SingleMuon/Run2018A-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD'
samples['data']['2018']['SingleMuon']['Run2018B'] = '/SingleMuon/Run2018B-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD'
samples['data']['2018']['SingleMuon']['Run2018C'] = '/SingleMuon/Run2018C-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD'
samples['data']['2018']['SingleMuon']['Run2018D'] = '/SingleMuon/Run2018D-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD'

#/SingleMuon/Run2017B-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD
#/SingleMuon/Run2017C-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD
#/SingleMuon/Run2017D-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD
#/SingleMuon/Run2017E-UL2017_MiniAODv1_NanoAODv2-v2/NANOAOD
#/SingleMuon/Run2017F-UL2017_MiniAODv1_NanoAODv2-v2/NANOAOD
#/SingleMuon/Run2017G-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD
#/SingleMuon/Run2017H-UL2017_LowPU_MiniAODv1_NanoAODv2-v1/NANOAOD
samples['data']['2017']['SingleMuon']['Run2017B'] = '/SingleMuon/Run2017B-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD'
samples['data']['2017']['SingleMuon']['Run2017C'] = '/SingleMuon/Run2017C-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD'
samples['data']['2017']['SingleMuon']['Run2017D'] = '/SingleMuon/Run2017D-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD'
samples['data']['2017']['SingleMuon']['Run2017E'] = '/SingleMuon/Run2017E-UL2017_MiniAODv1_NanoAODv2-v2/NANOAOD'
samples['data']['2017']['SingleMuon']['Run2017F'] = '/SingleMuon/Run2017F-UL2017_MiniAODv1_NanoAODv2-v2/NANOAOD'
samples['data']['2017']['SingleMuon']['Run2017G'] = '/SingleMuon/Run2017G-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD'
samples['data']['2017']['SingleMuon']['Run2017H'] = '/SingleMuon/Run2017H-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD'

#/SingleMuon/Run2016B-ver1_HIPM_UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD
#/SingleMuon/Run2016B-ver2_HIPM_UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD
#/SingleMuon/Run2016C-UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD
#/SingleMuon/Run2016D-UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD
#/SingleMuon/Run2016E-UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD
#/SingleMuon/Run2016F-HIPM_UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD
#/SingleMuon/Run2016F-UL2016_MiniAODv1_NanoAODv2-v4/NANOAOD
#/SingleMuon/Run2016G-UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD
#/SingleMuon/Run2016H-UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD
samples['data']['2016']['SingleMuon']['Run2016B-ver1_HIPM'] = '/SingleMuon/Run2016B-ver1_HIPM_UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD'
samples['data']['2016']['SingleMuon']['Run2016B-ver2_HIPM'] = '/SingleMuon/Run2016B-ver2_HIPM_UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD'
samples['data']['2016']['SingleMuon']['Run2016C'] = '/SingleMuon/Run2016C-UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD'
samples['data']['2016']['SingleMuon']['Run2016D'] = '/SingleMuon/Run2016D-UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD'
samples['data']['2016']['SingleMuon']['Run2016E'] = '/SingleMuon/Run2016E-UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD'
samples['data']['2016']['SingleMuon']['Run2016F-HIPM'] = '/SingleMuon/Run2016F-HIPM_UL2016_MiniAODv1_NanoAODv2-v4/NANOAOD'
samples['data']['2016']['SingleMuon']['Run2016F'] = '/SingleMuon/Run2016F-UL2016_MiniAODv1_NanoAODv2-v4/NANOAOD'
samples['data']['2016']['SingleMuon']['Run2016G'] = '/SingleMuon/Run2016G-UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD'
samples['data']['2016']['SingleMuon']['Run2016H'] = '/SingleMuon/Run2016H-UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD'




'''
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

samples['MC']['ST_tW_antitop_5f_NoFullyHadronicDecays'] = '/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia/'
samples['MC']['ST_tW_top_5f_NoFullyHadronicDecays'] = '/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/'

# Are these v2?
samples['MC']['ST_tW_antitop_5f_inclusiveDecays'] = '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/'
samples['MC']['ST_tW_top_5f_inclusiveDecays'] = '/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/'

samples['MC']['ST_tW_antitop_5f_NoFullyHadronicDecays'] = '/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/'

samples['MC']['TTGJets'] = '/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/'
samples['MC']['TTJets'] = '/TTJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/'
samples['MC']['TTWJetsToLNu'] = '/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/'
samples['MC']['TTWJetsToQQ'] = '/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/'

samples['MC']['TTZToNuNu'] = '/TTZToNuNu_TuneCP5_13TeV-amcatnlo-pythia8/'
samples['MC']['TTZToLLNuNu_M-10'] = '/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/'
samples['MC']['TTZToQQ'] = '/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/'

samples['MC']['WJetsToLNu'] = '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/'
samples['MC']['WJetsToQQ'] = '/WJetsToQQ_TuneCP5_13TeV-madgraphMLM-pythia8/'

# Might need to be v2 for Global Tag?
samples['MC']['ZJetsToQQ_HT-200to400'] = '/ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/'
samples['MC']['ZJetsToQQ_HT-400to600'] = '/ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/'
samples['MC']['ZJetsToQQ_HT-600to800'] = '/ZJetsToQQ_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/'
samples['MC']['ZJetsToQQ_HT-800toInf'] = '/ZJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8/'

# Might need to be v2 for Global Tag?
samples['MC']['WJetsToQQ_HT-200to400'] = '/WJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/'
samples['MC']['WJetsToQQ_HT-400to600'] = '/WJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/'
samples['MC']['WJetsToQQ_HT-600to800'] = '/WJetsToQQ_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/'
samples['MC']['WJetsToQQ_HT-800toInf'] = '/WJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8/'

# Might want to look at Mu and EM enriched as well. Those might be -v2
samples['MC']['QCD_Pt_15to30'] = '/QCD_Pt_15to30_TuneCP5_13TeV_pythia8/'
samples['MC']['QCD_Pt_30to50'] = '/QCD_Pt_30to50_TuneCP5_13TeV_pythia8/'
samples['MC']['QCD_Pt_50to80'] = '/QCD_Pt_50to80_TuneCP5_13TeV_pythia8/'
samples['MC']['QCD_Pt_80to120'] = '/QCD_Pt_80to120_TuneCP5_13TeV_pythia8/'
samples['MC']['QCD_Pt_120to170'] = '/QCD_Pt_120to170_TuneCP5_13TeV_pythia8/'
samples['MC']['QCD_Pt_170to300'] = '/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/'
samples['MC']['QCD_Pt_300to470'] = '/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/'
samples['MC']['QCD_Pt_470to600'] = '/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/'
samples['MC']['QCD_Pt_600to800'] = '/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/'
samples['MC']['QCD_Pt_800to1000'] = '/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/'

samples['MC']['DYJetsToLL_M-10to50'] = '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/'
samples['MC']['DYJetsToLL_M-50'] = '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/'
'''

#### Signal
samples['MC']['ST_TuneCP5_BNV_TBUMu'] = '/ST_TuneCP5_BNV_TBUMu_13TeV-madgraph-pythia8/'
samples['MC']['ST_TuneCP5_BNV_TDCE'] = '/ST_TuneCP5_BNV_TDCE_13TeV-madgraph-pythia8/'
samples['MC']['ST_TuneCP5_BNV_TDUE'] = '/ST_TuneCP5_BNV_TDUE_13TeV-madgraph-pythia8/'
samples['MC']['ST_TuneCP5_BNV_TSCE'] = '/ST_TuneCP5_BNV_TSCE_13TeV-madgraph-pythia8/'
samples['MC']['ST_TuneCP5_BNV_TSCE'] = '/ST_TuneCP5_BNV_TSCE_13TeV-madgraph-pythia8/'
samples['MC']['ST_TuneCP5_BNV_TSUE'] = '/ST_TuneCP5_BNV_TSUE_13TeV-madgraph-pythia8/'
samples['MC']['TT_TToBCE_TuneCP5_BNV'] = '/TT_TToBCE_TuneCP5_BNV_13TeV-madgraph-pythia8/'
samples['MC']['TT_TToDCMu_TuneCP5_BNV'] = '/TT_TToDCMu_TuneCP5_BNV_13TeV-madgraph-pythia8/'
samples['MC']['TT_TToDCMu_TuneCP5_BNV'] = '/TT_TToDCMu_TuneCP5_BNV_13TeV-madgraph-pythia8/'
samples['MC']['TT_TToDUMu_TuneCP5_BNV'] = '/TT_TToDUMu_TuneCP5_BNV_13TeV-madgraph-pythia8/'
samples['MC']['TT_TToSCE_TuneCP5_BNV'] = '/TT_TToSCE_TuneCP5_BNV_13TeV-madgraph-pythia8/'
samples['MC']['TT_TToSUE_TuneCP5_BNV'] = '/TT_TToSUE_TuneCP5_BNV_13TeV-madgraph-pythia8/'



################################################################################
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
        name = val + mc_type[year]['Run'] + "-" + mc_type[year]['GT'] + "/" + mc_tier
        if name.find('inclusiveDecays')>=0 or \
           name.find('ZJetsToQQ_HT')>=0 or \
           name.find('WJetsToQQ_HT')>=0:
            name = name.replace('-v1','-v2')
        samples['MC'][year][s] = name
    #print(samples['MC']['2018'][s])



