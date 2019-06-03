# Much of this is from the B2G data analysis school code

import ROOT, copy, sys, logging
from array import array
from DataFormats.FWLite import Events, Handle
from DataFormats.FWLite import Events, Handle

import fwlite_tools

# NEED THIS FOR DEEP CSV STUFF?
from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection



# https://twiki.cern.ch/twiki/bin/viewauth/CMS/JECDataMC
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
    add_option('disablePileup',      default=False, action='store_true',
        help='Disable pileup reweighting')

    (options, args) = parser.parse_args(argv)
    argv = []

    print ('===== Command line options =====')
    print (options)
    print ('================================')
    return options

#####################################################################################
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

    ######## ##      ## ##       #### ######## ########     ######  ######## ##     ## ######## ######## 
    ##       ##  ##  ## ##        ##     ##    ##          ##    ##    ##    ##     ## ##       ##       
    ##       ##  ##  ## ##        ##     ##    ##          ##          ##    ##     ## ##       ##       
    ######   ##  ##  ## ##        ##     ##    ######       ######     ##    ##     ## ######   ######   
    ##       ##  ##  ## ##        ##     ##    ##                ##    ##    ##     ## ##       ##       
    ##       ##  ##  ## ##        ##     ##    ##          ##    ##    ##    ##     ## ##       ##       
    ##        ###  ###  ######## ####    ##    ########     ######     ##     #######  ##       ##       

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
    pileups, pileuplabel = Handle("std::vector<PileupSummaryInfo>"), "slimmedAddPileupInfo"

    # NEED HLT2 for 80x 2016 (maybe only TTBar?
    # https://twiki.cern.ch/twiki/bin/view/CMS/TopTrigger#Summary_for_2016_Run2016B_H_25_n
    triggerBits, triggerBitLabel = Handle("edm::TriggerResults"), ("TriggerResults","", "HLT")
    #triggerPrescales, triggerPrescalesLabel = Handle("pat::PackedTriggerPrescales"), ("PackedTriggerPrescales","", "HLT")
    #triggerPrescales, triggerPrescalesLabel = Handle("pat::PackedTriggerPrescales"), ("TriggerUserData","", "HLT")
    triggerPrescales, triggerPrescalesLabel  = Handle("pat::PackedTriggerPrescales"), "patTrigger"




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

    #################################################################################
    #################################################################################
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

    # Weights
    ev_wt = array('f', [-1])
    outtree.Branch('ev_wt', ev_wt, 'ev_wt/F')
    pu_wt = array('f', [-1])
    outtree.Branch('pu_wt', pu_wt, 'pu_wt/F')
    gen_wt = array('f', [-1])
    outtree.Branch('gen_wt', gen_wt, 'gen_wt/F')


    #################################################################################
    #################################################################################
    # Muons
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideCMSDataAnalysisSchoolLPC2018Muons
    # https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2
    # https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2#Muon_Identification
    muondata = {}
    muondata['nmuon'] = ['muonpt', 'muoneta', 'muonphi', 'muone', 'muonpx', 'muonpy', 'muonpz', 'muonq']
    muondata['nmuon'] += ['muonsumchhadpt', 'muonsumnhadpt', 'muonsumphotEt', 'muonsumPUPt']
    muondata['nmuon'] += ['muonIsLoose', 'muonIsMedium', 'muonIsTight', 'muonPFiso']
    muondata['nmuon'] += ['muonPFIsoLoose', 'muonPFIsoMedium', 'muonPFIsoTight']
    muondata['nmuon'] += ['muonMvaLoose', 'muonMvaMedium', 'muonMvaTight']

    outMuons = {}
    for key in muondata.keys():

        outMuons[key] = array('i', [-1])
        outtree.Branch(key, outMuons[key], key+"/I")

        for branch in muondata[key]:
            outMuons[branch] = array('f', 16*[-1.])
            outtree.Branch(branch, outMuons[branch], '{0}[{1}]/F'.format(branch,key))


    #################################################################################
    #################################################################################
    # Electrons
    # https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2
    # https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideCMSDataAnalysisSchoolLPC2018egamma
    electrondata = {}
    electrondata['nelectron'] = {}
    electrondata['nelectron']['F'] = ['electronpt', 'electroneta', 'electronphi', 'electrone', 'electronpx', 'electronpy', 'electronpz', 'electronq']
    electrondata['nelectron']['F'] += ['electronTkIso', 'electronHCIso', 'electronECIso']
    electrondata['nelectron']['I'] = ['electronIsLoose', 'electronIsMedium', 'electronIsTight'] # These are nominally integers

    datatypes = {"F":['f',-1.0], "I":['i',-1]}
    
    outElectrons = {}
    for key in electrondata.keys():

        outElectrons[key] = array('i', [-1])
        outtree.Branch(key, outElectrons[key], key+"/I")

        print(key)
        for datatype in electrondata[key]:
            print(datatype)
            for branch in electrondata[key][datatype]:
                outElectrons[branch] = array(datatypes[datatype][0], 16*[datatypes[datatype][1]])
                outtree.Branch(branch, outElectrons[branch], '{0}[{1}]/{2}'.format(branch,key,datatype))



    ############################################################################
    #################################################################################
    # MET 
    
    metdata = ['metpt', 'metphi']

    outMET = {}
    for key in metdata:
        outMET[key] = array('f', [-1])
        outtree.Branch(key, outMET[key], key+"/F")


    #################################################################################
    #################################################################################
    # Vertex/Trigger

    trigdata = {}
    trigdata['ntrig_muon'] = ['trig_muon']
    trigdata['ntrig_electron'] = ['trig_electron']
    trigdata['ntrig_dilepmue'] = ['trig_dilepmue']
    trigdata['ntrig_dilepemu'] = ['trig_dilepemu']
    trigdata['ntrig_dilepmumu'] = ['trig_dilepmumu']
    trigdata['ntrig_dilepee'] = ['trig_dilepee']

    outTriggers = {}
    for key in trigdata.keys():
        print(key)
        outTriggers[key] = array('i', [-1])
        outtree.Branch(key, outTriggers[key], key+"/I")

        for branch in trigdata[key]:
            # Save them as integers
            outTriggers[branch] = array('i', 8*[-1])
            outtree.Branch(branch, outTriggers[branch], '{0}[{1}]/I'.format(branch,key))

    trigger_tree_branches = {
        "SingleMuon":outTriggers['trig_muon'],
        "SingleElectron":outTriggers['trig_electron'],
        "DileptonMuE":outTriggers['trig_dilepmue'],
        "DileptonEMu":outTriggers['trig_dilepemu'],
        "DileptonMuMu":outTriggers['trig_dilepmumu'],
        "DileptonEE":outTriggers['trig_dilepee']
    }





          ## ######## ########     ######   #######  ########  ########  ########  ######  ######## ####  #######  ##    ##  ######  
          ## ##          ##       ##    ## ##     ## ##     ## ##     ## ##       ##    ##    ##     ##  ##     ## ###   ## ##    ## 
          ## ##          ##       ##       ##     ## ##     ## ##     ## ##       ##          ##     ##  ##     ## ####  ## ##       
          ## ######      ##       ##       ##     ## ########  ########  ######   ##          ##     ##  ##     ## ## ## ##  ######  
    ##    ## ##          ##       ##       ##     ## ##   ##   ##   ##   ##       ##          ##     ##  ##     ## ##  ####       ## 
    ##    ## ##          ##       ##    ## ##     ## ##    ##  ##    ##  ##       ##    ##    ##     ##  ##     ## ##   ### ##    ## 
    ######  ########    ##        ######   #######  ##     ## ##     ## ########  ######     ##    ####  #######  ##    ##  ######  
    
    
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
    
    
    # from within CMSSW:
    ROOT.gSystem.Load('libCondFormatsBTauObjects')
    ROOT.gSystem.Load('libCondToolsBTau')





    ######## ##     ## ######## ##    ## ########    ##        #######   #######  ########  
    ##       ##     ## ##       ###   ##    ##       ##       ##     ## ##     ## ##     ## 
    ##       ##     ## ##       ####  ##    ##       ##       ##     ## ##     ## ##     ## 
    ######   ##     ## ######   ## ## ##    ##       ##       ##     ## ##     ## ########  
    ##        ##   ##  ##       ##  ####    ##       ##       ##     ## ##     ## ##        
    ##         ## ##   ##       ##   ###    ##       ##       ##     ## ##     ## ##        
    ########    ###    ######## ##    ##    ##       ########  #######   #######  ##        


    # IMPORTANT : Run one FWLite instance per file. Otherwise,
    # FWLite aggregates ALL of the information immediately, which
    # can take a long time to parse.
    
    #################################################################################
    #################################################################################
    def processEvent(iev, event):
        
        ###########################################################################
        ###########################################################################
        # Vertex/Trigger

        event.getByLabel(triggerBitLabel, triggerBits)
        event.getByLabel(triggerPrescalesLabel, triggerPrescales )

        trigger_names = event.object().triggerNames(triggerBits.product())

        FLAG_passed_trigger = fwlite_tools.process_triggers(triggerBits, triggerPrescales, trigger_names, trigger_tree_branches, outdata, options, verbose=options.verbose)

        # Should do this early. We shouldn't analyze events that don't
        # pass any of the relevant triggers
        if FLAG_passed_trigger is False:
            return 0

        ###########################################################################
        ###########################################################################
        # If trigger test is passed, process event

        ev_wt[0] = 1.0
        pu_wt[0] = 1.0
        gen_wt[0] = 1.0

        genOut = "Event %d\n" % (iev)
        #print "GGGEEENNNNOUT...."
        #print genOut

        #event.getByLabel(triggerBitLabel, triggerBits)
        #event.getByLabel(metfiltBitLabel, metfiltBits)
        runnumber = event.eventAuxiliary().run()

        if options.verbose:
            print( "\nProcessing %d: run %6d, lumi %4d, event %12d" % \
                  (iev,event.eventAuxiliary().run(), \
                  event.eventAuxiliary().luminosityBlock(), \
                  event.eventAuxiliary().event()))


              ## ######## ########     ######  ######## ##       ########  ######  ######## ####  #######  ##    ## 
              ## ##          ##       ##    ## ##       ##       ##       ##    ##    ##     ##  ##     ## ###   ## 
              ## ##          ##       ##       ##       ##       ##       ##          ##     ##  ##     ## ####  ## 
              ## ######      ##        ######  ######   ##       ######   ##          ##     ##  ##     ## ## ## ## 
        ##    ## ##          ##             ## ##       ##       ##       ##          ##     ##  ##     ## ##  #### 
        ##    ## ##          ##       ##    ## ##       ##       ##       ##    ##    ##     ##  ##     ## ##   ### 
         ######  ########    ##        ######  ######## ######## ########  ######     ##    ####  #######  ##    ## 

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


        ############################################
        # Get the AK4 jet nearest the lepton:
        ############################################
        print("-------------")
        print("{0:10} {1:10} {2:10} {3:10} {4:10} {5:10}".format("Index", "probb", "probb", "sum", "eta", "pt"))
        sf = []
        for i,jet in enumerate(jets.product()):
            # Get the jet p4
            jetP4Raw = ROOT.TLorentzVector( jet.px(), jet.py(), jet.pz(), jet.energy() )
            # Get the correction that was applied at RECO level for MINIAOD
            jetJECFromMiniAOD = jet.jecFactor(0)
            # Remove the old JEC's to get raw energy
            jetP4Raw *= jetJECFromMiniAOD
            # Apply jet ID

            btagvar_probb = jet.bDiscriminator("pfDeepCSVJetTags:probb")
            btagvar_probbb = jet.bDiscriminator("pfDeepCSVJetTags:probbb")

            print("{0:10d} {1:10.3f} {2:10.3f} {3:10.3f} {4:10.3f} {5:10.3f}".format(i,btagvar_probb,btagvar_probbb, btagvar_probb+btagvar_probbb, abs(jet.eta()), jet.pt()))



        ###########################################################################
        ###########################################################################
        # Muons

        event.getByLabel (muonLabel, muons)
        fwlite_tools.process_muons(muons, outMuons, verbose=options.verbose)

        ###########################################################################
        ###########################################################################
        # Electrons

        event.getByLabel (electronLabel, electrons)
        fwlite_tools.process_electrons(electrons, outElectrons, verbose=options.verbose)

        ###########################################################################
        ###########################################################################
        # MET

        event.getByLabel( metLabel, mets )
        fwlite_tools.process_mets(mets, outMET, verbose=options.verbose)




        ######## #### ##       ##          ######## ########  ######## ######## 
        ##        ##  ##       ##             ##    ##     ## ##       ##       
        ##        ##  ##       ##             ##    ##     ## ##       ##       
        ######    ##  ##       ##             ##    ########  ######   ######   
        ##        ##  ##       ##             ##    ##   ##   ##       ##       
        ##        ##  ##       ##             ##    ##    ##  ##       ##       
        ##       #### ######## ########       ##    ##     ## ######## ######## 
        
        outtree.Fill()
        #print("Made it to end!")

        return genOut



    ###########################################################################
    ###########################################################################
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

    #outtree.Print()
    # Close the output ROOT file
    f.cd()
    f.Write()
    f.Close()

    #genoutputfile.close()



#####################################################################################
#####################################################################################
if __name__ == "__main__":
    topbnv_fwlite(sys.argv)


