# Much of this is from the B2G data analysis school code
#####################################################################################
import fwlite_tools

import ROOT, sys
from array import array
from DataFormats.FWLite import Events, Handle



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
            outtree.Branch(key, outdata[branch], '{0}[{1}]/F'.format(branch,key))


    '''
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
    '''

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

        event.getByLabel (jetLabel, jets)          # For b-tagging

        fwlite_tools.process_jets(jets, outdata, verbose=options.verbose)


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
if __name__ == "__main__":
    topbnv_fwlite(sys.argv)



