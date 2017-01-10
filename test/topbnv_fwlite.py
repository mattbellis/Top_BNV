# Much of this is from the B2G data analysis school code

import ROOT, copy, sys, logging
from array import array
from DataFormats.FWLite import Events, Handle
# Use the VID framework for the electron ID. Tight ID without the PF isolation cut.
from RecoEgamma.ElectronIdentification.VIDElectronSelector import VIDElectronSelector
from RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_25ns_V1_cff import cutBasedElectronID_Spring15_25ns_V1_standalone_tight
from RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_nonTrig_V1_cff import mvaEleID_Spring15_25ns_nonTrig_V1_wp80

############################################
# Command line parsing

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

    add_option('trigProc',           default='HLT',
        help='Name of trigger process')
    add_option('trigProcMETFilters', default='PAT',
        help='Name of trigger process for MET filters')


    (options, args) = parser.parse_args(argv)
    argv = []

    print '===== Command line options ====='
    print options
    print '================================'
    return options






#####################################################################################
def b2gdas_fwlite(argv):
    ## _____________      __.____    .__  __             _________ __          _____  _____
    ## \_   _____/  \    /  \    |   |__|/  |_  ____    /   _____//  |_ __ ___/ ____\/ ____\
    ##  |    __) \   \/\/   /    |   |  \   __\/ __ \   \_____  \\   __\  |  \   __\\   __\
    ##  |     \   \        /|    |___|  ||  | \  ___/   /        \|  | |  |  /|  |   |  |
    ##  \___  /    \__/\  / |_______ \__||__|  \___  > /_______  /|__| |____/ |__|   |__|
    ##      \/          \/          \/             \/          \/

    options = getUserOptions(argv)
    ROOT.gROOT.Macro("rootlogon.C")

    print argv
    print options

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
    genInfo, genInfoLabel = Handle("GenEventInfoProduct"), "generator"
    # Enterprising students could figure out the LHE weighting for theoretical uncertainties
    #lheInfo, lheInfoLabel = Handle("LHEEventProduct"), "externalLHEProducer"
    triggerBits, triggerBitLabel = Handle("edm::TriggerResults"), ("TriggerResults","", options.trigProc)
    metfiltBits, metfiltBitLabel = Handle("edm::TriggerResults"), ("TriggerResults","", options.trigProcMETFilters)

    f = ROOT.TFile(options.output, "RECREATE")
    f.cd()

    def processEvent(iev, event):

        event.getByLabel(triggerBitLabel, triggerBits)
        event.getByLabel(metfiltBitLabel, metfiltBits)
        runnumber = event.eventAuxiliary().run()



    #########################################
    # Main event loop

    nevents = 0
    maxevents = int(options.maxevents)
    for ifile in getInputFiles(options):
        print 'Processing file ' + ifile
        events = Events (ifile)
        if maxevents > 0 and nevents > maxevents:
            break

        # loop over events in this file
        for iev, event in enumerate(events):

            if maxevents > 0 and nevents > maxevents:
                break
            nevents += 1

            if nevents % 1000 == 0:
                print '==============================================='
                print '    ---> Event ' + str(nevents)
            elif options.verbose:
                print '    ---> Event ' + str(nevents)

            processEvent(iev, events)

    # Close the output ROOT file
    f.cd()
    f.Write()
    f.Close()
    


#####################################################################################
if __name__ == "__main__":
    b2gdas_fwlite(sys.argv)


