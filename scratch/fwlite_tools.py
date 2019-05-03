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
    add_option('localInputFiles',    default=False, action='store_true',
        help='Use this flag when running with with local files')
    add_option('disablePileup',      default=False, action='store_true',
        help='Disable pileup reweighting')



    (options, args) = parser.parse_args(argv)
    argv = []

    return options
#####################################################################################





################################################################################
# Pass in a slimmedJets object
################################################################################
def process_jets(jets, outdata, verbose=False): 

    ############################################
    # Get the AK4 jet nearest the lepton:
    ############################################
    if verbose:
        print("-------------")
        print("{0:10} {1:10} {2:10} {3:10} {4:10} {5:10}".format("Index", "probb", "probb", "sum", "eta", "pt"))
    sf = []
    i=0
    for i,jet in enumerate(jets.product()):

        # We're only going to look at the first 16 jets
        if i>=16:
            break

        ############# NEED TO FIGURE OUT IF WE ARE DOING CORRECTIONS THIS WAY FOR 9_4_X!!!!!!!!!
        # Get the jet p4
        jetP4Raw = ROOT.TLorentzVector( jet.px(), jet.py(), jet.pz(), jet.energy() )
        # Get the correction that was applied at RECO level for MINIAOD
        jetJECFromMiniAOD = jet.jecFactor(0)
        # Remove the old JEC's to get raw energy
        jetP4Raw *= jetJECFromMiniAOD
        # Apply jet ID

        #btagvar = jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")
        btagvar_probb = jet.bDiscriminator("pfDeepCSVJetTags:probb")
        btagvar_probbb = jet.bDiscriminator("pfDeepCSVJetTags:probbb")

        if verbose:
            print("{0:10d} {1:10.3f} {2:10.3f} {3:10.3f} {4:10.3f} {5:10.3f}".format(i,btagvar_probb,btagvar_probbb, btagvar_probb+btagvar_probbb, abs(jet.eta()), jet.pt()))

        #sf.append(reader.eval(0, abs(jet.eta()), jet.pt()))  # jet flavor, abs(eta), pt

        outdata['jete'][i] = jet.energy()
        outdata['jetpx'][i] = jet.px()
        outdata['jetpy'][i] = jet.py()
        outdata['jetpz'][i] = jet.pz()

        outdata['jetpt'][i] = jet.pt()
        outdata['jeteta'][i] = jet.eta()
        outdata['jetphi'][i] = jet.phi()

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
def process_electrons(electrons, outdata, verbose=False): 

    # https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2
    # https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2#Recipe_for_FWLite

    if verbose:
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

        outdata['electronIsLoose'][i] = electron.electronID("cutBasedElectronID-Summer16-80X-V1-loose")
        outdata['electronIsMedium'][i] = electron.electronID("cutBasedElectronID-Summer16-80X-V1-medium")
        outdata['electronIsTight'][i] = electron.electronID("cutBasedElectronID-Summer16-80X-V1-tight")

        outdata['electronTkIso'][i] = electron.dr03TkSumPt()
        outdata['electronHCIso'][i] = electron.dr03HcalTowerSumEt()
        outdata['electronECIso'][i] = electron.dr03EcalRecHitSumEt()

        if verbose:
            print("{0:10d} {1:10.3f} {2:10.3f} {3:10.3f} {4:10.3f} {5:10.3f}".format(i, abs(electron.eta()), electron.pt(), outdata['electronIsLoose'][i], outdata['electronIsMedium'][i],outdata['electronIsTight'][i],  ))


    outdata['nelectron'][0] = i



################################################################################
# Pass in a slimmedPrimaryVertices object
################################################################################
def process_vertices(vertices, outdata, verbose=False): 

    PV = None # Primary vertex
    # Vertices

    outdata['nvertex'][0] = len(vertices.product())

    if len(vertices.product()) == 0 or vertices.product()[0].ndof() < 4:
        if verbose:
            print ("Event has no good primary vertex.")
        return PV
    else:
        # This assigning of the first entry to the primary vertex (PV) is something we
        # took from other code, but I don't actually know if it's true. 
        PV = vertices.product()[0]
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

    return PV


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




