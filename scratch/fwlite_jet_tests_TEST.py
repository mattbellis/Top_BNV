# Much of this is from the B2G data analysis school code
#####################################################################################
import fwlite_tools
from fwlite_tools import jet_energy_corrections, jet_energy_correction_GT_for_MC 

import ROOT, sys
from array import array
from DataFormats.FWLite import Events, Handle

#####################################################################################
def topbnv_fwlite(argv):
    ## _____________      __.____    .__  __             _________ __          _____  _____
    ## \_   _____/  \    /  \    |   |__|/  |_  ____    /   _____//  |_ __ ___/ ____\/ ____\
    ##  |    __) \   \/\/   /    |   |  \   __\/ __ \   \_____  \\   __\  |  \   __\\   __\
    ##  |     \   \        /|    |___|  ||  | \  ___/   /        \|  | |  |  /|  |   |  |
    ##  \___  /    \__/\  / |_______ \__||__|  \___  > /_______  /|__| |____/ |__|   |__|
    ##      \/          \/          \/             \/          \/

    options = fwlite_tools.getUserOptions(argv)
    ROOT.gROOT.Macro("rootlogon.C")

    # Need these for the jec and jes
    vertices, vertexLabel = Handle("std::vector<reco::Vertex>"), "offlineSlimmedPrimaryVertices"
    rhos, rhoLabel = Handle("double"), "fixedGridRhoAll"

    jets, jetLabel = Handle("std::vector<pat::Jet>"), "slimmedJets"


    f = ROOT.TFile(options.output, "RECREATE")
    f.cd()

    outtree = ROOT.TTree("T", "Our tree of everything")

    # Jets
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideCMSDataAnalysisSchoolLPC2018Jets
    jetdata = {}
    jetdata['njet'] = ['jetpt', 'jeteta', 'jetphi', 'jete', 'jetpx', 'jetpy', 'jetpz']
    jetdata['njet'] += ['jetbtag0', 'jetbtag1', 'jetbtagsum']
    jetdata['njet'] += ['jetarea', 'jetjec', 'jetNHF', 'jetNEMF', 'jetCHF', 'jetCHM', 'jetMUF', 'jetCEMF']
    jetdata['njet'] += ['jetNumConst', 'jetNumNeutralParticles']

    outdata = {}
    for key in jetdata.keys():

        outdata[key] = array('i', [-1])
        outtree.Branch(key, outdata[key], key+"/I")

        for branch in jetdata[key]:
            outdata[branch] = array('f', 16*[-1.])
            outtree.Branch(branch, outdata[branch], '{0}[{1}]/F'.format(branch,key))

    ############################################################################
    # Vertex 
    ############################################################################
    vertexdata = {}
    vertexdata['nvertex'] = ['vertexX', 'vertexY', 'vertexZ', 'vertexndof']

    for key in vertexdata.keys():
        outdata[key] = array('i', [-1])
        outtree.Branch(key, outdata[key], key+"/I")

        for branch in vertexdata[key]:
            outdata[branch] = array('f', 64*[-1.])
            outtree.Branch(branch, outdata[branch], '{0}[{1}]/F'.format(branch,key))

    '''
    njet = array('i', [-1])
    outtree.Branch('njet', njet, 'njet/I')

    jetpt = array('f', 16*[-1.])
    outtree.Branch('jetpt', jetpt, 'jetpt[njet]/F')
    '''



    ############################################################################
    # Set things up to do jet energy corrections later
    ############################################################################
    ROOT.gSystem.Load('libCondFormatsJetMETObjects')
    if options.isMC:
        # CHANGE THIS FOR DIFFERENT MCs down the road
        jecAK4 = fwlite_tools.createJEC('JECs/Summer/'+jet_energy_correction_GT_for_MC, ['L1FastJet', 'L2Relative', 'L3Absolute'], 'AK4PFchs')
        jecUncAK4 = ROOT.JetCorrectionUncertainty(ROOT.std.string('JECs/Summer/'+jet_energy_correction_GT_for_MC+'_Uncertainty_AK4PFchs.txt'))
    else:
        # CHANGE THIS FOR DATA
        DataJECs = fwlite_tools.DataJEC(jet_energy_corrections)


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

        runnumber = event.eventAuxiliary().run()

        event.getByLabel(vertexLabel, vertices)
        event.getByLabel(rhoLabel, rhos)

        event.getByLabel (jetLabel, jets)          

        # Need the number of vertices and rho for jet energy corrections and smearing
        PV,NPV = fwlite_tools.process_vertices(vertices, outdata, verbose=options.verbose)
        if PV is None:
            return 0

        rho = fwlite_tools.process_rhos(rhos, verbose=options.verbose)
        if rho is None:
            return 0

        if options.isMC:
            fwlite_tools.process_jets(jets, outdata, options, jecAK4=jecAK4, jecUncAK4=jecUncAK4, runnumber=runnumber, rho=rho, NPV=NPV, verbose=options.verbose)
        else:
            fwlite_tools.process_jets(jets, outdata, options, DataJECs=DataJECs, runnumber=runnumber, rho=rho, NPV=NPV, verbose=options.verbose)


        ## ___________.__.__  .__    ___________
        ## \_   _____/|__|  | |  |   \__    ___/______   ____   ____
        ##  |    __)  |  |  | |  |     |    |  \_  __ \_/ __ \_/ __ \
        ##  |     \   |  |  |_|  |__   |    |   |  | \/\  ___/\  ___/
        ##  \___  /   |__|____/____/   |____|   |__|    \___  >\___  >
        ##      \/                                          \/     \/
        outtree.Fill()
        #print("Made it to end!")

        return 1



    #########################################
    # Main event loop
    nevents = 0
    maxevents = int(options.maxevents)
    for ifile in fwlite_tools.getInputFiles(options):
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

    #outtree.Print()
    # Close the output ROOT file
    f.cd()
    f.Write()
    f.Close()

    #genoutputfile.close()
    


#####################################################################################
if __name__ == "__main__":
    topbnv_fwlite(sys.argv)



