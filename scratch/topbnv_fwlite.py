# Much of this is from the B2G data analysis school code

import ROOT, copy, sys, logging
from array import array
from DataFormats.FWLite import Events, Handle

from RecoEgamma.ElectronIdentification.VIDElectronSelector import VIDElectronSelector
# Cut-based...we should use this!
# https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2#Recipe80X
#from RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff import cutBasedElectronID_Summer16_80X_V1_loose
from RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff import cutBasedElectronID_Summer16_80X_V1_medium

# Need to do this globally because there's a warning associated with the attribute, isPOGApproved
# that doesn't need to be there but would get called every time we called this from the event
# loop!
selectElectron = VIDElectronSelector(cutBasedElectronID_Summer16_80X_V1_medium)

#import RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff.cutBasedElectronID-Summer16-80X-V1-loose as electron_loose
#import RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff.cutBasedElectronID-Summer16-80X-V1-medium as electron_medium
#import RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff.cutBasedElectronID-Summer16-80X-V1-tight as electron_tight

#####################################################################################
#jet_energy_corrections = [ # Values from https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC
#    [1,276811,"Spring16_23Sep2016BCDV2_DATA"],
#    [276831,278801,"Spring16_23Sep2016EFV2_DATA"],
#    [278802,280385,"Spring16_23Sep2016GV2_DATA"],
#    [280386,float("inf"),"Spring16_23Sep2016HV2_DATA"]
#]

# https://twiki.cern.ch/twiki/bin/viewauth/CMS/JECDataMC
########## NEED TO CHECK TO SEE IF THESE ARE CORRECT!!!!!!!!!
# How do I get these ranges?
#jet_energy_corrections = [ [1,276811,"Summer16_23Sep2016V4"],
        #[276831,278801,"Summer16_23Sep2016V4"],
        #[278802,280385,"Summer16_23Sep2016V4"],
        #[280919,float("inf"),"Summer16_23Sep2016V4"] ]

# THESE SHOULD BE THE LATEST - 9/12/2018
jet_energy_corrections = [ [1,276811,"Summer16_07Aug2017BCD_V11_DATA"],
        [276831,278801,"Summer16_07Aug2017EF_V11_DATA"],
        [278802,float("inf"),"Summer16_07Aug2017GH_V11_DATA"] ]
        

#####################################################################################
# CHECK THIS!!!!!!!!!!
#####################################################################################
jet_energy_resolution = [ # Values from https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution
                (0.0, 0.5, 1.109, 0.008),
                (0.5, 0.8, 1.138, 0.013),
                (0.8, 1.1, 1.114, 0.013),
                (1.1, 1.3, 1.123, 0.024),
                (1.3, 1.7, 1.084, 0.011),
                (1.7, 1.9, 1.082, 0.035),
                (1.9, 2.1, 1.140, 0.047),
                (2.1, 2.3, 1.067, 0.053),
                (2.3, 2.5, 1.177, 0.041),
                (2.5, 2.8, 1.364, 0.039),
                (2.8, 3.0, 1.857, 0.071),
                (3.0, 3.2, 1.328, 0.022),
                (3.2, 5.0, 1.160, 0.029),
                                                            ]

#####################################################################################
def createJEC(jecSrc, jecLevelList, jetAlgo):
    print("Creating JECs....")
    log = logging.getLogger('JEC')
    log.info('Getting jet energy corrections for %s jets', jetAlgo)
    jecParameterList = ROOT.vector('JetCorrectorParameters')()
    # Load the different JEC levels (the order matters!)
    for jecLevel in jecLevelList:
        log.debug('  - %s jet corrections', jecLevel)
        jec_parameter_name = ('%s_%s_%s.txt' % (jecSrc, jecLevel, jetAlgo));
        print(jec_parameter_name)
        jecParameter = ROOT.JetCorrectorParameters(jec_parameter_name)
        print(jecParameter)
        jecParameterList.push_back(jecParameter)
    # Chain the JEC levels together
    #jecParameterList.Print()
    return ROOT.FactorizedJetCorrector(jecParameterList)

#####################################################################################
def getJEC(jecSrc, uncSrc, jet, area, rho, nPV): # get JEC and uncertainty for an *uncorrected* jet
    # Give jet properties to JEC source
    jecSrc.setJetEta(jet.Eta())
    jecSrc.setJetPt(jet.Perp())
    jecSrc.setJetE(jet.E())
    jecSrc.setJetA(area)
    jecSrc.setRho(rho)
    jecSrc.setNPV(nPV)
    jec = jecSrc.getCorrection() # get jet energy correction

    # Give jet properties to JEC uncertainty source
    uncSrc.setJetPhi(jet.Phi())
    uncSrc.setJetEta(jet.Eta())
    uncSrc.setJetPt(jet.Perp() * jec)
    corrDn = 1. - uncSrc.getUncertainty(0) # get jet energy uncertainty (down)

    uncSrc.setJetPhi(jet.Phi())
    uncSrc.setJetEta(jet.Eta())
    uncSrc.setJetPt(jet.Perp() * jec)
    corrUp = 1. + uncSrc.getUncertainty(1) # get jet energy uncertainty (up)

    return (jec, corrDn, corrUp)

#####################################################################################
#####################################################################################
def getJER(jetEta, sysType):
    """
    Here, jetEta should be the jet pseudorapidity, and sysType is:
        nominal : 0
        down    : -1
        up      : +1
    """

    if sysType not in [0, -1, 1]:
        raise Exception('ERROR: Unable to get JER! use type=0 (nom), -1 (down), +1 (up)')

    for (etamin, etamax, scale_nom, scale_uncert) in jet_energy_resolution:
        if etamin <= abs(jetEta) < etamax:
            if sysType < 0:
                return scale_nom - scale_uncert
            elif sysType > 0:
                return scale_nom + scale_uncert
            else:
                return scale_nom
    raise Exception('ERROR: Unable to get JER for jets at eta = %.3f!' % jetEta)

#####################################################################################
#####################################################################################
class DataJEC:
    JECList = []
    def __init__(self,inputmap):
        for minrun,maxrun,version in inputmap:
            JECMap = {}
            JECMap['jecAK4'] = createJEC('JECs/Summer/'+version, ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual'], 'AK4PFchs')
            JECMap['jecAK8'] = createJEC('JECs/Summer/'+version, ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual'], 'AK8PFchs')
            JECMap['jecUncAK4'] = ROOT.JetCorrectionUncertainty(ROOT.std.string('JECs/Summer/'+version+'_Uncertainty_AK4PFchs.txt'))
            JECMap['jecUncAK8'] = ROOT.JetCorrectionUncertainty(ROOT.std.string('JECs/Summer/'+version+'_Uncertainty_AK8PFchs.txt'))
            self.JECList.append([minrun, maxrun, JECMap])

    def GetJECMap(self, run):
        for minrun,maxrun,returnmap in self.JECList:
            if run >= minrun and run <= maxrun:
                return returnmap
        raise Exception("Error! Run "+str(run)+" not found in run ranges")

    def jecAK4(self, run):
        JECMap = self.GetJECMap(run)
        return JECMap["jecAK4"]

    def jecAK8(self, run):
        JECMap = self.GetJECMap(run)
        return JECMap["jecAK8"]

    def jecUncAK4(self, run):
        JECMap = self.GetJECMap(run)
        return JECMap["jecUncAK4"]

    def jecUncAK8(self, run):
        JECMap = self.GetJECMap(run)
        return JECMap["jecUncAK8"]



#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################

# MC values are for the 2016 data
muon_triggers_of_interest = [
    ["HLT_IsoMu24_v", "v4"],
    ["HLT_IsoTkMu24_v","v4"],
    ["HLT_IsoMu22_eta2p1_v","v4"],
    ["HLT_IsoTkMu22_eta2p1_v","v4"]
    ]

electron_triggers_of_interest = [
    ["HLT_Ele32_eta2p1_WPTight_Gsf_v", "v7"],
    ["HLT_Ele27_WPTight_Gsf_v", "v8"],
    ["HLT_Ele25_eta2p1_WPTight_Gsf_v", "v8"]
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

triggers_of_interest = [
["SingleMuon",muon_triggers_of_interest],
["SingleElectron",electron_triggers_of_interest],
["DileptonMuE",dilepmue_triggers_of_interest],
["DileptonEMu",dilepemu_triggers_of_interest],
["DileptonMuMu",dilepmumu_triggers_of_interest],
["DileptonEE",dilepee_triggers_of_interest]
]


#####################################################################################
# Command line parsing
#####################################################################################
def getUserOptions(argv):
    from optparse import OptionParser
    parser = OptionParser()

    def add_option(option, **kwargs):
        parser.add_option('--' + option, dest=option, **kwargs)

    add_option('input',              default='',
        help='Name of file with list of input files')
    add_option('output',             default='output.root',
        help='Name of output file')
    add_option('verbose',            default=False, action='store_true',
        help='Print debugging info')
    add_option('maxevents',          default=-1,
        help='Number of events to run. -1 is all events')
    add_option('trigType',         default="SingleMuon", 
        help='SingleMuon, SingleElectron, etc.')
    add_option('bdisc',          default="pfCombinedInclusiveSecondaryVertexV2BJetTags",
        help='pfCombinedInclusiveSecondaryVertexV2BJetTags, etc.')
    add_option('isMC',          default=False, action='store_true',
        help='Running over MC. We need this for the trigger and other stuff.')
    add_option('isCrabRun',          default=False, action='store_true',
        help='Use this flag when running with crab on the grid')
    add_option('localInputFiles',    default=False, action='store_true',
        help='Use this flag when running with with local files')

    (options, args) = parser.parse_args(argv)
    argv = []

    print ('===== Command line options =====')
    print (options)
    print ('================================')
    return options



#####################################################################################
def getInputFiles(options):
    result = []
    with open(options.input, 'r') as fpInput:
        for lfn in fpInput:
            print("lfn: ")
            print(lfn)
            lfn = lfn.strip()
            print(lfn)
            if lfn:
                if not options.isCrabRun:
                    if options.localInputFiles:
                        pfn = lfn
                        print('pfn: ')
                        print(pfn)
                    else:
                        #pfn = 'file:/pnfs/desy.de/cms/tier2/' + lfn
                        pfn = 'root://cmsxrootd-site.fnal.gov/' + lfn
                else:
                    #pfn = 'root://cmsxrootd-site.fnal.gov/' + lfn
                    pfn = 'root://xrootd-cms.infn.it/' + lfn
                print ('Adding ' + pfn)
                result.append(pfn)
    print(result)
    return result
#####################################################################################





#####################################################################################
def topbnv_fwlite(argv):
    ## _____________      __.____    .__  __             _________ __          _____  _____
    ## \_   _____/  \    /  \    |   |__|/  |_  ____    /   _____//  |_ __ ___/ ____\/ ____\
    ##  |    __) \   \/\/   /    |   |  \   __\/ __ \   \_____  \\   __\  |  \   __\\   __\
    ##  |     \   \        /|    |___|  ||  | \  ___/   /        \|  | |  |  /|  |   |  |
    ##  \___  /    \__/\  / |_______ \__||__|  \___  > /_______  /|__| |____/ |__|   |__|
    ##      \/          \/          \/             \/          \/

    options = getUserOptions(argv)
    ROOT.gROOT.Macro("rootlogon.C")

    #print argv
    #print options

    jets, jetLabel = Handle("std::vector<pat::Jet>"), "slimmedJets"
    muons, muonLabel = Handle("std::vector<pat::Muon>"), "slimmedMuons"
    electrons, electronLabel = Handle("std::vector<pat::Electron>"), "slimmedElectrons"
    gens, genLabel = Handle("std::vector<reco::GenParticle>"), "prunedGenParticles"
    #packedgens, packedgenLabel = Handle("std::vector<reco::packedGenParticle>"), "PACKEDgENpARTICLES"
    packedgens, packedgenLabel = Handle("std::vector<pat::PackedGenParticle>"), "packedGenParticles"
    rhos, rhoLabel = Handle("double"), "fixedGridRhoAll"
    vertices, vertexLabel = Handle("std::vector<reco::Vertex>"), "offlineSlimmedPrimaryVertices"
    genInfo, genInfoLabel = Handle("GenEventInfoProduct"), "generator"
    mets, metLabel = Handle("std::vector<pat::MET>"), "slimmedMETs"

    # NEED HLT2 for 80x 2016 (maybe only TTBar?
    # https://twiki.cern.ch/twiki/bin/view/CMS/TopTrigger#Summary_for_2016_Run2016B_H_25_n
    triggerBits, triggerBitLabel = Handle("edm::TriggerResults"), ("TriggerResults","", "HLT")



    f = ROOT.TFile(options.output, "RECREATE")
    f.cd()

    outtree = ROOT.TTree("T", "Our tree of everything")

    def bookFloatBranch(name, default):
        tmp = array('f', [default])
        outtree.Branch(name, tmp, '%s/F' %name)
        return tmp
    def bookIntBranch(name, default):
        tmp = array('i', [default])
        outtree.Branch(name, tmp, '%s/I' %name)
        return tmp
    def bookLongIntBranch(name, default):
        tmp = array('l', [default])
        outtree.Branch(name, tmp, '%s/L' %name)
        return tmp

    # Generated MC 4-momentum
    ngen = array('i', [-1])
    outtree.Branch('ngen', ngen, 'ngen/I')

    genpt = array('f', 16*[-1.])
    outtree.Branch('genpt', genpt, 'genpt[ngen]/F')
    geneta = array('f', 16*[-1.])
    outtree.Branch('geneta', geneta, 'geneta[ngen]/F')
    genphi = array('f', 16*[-1.])
    outtree.Branch('genphi', genphi, 'genphi[ngen]/F')
    gene = array('f', 16*[-1.])
    outtree.Branch('gene', gene, 'gene[ngen]/F')
    genpx = array('f', 16*[-1.])
    outtree.Branch('genpx', genpx, 'genpx[ngen]/F')
    genpy = array('f', 16*[-1.])
    outtree.Branch('genpy', genpy, 'genpy[ngen]/F')
    genpz = array('f', 16*[-1.])
    outtree.Branch('genpz', genpz, 'genpz[ngen]/F')

    genpdg = array('i', 16*[-1])
    outtree.Branch('genpdg', genpdg, 'genpdg[ngen]/I')
    genmotherpdg = array('i', 16*[-1])
    outtree.Branch('genmotherpdg', genmotherpdg, 'genmotherpdg[ngen]/I')
    genmotheridx = array('i', 16*[-1])
    outtree.Branch('genmotheridx', genmotheridx, 'genmotheridx[ngen]/I')
    genndau = array('i', 16*[-1])
    outtree.Branch('genndau', genndau, 'genndau[ngen]/I')

    # Jets
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideCMSDataAnalysisSchoolLPC2018Jets
    njet = array('i', [-1])
    outtree.Branch('njet', njet, 'njet/I')

    jetpt = array('f', 16*[-1.])
    outtree.Branch('jetpt', jetpt, 'jetpt[njet]/F')
    jeteta = array('f', 16*[-1.])
    outtree.Branch('jeteta', jeteta, 'jeteta[njet]/F')
    jetphi = array('f', 16*[-1.])
    outtree.Branch('jetphi', jetphi, 'jetphi[njet]/F')
    jetpx = array('f', 16*[-1.])
    outtree.Branch('jetpx', jetpx, 'jetpx[njet]/F')
    jetpy = array('f', 16*[-1.])
    outtree.Branch('jetpy', jetpy, 'jetpy[njet]/F')
    jetpz = array('f', 16*[-1.])
    outtree.Branch('jetpz', jetpz, 'jetpz[njet]/F')
    jete = array('f', 16*[-1.])
    outtree.Branch('jete', jete, 'jete[njet]/F')

    jetbtag = array('f', 16*[-1.])
    outtree.Branch('jetbtag', jetbtag, 'jetbtag[njet]/F')

    jetarea = array('f', 16*[-1.])
    outtree.Branch('jetarea', jetarea, 'jetarea[njet]/F')

    jetjec = array('f', 16*[-1.])
    outtree.Branch('jetjec', jetjec, 'jetjec[njet]/F')

    jetNHF = array('f', 16*[-1.])
    outtree.Branch('jetNHF', jetNHF, 'jetNHF[njet]/F')
    jetNEMF = array('f', 16*[-1.])
    outtree.Branch('jetNEMF', jetNEMF, 'jetNEMF[njet]/F')
    jetCHF = array('f', 16*[-1.])
    outtree.Branch('jetCHF', jetCHF, 'jetCHF[njet]/F')
    jetMUF = array('f', 16*[-1.])
    outtree.Branch('jetMUF', jetMUF, 'jetMUF[njet]/F')
    jetCEMF = array('f', 16*[-1.])
    outtree.Branch('jetCEMF', jetCEMF, 'jetCEMF[njet]/F')
    jetNumConst = array('f', 16*[-1.])
    outtree.Branch('jetNumConst', jetNumConst, 'jetNumConst[njet]/F')
    jetNumNeutralParticles = array('f', 16*[-1.])
    outtree.Branch('jetNumNeutralParticles', jetNumNeutralParticles, 'jetNumNeutralParticles[njet]/F')
    jetCHM = array('f', 16*[-1.])
    outtree.Branch('jetCHM', jetCHM, 'jetCHM[njet]/F')

    # Muons
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideCMSDataAnalysisSchoolLPC2018Muons
    # https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2
    nmuon = array('i', [-1])
    outtree.Branch('nmuon', nmuon, 'nmuon/I')
    muonpt = array('f', 16*[-1.])
    outtree.Branch('muonpt', muonpt, 'muonpt[nmuon]/F')
    muoneta = array('f', 16*[-1.])
    outtree.Branch('muoneta', muoneta, 'muoneta[nmuon]/F')
    muonphi = array('f', 16*[-1.])
    outtree.Branch('muonphi', muonphi, 'muonphi[nmuon]/F')
    muonq = array('f', 16*[-1.])
    outtree.Branch('muonq', muonq, 'muonq[nmuon]/F')
    muonpx = array('f', 16*[-1.])
    outtree.Branch('muonpx', muonpx, 'muonpx[nmuon]/F')
    muonpy = array('f', 16*[-1.])
    outtree.Branch('muonpy', muonpy, 'muonpy[nmuon]/F')
    muonpz = array('f', 16*[-1.])
    outtree.Branch('muonpz', muonpz, 'muonpz[nmuon]/F')
    muone = array('f', 16*[-1.])
    outtree.Branch('muone', muone, 'muone[nmuon]/F')
    muonsumchhadpt = array('f', 16*[-1.])
    outtree.Branch('muonsumchhadpt', muonsumchhadpt, 'muonsumchhadpt[nmuon]/F')
    muonsumnhadpt = array('f', 16*[-1.])
    outtree.Branch('muonsumnhadpt', muonsumnhadpt, 'muonsumnhadpt[nmuon]/F')
    muonsumphotEt = array('f', 16*[-1.])
    outtree.Branch('muonsumphotEt', muonsumphotEt, 'muonsumphotEt[nmuon]/F')
    muonsumPUPt = array('f', 16*[-1.])
    outtree.Branch('muonsumPUPt', muonsumPUPt, 'muonsumPUPt[nmuon]/F')
    muonisLoose = array('i', 16*[-1])
    outtree.Branch('muonisLoose', muonisLoose, 'muonisLoose[nmuon]/I')
    muonisMedium = array('i', 16*[-1])
    outtree.Branch('muonisMedium', muonisMedium, 'muonisMedium[nmuon]/I')

    muonPFiso = array('f', 16*[-1.]); outtree.Branch('muonPFiso', muonPFiso, 'muonPFiso[nmuon]/F')


    # Electrons
    nelectron = array('i', [-1])
    outtree.Branch('nelectron', nelectron, 'nelectron/I')
    electronpt = array('f', 16*[-1.])
    outtree.Branch('electronpt', electronpt, 'electronpt[nelectron]/F')
    electroneta = array('f', 16*[-1.])
    outtree.Branch('electroneta', electroneta, 'electroneta[nelectron]/F')
    electronphi = array('f', 16*[-1.])
    outtree.Branch('electronphi', electronphi, 'electronphi[nelectron]/F')
    electronq = array('f', 16*[-1.])
    outtree.Branch('electronq', electronq, 'electronq[nelectron]/F')
    electronpx = array('f', 16*[-1.])
    outtree.Branch('electronpx', electronpx, 'electronpx[nelectron]/F')
    electronpy = array('f', 16*[-1.])
    outtree.Branch('electronpy', electronpy, 'electronpy[nelectron]/F')
    electronpz = array('f', 16*[-1.])
    outtree.Branch('electronpz', electronpz, 'electronpz[nelectron]/F')
    electrone = array('f', 16*[-1.])
    outtree.Branch('electrone', electrone, 'electrone[nelectron]/F')
    electronTkIso = array('f',16*[-1.])
    outtree.Branch('electronTkIso', electronTkIso, 'electronTkIso[nelectron]/F')
    electronHCIso = array('f',16*[-1.])
    outtree.Branch('electronHCIso', electronHCIso, 'electronHCIso[nelectron]/F')
    electronECIso = array('f',16*[-1.])
    outtree.Branch('electronECIso', electronECIso, 'electronECIso[nelectron]/F')

    # MET
    metpt = array('f', [-1])
    outtree.Branch('metpt', metpt, 'metpt/F')
    metphi = array('f', [-1])
    outtree.Branch('metphi', metphi, 'metphi/F')
    mete = array('f', [-1])
    outtree.Branch('mete',mete, 'mete/F')
    meteta = array('f',[-1])
    outtree.Branch('meteta', meteta, 'meteta/F')

    # Vertex stuff
    vertexX = array('f',[-1.])
    outtree.Branch('vertexX', vertexX, 'vertexX/F')
    vertexY = array('f',[-1.])
    outtree.Branch('vertexY', vertexY, 'vertexY/F')
    vertexZ = array('f',[-1.])
    outtree.Branch('vertexZ', vertexZ, 'vertexZ/F')

    # Triggers
    # We'll record 4 muon trigger bits for 2016 data
    ntrig_muon = array('i', [-1])
    outtree.Branch('ntrig_muon', ntrig_muon, 'ntrig_muon/I')
    trig_muon = array('i',8*[-1])
    outtree.Branch('trig_muon', trig_muon, 'trig_muon[ntrig_muon]/I')

    ntrig_electron = array('i', [-1])
    outtree.Branch('ntrig_electron', ntrig_electron, 'ntrig_electron/I')
    trig_electron = array('i',8*[-1])
    outtree.Branch('trig_electron', trig_electron, 'trig_electron[ntrig_electron]/I')

    ntrig_dilepmue = array('i', [-1])
    outtree.Branch('ntrig_dilepmue', ntrig_dilepmue, 'ntrig_dilepmue/I')
    trig_dilepmue = array('i',8*[-1])
    outtree.Branch('trig_dilepmue', trig_dilepmue, 'trig_dilepmue[ntrig_electron]/I')

    ntrig_dilepemu = array('i', [-1])
    outtree.Branch('ntrig_dilepemu', ntrig_dilepemu, 'ntrig_dilepemu/I')
    trig_dilepemu = array('i',8*[-1])
    outtree.Branch('trig_dilepemu', trig_dilepemu, 'trig_dilepemu[ntrig_electron]/I')

    ntrig_dilepmumu = array('i', [-1])
    outtree.Branch('ntrig_dilepmumu', ntrig_dilepmumu, 'ntrig_dilepmumu/I')
    trig_dilepmumu = array('i',8*[-1])
    outtree.Branch('trig_dilepmumu', trig_dilepmumu, 'trig_dilepmumu[ntrig_electron]/I')

    ntrig_dilepee = array('i', [-1])
    outtree.Branch('ntrig_dilepee', ntrig_dilepee, 'ntrig_dilepee/I')
    trig_dilepee = array('i',8*[-1])
    outtree.Branch('trig_dilepee', trig_dilepee, 'trig_dilepee[ntrig_electron]/I')

    trigger_tree_branches = {
    "SingleMuon":trig_muon,
    "SingleElectron":trig_electron,
    "DileptonMuE":trig_dilepmue,
    "DileptonEMu":trig_dilepemu,
    "DileptonMuMu":trig_dilepmumu,
    "DileptonEE":trig_dilepee
    }

    #################################################################################
    ##      ____.       __    _________                                     __  .__
    ##     |    | _____/  |_  \_   ___ \  __________________   ____   _____/  |_|__| ____   ____   ______
    ##     |    |/ __ \   __\ /    \  \/ /  _ \_  __ \_  __ \_/ __ \_/ ___\   __\  |/  _ \ /    \ /  ___/
    ## /\__|    \  ___/|  |   \     \___(  <_> )  | \/|  | \/\  ___/\  \___|  | |  (  <_> )   |  \\___ \
    ## \________|\___  >__|    \______  /\____/|__|   |__|    \___  >\___  >__| |__|\____/|___|  /____  >
    ##               \/               \/                          \/     \/                    \/     \/
    #################################################################################
    ROOT.gSystem.Load('libCondFormatsJetMETObjects')
    if options.isMC:
        # CHANGE THIS FOR DIFFERENT MCs down the road
        jecAK4 = createJEC('JECs/Summer/Summer16_23Sep2016V4_MC', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'AK4PFchs')
        jecAK8 = createJEC('JECs/Summer/Summer16_23Sep2016V4_MC', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'AK8PFchs')
        jecUncAK4 = ROOT.JetCorrectionUncertainty(ROOT.std.string('JECs/Summer/Summer16_23Sep2016V4_MC_Uncertainty_AK4PFchs.txt'))
        jecUncAK8 = ROOT.JetCorrectionUncertainty(ROOT.std.string('JECs/Summer/Summer16_23Sep2016V4_MC_Uncertainty_AK8PFchs.txt'))
    else:
        # CHANGE THIS FOR DATA
        DataJECs = DataJEC(jet_energy_corrections)




    #################################################################################
    ## ___________                    __    .____
    ## \_   _____/__  __ ____   _____/  |_  |    |    ____   ____ ______
    ##  |    __)_\  \/ // __ \ /    \   __\ |    |   /  _ \ /  _ \\____ \
    ##  |        \\   /\  ___/|   |  \  |   |    |__(  <_> |  <_> )  |_> >
    ## /_______  / \_/  \___  >___|  /__|   |_______ \____/ \____/|   __/
    ##         \/           \/     \/               \/            |__|


    # IMPORTANT : Run one FWLite instance per file. Otherwise,
    # FWLite aggregates ALL of the information immediately, which
    # can take a long time to parse.
    #################################################################################
    def processEvent(iev, event):

        evWeight = 1.0 

        genOut = "Event %d\n" % (iev)
        #print "GGGEEENNNNOUT...."
        #print genOut

        #event.getByLabel(triggerBitLabel, triggerBits)
        #event.getByLabel(metfiltBitLabel, metfiltBits)
        runnumber = event.eventAuxiliary().run()

        if options.verbose:
            print "\nProcessing %d: run %6d, lumi %4d, event %12d" % \
                  (iev,event.eventAuxiliary().run(), \
                  event.eventAuxiliary().luminosityBlock(), \
                  event.eventAuxiliary().event())

        ###############################################################
        # Triggers
        ###############################################################
        event.getByLabel(triggerBitLabel, triggerBits)

        trigger_names = event.object().triggerNames(triggerBits.product())

        # Get list of triggers that fired
        #firedTrigs = []
        ntrig_muon[0] = len(muon_triggers_of_interest)
        ntrig_electron[0] = len(electron_triggers_of_interest)
        ntrig_dilepmue[0] = len(dilepmue_triggers_of_interest)
        ntrig_dilepemu[0] = len(dilepemu_triggers_of_interest)
        ntrig_dilepmumu[0] = len(dilepmumu_triggers_of_interest)
        ntrig_dilepee[0] = len(dilepee_triggers_of_interest)


        #print("------- Triggers ---------")
        # Zero out the triggers
        for toi in triggers_of_interest:

            trigger_type = toi[0]
            trigger_bit_names = toi[1]

            for iname,name in enumerate(trigger_bit_names):
                trigger_tree_branches[trigger_type][iname] = 0 # Didn't fire!

        FLAG_passed_trigger = False
        for itrig in xrange(triggerBits.product().size()):

            if triggerBits.product().accept(itrig):
                trigname = trigger_names.triggerName(itrig)

                mc_selection = True

                for toi in triggers_of_interest:

                    trigger_type = toi[0]
                    trigger_bit_names = toi[1]

                    for iname,name in enumerate(trigger_bit_names):

                        if options.isMC:
                            mc_selection = trigname.find(name[1]) # This is the version


                        if trigname.find(name[0]) >= 0 and mc_selection:
                            #print(trigname,trigger_type)
                            #print(iname,trigger_tree_branches[trigger_type])
                            #print(iname,trigger_tree_branches[trigger_type].Name())
                            trigger_tree_branches[trigger_type][iname] = 1 # Fired!
                            if trigger_type == options.trigType:
                                FLAG_passed_trigger = True
                                #print("PASSED TRIGGER REQUIREMENT!")
                        #else:
                            #trigger_tree_branches[trigger_type][iname] = 0 # Didn't fire!

                    #firedTrigs.append( itrig )

        #print("PASSED!!!!!!!!!!!!!! --------------")
        # THIS SHOULD ONLY WRITE EVENTS THAT PASSED THE TRIGGER
        #print("FLAG_passed_trigger: ",FLAG_passed_trigger)
        if not FLAG_passed_trigger:
            #print("NOT PASSING!")
            return -1

        ##   ________                __________.__          __
        ##  /  _____/  ____   ____   \______   \  |   _____/  |_  ______
        ## /   \  ____/ __ \ /    \   |     ___/  |  /  _ \   __\/  ___/
        ## \    \_\  \  ___/|   |  \  |    |   |  |_(  <_> )  |  \___ \
        ##  \______  /\___  >___|  /  |____|   |____/\____/|__| /____  >
        ##         \/     \/     \/                                  \/
        if options.isMC:
            
            '''
            isPackedGenPresent = event.getByLabel( packedgenLabel, packedgens )
            if isPackedGenPresent:
                print("--------------")
                for igen,gen in enumerate( packedgens.product() ):
                    if abs(gen.pdgId())<30:
                        packedgenOut = 'PACKED GEN pdg id=%d energy=%5.3f pt=%+5.3f status=%d ndau: %d mother: %d' % \
                                        ( gen.pdgId(), gen.energy(), gen.pt(), gen.status(), gen.numberOfDaughters(), gen.mother(0).pdgId() )
                        print(packedgenOut)

            ''' 


            haveGenSolution = False
            isGenPresent = event.getByLabel( genLabel, gens )
            if options.verbose:
                print("==========================\nisGenPresent: ",isGenPresent)
                print("==========================")
            if isGenPresent:
                #print(" ----------------------------- ")
                ngen[0] = 10


                topQuark = None
                antitopQuark = None
                found_top = False
                found_antitop = False
                if options.verbose:
                    print("------------------------------------------------------------")
                gcount = 0
                wmenergy = 0
                wpenergy = 0
                for igen,gen in enumerate( gens.product() ):
                    ##### WHEN LOOPING OVER CHECK THE HARD SCATTERING FLAG 
                    ##### TO MAKE SURE WE DON'T WORRY ABOUT TOPS THAT ARE JUST
                    ##### PROPAGATING FROM THEMSELVES
                    mother = -999
                    if gen.mother()!=None:
                        mother = gen.mother().pdgId()
                    if options.verbose:
                        print("----")
                        print( gen.pdgId(), gen.pt(), gen.status(), gen.numberOfDaughters(), mother, gen.isLastCopy() )
                    if 1:
                        genOut = "" # For debugging
                        mother = -999
                        if gen.mother() != None:
                            #'''
                            mother = gen.mother().pdgId() 

                            #genpdg[gcount] = gen.pdgId()
                            if options.verbose:
                                genOut += 'GEN pdg id=%d pt=%+5.3f status=%d ndau: %d mother: %d isLastCopy: %d\n' % \
                                        ( gen.pdgId(), gen.pt(), gen.status(), gen.numberOfDaughters(), mother, gen.isLastCopy() )
                                for ndau in range(0,gen.numberOfDaughters()):
                                    genOut += "daughter pdgid: %d   pt: %f  %f\n" % (gen.daughter(ndau).pdgId(), gen.daughter(ndau).pt(), gen.daughter(ndau).mother().pt())
                                print genOut
                            #'''
                            ##### FIND TOPS AND THEIR DECAYS
                            if abs(gen.pdgId()) == 6 and gen.isLastCopy():
                                parent = gen

                                gene[gcount] = parent.energy()
                                genpt[gcount] = parent.pt()
                                geneta[gcount] = parent.eta()
                                genphi[gcount] = parent.phi()
                                genpdg[gcount] = parent.pdgId()
                                genpx[gcount] = parent.px()
                                genpy[gcount] = parent.py()
                                genpz[gcount] = parent.pz()
                                genmotherpdg[gcount] = -1
                                genmotheridx[gcount] = -1
                                genndau[gcount] = parent.numberOfDaughters()

                                parentidx = gcount

                                if options.verbose:
                                    print(gene[gcount], genpt[gcount], geneta[gcount], genphi[gcount], genpdg[gcount], genpx[gcount], genpy[gcount], genpz[gcount], genmotherpdg[gcount], genmotheridx[gcount], genndau[gcount])

                                gcount += 1

                                if parent.numberOfDaughters()>=2:
                                    for dauidx in range(parent.numberOfDaughters()):
                                        dau = parent.daughter(dauidx)

                                        gene[gcount] = dau.energy()
                                        genpt[gcount] = dau.pt()
                                        geneta[gcount] = dau.eta()
                                        genphi[gcount] = dau.phi()
                                        genpdg[gcount] = dau.pdgId()
                                        genpx[gcount] = dau.px()
                                        genpy[gcount] = dau.py()
                                        genpz[gcount] = dau.pz()
                                        genmotherpdg[gcount] = dau.mother().pdgId()
                                        genmotheridx[gcount] = parentidx
                                        genndau[gcount] = dau.numberOfDaughters()

                                        gcount += 1 

                                        if dau.pdgId()==-24:
                                            wmenergy = dau.energy() # For matching
                                        elif dau.pdgId()==24:
                                            wpenergy = dau.energy() # For matching

                                        if options.verbose:
                                            print(gene[gcount], genpt[gcount], geneta[gcount], genphi[gcount], genpdg[gcount], genpx[gcount], genpy[gcount], genpz[gcount], genmotherpdg[gcount], genmotheridx[gcount], genndau[gcount])

                            ##### FIND Ws AND THEIR DECAYS
                            elif (gen.pdgId() == 24 and gen.isLastCopy() and abs(gen.energy()-wpenergy)< 10) \
                              or (gen.pdgId() ==-24 and gen.isLastCopy() and abs(gen.energy()-wmenergy)< 10):

                                parent = gen

                                parentidx = gcount

                                if parent.numberOfDaughters()==2:
                                    for dauidx in [0,1]:
                                        dau = parent.daughter(dauidx)

                                        gene[gcount] = dau.energy()
                                        genpt[gcount] = dau.pt()
                                        geneta[gcount] = dau.eta()
                                        genphi[gcount] = dau.phi()
                                        genpdg[gcount] = dau.pdgId()
                                        genpx[gcount] = dau.px()
                                        genpy[gcount] = dau.py()
                                        genpz[gcount] = dau.pz()
                                        genmotherpdg[gcount] = dau.mother().pdgId()
                                        genmotheridx[gcount] = parentidx
                                        genndau[gcount] = dau.numberOfDaughters()

                                        if options.verbose:
                                            print(gene[gcount], genpt[gcount], geneta[gcount], genphi[gcount], genpdg[gcount], genpx[gcount], genpy[gcount], genpz[gcount], genmotherpdg[gcount], genmotheridx[gcount], genndau[gcount])

                                        gcount += 1 


                else:
                    if options.verbose:
                        print ('No top quarks, not filling mttbar')

            #'''
            if options.verbose:
                #print(ngen)
                for a,b,c,d,e,f,g,h,aa,bb,cc in zip( genpt, geneta, genphi, gene, genpx, genpy, genpz, genpdg, genmotheridx, genmotherpdg, genndau):
                    print(a,b,c,d,e,f,g,h,aa,bb,cc)
            #'''

            # Get MC weight
            event.getByLabel( genInfoLabel, genInfo )
            genWeight = genInfo.product().weight()
            evWeight *= genWeight

        ## __________.__             ____   ____      .__
        ## \______   \  |__   ____   \   \ /   /____  |  |  __ __   ____
        ##  |       _/  |  \ /  _ \   \   Y   /\__  \ |  | |  |  \_/ __ \
        ##  |    |   \   Y  (  <_> )   \     /  / __ \|  |_|  |  /\  ___/
        ##  |____|_  /___|  /\____/     \___/  (____  /____/____/  \___  >
        ##         \/     \/                        \/                 \/
        #print("E")
        event.getByLabel(rhoLabel, rhos)
        # Rhos
        if len(rhos.product()) == 0:
            print ("Event has no rho values.")
            return
        else:
            rho = rhos.product()[0]
            if options.verbose:
                print ('rho = {0:6.2f}'.format( rho ))


        ## ____   ____             __                    _________      .__                 __  .__
        ## \   \ /   /____________/  |_  ____ ___  ___  /   _____/ ____ |  |   ____   _____/  |_|__| ____   ____
        ##  \   Y   // __ \_  __ \   __\/ __ \\  \/  /  \_____  \_/ __ \|  | _/ __ \_/ ___\   __\  |/  _ \ /    \
        ##   \     /\  ___/|  | \/|  | \  ___/ >    <   /        \  ___/|  |_\  ___/\  \___|  | |  (  <_> )   |  \
        ##    \___/  \___  >__|   |__|  \___  >__/\_ \ /_______  /\___  >____/\___  >\___  >__| |__|\____/|___|  /
        ##               \/                 \/      \/         \/     \/          \/     \/                    \/



        #print("D")

        event.getByLabel(vertexLabel, vertices)
        # Vertices
        NPV = len(vertices.product())
        if len(vertices.product()) == 0 or vertices.product()[0].ndof() < 4:
            if options.verbose:
            #if 1:
                print ("Event has no good primary vertex.")
            vertexX[0] = -999
            vertexY[0] = -999
            vertexZ[0] = -999
            return
        else:
            PV = vertices.product()[0]
            vertexX[0] = PV.x()
            vertexY[0] = PV.y()
            vertexZ[0] = PV.z()
        if options.verbose:
            print ("PV at x,y,z = %+5.3f, %+5.3f, %+6.3f (ndof %.1f)" % (PV.x(), PV.y(), PV.z(), PV.ndof()))


        #exit()
        ##      ____.       __      _________      .__                 __  .__
        ##     |    | _____/  |_   /   _____/ ____ |  |   ____   _____/  |_|__| ____   ____

        ##     |    |/ __ \   __\  \_____  \_/ __ \|  | _/ __ \_/ ___\   __\  |/  _ \ /    \
        ## /\__|    \  ___/|  |    /        \  ___/|  |_\  ___/\  \___|  | |  (  <_> )   |  \
        ## \________|\___  >__|   /_______  /\___  >____/\___  >\___  >__| |__|\____/|___|  /
        ##               \/               \/     \/          \/     \/                    \/

        #
        # In addition, we must perform "lepton-jet" cleaning.
        # This is because the PF leptons are actually counted in the
        # list of particles sent to the jet clustering.
        # Therefore, we need to loop over the jet constituents and
        # remove the lepton.
        #
        # Jet info
        # https://twiki.cern.ch/twiki/bin/view/CMS/TopJME#Jets_AN2
        # Jet selection
        # https://twiki.cern.ch/twiki/bin/view/CMS/TTbarXSecSynchronization

        # use getByLabel, just like in cmsRun
        event.getByLabel (jetLabel, jets)          # For b-tagging

        # loop over jets and fill hists
        ijet = 0

        # These will hold all of the jets we need for the selection
        ak4JetsGood = []
        ak4JetsGoodP4 = []
        ak4JetsGoodSysts = []

        # For selecting leptons, look at 2-d cut of dRMin, ptRel of
        # lepton and nearest jet that has pt > 30 GeV
        dRMin = 9999.0
        inearestJet = -1    # Index of nearest jet
        nearestJet = None   # Nearest jet


        ############################################
        # Get the AK4 jet nearest the lepton:
        ############################################
        njets2write = 0
        for i,jet in enumerate(jets.product()):
            # Get the jet p4
            jetP4Raw = ROOT.TLorentzVector( jet.px(), jet.py(), jet.pz(), jet.energy() )
            # Get the correction that was applied at RECO level for MINIADO
            jetJECFromMiniAOD = jet.jecFactor(0)
            # Remove the old JEC's to get raw energy
            jetP4Raw *= jetJECFromMiniAOD
            # Apply jet ID
            nhf = jet.neutralHadronEnergy() / jetP4Raw.E()
            nef = jet.neutralEmEnergy() / jetP4Raw.E()
            chf = jet.chargedHadronEnergy() / jetP4Raw.E()
            cef = jet.chargedEmEnergy() / jetP4Raw.E()
            nconstituents = jet.numberOfDaughters()
            nch = jet.chargedMultiplicity()

            # Do some simple checks for the data
            goodJet = \
              nhf < 0.99 and \
              nef < 0.99 and \
              chf > 0.00 and \
              cef < 0.99 and \
              nconstituents > 1 and \
              nch > 0

            if goodJet:
                if njets2write<16:

                    ##############################
                    # Apply new JEC's
                    ##############################
                    if options.isMC:
                        (newJEC, corrDn, corrUp) = getJEC(jecAK4, jecUncAK4, jetP4Raw, jet.jetArea(), rho, NPV)
                    else:
                        (newJEC, corrDn, corrUp) = getJEC(DataJECs.jecAK4(runnumber), DataJECs.jecUncAK4(runnumber), jetP4Raw, jet.jetArea(), rho, NPV)

                    # If MC, get jet energy resolution
                    ptsmear   = 1.0
                    ptsmearUp = 1.0
                    ptsmearDn = 1.0
                    if options.isMC:
                        # ---------------------------------------
                        # JER
                        # ---------------------------------------
                        eta = jetP4Raw.Eta()
                        if eta>=5.0:
                            eta=4.999
                        if eta<=-5.0:
                            eta=-4.999
                        smear     = getJER( eta,  0)
                        smearUp   = getJER( eta,  1)
                        smearDn   = getJER( eta, -1)
                        #print "HERE WE ARE!!!!!!!!!!!"
                        #print jetP4Raw.Perp()
                        #print newJEC
                        recopt    = jetP4Raw.Perp() * newJEC
                        '''
                        if jet.genJet() != None:
                            genpt     = jet.genJet().pt()
                            deltapt   = (recopt-genpt)*(smear-1.0)
                            deltaptUp = (recopt-genpt)*(smearUp-1.0)
                            deltaptDn = (recopt-genpt)*(smearDn-1.0)
                            ptsmear   = max(0.0, (recopt+deltapt)/recopt)
                            ptsmearUp = max(0.0, (recopt+deltaptUp)/recopt)
                            ptsmearDn = max(0.0, (recopt+deltaptDn)/recopt)
                        '''
                    #print(newJEC,ptsmear)
                    #print("UNCORR: ",jetP4Raw.Pt(), jetP4Raw.E(), jetP4Raw.Px(), jetP4Raw.Py(), jetP4Raw.Pz())
                    jetP4 = jetP4Raw * newJEC * ptsmear
                    #print("UN    : ",jetP4.Pt(), jetP4.E(), jetP4.Px(), jetP4.Py(), jetP4.Pz())

                    i = njets2write

                    # Uncorrected
                    #jetpt[i] = jet.pt()
                    #jeteta[i] = jet.eta()
                    #jetphi[i] = jet.phi()
                    #jete[i] = jet.energy()
                    #jetpx[i] = jet.px()
                    #jetpy[i] = jet.py()
                    #jetpz[i] = jet.pz()

                    jetjec[i] = newJEC

                    # Corrected
                    jetpt[i] = jetP4.Pt()
                    jeteta[i] = jetP4.Eta()
                    jetphi[i] = jetP4.Phi()
                    jete[i] = jetP4.E()
                    jetpx[i] = jetP4.Px()
                    jetpy[i] = jetP4.Py()
                    jetpz[i] = jetP4.Pz()

                    jetbtag[i] = jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")
                    jetarea[i] = jet.jetArea()
                    #print(jetarea[i])
                    # Do the loose flag.
                    jetNHF[i] = jet.neutralHadronEnergyFraction();
                    jetNEMF[i] = jet.neutralEmEnergyFraction();
                    jetCHF[i] = jet.chargedHadronEnergyFraction();
                    jetMUF[i] = jet.muonEnergyFraction();
                    jetCEMF[i] = jet.chargedEmEnergyFraction();
                    jetNumConst[i] = jet.chargedMultiplicity()+jet.neutralMultiplicity();
                    jetNumNeutralParticles[i] =jet.neutralMultiplicity();
                    jetCHM[i] = jet.chargedMultiplicity(); 

                    njets2write += 1



            if not goodJet:
                if options.verbose:
                    print ('bad jet pt = {0:6.2f}, y = {1:6.2f}, phi = {2:6.2f}, m = {3:6.2f}, bdisc = {4:6.2f}'.format (
                        jetP4Raw.Perp(), jetP4Raw.Rapidity(), jetP4Raw.Phi(), jetP4Raw.M(), jet.bDiscriminator( options.bdisc )
                        ))
                continue



            if options.verbose:
                print ('raw jet pt = {0:6.2f}, y = {1:6.2f}, phi = {2:6.2f}, m = {3:6.2f}, bdisc = {4:6.2f}'.format (
                    jetP4Raw.Perp(), jetP4Raw.Rapidity(), jetP4Raw.Phi(), jetP4Raw.M(), jet.bDiscriminator( options.bdisc )
                    ))


            # Remove the lepton from the list of constituents for lepton/jet cleaning
            # Speed up computation, only do this for DR < 0.6


        # OUR STUFF
        njet[0] = njets2write


        ########### MUONS ##################
        event.getByLabel( muonLabel, muons )
        nmuons2write = 0
        if len(muons.product()) > 0:
            for i,muon in enumerate( muons.product() ):
                #if muon.pt() > options.minMuonPt and abs(muon.eta()) < options.maxMuonEta and muon.isMediumMuon():
                if i<16: # This is because we are only storing 16 muons at a time
                   muonpt[i] = muon.pt()
                   muoneta[i] = muon.eta()
                   muonphi[i] = muon.phi()
                   muone[i] = muon.energy()
                   muonq[i] = muon.charge()
                   muonpx[i] = muon.px()
                   muonpy[i] = muon.py()
                   muonpz[i] = muon.pz()
                   #pfi  = muon.pfIsolationR03()
                   pfi  = muon.pfIsolationR04()
                   #print( pfi.sumChargedHadronPt, pfi.sumChargedParticlePt, pfi.sumNeutralHadronEt, pfi.sumPhotonEt, pfi.sumNeutralHadronEtHighThreshold, pfi.sumPhotonEtHighThreshold, pfi.sumPUPt)
                   muonsumchhadpt[i] = pfi.sumChargedHadronPt
                   muonsumnhadpt[i] = pfi.sumNeutralHadronEt
                   muonsumphotEt[i] = pfi.sumPhotonEt
                   muonsumPUPt[i] = pfi.sumPUPt
                   muonisLoose[i] = int(muon.isLooseMuon())
                   muonisMedium[i] = int(muon.isMediumMuon())

                   #(mu->pfIsolationR04().sumChargedHadronPt + max(0., mu->pfIsolationR04().sumNeutralHadronEt + mu->pfIsolationR04().sumPhotonEt - 0.5*mu->pfIsolationR04().sumPUPt))/mu->pt()

                   muonPFiso[i] = (muonsumchhadpt[i] + max(0., muonsumnhadpt[i] + muonsumphotEt[i] - 0.5*muonsumPUPt[i]))/muonpt[i]
                   nmuons2write += 1


        nmuon[0] = nmuons2write



        ##############################################################
        # Electrons
        ##############################################################
        #selectElectron = VIDElectronSelector(cutBasedElectronID_Summer16_80X_V1_loose)
        # Do we need this? Got this from...
        # https://github.com/ikrav/EgammaWork/blob/ntupler_and_VID_demos_7.4.12/FWLiteExamples/bin/FWLiteVIDElectronsDemo_cfg.py
        event.getByLabel( electronLabel, electrons )

        # Referencing
        # https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2
        # https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2#Working_points_for_2016_data_for
        # For when we look at 2017
        # https://twiki.cern.ch/twiki/bin/view/CMS/Egamma2017DataRecommendations
        #
        # Also look here
        # https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideCMSDataAnalysisSchoolLPC2018egamma
        # https://indico.cern.ch/event/662371/contributions/2704697/attachments/1514547/2496142/ShortExercise1.pdf
        # https://indico.cern.ch/event/662371/contributions/2704714/attachments/1514558/2496227/ShortExercise2.pdf
        # Do something like this for isolation?
        # https://twiki.cern.ch/twiki/bin/view/CMS/EgammaPFBasedIsolationRun2#Recipe_for_accessing_PF_isolatio




        ########### ELECTRONS ##################
        event.getByLabel( electronLabel, electrons )
        nelectrons2write = 0
        if len(electrons.product()) > 0:
            for i,electron in enumerate( electrons.product() ):


                #print("Here! ----  A")
                passSelection = selectElectron( electron, event )
                #print(passSelection,type(passSelection))
                #print("Here! ----  B")
                if passSelection and i<16: # we're only keeping 16 electrons
                   electronpt[i] = electron.pt()
                   electroneta[i] = electron.eta()
                   electronphi[i] = electron.phi()
                   electrone[i] = electron.energy()
                   electronq[i] = electron.charge()
                   electronpx[i] = electron.px()
                   electronpy[i] = electron.py()
                   electronpz[i] = electron.pz()
                   electronTkIso[i] = electron.dr03TkSumPt()
                   electronHCIso[i] = electron.dr03HcalTowerSumEt()
                   electronECIso[i] = electron.dr03EcalRecHitSumEt()

                   nelectrons2write += 1


        nelectron[0] = nelectrons2write

        #######################################################################
        # MET, Missing energy in transverse plane
        # https://indico.cern.ch/event/662371/contributions/2823187/attachments/1574267/2496977/PileupMET_DAS2018LPC.pdf
        # https://indico.cern.ch/event/662371/timetable/
        # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideCMSDataAnalysisSchoolLPC2018METandPileupExercise
        # SHOULD GO THROUGH THE EXERCISE! DO WE CORRECT? OR USE PUPPI????
        #######################################################################
        event.getByLabel( metLabel, mets )
        #met = mets.product()[0]
        met = mets.product().front()
        metpt[0] = met.pt()
        metphi[0] = met.phi()
        mete[0] = met.energy()
        meteta[0] = met.eta()
        #print("MET pt/phi: %f %f" % (metpt[0],metphi[0]))


        ## ___________.__.__  .__    ___________
        ## \_   _____/|__|  | |  |   \__    ___/______   ____   ____
        ##  |    __)  |  |  | |  |     |    |  \_  __ \_/ __ \_/ __ \
        ##  |     \   |  |  |_|  |__   |    |   |  | \/\  ___/\  ___/
        ##  \___  /   |__|____/____/   |____|   |__|    \___  >\___  >
        ##      \/                                          \/     \/
        outtree.Fill()

        return genOut



    #########################################
    # Main event loop

    #genoutputfile = open("generator_information.dat",'w')
    nevents = 0
    maxevents = int(options.maxevents)
    for ifile in getInputFiles(options):
        print ('Processing file ' + ifile)
        events = Events (ifile)
        if maxevents > 0 and nevents > maxevents:
            break

        # loop over events in this file
        print('Tot events in this file: ' + str(events.size()))
        for iev, event in enumerate(events):
            #print(iev)

            if maxevents > 0 and nevents > maxevents:
                break
            nevents += 1

            #if nevents % 1000 == 0:
            if nevents % 100 == 0:
                print ('===============================================')
                print ('    ---> Event ' + str(nevents))
            elif options.verbose:
                print ('    ---> Event ' + str(nevents))

            genOut = processEvent(iev, events)
            #print type(genOut)
            #print genOut
            #if genOut is not None:
                #genoutputfile.write(genOut)

    outtree.Print()
    # Close the output ROOT file
    f.cd()
    f.Write()
    f.Close()

    #genoutputfile.close()
    


#####################################################################################
if __name__ == "__main__":
    topbnv_fwlite(sys.argv)



