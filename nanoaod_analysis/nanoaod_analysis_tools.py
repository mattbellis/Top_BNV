################################################################################
#####################################################################################
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopTrigger
# https://twiki.cern.ch/twiki/bin/view/CMS/TopTriggerYear2016
# https://twiki.cern.ch/twiki/bin/view/CMS/TopTriggerYear2017 
# https://twiki.cern.ch/twiki/bin/view/CMS/TopTriggerYear2018 
################################################################################
# Triggers
################################################################################

# MC values are for the 2016 data
muon_triggers_of_interest = {}
muon_triggers_of_interest['2016'] = ['IsoMu24']
muon_triggers_of_interest['2017'] = ['IsoMu24_eta2p1']
muon_triggers_of_interest['2018'] = ['IsoMu24']

electron_triggers_of_interest = {}
electron_triggers_of_interest['2016'] = ['Ele32_WPTight_Gsf','Ele27_WPTight_Gsf']
electron_triggers_of_interest['2017'] = ['Ele32_WPTight_Gsf_L1DoubleEG', 'Ele35_WPTight_Gsf','Ele38_WPTight_Gsf','Ele40_WPTight_Gsf']
electron_triggers_of_interest['2018'] = ['Ele32_WPTight_Gsf','Ele35_WPTight_Gsf','Ele38_WPTight_Gsf']


'''
muon_triggers_of_interest = [
    ["HLT_IsoMu24_v", "v4"], # 2016 and 2018
    ["HLT_IsoTkMu24_v","v4"],
    ["HLT_IsoMu22_eta2p1_v","v4"],
    ["HLT_IsoTkMu22_eta2p1_v","v4"],
    ["HLT_IsoMu24_eta2p1_v","v"], # Maybe for 2017 data?
    ["HLT_IsoMu27_v","v"] # Maybe for 2017 data?
    ]

electron_triggers_of_interest = [
    ["HLT_Ele32_eta2p1_WPTight_Gsf_v", "v8"],
    ["HLT_Ele27_WPTight_Gsf_v", "v7"],
    ["HLT_Ele25_eta2p1_WPTight_Gsf_v", "v7"],
    ["HLT_Ele35_WPTight_Gsf_v", "v"], # 2017
    ["HLT_Ele32_WPTight_Gsf_v", "v"] # 2017
    ]

dilepmue_triggers_of_interest = [
    ["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v", "v9"],
    ["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v", "v4"]
]

dilepemu_triggers_of_interest = [
    ["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v", "v9"],
    ["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v", ""],
    ["HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v", "v3"],
    ["HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v", "v4"]
]

dilepmumu_triggers_of_interest = [
    ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v", "v7"],
    ["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v", "v6"]
    ]

dilepee_triggers_of_interest = [
    ["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v", "v9"],
    ["HLT_DoubleEle24_22_eta2p1_WPLoose_Gsf_v", "v8"]
    ]
'''

triggers_of_interest = [
["SingleMuon",muon_triggers_of_interest],
["SingleElectron",electron_triggers_of_interest],
]
#["DileptonMuE",dilepmue_triggers_of_interest],
#["DileptonEMu",dilepemu_triggers_of_interest],
#["DileptonMuMu",dilepmumu_triggers_of_interest],
#["DileptonEE",dilepee_triggers_of_interest]
#]

################################################################################
def trigger_mask(triggers_choice, events_HLT):

    mask = None
    for i,trigger in enumerate(triggers_choice):

        if i==0:
            mask = (events_HLT[trigger] == True)
        else:
            mask &= (events_HLT[trigger] == True)

    return mask

################################################################################
#def pileup_reweighting(triggers_choice, events_HLT):


################################################################################
# https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2#Muon_selectors_Since_9_4_X
def muon_mask(muons, flag='loose', isoflag=0, ptcut=10):

    # Pt cut
    mask_pt = (muons.pt > ptcut)

    # ID flag
    mask_id = None
    if flag == 'loose':
        mask_id = (muons.looseId==True)
    elif flag == 'medium':
        mask_id = (muons.mediumId==True)
    elif flag == 'tight':
        mask_id = (muons.tightId==True)

    # Isolation
    # https://cms-nanoaod-integration.web.cern.ch/integration/master-106X/mc102X_doc.html#Muon
    # (1=PFIsoVeryLoose, 2=PFIsoLoose, 3=PFIsoMedium, 4=PFIsoTight, 5=PFIsoVeryTight, 6=PFIsoVeryVeryTight)
    mask_iso = (muons.pfIsoId >= isoflag)

    mask = mask_pt & mask_id & mask_iso

    return mask


