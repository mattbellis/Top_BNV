# Much of this is from the B2G data analysis school code

import ROOT, copy, sys, logging
from array import array
from DataFormats.FWLite import Events, Handle
# Use the VID framework for the electron ID. Tight ID without the PF isolation cut.
from RecoEgamma.ElectronIdentification.VIDElectronSelector import VIDElectronSelector
#from RecoEgamma.ElectronIdentification.Identification.VersionedGsfElectronSelector import VersionedGsfElectronSelector
from RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_25ns_V1_cff import cutBasedElectronID_Spring15_25ns_V1_standalone_tight
from RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_nonTrig_V1_cff import mvaEleID_Spring15_25ns_nonTrig_V1_wp80
# Cut-based...we should use this!
# https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2#Recipe80X
from RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff import cutBasedElectronID_Summer16_80X_V1_loose 
#import RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff.cutBasedElectronID-Summer16-80X-V1-loose as electron_loose
#import RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff.cutBasedElectronID-Summer16-80X-V1-medium as electron_medium
#import RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff.cutBasedElectronID-Summer16-80X-V1-tight as electron_tight

############################################
# Jet Energy Corrections / Resolution tools
#
# THESE VALUES ARE ALL FROM THE B2G VERSION AND SO THEY ARE PROBABLY 
# NOT CORRECT FOR WHAT WE'RE DOING!!!!!!!!!!!!!
#

#####################################################################################
#jet_energy_corrections = [ # Values from https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC
#    [1,276811,"Spring16_23Sep2016BCDV2_DATA"],
#    [276831,278801,"Spring16_23Sep2016EFV2_DATA"],
#    [278802,280385,"Spring16_23Sep2016GV2_DATA"],
#    [280386,float("inf"),"Spring16_23Sep2016HV2_DATA"]
#]

#jet_energy_corrections = "Summer16_23Sep2016V4_MC"
jet_energy_corrections = [ [1,276811,"Summer16_23Sep2016V4"], 
[276831,278801,"Summer16_23Sep2016V4"], 
[278802,280385,"Summer16_23Sep2016V4"], 
[280919,float("inf"),"Summer16_23Sep2016V4"] ] 

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
    log = logging.getLogger('JEC')
    log.info('Getting jet energy corrections for %s jets', jetAlgo)
    jecParameterList = ROOT.vector('JetCorrectorParameters')()
    # Load the different JEC levels (the order matters!)
    for jecLevel in jecLevelList:
        log.debug('  - %s jet corrections', jecLevel)
        jecParameter = ROOT.JetCorrectorParameters('%s_%s_%s.txt' % (jecSrc, jecLevel, jetAlgo));
        #print jecParameter
        jecParameterList.push_back(jecParameter)
    # Chain the JEC levels together
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
    add_option('isCrabRun',          default=False, action='store_true',
        help='Use this flag when running with crab on the grid')
    add_option('localInputFiles',    default=False, action='store_true',
        help='Use this flag when running with with local files')

    add_option('trigProc',           default='HLT',
        help='Name of trigger process')
    add_option('trigProcMETFilters', default='PAT',
        help='Name of trigger process for MET filters')


    add_option('disableTree',        default=False, action='store_true',
        help='Disable Tree creation')
    add_option('disablePileup',      default=False, action='store_true',
        help='Disable pileup reweighting')
    add_option('isData',             default=False, action='store_true',
        help='Enable processing as data')

    add_option('bdisc',              default='pfCombinedInclusiveSecondaryVertexV2BJetTags',
        help='Name of b jet discriminator')
    add_option('bdiscMin',           default=0.5426, type='float',
        help='Minimum b discriminator')
    add_option('minMuonPt',          default=45.,   type='float',
        help='Minimum PT for muons')
    add_option('maxMuonEta',         default=2.4,   type='float',
        help='Maximum muon pseudorapidity')
    add_option('minElectronPt',      default=45.,   type='float',
        help='Minimum PT for electrons')
    add_option('maxElectronEta',     default=2.5,   type='float',
        help='Maximum electron pseudorapidity')
    add_option('minAK4Pt',           default=30.,   type='float',
        help='Minimum PT for AK4 jets')
    add_option('maxAK4Rapidity',     default=2.4,   type='float',
        help='Maximum AK4 rapidity')
    add_option('minAK8Pt',           default=170.,  type='float',
        help='Minimum PT for AK8 jets')
    add_option('maxAK8Rapidity',     default=2.4,   type='float',
        help='Maximum AK8 rapidity')


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
            lfn = lfn.strip()
            if lfn:
                if not options.isCrabRun:
                    if options.localInputFiles:
                        pfn = lfn
                    else:
                        #pfn = 'file:/pnfs/desy.de/cms/tier2/' + lfn
                        pfn = 'root://cmsxrootd-site.fnal.gov/' + lfn
                else:
                    #pfn = 'root://cmsxrootd-site.fnal.gov/' + lfn
                    pfn = 'root://xrootd-cms.infn.it/' + lfn
                print ('Adding ' + pfn)
                result.append(pfn)
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

    muons, muonLabel = Handle("std::vector<pat::Muon>"), "slimmedMuons"
    electrons, electronLabel = Handle("std::vector<pat::Electron>"), "slimmedElectrons"
    photons, photonLabel = Handle("std::vector<pat::Photon>"), "slimmedPhotons"
    taus, tauLabel = Handle("std::vector<pat::Tau>"), "slimmedTaus"
    jets, jetLabel = Handle("std::vector<pat::Jet>"), "slimmedJets"
    ak8jets, ak8jetLabel = Handle("std::vector<pat::Jet>"), "slimmedJetsAK8"
    mets, metLabel = Handle("std::vector<pat::MET>"), "slimmedMETs"
    vertices, vertexLabel = Handle("std::vector<reco::Vertex>"), "offlineSlimmedPrimaryVertices"
    pileups, pileuplabel = Handle("std::vector<PileupSummaryInfo>"), "slimmedAddPileupInfo"
    rhos, rhoLabel = Handle("double"), "fixedGridRhoAll"
    gens, genLabel = Handle("std::vector<reco::GenParticle>"), "prunedGenParticles"
    #packedgens, packedgenLabel = Handle("std::vector<reco::packedGenParticle>"), "PACKEDgENpARTICLES"
    packedgens, packedgenLabel = Handle("std::vector<pat::PackedGenParticle>"), "packedGenParticles"
    genInfo, genInfoLabel = Handle("GenEventInfoProduct"), "generator"
    # Enterprising students could figure out the LHE weighting for theoretical uncertainties
    #lheInfo, lheInfoLabel = Handle("LHEEventProduct"), "externalLHEProducer"
    triggerBits, triggerBitLabel = Handle("edm::TriggerResults"), ("TriggerResults","", options.trigProc)
    metfiltBits, metfiltBitLabel = Handle("edm::TriggerResults"), ("TriggerResults","", options.trigProcMETFilters)

    trigsToRun = [
        "HLT_Mu50",
        "HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165",
        "HLT_Ele115_CaloIdVT_GsfTrkIdT",
        # Triggers for the Spring16 Samples running with the wrong HLT
        'HLT_Ele35_CaloIdVT_GsfTrkIdT_PFJet150_PFJet50',
        'HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50',
        'HLT_Ele105_CaloIdVT_GsfTrkIdT',
        'digitisation_step',
        ]


    f = ROOT.TFile(options.output, "RECREATE")
    f.cd()

    #################################################################################
    # Actually to make life easy, we're going to make "N-dimensional histograms" aka Ntuples
    #################################################################################
    if not options.disableTree:
        TreeSemiLept = ROOT.TTree("TreeSemiLept", "TreeSemiLept")

        SemiLeptTrig = ROOT.vector('int')(16) # Maximum of 16 triggers to store? this is at least len(trigsToRun)
        TreeSemiLept.Branch('SemiLeptTrig', "std::vector<int>",  SemiLeptTrig)

        def bookFloatBranch(name, default):
            tmp = array('f', [default])
            TreeSemiLept.Branch(name, tmp, '%s/F' %name)
            return tmp
        def bookIntBranch(name, default):
            tmp = array('i', [default])
            TreeSemiLept.Branch(name, tmp, '%s/I' %name)
            return tmp
        def bookLongIntBranch(name, default):
            tmp = array('l', [default])
            TreeSemiLept.Branch(name, tmp, '%s/L' %name)
            return tmp

        ##### OUR STUFF #####################
        #'''

        # Generated MC
        gendecayflag = array('i', [-1])
        TreeSemiLept.Branch('gendecayflag', gendecayflag, 'gendecayflag/I')
        # 0    t    --> hadronic    
        # 1    t    --> leptonic    
        # 10*0 tbar --> hadronic    
        # 10*1 tbar --> leptonic    

        # Generated MC 4-momentum
        ngen = array('i', [-1])
        TreeSemiLept.Branch('ngen', ngen, 'ngen/I')
        genpt = array('f', 16*[-1.])
        TreeSemiLept.Branch('genpt', genpt, 'genpt[ngen]/F')
        geneta = array('f', 16*[-1.])
        TreeSemiLept.Branch('geneta', geneta, 'geneta[ngen]/F')
        genphi = array('f', 16*[-1.])
        TreeSemiLept.Branch('genphi', genphi, 'genphi[ngen]/F')
        gene = array('f', 16*[-1.])
        TreeSemiLept.Branch('gene', gene, 'gene[ngen]/F')
        genpdg = array('i', 16*[-1])
        TreeSemiLept.Branch('genpdg', genpdg, 'genpdg[ngen]/I')
        # 0 - top quark
        # 1 - b from top quark
        # 2 - W+ from top quark
        # 3 - child1 from W+ (top)
        # 4 - child2 from W+ (top)

        # 5 - anti-top quark
        # 6 - b+ from anti-top quark
        # 7 - W- from anti-top quark
        # 8 - child1 from W- (anti-top)
        # 9 - child2 from W- (anti-top)

        # MET
        metpt = array('f', [-1])
        TreeSemiLept.Branch('metpt', metpt, 'metpt/F')
        metphi = array('f', [-1])
        TreeSemiLept.Branch('metphi', metphi, 'metphi/F')
        mete = array('f', [-1])
        TreeSemiLept.Branch('mete',mete, 'mete/F')
        meteta = array('f',[-1])
        TreeSemiLept.Branch('meteta', meteta, 'meteta/F')

        # Muons
        nmuon = array('i', [-1])
        TreeSemiLept.Branch('nmuon', nmuon, 'nmuon/I')
        muonpt = array('f', 16*[-1.])
        TreeSemiLept.Branch('muonpt', muonpt, 'muonpt[nmuon]/F')
        muoneta = array('f', 16*[-1.])
        TreeSemiLept.Branch('muoneta', muoneta, 'muoneta[nmuon]/F')
        muonphi = array('f', 16*[-1.])
        TreeSemiLept.Branch('muonphi', muonphi, 'muonphi[nmuon]/F')
        muonq = array('f', 16*[-1.])
        TreeSemiLept.Branch('muonq', muonq, 'muonq[nmuon]/F')
        muonpx = array('f', 16*[-1.])
        TreeSemiLept.Branch('muonpx', muonpx, 'muonpx[nmuon]/F')
        muonpy = array('f', 16*[-1.])
        TreeSemiLept.Branch('muonpy', muonpy, 'muonpy[nmuon]/F')
        muonpz = array('f', 16*[-1.])
        TreeSemiLept.Branch('muonpz', muonpz, 'muonpz[nmuon]/F')
        muone = array('f', 16*[-1.])
        TreeSemiLept.Branch('muone', muone, 'muone[nmuon]/F')
        muonsumchhadpt = array('f', 16*[-1.])
        TreeSemiLept.Branch('muonsumchhadpt', muonsumchhadpt, 'muonsumchhadpt[nmuon]/F')
        muonsumnhadpt = array('f', 16*[-1.])
        TreeSemiLept.Branch('muonsumnhadpt', muonsumnhadpt, 'muonsumnhadpt[nmuon]/F')
        muonsumphotEt = array('f', 16*[-1.])
        TreeSemiLept.Branch('muonsumphotEt', muonsumphotEt, 'muonsumphotEt[nmuon]/F')

        # Electrons
        nelectron = array('i', [-1])
        TreeSemiLept.Branch('nelectron', nelectron, 'nelectron/I')
        electronpt = array('f', 16*[-1.])
        TreeSemiLept.Branch('electronpt', electronpt, 'electronpt[nelectron]/F')
        electroneta = array('f', 16*[-1.])
        TreeSemiLept.Branch('electroneta', electroneta, 'electroneta[nelectron]/F')
        electronphi = array('f', 16*[-1.])
        TreeSemiLept.Branch('electronphi', electronphi, 'electronphi[nelectron]/F')
        electronq = array('f', 16*[-1.])
        TreeSemiLept.Branch('electronq', electronq, 'electronq[nelectron]/F')
        electronpx = array('f', 16*[-1.])
        TreeSemiLept.Branch('electronpx', electronpx, 'electronpx[nelectron]/F')
        electronpy = array('f', 16*[-1.])
        TreeSemiLept.Branch('electronpy', electronpy, 'electronpy[nelectron]/F')
        electronpz = array('f', 16*[-1.])
        TreeSemiLept.Branch('electronpz', electronpz, 'electronpz[nelectron]/F')
        electrone = array('f', 16*[-1.])
        TreeSemiLept.Branch('electrone', electrone, 'electrone[nelectron]/F')
	electronTkIso = array('f',16*[-1.])
    	TreeSemiLept.Branch('electronTkIso', electronTkIso, 'electronTkIso[nelectron]/F')
    	electronHCIso = array('f',16*[-1.])
    	TreeSemiLept.Branch('electronHCIso', electronHCIso, 'electronHCIso[nelectron]/F')
    	electronECIso = array('f',16*[-1.])
    	TreeSemiLept.Branch('electronECIso', electronECIso, 'electronECIso[nelectron]/F')

        #electronchiso = array('f', 16*[-1.])
        #TreeSemiLept.Branch('electronchiso', electronchiso, 'electronchiso[nelectron]/F')
        #electronnhiso = array('f', 16*[-1.])
        #TreeSemiLept.Branch('electronnhiso', electronnhiso, 'electronnhiso[nelectron]/F')
        #electronphotiso = array('f', 16*[-1.])
        #TreeSemiLept.Branch('electronphotiso', electronphotiso, 'electronphotiso[nelectron]/F')
        # Electrons before corrections are applied
        #nprecorrelectron = array('i', [-1])
        #TreeSemiLept.Branch('nprecorrelectron', nprecorrelectron, 'nprecorrelectron/I')
        #precorrelectronpt = array('f', 16*[-1.])
        #TreeSemiLept.Branch('precorrelectronpt', precorrelectronpt, 'precorrelectronpt[nprecorrelectron]/F')
        #precorrelectroneta = array('f', 16*[-1.])
        #TreeSemiLept.Branch('precorrelectroneta', precorrelectroneta, 'precorrelectroneta[nprecorrelectron]/F')
        #precorrelectronphi = array('f', 16*[-1.])
        #TreeSemiLept.Branch('precorrelectronphi', precorrelectronphi, 'precorrelectronphi[nprecorrelectron]/F')
        #precorrelectrone = array('f', 16*[-1.])
        #TreeSemiLept.Branch('precorrelectrone', precorrelectrone, 'precorrelectrone[nprecorrelectron]/F')

        # Jets
        njet = array('i', [-1])
        TreeSemiLept.Branch('njet', njet, 'njet/I')

        jetpt = array('f', 16*[-1.])
        TreeSemiLept.Branch('jetpt', jetpt, 'jetpt[njet]/F')
        jeteta = array('f', 16*[-1.])
        TreeSemiLept.Branch('jeteta', jeteta, 'jeteta[njet]/F')
        jetphi = array('f', 16*[-1.])
        TreeSemiLept.Branch('jetphi', jetphi, 'jetphi[njet]/F')
        jetpx = array('f', 16*[-1.])
        TreeSemiLept.Branch('jetpx', jetpx, 'jetpx[njet]/F')
        jetpy = array('f', 16*[-1.])
        TreeSemiLept.Branch('jetpy', jetpy, 'jetpy[njet]/F')
        jetpz = array('f', 16*[-1.])
        TreeSemiLept.Branch('jetpz', jetpz, 'jetpz[njet]/F')
        jete = array('f', 16*[-1.])
        TreeSemiLept.Branch('jete', jete, 'jete[njet]/F')

        jetjecpt = array('f', 16*[-1.])
        TreeSemiLept.Branch('jetjecpt', jetjecpt, 'jetjecpt[njet]/F')
        jetjeceta = array('f', 16*[-1.])
        TreeSemiLept.Branch('jetjeceta', jetjeceta, 'jetjeceta[njet]/F')
        jetjecphi = array('f', 16*[-1.])
        TreeSemiLept.Branch('jetjecphi', jetjecphi, 'jetjecphi[njet]/F')
        jetjecpx = array('f', 16*[-1.])
        TreeSemiLept.Branch('jetjecpx', jetjecpx, 'jetjecpx[njet]/F')
        jetjecpy = array('f', 16*[-1.])
        TreeSemiLept.Branch('jetjecpy', jetjecpy, 'jetjecpy[njet]/F')
        jetjecpz = array('f', 16*[-1.])
        TreeSemiLept.Branch('jetjecpz', jetjecpz, 'jetjecpz[njet]/F')
        jetjece = array('f', 16*[-1.])
        TreeSemiLept.Branch('jetjece', jetjece, 'jetjece[njet]/F')

        #'''
        jetbtag = array('f', 16*[-1.])
        TreeSemiLept.Branch('jetbtag', jetbtag, 'jetbtag[njet]/F')

        jetNHF = array('f', 16*[-1.])
        TreeSemiLept.Branch('jetNHF', jetNHF, 'jetNHF[njet]/F')
        jetNEMF = array('f', 16*[-1.])
        TreeSemiLept.Branch('jetNEMF', jetNEMF, 'jetNEMF[njet]/F')
        jetCHF = array('f', 16*[-1.])
        TreeSemiLept.Branch('jetCHF', jetCHF, 'jetCHF[njet]/F')
        jetMUF = array('f', 16*[-1.])
        TreeSemiLept.Branch('jetMUF', jetMUF, 'jetMUF[njet]/F')
        jetCEMF = array('f', 16*[-1.])
        TreeSemiLept.Branch('jetCEMF', jetCEMF, 'jetCEMF[njet]/F')
        jetNumConst = array('f', 16*[-1.])
        TreeSemiLept.Branch('jetNumConst', jetNumConst, 'jetNumConst[njet]/F')
        jetNumNeutralParticles = array('f', 16*[-1.])
        TreeSemiLept.Branch('jetNumNeutralParticles', jetNumNeutralParticles, 'jetNumNeutralParticles[njet]/F')
        jetCHM = array('f', 16*[-1.])
        TreeSemiLept.Branch('jetCHM', jetCHM, 'jetCHM[njet]/F')



        # Vertex stuff
        vertexX = array('f',[-1.])
        TreeSemiLept.Branch('vertexX', vertexX, 'vertexX/F')
        vertexY = array('f',[-1.])
        TreeSemiLept.Branch('vertexY', vertexY, 'vertexY/F')
        vertexZ = array('f',[-1.])
        TreeSemiLept.Branch('vertexZ', vertexZ, 'vertexZ/F')





        '''
        pats = ["muon"]
        attributes = ["n","pt","eta","phi","px","py","pz","e"]
        nmuon = array('i',[-1])
        muonpt = array('f',16*[-1])
        muoneta = array('f',16*[-1])
        muonphi = array('f',16*[-1])
        muonpx = array('f',16*[-1])
        muonpy = array('f',16*[-1])
        muonpz = array('f',16*[-1])
        muone = array('f',16*[-1])
        elements = [nmuon,muonpt,muoneta,muonphi,muonpx,muonpy,muonpz,muone] 
        for i,pat in enumerate(pats):
            numbername = 0
            for j,(element,attribute) in enumerate(zip(elements,attributes)):
                if j==0:
                    numbername = "%s%s" % (attribute,pat)
                    branchID = "%s/I" % (numbername)
                    element = array('i',[-1])
                    TreeSemiLept.Branch(numbername, element, branchID)
                else:
                    branchname = "%s%s" % (pat,attribute)
                    branchID = "%s[%s]/F" % (branchname,numbername)
                    element = array('f',16*[-1])
                    TreeSemiLept.Branch(branchname, element, branchID)

        for e in elements:
            print(e,type(e))
        '''





        

        # Event weights
        GenWeight             = bookFloatBranch('GenWeight', 0.)
        PUWeight              = bookFloatBranch('PUWeight', 0.)
        MuonTrkWeight         = bookFloatBranch('MuonTrkWeight', 0.)
        MuonTrkWeightUnc      = bookFloatBranch('MuonTrkWeightUnc', 0.)
        # Fat jet properties
        FatJetBDisc           = bookFloatBranch('FatJetBDisc', -1.)
        FatJetDeltaPhiLep     = bookFloatBranch('FatJetDeltaPhiLep', -1.)
        FatJetEnergy          = bookFloatBranch('FatJetEnergy', -1.)
        FatJetEta             = bookFloatBranch('FatJetEta', -1.)
        FatJetJECDnSys        = bookFloatBranch('FatJetJECDnSys', -1.)
        FatJetJECUpSys        = bookFloatBranch('FatJetJECUpSys', -1.)
        FatJetJERDnSys        = bookFloatBranch('FatJetJERDnSys', -1.)
        FatJetJERUpSys        = bookFloatBranch('FatJetJERUpSys', -1.)
        FatJetMass            = bookFloatBranch('FatJetMass', -1.)
        FatJetMassSoftDrop    = bookFloatBranch('FatJetMassSoftDrop', -1.)
        FatJetPhi             = bookFloatBranch('FatJetPhi', -1.)
        FatJetPt              = bookFloatBranch('FatJetPt', -1.)
        FatJetRap             = bookFloatBranch('FatJetRap', -1.)
        FatJetSDBDiscB        = bookFloatBranch('FatJetSDBDiscB', -1.)
        FatJetSDBDiscW        = bookFloatBranch('FatJetSDBDiscW', -1.)
        FatJetSDsubjetBmass   = bookFloatBranch('FatJetSDsubjetBmass', -1.)
        FatJetSDsubjetBpt     = bookFloatBranch('FatJetSDsubjetBpt', -1.)
        FatJetSDsubjetWmass   = bookFloatBranch('FatJetSDsubjetWmass', -1.)
        FatJetSDsubjetWpt     = bookFloatBranch('FatJetSDsubjetWpt', -1.)
        FatJetTau21           = bookFloatBranch('FatJetTau21', -1.)
        FatJetTau32           = bookFloatBranch('FatJetTau32', -1.)
        # Lepton properties
        LeptonDRMin           = bookFloatBranch('LeptonDRMin', -1.)
        LeptonEnergy          = bookFloatBranch('LeptonEnergy', -1.)
        LeptonEta             = bookFloatBranch('LeptonEta', -1.)
        LeptonIDWeight        = bookFloatBranch('LeptonIDWeight', 0.)
        LeptonIDWeightUnc     = bookFloatBranch('LeptonIDWeightUnc', 0.)
        LeptonIso             = bookFloatBranch('LeptonIso', -1.)
        LeptonPhi             = bookFloatBranch('LeptonPhi', -1.)
        LeptonPt              = bookFloatBranch('LeptonPt', -1.)
        LeptonPtRel           = bookFloatBranch('LeptonPtRel', -1.)
        LeptonType            = bookIntBranch('LeptonType', -1)
        # Nearest AK4 Jet properties
        NearestAK4JetBDisc    = bookFloatBranch('NearestAK4JetBDisc', -1.)
        NearestAK4JetEta      = bookFloatBranch('NearestAK4JetEta', -1.)
        NearestAK4JetJECDnSys = bookFloatBranch('NearestAK4JetJECDnSys', -1.)
        NearestAK4JetJECUpSys = bookFloatBranch('NearestAK4JetJECUpSys', -1.)
        NearestAK4JetJERDnSys = bookFloatBranch('NearestAK4JetJERDnSys', -1.)
        NearestAK4JetJERUpSys = bookFloatBranch('NearestAK4JetJERUpSys', -1.)
        NearestAK4JetMass     = bookFloatBranch('NearestAK4JetMass', -1.)
        NearestAK4JetPhi      = bookFloatBranch('NearestAK4JetPhi', -1.)
        NearestAK4JetPt       = bookFloatBranch('NearestAK4JetPt', -1.)
        # Semi leptonic event properties
        SemiLepMETe           = bookFloatBranch('SemiLepMETe', -1.)
        SemiLepMETeta         = bookFloatBranch('SemiLepMETeta', -1.)
        SemiLepMETphi         = bookFloatBranch('SemiLepMETphi', -1.)
        SemiLepMETpt          = bookFloatBranch('SemiLepMETpt', -1.)
        SemiLepNvtx           = bookIntBranch('SemiLepNvtx', -1)
        SemiLeptWeight        = bookFloatBranch('SemiLeptWeight', 0.)
        # Event information
        SemiLeptEventNum      = bookLongIntBranch('SemiLeptEventNum', -1)
        SemiLeptLumiNum       = bookIntBranch('SemiLeptLumiNum', -1)
        SemiLeptRunNum        = bookIntBranch('SemiLeptRunNum', -1)

        ###### OUR STUFF #######
        #muonpt = bookFloatBranch('muonpt',-999)



    # and also make a few 1-d histograms
    '''
    h_mttbar = ROOT.TH1F("h_mttbar", ";m_{t#bar{t}} (GeV)", 200, 0, 6000)
    h_mttbar_true = ROOT.TH1F("h_mttbar_true", "True m_{t#bar{t}};m_{t#bar{t}} (GeV)", 200, 0, 6000)

    h_ptLep = ROOT.TH1F("h_ptLep", "Lepton p_{T};p_{T} (GeV)", 100, 0, 1000)
    h_etaLep = ROOT.TH1F("h_etaLep", "Lepton #eta;#eta", 120, -6, 6 )
    h_met = ROOT.TH1F("h_met", "Missing p_{T};p_{T} (GeV)", 100, 0, 1000)
    h_ptRel = ROOT.TH1F("h_ptRel", "p_{T}^{REL};p_{T}^{REL} (GeV)", 100, 0, 100)
    h_dRMin = ROOT.TH1F("h_dRMin", "#Delta R_{MIN};#Delta R_{MIN}", 100, 0, 5.0)
    h_2DCut = ROOT.TH2F("h_2DCut", "2D Cut;#Delta R;p_{T}^{REL}", 20, 0, 5.0, 20, 0, 100 )

    h_ptAK4 = ROOT.TH1F("h_ptAK4", "AK4 Jet p_{T};p_{T} (GeV)", 300, 0, 3000)
    h_etaAK4 = ROOT.TH1F("h_etaAK4", "AK4 Jet #eta;#eta", 120, -6, 6)
    h_yAK4 = ROOT.TH1F("h_yAK4", "AK4 Jet Rapidity;y", 120, -6, 6)
    h_phiAK4 = ROOT.TH1F("h_phiAK4", "AK4 Jet #phi;#phi (radians)",100,-ROOT.Math.Pi(),ROOT.Math.Pi())
    h_mAK4 = ROOT.TH1F("h_mAK4", "AK4 Jet Mass;Mass (GeV)", 100, 0, 1000)
    h_BDiscAK4 = ROOT.TH1F("h_BDiscAK4", "AK4 b discriminator;b discriminator", 100, 0, 1.0)

    h_ptAK8 = ROOT.TH1F("h_ptAK8", "AK8 Jet p_{T};p_{T} (GeV)", 300, 0, 3000)
    h_etaAK8 = ROOT.TH1F("h_etaAK8", "AK8 Jet #eta;#eta", 120, -6, 6)
    h_yAK8 = ROOT.TH1F("h_yAK8", "AK8 Jet Rapidity;y", 120, -6, 6)
    h_phiAK8 = ROOT.TH1F("h_phiAK8", "AK8 Jet #phi;#phi (radians)",100,-ROOT.Math.Pi(),ROOT.Math.Pi())
    h_mAK8 = ROOT.TH1F("h_mAK8", "AK8 Jet Mass;Mass (GeV)", 100, 0, 1000)
    h_msoftdropAK8 = ROOT.TH1F("h_msoftdropAK8", "AK8 Softdrop Jet Mass;Mass (GeV)", 100, 0, 1000)
    h_mprunedAK8 = ROOT.TH1F("h_mprunedAK8", "AK8 Pruned Jet Mass;Mass (GeV)", 100, 0, 1000)
    #h_mfilteredAK8 = ROOT.TH1F("h_mfilteredAK8", "AK8 Filtered Jet Mass;Mass (GeV)", 100, 0, 1000)
    #h_mtrimmedAK8 = ROOT.TH1F("h_mtrimmedAK8", "AK8 Trimmed Jet Mass;Mass (GeV)", 100, 0, 1000)
    h_minmassAK8 = ROOT.TH1F("h_minmassAK8", "AK8 CMS Top Tagger Min Mass Paring;m_{min} (GeV)", 100, 0, 1000)
    h_nsjAK8 = ROOT.TH1F("h_nsjAK8", "AK8 CMS Top Tagger N_{subjets};N_{subjets}", 5, 0, 5)
    h_tau21AK8 = ROOT.TH1F("h_tau21AK8", "AK8 Jet #tau_{2} / #tau_{1};Mass#tau_{21}", 100, 0, 1.0)
    h_tau32AK8 = ROOT.TH1F("h_tau32AK8", "AK8 Jet #tau_{3} / #tau_{2};Mass#tau_{32}", 100, 0, 1.0)
    '''

    ##      ____.       __    _________                                     __  .__
    ##     |    | _____/  |_  \_   ___ \  __________________   ____   _____/  |_|__| ____   ____   ______
    ##     |    |/ __ \   __\ /    \  \/ /  _ \_  __ \_  __ \_/ __ \_/ ___\   __\  |/  _ \ /    \ /  ___/
    ## /\__|    \  ___/|  |   \     \___(  <_> )  | \/|  | \/\  ___/\  \___|  | |  (  <_> )   |  \\___ \
    ## \________|\___  >__|    \______  /\____/|__|   |__|    \___  >\___  >__| |__|\____/|___|  /____  >
    ##               \/               \/                          \/     \/                    \/     \/
    ROOT.gSystem.Load('libCondFormatsJetMETObjects')
    if options.isData:
        # CHANGE THIS FOR DATA
        DataJECs = DataJEC(jet_energy_corrections)
    else:
        # CHANGE THIS FOR DIFFERENT MCs down the road
        jecAK4 = createJEC('JECs/Summer/Summer16_23Sep2016V4_MC', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'AK4PFchs')
        jecAK8 = createJEC('JECs/Summer/Summer16_23Sep2016V4_MC', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'AK8PFchs')
        jecUncAK4 = ROOT.JetCorrectionUncertainty(ROOT.std.string('JECs/Summer/Summer16_23Sep2016V4_MC_Uncertainty_AK4PFchs.txt'))
        jecUncAK8 = ROOT.JetCorrectionUncertainty(ROOT.std.string('JECs/Summer/Summer16_23Sep2016V4_MC_Uncertainty_AK8PFchs.txt'))

    print("electron selectors....")
    print(type(mvaEleID_Spring15_25ns_nonTrig_V1_wp80))
    print(type(cutBasedElectronID_Summer16_80X_V1_loose))
    print("this one")
    print(mvaEleID_Spring15_25ns_nonTrig_V1_wp80)
    print(" and then this one")
    print(cutBasedElectronID_Summer16_80X_V1_loose)
    #selectElectron = VIDElectronSelector(mvaEleID_Spring15_25ns_nonTrig_V1_wp80)
    selectElectron = VIDElectronSelector(cutBasedElectronID_Summer16_80X_V1_loose)
    #selectElectron = VersionedGsfElectronSelector(cutBasedElectronID_Summer16_80X_V1_loose)
    #selectElectronvidelectron._VIDSelectorBase__instance.ignoreCut('GsfEleEffAreaPFIsoCut_0')

    ## __________.__.__                        __________                     .__       .__     __  .__
    ## \______   \__|  |   ____  __ ________   \______   \ ______  _  __ ____ |__| ____ |  |___/  |_|__| ____    ____
    ##  |     ___/  |  | _/ __ \|  |  \____ \   |       _// __ \ \/ \/ // __ \|  |/ ___\|  |  \   __\  |/    \  / ___\
    ##  |    |   |  |  |_\  ___/|  |  /  |_> >  |    |   \  ___/\     /\  ___/|  / /_/  >   Y  \  | |  |   |  \/ /_/  >
    ##  |____|   |__|____/\___  >____/|   __/   |____|_  /\___  >\/\_/  \___  >__\___  /|___|  /__| |__|___|  /\___  /
    ##                        \/      |__|             \/     \/            \/  /_____/      \/             \//_____/
    # Obtained on lxplus using this recipe:
    # https://twiki.cern.ch/twiki/bin/view/CMS/PileupJSONFileforData#2015_Pileup_JSON_Files
    # cmsrel (bla bla bla)
    # cp /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/PileUp/pileup_latest.txt .
    # cp /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_Silver_v2.txt .
    # pileupCalc.py -i Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_Silver_v2.txt \
    #       --inputLumiJSON pileup_latest.txt --calcMode true --minBiasXsec 69000 --maxPileupBin 50 \
    #       --numPileupBins 50 MyDataPileupHistogram.root
    #
    # Then we compute our pileup distribution in MC ourselves, and divide data/MC, with these commands:
    # python makepu_fwlite.py --files inputfiles/ttjets.txt --maxevents 100000
    # python makepuhist.py --file_data MyDataPileupHistogram.root --file_mc pumc.root --file_out purw.root
    #

    if not options.isData and not options.disablePileup:
        pileupReweightFile = ROOT.TFile('purw.root', 'READ')
        purw = pileupReweightFile.Get('pileup')


    # Lepton efficiencies
    # THESE ARE PROBABLY NOT THE EFFICIENCY FILES WE WILL USE  
    if not options.isData:
        electonSFFile = ROOT.TFile('egammaEffi.txt_SF2D.root', 'READ')
        ele_SFs = electonSFFile.Get('EGamma_SF2D')

        muonSFFile = ROOT.TFile('MuonID_Z_RunBCD_prompt80X_7p65.root', 'READ')
        muon_SFs = muonSFFile.Get('MC_NUM_TightIDandIPCut_DEN_genTracks_PAR_pt_spliteta_bin1/pt_abseta_ratio')

        #print "THIS IS MUONSFS"
        #print type(muon_SFs)
        #print muon_SFs.GetBinContent(1,1)
        #exit()

        muonTrkSFFile = ROOT.TFile('general_tracks_and_early_general_tracks_corr_ratio.root', 'READ')
        muonTrk_SFs = muonTrkSFFile.Get('mutrksfptg10')


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

        genOut = "Event %d\n" % (iev)
        #print "GGGEEENNNNOUT...."
        #print genOut

        evWeight = 1.0 # Event weight
        puWeight = 1.0 # Pileup weight
        genWeight = 1.0 # ?
        LepWeight = 1.0 # ?
        LepWeightUnc = 0.0 # ?
        MuTrkWeight = 1.0 # ?
        MuTrkWeightUnc = 0.0 # ?



        event.getByLabel(triggerBitLabel, triggerBits)
        event.getByLabel(metfiltBitLabel, metfiltBits)
        runnumber = event.eventAuxiliary().run()

        #if options.verbose:
        if 1:
            #print "\nProcessing %d: run %6d, lumi %4d, event %12d" % \
                  (iev,event.eventAuxiliary().run(), \
                  event.eventAuxiliary().luminosityBlock(), \
                  event.eventAuxiliary().event())
            #print "\n === TRIGGER PATHS ==="

        # Check the names of the triggers to see if any of "our" trigger fired
        #print("Debugging....")
        #print(triggerBits)
        #print(triggerBits.product())
        #print(triggerNames(triggerBits.product()))
        names = event.object().triggerNames(triggerBits.product())

        # Get list of triggers that fired
        firedTrigs = []
        for itrig in xrange(triggerBits.product().size()):
            if triggerBits.product().accept(itrig):
                firedTrigs.append( itrig )

        passTrig = True # THIS IS PROBABLY NOT RIGHT AND SHOULD BE FIXED!!!!!!!!
        for trig in firedTrigs:
            trigName = names.triggerName(trig)
            for itrigToRun in xrange(0,len(trigsToRun)):
                if trigsToRun[itrigToRun] in trigName:
                    if options.verbose:
                        print ("Trigger ", trigName,  " PASSED ")
                    passTrig = True
                    if options.verbose:
                        print ("itrigToRun: ",itrigToRun)
                    SemiLeptTrig[itrigToRun] = True


        if options.verbose:
            print ("\n === MET FILTER PATHS ===")
        names2 = event.object().triggerNames(metfiltBits.product())
        passFilters = True
        for itrig in xrange(metfiltBits.product().size()):
            if names2.triggerName(itrig) == "Flag_HBHENoiseFilter" and not metfiltBits.product().accept(itrig):
                passFilters = False
            if names2.triggerName(itrig) == "Flag_HBHENoiseIsoFilter" and not metfiltBits.product().accept(itrig):
                passFilters = False
            if names2.triggerName(itrig) == "Flag_CSCTightHalo2015Filter" and not metfiltBits.product().accept(itrig):
                passFilters = False
            if names2.triggerName(itrig) == "Flag_EcalDeadCellTriggerPrimitiveFilter" and not metfiltBits.product().accept(itrig):
                passFilters = False
            if names2.triggerName(itrig) == "Flag_goodVertices" and not metfiltBits.product().accept(itrig):
                passFilters = False
            if names2.triggerName(itrig) == "Flag_eeBadScFilter" and not metfiltBits.product().accept(itrig):
                passFilters = False
            if options.verbose:
                print ("MET Filter ", names2.triggerName(itrig),  ": ", ("PASS" if metfiltBits.product().accept(itrig) else "fail (or not run)"))

        #print("A")
        passFilters = True ######### NOT RIGHT!!!!!!!!!!!!!!!!!!!
        if not passFilters:
            return

        #print("B")
        passTrig = True ############# NOT RIGHT!!!!!!!!!!!!!!!!!!!!!!!
        if not passTrig:
            return

        #print("C")
        ##   ________                __________.__          __
        ##  /  _____/  ____   ____   \______   \  |   _____/  |_  ______
        ## /   \  ____/ __ \ /    \   |     ___/  |  /  _ \   __\/  ___/
        ## \    \_\  \  ___/|   |  \  |    |   |  |_(  <_> )  |  \___ \
        ##  \______  /\___  >___|  /  |____|   |____/\____/|__| /____  >
        ##         \/     \/     \/                                  \/
        if not options.isData:
            
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
            if isGenPresent:
                #print(" ----------------------------- ")
                ngen[0] = 10
                gendecayflag[0] = 0
                tdecayflag = -1
                tbardecayflag = -1

                wpenergy = -999
                wmenergy = -999

                topQuark = None
                antitopQuark = None
                found_top = False
                found_antitop = False
                #print("------------------------------------------------------------")
                for igen,gen in enumerate( gens.product() ):
                    ##### WHEN LOOPING OVER CHECK THE HARD SCATTERING FLAG 
                    ##### TO MAKE SURE WE DON'T WORRY ABOUT TOPS THAT ARE JUST
                    ##### PROPAGATING FROM THEMSELVES
                    #if options.verbose:
                    if 0:
                        genOut = "" # For debugging
                        mother = -999
                        if gen.mother() != None:
                            mother = gen.mother().pdgId() 
                        genOut += 'GEN pdg id=%d pt=%+5.3f status=%d ndau: %d mother: %d isLastCopy: %d\n' % \
                                ( gen.pdgId(), gen.pt(), gen.status(), gen.numberOfDaughters(), mother, gen.isLastCopy() )
                        for ndau in range(0,gen.numberOfDaughters()):
                            genOut += "daughter pdgid: %d   pt: %f  %f\n" % (gen.daughter(ndau).pdgId(), gen.daughter(ndau).pt(), gen.daughter(ndau).mother().pt())
                        print genOut
                    if gen.pdgId() == 6 and gen.isLastCopy():
                        topQuark = gen
                        if found_top is False:

                            gene[0] = gen.energy()
                            genpt[0] = gen.pt()
                            geneta[0] = gen.eta()
                            genphi[0] = gen.phi()
                            genpdg[0] = gen.pdgId()

                            found_top = True

                        if topQuark.numberOfDaughters()==2:
                            d0 = gen.daughter(0)
                            d1 = gen.daughter(1)
                            if d0.pdgId()==24:

                                # b
                                gene[1] = d1.energy()
                                genpt[1] = d1.pt()
                                geneta[1] = d1.eta()
                                genphi[1] = d1.phi()
                                genpdg[1] = d1.pdgId()
                                # W
                                gene[2] = d0.energy()
                                genpt[2] = d0.pt()
                                geneta[2] = d0.eta()
                                genphi[2] = d0.phi()
                                genpdg[2] = d0.pdgId()

                                wpenergy = d0.energy() # For matching

                            elif d1.pdgId()==24:

                                # b
                                gene[1] = d0.energy()
                                genpt[1] = d0.pt()
                                geneta[1] = d0.eta()
                                genphi[1] = d0.phi()
                                genpdg[1] = d0.pdgId()
                                # W
                                gene[2] = d1.energy()
                                genpt[2] = d1.pt()
                                geneta[2] = d1.eta()
                                genphi[2] = d1.phi()
                                genpdg[2] = d1.pdgId()

                                wpenergy = d1.energy() # For matching

                    elif gen.pdgId() == -6 and gen.isLastCopy():
                        antitopQuark = gen
                        if found_antitop is False:
                            found_antitop  = True

                            # tbar
                            gene[5] = gen.energy()
                            genpt[5] = gen.pt()
                            geneta[5] = gen.eta()
                            genphi[5] = gen.phi()
                            genpdg[5] = gen.pdgId()

                        if antitopQuark.numberOfDaughters()==2:
                            d0 = gen.daughter(0)
                            d1 = gen.daughter(1)
                            if d0.pdgId()==-24:

                                # b
                                gene[6] = d1.energy()
                                genpt[6] = d1.pt()
                                geneta[6] = d1.eta()
                                genphi[6] = d1.phi()
                                genpdg[6] = d1.pdgId()
                                # W
                                gene[7] = d0.energy()
                                genpt[7] = d0.pt()
                                geneta[7] = d0.eta()
                                genphi[7] = d0.phi()
                                genpdg[7] = d0.pdgId()

                                wmenergy = d0.energy() # For matching

                            elif d1.pdgId()==-24:

                                # b
                                gene[6] = d0.energy()
                                genpt[6] = d0.pt()
                                geneta[6] = d0.eta()
                                genphi[6] = d0.phi()
                                genpdg[6] = d0.pdgId()
                                # W
                                gene[7] = d1.energy()
                                genpt[7] = d1.pt()
                                geneta[7] = d1.eta()
                                genphi[7] = d1.phi()
                                genpdg[7] = d1.pdgId()

                                wmenergy = d1.energy() # For matching

                    elif gen.pdgId() == 24 and gen.isLastCopy() and \
                            abs(gen.energy()-wpenergy)< 10:
                        if gen.numberOfDaughters()==2:
                            d0 = gen.daughter(0)
                            d1 = gen.daughter(1)

                            # W children 1
                            gene[3] = d0.energy()
                            genpt[3] = d0.pt()
                            geneta[3] = d0.eta()
                            genphi[3] = d0.phi()
                            genpdg[3] = d0.pdgId()
                            # W children 2
                            gene[4] = d1.energy()
                            genpt[4] = d1.pt()
                            geneta[4] = d1.eta()
                            genphi[4] = d1.phi()
                            genpdg[4] = d1.pdgId()

                            #print("HERE!!!! - %d %d" % (d0.pdgId(),d1.pdgId()))

                            if d0.pdgId() in [1,2,3,4, -1, -2, -3, -4]:
                                tdecayflag = 0
                            elif d0.pdgId() in [11, 13, 15, 12, 14, 16]:
                                tdecayflag = 1

                    #elif gen.pdgId() == -24 and gen.mother().pdgId()==-6:
                    elif gen.pdgId() == -24 and gen.isLastCopy() and \
                            abs(gen.energy()-wmenergy)< 10:
                        if gen.numberOfDaughters()==2:
                            d0 = gen.daughter(0)
                            d1 = gen.daughter(1)

                            # W children 1
                            gene[8] = d0.energy()
                            genpt[8] = d0.pt()
                            geneta[8] = d0.eta()
                            genphi[8] = d0.phi()
                            genpdg[8] = d0.pdgId()
                            # W children 2
                            gene[9] = d1.energy()
                            genpt[9] = d1.pt()
                            geneta[9] = d1.eta()
                            genphi[9] = d1.phi()
                            genpdg[9] = d1.pdgId()

                            #print("THERE!!!! - %d %d" % (d0.pdgId(),d1.pdgId()))

                            if d0.pdgId() in [1,2,3,4,-1,-2,-3,-4]:
                                tbardecayflag = 0
                            elif d0.pdgId() in [11, 13, 15, 12, 14, 16]:
                                tbardecayflag = 1
                    
                if topQuark != None and antitopQuark != None:
                    ttbarCandP4 = topQuark.p4() + antitopQuark.p4()
                    #h_mttbar_true.Fill( ttbarCandP4.mass() )
                    haveGenSolution = True
                    #print("tbar/t flag: %d %d" % (tbardecayflag, tdecayflag))
                    gendecayflag[0] = 10*tbardecayflag + tdecayflag
                else:
                    if options.verbose:
                        print ('No top quarks, not filling mttbar')
            event.getByLabel( genInfoLabel, genInfo )
            genWeight = genInfo.product().weight()
            evWeight *= genWeight

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

		##   __________.__.__                        __________                     .__       .__     __  .__
		##   \______   \__|  |   ____  __ ________   \______   \ ______  _  __ ____ |__| ____ |  |___/  |_|__| ____    ____
		##    |     ___/  |  | _/ __ \|  |  \____ \   |       _// __ \ \/ \/ // __ \|  |/ ___\|  |  \   __\  |/    \  / ___\
		##    |    |   |  |  |_\  ___/|  |  /  |_> >  |    |   \  ___/\     /\  ___/|  / /_/  >   Y  \  | |  |   |  \/ /_/  >
		##    |____|   |__|____/\___  >____/|   __/   |____|_  /\___  >\/\_/  \___  >__\___  /|___|  /__| |__|___|  /\___  /
		##                          \/      |__|             \/     \/            \/  /_____/      \/             \//_____/

        '''
        if not options.isData: # Is Monte Carlo
		    # Need to make sure we read in the pileup reweighting info from another file. 
		    # See original code from where we got this. 
		    event.getByLabel(pileuplabel, pileups)

		    TrueNumInteractions = 0
		    if len(pileups.product())>0:
			TrueNumInteractions = pileups.product()[0].getTrueNumInteractions()
		    else:
			print 'Event has no pileup information, setting TrueNumInteractions to 0.'
=======
            vertexX = PV.x()
            vertexY = PV.y()
            vertexZ = PV.z()
            if options.verbose:
                print ("PV at x,y,z = %+5.3f, %+5.3f, %+6.3f (ndof %.1f)" % (vertexX, vertexY, vertexZ, PV.ndof()))

        ##   __________.__.__                        __________                     .__       .__     __  .__
        ##   \______   \__|  |   ____  __ ________   \______   \ ______  _  __ ____ |__| ____ |  |___/  |_|__| ____    ____
        ##    |     ___/  |  | _/ __ \|  |  \____ \   |       _// __ \ \/ \/ // __ \|  |/ ___\|  |  \   __\  |/    \  / ___\
        ##    |    |   |  |  |_\  ___/|  |  /  |_> >  |    |   \  ___/\     /\  ___/|  / /_/  >   Y  \  | |  |   |  \/ /_/  >
        ##    |____|   |__|____/\___  >____/|   __/   |____|_  /\___  >\/\_/  \___  >__\___  /|___|  /__| |__|___|  /\___  /
        ##                          \/      |__|             \/     \/            \/  /_____/      \/             \//_____/

        '''
        if not options.isData: # Is Monte Carlo
            # Need to make sure we read in the pileup reweighting info from another file. 
            # See original code from where we got this. 
            event.getByLabel(pileuplabel, pileups)
            TrueNumInteractions = 0
            if len(pileups.product())>0:
                TrueNumInteractions = pileups.product()[0].getTrueNumInteractions()
            else:
                print('Event has no pileup information, setting TrueNumInteractions to 0.')

            if not options.isData and not options.disablePileup:
                puWeight = purw.GetBinContent( purw.GetXaxis().FindBin( TrueNumInteractions ) )
                evWeight *= puWeight
		

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

        #print("F")

        ## .____                  __                    _________      .__                 __  .__
        ## |    |    ____ _______/  |_  ____   ____    /   _____/ ____ |  |   ____   _____/  |_|__| ____   ____
        ## |    |  _/ __ \\____ \   __\/  _ \ /    \   \_____  \_/ __ \|  | _/ __ \_/ ___\   __\  |/  _ \ /    \
        ## |    |__\  ___/|  |_> >  | (  <_> )   |  \  /        \  ___/|  |_\  ___/\  \___|  | |  (  <_> )   |  \
        ## |_______ \___  >   __/|__|  \____/|___|  / /_______  /\___  >____/\___  >\___  >__| |__|\____/|___|  /
        ##         \/   \/|__|                    \/          \/     \/          \/     \/                    \/

        #print("G")
        event.getByLabel( muonLabel, muons )
        event.getByLabel( electronLabel, electrons )

        #print("H")
	

        #print("I")
        # Select tight good muons
        goodmuons = []
        #print("NUMBER OF MUONS: %d" % (len(muons.product())))
        if len(muons.product()) > 0:
            for i,muon in enumerate( muons.product() ):
                #if muon.pt() > options.minMuonPt and abs(muon.eta()) < options.maxMuonEta and muon.muonBestTrack().dz(PV.position()) < 5.0 and muon.isTightMuon(PV):
                #if 1:
                if muon.pt() > options.minMuonPt and abs(muon.eta()) < options.maxMuonEta: 
                    goodmuons.append( muon )
                    if options.verbose:
                        print ("muon %2d: pt %4.1f, eta %+5.3f phi %+5.3f dz(PV) %+5.3f, POG loose id %d, tight id %d." % (
                            i, muon.pt(), muon.eta(), muon.phi(), muon.muonBestTrack().dz(PV.position()), muon.isLooseMuon(), muon.isTightMuon(PV)))

        nmuon[0] = len(goodmuons)
        for i,m in enumerate(goodmuons):
            if i<16:
                muonpt[i] = m.pt()
                muoneta[i] = m.eta()
                muonphi[i] = m.phi()
                muone[i] = m.energy()
                muonq[i] = m.charge()
                muonpx[i] = m.px()
                muonpy[i] = m.py()
                muonpz[i] = m.pz()
                pfi  = m.pfIsolationR03()
                #print( pfi.sumChargedHadronPt, pfi.sumChargedParticlePt, pfi.sumNeutralHadronEt, pfi.sumPhotonEt, pfi.sumNeutralHadronEtHighThreshold, pfi.sumPhotonEtHighThreshold, pfi.sumPUPt)
                muonsumchhadpt[i] = pfi.sumChargedHadronPt
                muonsumnhadpt[i] = pfi.sumNeutralHadronEt
                muonsumphotEt[i] = pfi.sumPhotonEt




        #print("J")
        #'''
        # Select tight good electrons
        goodelectrons = []
        if len(electrons.product()) > 0:
            for i,electron in enumerate( electrons.product() ):
                #print type(electron),"\n",electron
                #print type(event),"\n",event
                passTight = selectElectron( electron, event )
                if electron.pt() > options.minElectronPt and abs(electron.eta()) < options.maxElectronEta and passTight:
                    goodelectrons.append( electron )
		            #elec = electron.electronIDs()
		            #print('New set')
		            #for i in range(len(elec)):
                    #	print(elec[i][0], elec[i][1])
                    if options.verbose:
                        print ("elec %2d: pt %4.1f, supercluster eta %+5.3f, phi %+5.3f sigmaIetaIeta %.3f (%.3f with full5x5 shower shapes), pass conv veto %d" % \
                            ( i, electron.pt(), electron.superCluster().eta(), electron.phi(), electron.sigmaIetaIeta(), electron.full5x5_sigmaIetaIeta(), electron.passConversionVeto()))
        
        #print("K")
        nelectron[0] = len(goodelectrons)
        for i,m in enumerate(goodelectrons):
	    #goodelecID = m.electronIDs()
	    #print(len(goodelecID))
            if i<16:
                electronpt[i] = m.pt()
                electroneta[i] = m.eta()
                electronphi[i] = m.phi()
                electrone[i] = m.energy()
                electronpx[i] = m.px()
                electronpy[i] = m.py()
                electronpz[i] = m.pz()
                electronq[i] = m.charge()
                #print(m.dr03TkSumPt())
                electronTkIso[i] = m.dr03TkSumPt()
                #print(electronTkIso[i])
                electronHCIso[i] = m.dr03HcalTowerSumEt()
                electronECIso[i] = m.dr03EcalRecHitSumEt()
                #pfe  = m.isolationVariables03()
                #electronchiso[i] = pfe.chargedHadronIso
                #electronnhiso[i] = pfe.neutralHadronIso
	            #electronphotiso[i] = pfe.photonIso
        #'''

        # Veto on dilepton events
        # Also keep track of the PF index of the lepton
        # for lepton-jet cleaning (see below)
        theLeptonObjKey = -1

        #if len(goodmuons) + len(goodelectrons) != 1:
        #if len(goodmuons) != 1: 
        #print("NNNNN")
        #print(len(goodmuons))
        if len(goodmuons) == 0: 
            return
        elif len(goodmuons) > 0:
            theLeptonCand = goodmuons[0]
            theLepton = ROOT.TLorentzVector( goodmuons[0].px(),
                                             goodmuons[0].py(),
                                             goodmuons[0].pz(),
                                             goodmuons[0].energy() )
            theLeptonObjKey = goodmuons[0].originalObjectRef().key()
            leptonType = 13

            # Get the muon ID and TRK scale factors for simulation
            if not options.isData:
                pt = goodmuons[0].pt()
                eta = abs(goodmuons[0].eta())
                # ID scale factors
                overflow = False
                if pt >=200:
                    pt=199.9
                    overflow =True
                LepWeight = muon_SFs.GetBinContent( muon_SFs.GetXaxis().FindBin( pt ), muon_SFs.GetYaxis().FindBin( eta ) )
                LepWeightUnc =  muon_SFs.GetBinError( muon_SFs.GetXaxis().FindBin( pt ), muon_SFs.GetYaxis().FindBin( eta ) )
                #if overflow:
                #    LepWeightUnc *=2
                # add additional 1% systematic uncertainty for ID +0.5% for HIP effect
                LepWeightUnc = (LepWeightUnc**2 + (0.01*LepWeight)**2 + (0.005*LepWeight)**2)**0.5
                evWeight *= LepWeight

                # tracker efficiency sccale factors
                eta = goodmuons[0].eta()
                MuTrkWeight = muonTrk_SFs.GetBinContent( muonTrk_SFs.GetXaxis().FindBin( eta ))
                MuTrkWeightUnc = muonTrk_SFs.GetBinError( muonTrk_SFs.GetXaxis().FindBin( eta ))
                evWeight *= MuTrkWeight

        #print("A")
        #print("NNNNN")
        '''
        else:
            theLeptonCand = goodelectrons[0]
            theLepton = ROOT.TLorentzVector( goodelectrons[0].px(),
                                             goodelectrons[0].py(),
                                             goodelectrons[0].pz(),
                                             goodelectrons[0].energy() )
            theLeptonObjKey = goodelectrons[0].originalObjectRef().key()
            leptonType = 11

            # Get the electron ID scale factor for simulation
            if not options.isData:
                pt = goodelectrons[0].pt()
                eta =  goodelectrons[0].superCluster().eta()
                overflow = False
                if pt >=200:
                    pt=199.9
                    overflow =True
                LepWeight = ele_SFs.GetBinContent( ele_SFs.GetXaxis().FindBin( eta ), ele_SFs.GetYaxis().FindBin( pt ) )
                LepWeightUnc =  ele_SFs.GetBinError( ele_SFs.GetXaxis().FindBin( eta ), ele_SFs.GetYaxis().FindBin( pt ) )
                if overflow:
                    LepWeightUnc *=2
                evWeight *= LepWeight

        '''
        # Get the "footprint" of the lepton. That is, all of the candidates making up the lepton.

        # now get a list of the PF candidates used to build this lepton, so to exclude them
        footprint = set()
        for i in xrange(theLeptonCand.numberOfSourceCandidatePtrs()):
            footprint.add(theLeptonCand.sourceCandidatePtr(i).key()) # the key is the index in the pf collection


        #print("B")
        ##      ____.       __      _________      .__                 __  .__
        ##     |    | _____/  |_   /   _____/ ____ |  |   ____   _____/  |_|__| ____   ____
        ##     |    |/ __ \   __\  \_____  \_/ __ \|  | _/ __ \_/ ___\   __\  |/  _ \ /    \
        ## /\__|    \  ___/|  |    /        \  ___/|  |_\  ___/\  \___|  | |  (  <_> )   |  \
        ## \________|\___  >__|   /_______  /\___  >____/\___  >\___  >__| |__|\____/|___|  /
        ##               \/               \/     \/          \/     \/                    \/

        #
        #
        #
        # Here, we have TWO jet collections, AK4 and AK8. The
        # AK4 jets are used for b-tagging, while the AK8 jets are used
        # for top-tagging.
        # In the future, the AK8 jets will contain "subjet b-tagging" in
        # miniAOD but as of now (Dec 2014) this is not ready so we
        # need to adjust.
        #
        #
        # In addition, we must perform "lepton-jet" cleaning.
        # This is because the PF leptons are actually counted in the
        # list of particles sent to the jet clustering.
        # Therefore, we need to loop over the jet constituents and
        # remove the lepton.

        # use getByLabel, just like in cmsRun
        event.getByLabel (jetLabel, jets)          # For b-tagging
        event.getByLabel (ak8jetLabel, ak8jets)    # For top-tagging

        # loop over jets and fill hists
        ijet = 0

        # These will hold all of the jets we need for the selection
        ak4JetsGood = []
        ak8JetsGood = []
        ak4JetsGoodP4 = []
        ak8JetsGoodP4 = []
        ak4JetsGoodSysts = []
        ak8JetsGoodSysts = []

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

            # Is this the b-jet tagging?
            #print("B-tagging...: %f " % (jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")))
            goodJet = \
              nhf < 0.99 and \
              nef < 0.99 and \
              chf > 0.00 and \
              cef < 0.99 and \
              nconstituents > 1 and \
              nch > 0

            if goodJet:
                if njets2write<16:
                    i = njets2write
                    jetpt[i] = jet.pt()
                    jeteta[i] = jet.eta()
                    jetphi[i] = jet.phi()
                    jete[i] = jet.energy()
                    jetpx[i] = jet.px()
                    jetpy[i] = jet.py()
                    jetpz[i] = jet.pz()
                    jetbtag[i] = jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")
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
            cleaned = False
            if theLepton.DeltaR(jetP4Raw) < 0.6:
                # Check all daughters of jets close to the lepton
                pfcands = jet.daughterPtrVector()
                for ipf,pf in enumerate( pfcands ):

                    # If any of the jet daughters matches the good lepton, remove the lepton p4 from the jet p4
                    if pf.key() in footprint:
                        if options.verbose:
                            print ('REMOVING LEPTON, pt/eta/phi = {0:6.2f},{1:6.2f},{2:6.2f}'.format(
                                theLepton.Perp(), theLepton.Eta(), theLepton.Phi()
                                ))
                        if jetP4Raw.Energy() > theLepton.Energy():
                            jetP4Raw -= theLepton
                        else:
                            jetP4Raw -= theLepton
                            jetP4Raw.SetE(0.0)
                        cleaned = True
                        break

            # Apply new JEC's
            if options.isData:
                (newJEC, corrDn, corrUp) = getJEC(DataJECs.jecAK4(runnumber), DataJECs.jecUncAK4(runnumber), jetP4Raw, jet.jetArea(), rho, NPV)
            else:
                (newJEC, corrDn, corrUp) = getJEC(jecAK4, jecUncAK4, jetP4Raw, jet.jetArea(), rho, NPV)

            # If MC, get jet energy resolution
            ptsmear   = 1.0
            ptsmearUp = 1.0
            ptsmearDn = 1.0
            if not options.isData:
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


            #print("---------")
            #print(jetP4Raw.Perp())
            jetP4 = jetP4Raw * newJEC * ptsmear
            #print(jetP4.Perp())
            if goodJet:
                if njets2write-1<16:
                    i = njets2write-1
                    jetjecpt[i] = jetP4.Perp()
                    jetjeceta[i] = jetP4.Eta()
                    jetjecphi[i] = jetP4.Phi()
                    jetjece[i] = jetP4.E()
                    jetjecpx[i] = jetP4.Px()
                    jetjecpy[i] = jetP4.Py()
                    jetjecpz[i] = jetP4.Pz()

            # Now perform jet kinematic cuts
            ##print(jetP4.Perp())
            if jetP4.Perp() < options.minAK4Pt or abs(jetP4.Rapidity()) > options.maxAK4Rapidity:
                #print("JETCONTINUE")
                continue

            # Get the jet nearest the lepton
            dR = jetP4.DeltaR(theLepton )
            ak4JetsGood.append(jet)
            ak4JetsGoodP4.append( jetP4 )
            ak4JetsGoodSysts.append( [corrUp, corrDn, ptsmearUp, ptsmearDn] )
            if options.verbose:
                print ('corrjet pt = {0:6.2f}, y = {1:6.2f}, phi = {2:6.2f}, m = {3:6.2f}, bdisc = {4:6.2f}'.format (
                    jetP4.Perp(), jetP4.Rapidity(), jetP4.Phi(), jetP4.M(), jet.bDiscriminator( options.bdisc )
                    ))

            if dR < dRMin:
                inearestJet = ijet
                nearestJet = jet
                nearestJetP4 = jetP4
                dRMin = dR

        # OUR STUFF
        njet[0] = njets2write

        ############################################
        # Require at least one leptonic-side jet, and 2d isolation cut
        ############################################
        if nearestJet == None:
            print ("RETURNINGNEARESTJET")
            return

        # Finally get the METs
        event.getByLabel( metLabel, mets )
        #met = mets.product()[0]
        met = mets.product().front()
        metpt[0] = met.pt()
        metphi[0] = met.phi()
        mete[0] = met.energy()
        meteta[0] = met.eta()
        #print("MET pt/phi: %f %f" % (metpt[0],metphi[0]))

        theLepJet = nearestJetP4
        theLepJetBDisc = nearestJet.bDiscriminator( options.bdisc )

        # Fill some plots related to the jets
        #h_ptAK4.Fill( theLepJet.Perp(), evWeight )
        #h_etaAK4.Fill( theLepJet.Eta(), evWeight )
        #h_yAK4.Fill( theLepJet.Rapidity(), evWeight )
        #h_phiAK4.Fill( theLepJet.Phi(), evWeight )
        #h_mAK4.Fill( theLepJet.M(), evWeight )
        #h_BDiscAK4.Fill( theLepJetBDisc, evWeight )
        # Fill some plots related to the lepton, the MET, and the 2-d cut
        ptRel = theLepJet.Perp( theLepton.Vect() )
        #h_ptLep.Fill(theLepton.Perp(), evWeight)
        #h_etaLep.Fill(theLepton.Eta(), evWeight)
        #h_met.Fill(met.pt(), evWeight)
        #h_ptRel.Fill( ptRel, evWeight )
        #h_dRMin.Fill( dRMin, evWeight )
        #h_2DCut.Fill( dRMin, ptRel, evWeight )
        pass2D = ptRel > 20.0 or dRMin > 0.4
        if options.verbose:
            print ('2d cut : dRMin = {0:6.2f}, ptRel = {1:6.2f}, pass = {2:6d}'.format( dRMin, ptRel, pass2D ))
        if not pass2D:
            #print("NOPASS2D") # This seems to cut out about 20% of the events
            return

        ############################################
        # Get the AK8 jet away from the lepton
        ############################################
        for i,jet in enumerate(ak8jets.product()):


            # perform jet ID with UNCORRECTED jet energy
            jetP4 = ROOT.TLorentzVector( jet.px(), jet.py(), jet.pz(), jet.energy() )
            jetP4Raw = copy.copy(jetP4)
            jetP4Raw *= jet.jecFactor(0)

            nhf = jet.neutralHadronEnergy() / jetP4Raw.E()
            nef = jet.neutralEmEnergy() / jetP4Raw.E()
            chf = jet.chargedHadronEnergy() / jetP4Raw.E()
            cef = jet.chargedEmEnergy() / jetP4Raw.E()
            nconstituents = jet.numberOfDaughters()
            nch = jet.chargedMultiplicity()
            goodJet = \
              nhf < 0.99 and \
              nef < 0.99 and \
              chf > 0.00 and \
              cef < 0.99 and \
              nconstituents > 1 and \
              nch > 0

            if not goodJet:
                print("NOGOODAK8JET")
                return

            if options.isData:
                (newJEC, corrDn, corrUp) = getJEC(DataJECs.jecAK8(runnumber), DataJECs.jecUncAK8(runnumber), jetP4Raw, jet.jetArea(), rho, NPV)
            else:
                (newJEC, corrDn, corrUp) = getJEC(jecAK8, jecUncAK8, jetP4Raw, jet.jetArea(), rho, NPV)

            # If MC, get jet energy resolution
            ptsmear   = 1.0
            ptsmearUp = 1.0
            ptsmearDn = 1.0
            if not options.isData:
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

            jetP4 = jetP4Raw * newJEC * ptsmear   # Nominal JEC, nominal JER

            # Now perform jet kinematic cuts
            if jetP4.Perp() < options.minAK8Pt or abs(jetP4.Rapidity()) > options.maxAK8Rapidity:
                continue

            # Only keep AK8 jets "away" from the lepton, so we do not need
            # lepton-jet cleaning here. There's no double counting.
            dR = jetP4.DeltaR(theLepton )
            if dR > ROOT.TMath.Pi()/2.0:
                ak8JetsGood.append(jet)
                ak8JetsGoodP4.append( jetP4 )
                ak8JetsGoodSysts.append( [corrUp, corrDn, ptsmearUp, ptsmearDn] )

        ## ___________                     .__
        ## \__    ___/____     ____   ____ |__| ____    ____
        ##   |    |  \__  \   / ___\ / ___\|  |/    \  / ___\
        ##   |    |   / __ \_/ /_/  > /_/  >  |   |  \/ /_/  >
        ##   |____|  (____  /\___  /\___  /|__|___|  /\___  /
        ##                \//_____//_____/         \//_____/

        ############################################
        # Investigate the b-tagging and t-tagging
        ############################################
        '''
        if len(ak4JetsGoodP4) < 1 or len(ak8JetsGoodP4) < 1:
            print("LENJETS") # CUTS OUT 50% of ttbar events
            return
        '''
        if len(ak4JetsGoodP4)<1:
            print("LENJETS") 
            return


        tJets = []

        '''
        for ijet,jet in enumerate(ak8JetsGood):
            if jet.pt() < options.minAK8Pt:
                continue

            mAK8Softdrop,mAK8Pruned  = -999,-999 
            if ( jet.hasUserFloat('ak8PFJetsCHSSoftDropMass') ): mAK8Softdrop = jet.userFloat('ak8PFJetsCHSSoftDropMass')
            if ( jet.hasUserFloat('ak8PFJetsCHSPrunedMass') )  : mAK8Pruned = jet.userFloat('ak8PFJetsCHSPrunedMass')
            #mAK8Filtered = jet.userFloat('ak8PFJetsCHSFilteredMass')
            #mAK8Trimmed = jet.userFloat('ak8PFJetsCHSTrimmedMass')


            h_ptAK8.Fill( jet.pt(), evWeight )
            h_etaAK8.Fill( jet.eta(), evWeight )
            h_yAK8.Fill( jet.rapidity(), evWeight )
            h_phiAK8.Fill( jet.phi(), evWeight )
            h_mAK8.Fill( jet.mass(), evWeight )
            
            h_msoftdropAK8.Fill( mAK8Softdrop, evWeight )
            h_mprunedAK8.Fill( mAK8Pruned, evWeight )

            #h_mfilteredAK8.Fill( mAK8Filtered, evWeight )
            #h_mtrimmedAK8.Fill( mAK8Trimmed, evWeight )



            tJets.append( jet )
        '''

        ## ___________.__.__  .__    ___________
        ## \_   _____/|__|  | |  |   \__    ___/______   ____   ____
        ##  |    __)  |  |  | |  |     |    |  \_  __ \_/ __ \_/ __ \
        ##  |     \   |  |  |_|  |__   |    |   |  | \/\  ___/\  ___/
        ##  \___  /   |__|____/____/   |____|   |__|    \___  >\___  >
        ##      \/                                          \/     \/
        if not options.disableTree:
            candToPlot = 0

            '''
            # Make sure there are top tags if we want to plot them
            tagInfoLabels = ak8JetsGood[candToPlot].tagInfoLabels()
            # Get n-subjettiness "tau" variables
            tau1,tau2,tau3 = -999,-999,-999
            tau21,tau32 = -999,-999
            if ( ak8JetsGood[candToPlot].hasUserFloat('NjettinessAK8:tau1') ): tau1 = ak8JetsGood[candToPlot].userFloat('NjettinessAK8:tau1')
            if ( ak8JetsGood[candToPlot].hasUserFloat('NjettinessAK8:tau2') ): tau2 = ak8JetsGood[candToPlot].userFloat('NjettinessAK8:tau2')
            if ( ak8JetsGood[candToPlot].hasUserFloat('NjettinessAK8:tau3') ): tau3 = ak8JetsGood[candToPlot].userFloat('NjettinessAK8:tau3')
            if tau1 > 0.0001:
                tau21 = tau2 / tau1
                h_tau21AK8.Fill( tau21, evWeight )
            else:
                h_tau21AK8.Fill( -1.0, evWeight )
            if tau2 > 0.0001:
                tau32 = tau3 / tau2
                h_tau32AK8.Fill( tau32, evWeight )
            else:
                h_tau32AK8.Fill( -1.0, evWeight )
            '''
            # Get the subjets from the modified mass drop algorithm
            # aka softdrop with beta=0.
            # The heaviest should correspond to the W and the lightest
            # should correspond to the b.
            subjetW,subjetB = -999,-999
            '''
            subjets = ak8JetsGood[candToPlot].subjets('SoftDrop')
            subjetW = None
            subjetB = None
            if len(subjets) >= 2:
                if subjets[0].mass() > subjets[1].mass():
                    subjetW = subjets[0]
                    subjetB = subjets[1]
                else:
                    subjetB = subjets[0]
                    subjetW = subjets[1]
            else:
                return
            '''

            SemiLeptWeight      [0] = evWeight
            PUWeight            [0] = puWeight
            LeptonIDWeight      [0] = LepWeight
            LeptonIDWeightUnc   [0] = LepWeightUnc
            MuonTrkWeight       [0] = MuTrkWeight
            MuonTrkWeightUnc    [0] = MuTrkWeightUnc
            GenWeight           [0] = genWeight
            #FatJetPt            [0] = ak8JetsGoodP4[candToPlot].Perp()
            #FatJetEta           [0] = ak8JetsGoodP4[candToPlot].Eta()
            #FatJetPhi           [0] = ak8JetsGoodP4[candToPlot].Phi()
            #FatJetRap           [0] = ak8JetsGoodP4[candToPlot].Rapidity()
            #FatJetEnergy        [0] = ak8JetsGoodP4[candToPlot].Energy()
            #FatJetMass          [0] = ak8JetsGoodP4[candToPlot].M()
            #FatJetBDisc         [0] = ak8JetsGood[candToPlot].bDiscriminator(options.bdisc)
            #if ( ak8JetsGood[candToPlot].hasUserFloat('ak8PFJetsCHSSoftDropMass') ): FatJetMassSoftDrop  [0] = ak8JetsGood[candToPlot].userFloat('ak8PFJetsCHSSoftDropMass')
            #FatJetTau32         [0] = tau32
            #FatJetTau21         [0] = tau21
            #FatJetJECUpSys      [0] = ak8JetsGoodSysts[candToPlot][0]
            #FatJetJECDnSys      [0] = ak8JetsGoodSysts[candToPlot][1]
            #FatJetJERUpSys      [0] = ak8JetsGoodSysts[candToPlot][2]
            #FatJetJERDnSys      [0] = ak8JetsGoodSysts[candToPlot][3]
            #FatJetDeltaPhiLep   [0] = ak8JetsGoodP4[candToPlot].DeltaR(theLepton)
            if subjetW != None and subjetW != -999:
                FatJetSDBDiscW      [0] = subjetW.bDiscriminator(options.bdisc)
                FatJetSDBDiscB      [0] = subjetB.bDiscriminator(options.bdisc)
                FatJetSDsubjetWpt   [0] = subjetW.pt()
                FatJetSDsubjetWmass [0] = subjetW.mass()
                FatJetSDsubjetBpt   [0] = subjetB.pt()
                FatJetSDsubjetBmass [0] = subjetB.mass()
            LeptonType          [0] = leptonType
            LeptonPt            [0] = theLepton.Perp()
            LeptonEta           [0] = theLepton.Eta()
            LeptonPhi           [0] = theLepton.Phi()
            LeptonEnergy        [0] = theLepton.E()
            LeptonPtRel         [0] = nearestJetP4.Perp(theLepton.Vect())
            LeptonDRMin         [0] = nearestJetP4.DeltaR(theLepton)
            SemiLepMETe         [0] = met.energy()
            SemiLepMETeta       [0] = met.eta()
            SemiLepMETpt        [0] = met.pt()
            SemiLepMETphi       [0] = met.phi()
            SemiLepNvtx         [0] = NPV
            NearestAK4JetBDisc  [0] = nearestJet.bDiscriminator(options.bdisc)
            NearestAK4JetPt     [0] = nearestJetP4.Perp()
            NearestAK4JetEta    [0] = nearestJetP4.Eta()
            NearestAK4JetPhi    [0] = nearestJetP4.Phi()
            NearestAK4JetMass   [0] = nearestJetP4.M()
            NearestAK4JetJECUpSys      [0] = ak4JetsGoodSysts[candToPlot][0]
            NearestAK4JetJECDnSys      [0] = ak4JetsGoodSysts[candToPlot][1]
            NearestAK4JetJERUpSys      [0] = ak4JetsGoodSysts[candToPlot][2]
            NearestAK4JetJERDnSys      [0] = ak4JetsGoodSysts[candToPlot][3]
            SemiLeptRunNum      [0] = event.object().id().run()
            SemiLeptLumiNum     [0] = event.object().luminosityBlock()
            SemiLeptEventNum    [0] = event.object().id().event()

            #print("I got to the end of the event loop!!!!")
            TreeSemiLept.Fill()

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
        for iev, event in enumerate(events):

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

    # Close the output ROOT file
    f.cd()
    f.Write()
    f.Close()

    #genoutputfile.close()
    


#####################################################################################
if __name__ == "__main__":
    topbnv_fwlite(sys.argv)



