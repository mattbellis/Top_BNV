# Much of this is from the B2G data analysis school code

import ROOT, copy, sys, logging
from array import array
from DataFormats.FWLite import Events, Handle

# NEED THIS FOR DEEP CSV STUFF?
from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection

################################################################################
# Helper utility to open files, both locally and with CRAB
################################################################################
def getInputFiles(options):
    result = []
    with open(options.input, 'r') as fpInput:
        for lfn in fpInput:
            if lfn[0]=="#":
                continue
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
    add_option('isMC',          default=False, action='store_true',
        help='Running over MC. We need this for the trigger and other stuff.')
    add_option('year',          default="2016", 
        help='Year of dataset (2016, 2017, 2018)')
    add_option('localInputFiles',    default=False, action='store_true',
        help='Use this flag when running with with local files')
    add_option('trigType',         default="SingleMuon",
        help='SingleMuon, SingleElectron, etc.')
    add_option('disablePileup',      default=False, action='store_true',
        help='Disable pileup reweighting')

    (options, args) = parser.parse_args(argv)
    argv = []

    return options
#####################################################################################

#####################################################################################
# Jet Energy Corrections
#####################################################################################
# Jet energy correction files for data
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/JECDataMC#2016_Data
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/JECDataMC#2017_Data
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/JECDataMC#2018_Data
# To get the intervals of validity (those first numbers, one can go here
# https://twiki.cern.ch/twiki/bin/view/CMS/PdmV2016Analysis
jet_energy_corrections = {"2016": [ [1,276811,"Summer16_07Aug2017BCD_V11_DATA"],
                           [276831,278801,"Summer16_07Aug2017EF_V11_DATA"],
                          [278802,float("inf"),"Summer16_07Aug2017GH_V11_DATA"] ],

                          "2017": [ [1,299329,"Fall17_17Nov2017B_V32_DATA"],
                           [299337,302029,"Fall17_17Nov2017C_V32_DATA"],
                           [302030,304826,"Fall17_17Nov2017DE_V32_DATA"],
                          [304911,306462,"Fall17_17Nov2017F_V32_DATA"] ],

                          "2018": [ [1,316995,"Autumn18_RunA_V8_DATA"],
                           [316998,319312,"Autumn18_RunB_V8_DATA"],
                           [319313,320393,"Autumn18_RunC_V8_DATA"],
                          [320394,325273,"Autumn18_RunD_V8_DATA"] ]
                          }
  
jet_energy_correction_GT_for_MC = {"2016":"Summer16_07Aug2017_V11_MC", 
                                   "2017":"Fall17_17Nov2017_V32_MC",
                                   "2018":"Autumn18_V8_MC"}

#####################################################################################
# This *should* be correct now
# Values from https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution
# https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution#2016_data
# https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution#2018_data
#####################################################################################
# Columns are
# Low-eta,  High-eta,  Data/MC SF,  uncertainty
jet_energy_resolution = {
        "2016": [
        (0.000, 0.522, 1.1595, 0.0645), 
        (0.522, 0.783, 1.1948, 0.0652), 
        (0.783, 1.131, 1.1464, 0.0632), 
        (1.131, 1.305, 1.1609, 0.1025), 
        (1.305, 1.740, 1.1278, 0.0986), 
        (1.740, 1.930, 1.1000, 0.1079), 
        (1.930, 2.043, 1.1426, 0.1214), 
        (2.043, 2.322, 1.1512, 0.1140), 
        (2.322, 2.500, 1.2963, 0.2371), 
        (2.500, 2.893, 1.3418, 0.2091), 
        (2.853, 2.964, 1.7788, 0.2008), 
        (2.964, 3.139, 1.1869, 0.1243), 
        (3.139, 5.191, 1.1922, 0.1488), 
        ], 

        "2017": [
        (0.000, 0.522, 1.1432, 0.0222), 
        (0.522, 0.783, 1.1815, 0.0484), 
        (0.783, 1.131, 1.0989, 0.0456), 
        (1.131, 1.305, 1.1137, 0.1397), 
        (1.305, 1.740, 1.1307, 0.1470), 
        (1.740, 1.930, 1.1600, 0.0976), 
        (1.930, 2.043, 1.2393, 0.1909), 
        (2.043, 2.322, 1.2604, 0.1501), 
        (2.322, 2.500, 1.4085, 0.2020), 
        (2.500, 2.893, 1.9909, 0.5684), 
        (2.853, 2.964, 2.2923, 0.3743), 
        (2.964, 3.139, 1.1296, 0.1089), 
        (3.139, 5.191, 1.1542, 0.1524), 
        ],

        "2018": [
        (0.000, 0.522, 1.15 , 0.043), 
        (0.522, 0.783, 1.134, 0.08 ), 
        (0.783, 1.131, 1.102, 0.052), 
        (1.131, 1.305, 1.134, 0.112), 
        (1.305, 1.740, 1.104, 0.211), 
        (1.740, 1.930, 1.149, 0.159), 
        (1.930, 2.043, 1.148, 0.209), 
        (2.043, 2.322, 1.114, 0.191), 
        (2.322, 2.500, 1.347, 0.274), 
        (2.500, 2.893, 2.137, 0.524), 
        (2.853, 2.964, 1.65 , 0.941), 
        (2.964, 3.139, 1.225, 0.194), 
        (3.139, 5.191, 1.082, 0.198), 
        ]

        }

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
def getJER(jetEta, sysType, year="2016"):
    """
    Here, jetEta should be the jet pseudorapidity, and sysType is:
        nominal : 0
        down    : -1
        up      : +1
    """

    if sysType not in [0, -1, 1]:
        raise Exception('ERROR: Unable to get JER! use type=0 (nom), -1 (down), +1 (up)')

    for (etamin, etamax, scale_nom, scale_uncert) in jet_energy_resolution[year]:
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
    def __init__(self,inputmap,year='2016'):
        for minrun,maxrun,version in inputmap:
            JECMap = {}
            JECMap['jecAK4'] = createJEC('JECs/'+year+'/'+version, ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual'], 'AK4PFchs')
            JECMap['jecUncAK4'] = ROOT.JetCorrectionUncertainty(ROOT.std.string('JECs/'+year+'/'+version+'_Uncertainty_AK4PFchs.txt'))
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

triggers_of_interest = [
["SingleMuon",muon_triggers_of_interest],
["SingleElectron",electron_triggers_of_interest],
["DileptonMuE",dilepmue_triggers_of_interest],
["DileptonEMu",dilepemu_triggers_of_interest],
["DileptonMuMu",dilepmumu_triggers_of_interest],
["DileptonEE",dilepee_triggers_of_interest]
]

################################################################################






################################################################################
# Pass in a slimmedJets object
################################################################################
def process_jets(jets, outdata, options, runnumber=None, jecAK4=None, jecUncAK4=None, DataJECs=None, NPV=1, rho=None, verbose=False): 

    ############################################
    # Get the AK4 jet nearest the lepton:
    ############################################
    if verbose:
        print("-------------")
        print("{0:10} {1:10} {2:10} {3:10} {4:10} {5:10}".format("Index", "probb", "probb", "sum", "eta", "pt"))
    sf = []
    i=0
    for jet in jets.product():

        # We're only going to look at the first 16 jets
        if i>=16:
            break

        # Get the jet p4
        jetP4Raw = ROOT.TLorentzVector( jet.px(), jet.py(), jet.pz(), jet.energy() )
        # Get the correction that was applied at RECO level for MINIAOD
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

        if not goodJet:
            continue

        ############################################################
        # Apply new JEC's and smear MC resolutions
        ############################################################
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
            smear     = getJER( eta,  0, options.year)
            smearUp   = getJER( eta,  1, options.year)
            smearDn   = getJER( eta, -1, options.year)
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
        jetP4 = jetP4Raw * newJEC * ptsmear
        if options.verbose:
            print("           PT         E        Px        Py       Pz")
            print("UNCORR: ",jetP4Raw.Pt(), jetP4Raw.E(), jetP4Raw.Px(), jetP4Raw.Py(), jetP4Raw.Pz())
            print("CORR  : ",jetP4.Pt(), jetP4.E(), jetP4.Px(), jetP4.Py(), jetP4.Pz())


        #btagvar = jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")
        btagvar_probb = jet.bDiscriminator("pfDeepCSVJetTags:probb")
        btagvar_probbb = jet.bDiscriminator("pfDeepCSVJetTags:probbb")

        if verbose:
            print("{0:10d} {1:10.3f} {2:10.3f} {3:10.3f} {4:10.3f} {5:10.3f}".format(i,btagvar_probb,btagvar_probbb, btagvar_probb+btagvar_probbb, abs(jet.eta()), jet.pt()))

        #sf.append(reader.eval(0, abs(jet.eta()), jet.pt()))  # jet flavor, abs(eta), pt

        outdata['jete'][i] = jetP4.E()
        outdata['jetpx'][i] = jetP4.Px()
        outdata['jetpy'][i] = jetP4.Py()
        outdata['jetpz'][i] = jetP4.Pz()

        outdata['jetpt'][i] = jetP4.Pt()
        outdata['jeteta'][i] = jetP4.Eta()
        outdata['jetphi'][i] = jetP4.Phi()

        outdata['jetbtag0'][i] = jet.bDiscriminator("pfDeepCSVJetTags:probb")
        outdata['jetbtag1'][i] = jet.bDiscriminator("pfDeepCSVJetTags:probbb")
        outdata['jetbtagsum'][i] = outdata['jetbtag0'][i] + outdata['jetbtag1'][i]

        outdata['jetarea'][i] = jet.jetArea()
        outdata['jetNHF'][i] = jet.neutralHadronEnergyFraction()

        outdata['jetNHF'][i] = jet.neutralHadronEnergyFraction();
        outdata['jetNEMF'][i] = jet.neutralEmEnergyFraction();
        outdata['jetCHF'][i] = jet.chargedHadronEnergyFraction();
        outdata['jetMUF'][i] = jet.muonEnergyFraction();
        outdata['jetCEMF'][i] = jet.chargedEmEnergyFraction();
        outdata['jetNumConst'][i] = jet.chargedMultiplicity()+jet.neutralMultiplicity();
        outdata['jetNumNeutralParticles'][i] =jet.neutralMultiplicity();
        outdata['jetCHM'][i] = jet.chargedMultiplicity();

        i += 1


    outdata['njet'][0] = i



################################################################################
# Pass in a slimmedMuons object
################################################################################
def process_muons(muons, outdata, verbose=False): 

    if verbose:
        output = "-------------\n"
        output += "{0:10} {1:10} {2:10}".format("Index", "eta", "pt")
        output += "{0:12} {1:12} {2:12} ".format('muonIsLoose', 'muonIsMedium', 'muonIsTight')
        output += "{0:15} {1:15} {2:15} ".format('muonPFIsoLoose', 'muonPFIsoMedium', 'muonPFIsoTight')
        output += "{0:12} {1:12} {2:12} ".format('muonMvaLoose', 'muonMvaMedium', 'muonMvaTight')
        print(output)
    
    i=0
    for i,muon in enumerate(muons.product()):

        # We're only going to look at the first 16 muons
        if i>=16:
            break

        outdata['muone'][i] = muon.energy()
        outdata['muonpx'][i] = muon.px()
        outdata['muonpy'][i] = muon.py()
        outdata['muonpz'][i] = muon.pz()

        outdata['muonpt'][i] = muon.pt()
        outdata['muoneta'][i] = muon.eta()
        outdata['muonphi'][i] = muon.phi()

        outdata['muonq'][i] = muon.charge()

        pfi  = muon.pfIsolationR04()

        outdata['muonsumchhadpt'][i] = pfi.sumChargedHadronPt
        outdata['muonsumnhadpt'][i] = pfi.sumNeutralHadronEt
        outdata['muonsumphotEt'][i] = pfi.sumPhotonEt
        outdata['muonsumPUPt'][i] = pfi.sumPUPt

        # https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2#Muon_selectors_Since_9_4_X
        # https://github.com/cms-sw/cmssw/blob/CMSSW_9_4_X/DataFormats/MuonReco/interface/Muon.h#L188-L212
        outdata['muonIsLoose'][i] = muon.passed(muon.CutBasedIdLoose)
        outdata['muonIsMedium'][i] = muon.passed(muon.CutBasedIdMedium)
        outdata['muonIsTight'][i] = muon.passed(muon.CutBasedIdTight)

        outdata['muonPFiso'][i] = (outdata['muonsumchhadpt'][i] + max(0., outdata['muonsumnhadpt'][i] + outdata['muonsumphotEt'][i] - 0.5*outdata['muonsumPUPt'][i]))/outdata['muonpt'][i]


        outdata['muonPFIsoLoose'][i] = muon.passed(muon.PFIsoLoose)
        outdata['muonPFIsoMedium'][i] = muon.passed(muon.PFIsoMedium)
        outdata['muonPFIsoTight'][i] = muon.passed(muon.PFIsoTight)

        outdata['muonMvaLoose'][i] = muon.passed(muon.MvaLoose)
        outdata['muonMvaMedium'][i] = muon.passed(muon.MvaMedium)
        outdata['muonMvaTight'][i] = muon.passed(muon.MvaTight)

        if verbose:
            output = "{0:10d} {1:10.3f} {2:10.3f} ".format(i, abs(muon.eta()), muon.pt())
            output += "{0:12.3f} {1:12.3f} {2:12.3f} ".format(outdata['muonIsLoose'][i], outdata['muonIsMedium'][i], outdata['muonIsTight'][i])
            output += "{0:15.3f} {1:15.3f} {2:15.3f} ".format(outdata['muonPFIsoLoose'][i], outdata['muonPFIsoMedium'][i], outdata['muonPFIsoTight'][i])
            output += "{0:12.3f} {1:12.3f} {2:12.3f} ".format(outdata['muonMvaLoose'][i], outdata['muonMvaMedium'][i], outdata['muonMvaTight'][i])
            print(output)

    outdata['nmuon'][0] = i




################################################################################
# Pass in a slimmedElectrons object
################################################################################
def process_electrons(electrons, outdata, year='2016', verbose=False): 

    # https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2
    # https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2#Recipe_for_FWLite
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedElectronIdentificationRun2#Working_points_for_94X_and_later

    if verbose:
        print("-------------")
        print("Electrons")
        print("-------------")
        print("{0:10} {1:10} {2:10} {3:10} {4:10} {5:10}".format("Index", "eta", "pt", "loose", "medium", "tight"))
    
    i=0
    for i,electron in enumerate(electrons.product()):

        # We're only going to look at the first 16 electrons
        if i>=16:
            break

        outdata['electrone'][i] = electron.energy()
        outdata['electronpx'][i] = electron.px()
        outdata['electronpy'][i] = electron.py()
        outdata['electronpz'][i] = electron.pz()

        outdata['electronpt'][i] = electron.pt()
        outdata['electroneta'][i] = electron.eta()
        outdata['electronphi'][i] = electron.phi()

        outdata['electronq'][i] = electron.charge()

        #outdata['electronIsLoose'][i] = int(electron.electronID("cutBasedElectronID-Summer16-80X-V1-loose"))
        #outdata['electronIsMedium'][i] = int(electron.electronID("cutBasedElectronID-Summer16-80X-V1-medium"))
        #outdata['electronIsTight'][i] = int(electron.electronID("cutBasedElectronID-Summer16-80X-V1-tight"))
        # Do we have to change this to V2 at some point?
        # https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedElectronIdentificationRun2#Working_points_for_94X_and_later
        outdata['electronIsLoose'][i] = int(electron.electronID("cutBasedElectronID-Fall17-94X-V1-loose"))
        outdata['electronIsMedium'][i] = int(electron.electronID("cutBasedElectronID-Fall17-94X-V1-medium"))
        outdata['electronIsTight'][i] = int(electron.electronID("cutBasedElectronID-Fall17-94X-V1-tight"))

        outdata['electronTkIso'][i] = electron.dr03TkSumPt()
        outdata['electronHCIso'][i] = electron.dr03HcalTowerSumEt()
        outdata['electronECIso'][i] = electron.dr03EcalRecHitSumEt()

        if verbose:
            print("{0:10d} {1:10.3f} {2:10.3f} {3:10d} {4:10d} {5:10d}".format(i, abs(electron.eta()), electron.pt(), outdata['electronIsLoose'][i], outdata['electronIsMedium'][i],outdata['electronIsTight'][i],  ))


    outdata['nelectron'][0] = i



################################################################################
# Pass in a slimmedPrimaryVertices object
################################################################################
def process_vertices(vertices, outdata, verbose=False): 

    PV = None # Primary vertex
    NPV = 0 # Number of primary vertices
    # Vertices

    outdata['nvertex'][0] = len(vertices.product())

    if len(vertices.product()) == 0 or vertices.product()[0].ndof() < 4:
        if verbose:
            print ("Event has no good primary vertex.")
        return PV,0
    else:
        # This assigning of the first entry to the primary vertex (PV) is something we
        # took from other code, but I don't actually know if it's true. 
        PV = vertices.product()[0]
        NPV = len(vertices.product())
        if verbose:
            print("--------------\nPrimary vertex first")
            print("PV at x,y,z = %+5.3f, %+5.3f, %+6.3f (ndof %.1f)" % (PV.x(), PV.y(), PV.z(), PV.ndof()))

        for i,vertex in enumerate(vertices.product()):

            if i>=64:
                break

            outdata['vertexX'][i] = vertex.x()
            outdata['vertexY'][i] = vertex.y()
            outdata['vertexZ'][i] = vertex.z()
            outdata['vertexndof'][i] = vertex.ndof()

            if verbose:
                print ("      x,y,z = %+5.3f, %+5.3f, %+6.3f (ndof %.1f)" % (vertex.x(), vertex.y(), vertex.z(), vertex.ndof()))

        outdata['nvertex'][0] = i

    return PV,NPV


################################################################################
# Pass in a slimmedMETs object
################################################################################
def process_mets(mets, outdata, verbose=False): 

    #######################################################################
    # MET, Missing energy in transverse plane
    # https://indico.cern.ch/event/662371/contributions/2823187/attachments/1574267/2496977/PileupMET_DAS2018LPC.pdf
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideCMSDataAnalysisSchoolLPC2018METandPileupExercise
    #######################################################################
    
    met = mets.product().front()

    outdata['metpt'][0] = met.pt()
    outdata['metphi'][0] = met.phi()

    if verbose:
        print("{0:10} {1:10}".format("metpt", "metphi"))
        print("{0:10.3f} {1:10.3f}".format(outdata["metpt"][0], outdata["metphi"][0]))


################################################################################
# Pass in a fixedGridRhoAll object
################################################################################
def process_rhos(rhos, verbose=False): 

    # Rhos
    if len(rhos.product()) == 0:
        print ("Event has no rho values.")
        return None
    else:
        rho = rhos.product()[0]
        if verbose:
            print ('rho = {0:6.2f}'.format( rho ))
    
    return rho





################################################################################
# Pass in a slimmedAddPileupInfo object
################################################################################
def process_pileup(pileups, outdata, purw, options, verbose=False): 

    # https://github.com/mattbellis/Top_BNV/blob/master/scratch/MAKE_ALL_THE_PILEUP_INFO.md
    outdata['pu_wt'][0] = -1

    TrueNumInteractions = 0
    if len(pileups.product())>0:
        TrueNumInteractions = pileups.product()[0].getTrueNumInteractions()
    else:
        print 'Event has no pileup information, setting TrueNumInteractions to 0.'

    if options.isMC and not options.disablePileup and purw is not None:
        outdata['pu_wt'][0] = purw.GetBinContent( purw.GetXaxis().FindBin( TrueNumInteractions ) )

        if verbose:
            print("Num interactions/pileup reweighting {0:10} {1:10}".format(TrueNumInteractions, outdata['pu_wt'][0]))

    else:
        outdata['pu_wt'][0] = 1.0







################################################################################
# Pass in a slimmedAddPileupInfo object
################################################################################
def process_pileup(pileups, outdata, purw, options, verbose=False): 

    # https://github.com/mattbellis/Top_BNV/blob/master/scratch/MAKE_ALL_THE_PILEUP_INFO.md
    outdata['pu_wt'][0] = -1

    TrueNumInteractions = 0
    if len(pileups.product())>0:
        TrueNumInteractions = pileups.product()[0].getTrueNumInteractions()
    else:
        print 'Event has no pileup information, setting TrueNumInteractions to 0.'

    if options.isMC and not options.disablePileup and purw is not None:
        outdata['pu_wt'][0] = purw.GetBinContent( purw.GetXaxis().FindBin( TrueNumInteractions ) )

        if verbose:
            print("Num interactions/pileup reweighting {0:10} {1:10}".format(TrueNumInteractions, outdata['pu_wt'][0]))

    else:
        outdata['pu_wt'][0] = 1.0



################################################################################
# Pass in a triggerResults object
################################################################################
def process_triggers(triggerBits, triggerPrescales, trigger_names, trigger_tree_branches, outdata, options, verbose=False): 

    # Get list of triggers that fired
    outdata['ntrig_muon'][0] = len(muon_triggers_of_interest)
    outdata['ntrig_electron'][0] = len(electron_triggers_of_interest)
    outdata['ntrig_dilepmue'][0] = len(dilepmue_triggers_of_interest)
    outdata['ntrig_dilepemu'][0] = len(dilepemu_triggers_of_interest)
    outdata['ntrig_dilepmumu'][0] = len(dilepmumu_triggers_of_interest)
    outdata['ntrig_dilepee'][0] = len(dilepee_triggers_of_interest)

    '''
    print()
    print(triggerBits)
    print(type(triggerBits))
    print(triggerBits.product())
    print()
    print(triggerPrescales)
    print(type(triggerPrescales))
    print(triggerPrescales.product())
    '''
    trigger_prescales = triggerPrescales.product()

    #print("------- Triggers ---------")
    # Zero out the triggers
    for toi in triggers_of_interest:

        trigger_type = toi[0]
        trigger_bit_names = toi[1]

        for iname,name in enumerate(trigger_bit_names):
            trigger_tree_branches[trigger_type][iname] = 0 # Didn't fire!
            #if verbose:
            if 0:
                print("Zeroing out {0} {1}".format(trigger_type, name))

    # Run over the triggers and see what fired
    FLAG_passed_trigger = False
    # Loop over *all* the stored triggers
    for itrig in xrange(triggerBits.product().size()):

        if triggerBits.product().accept(itrig):
            trigname = trigger_names.triggerName(itrig)

            prescale = trigger_prescales.getPrescaleForIndex(itrig)
            #print(prescale)


            #if verbose:
            if 0:
                print("Checking on trigger {0}".format(trigname))

            mc_selection = True

            # Loop over the triggers that we are interested in
            for toi in triggers_of_interest:

                # trigger_type is our labeling of SingleMuon, SingleElectron, etc.
                trigger_type = toi[0]
                trigger_bit_names = toi[1]

                for iname,name in enumerate(trigger_bit_names):

                    if options.isMC:
                        mc_selection = trigname.find(name[1]) # This is the version, like v4, v6, etc.

                    if trigname.find(name[0]) >= 0 and mc_selection:
                        #print(trigname,trigger_type)
                        #print(iname,trigger_tree_branches[trigger_type])
                        #print(iname,trigger_tree_branches[trigger_type].Name())
                        trigger_tree_branches[trigger_type][iname] = 1 # Fired!
                        if trigger_type == options.trigType:
                            FLAG_passed_trigger = True
                            if verbose:
                                print("PASSED TRIGGER REQUIREMENT for {0} {1}".format(trigger_type, name[0]))
                        #else:
                            #trigger_tree_branches[trigger_type][iname] = 0 # Didn't fire!


    return FLAG_passed_trigger







