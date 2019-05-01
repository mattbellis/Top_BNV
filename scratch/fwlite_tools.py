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
    add_option('localInputFiles',    default=False, action='store_true',
        help='Use this flag when running with with local files')


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
        print("-------------")
        print("{0:10} {1:10} {2:10}".format("Index", "eta", "pt"))
    
    i=0
    for i,muon in enumerate(muons.product()):

        # We're only going to look at the first 16 muons
        if i>=16:
            break

        if verbose:
            print("{0:10d} {1:10.3f} {2:10.3f}".format(i, abs(muon.eta()), muon.pt()))

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

        outdata['muonisLoose'][i] = int(muon.isLooseMuon())
        outdata['muonisMedium'][i] = int(muon.isMediumMuon())

        outdata['muonPFiso'][i] = (outdata['muonsumchhadpt'][i] + max(0., outdata['muonsumnhadpt'][i] + outdata['muonsumphotEt'][i] - 0.5*outdata['muonsumPUPt'][i]))/outdata['muonpt'][i]


    outdata['nmuon'][0] = i





