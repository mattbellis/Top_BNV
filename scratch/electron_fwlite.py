# Much of this is from the B2G data analysis school code

import ROOT, copy, sys, logging
from array import array
from DataFormats.FWLite import Events, Handle

from RecoEgamma.ElectronIdentification.VIDElectronSelector import VIDElectronSelector
from RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff import cutBasedElectronID_Summer16_80X_V1_medium



'''
if hasattr(cutBasedElectronID_Summer16_80X_V1_medium,'isPOGApproved'):
    del cutBasedElectronID_Summer16_80X_V1_medium.isPOGApproved
'''




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
def electron_fwlite(argv):
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

    electrons, electronLabel = Handle("std::vector<pat::Electron>"), "slimmedElectrons"


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

        runnumber = event.eventAuxiliary().run()

        if options.verbose:
            print "\nProcessing %d: run %6d, lumi %4d, event %12d" % \
                  (iev,event.eventAuxiliary().run(), \
                  event.eventAuxiliary().luminosityBlock(), \
                  event.eventAuxiliary().event())


        ##############################################################
        # Electrons
        ##############################################################
        #selectElectron = VIDElectronSelector(cutBasedElectronID_Summer16_80X_V1_loose)
        print("------ Electrons --------")

        '''
        # This doesn't seem to help here either
        if hasattr(cutBasedElectronID_Summer16_80X_V1_medium,'isPOGApproved'):
            del cutBasedElectronID_Summer16_80X_V1_medium.isPOGApproved
        '''

        #print(cutBasedElectronID_Summer16_80X_V1_medium)
        #print(cutBasedElectronID_Summer16_80X_V1_medium.isPOGApproved)
        #print(cutBasedElectronID_Summer16_80X_V1_medium.isPOGApproved.value())

        selectElectron = VIDElectronSelector(cutBasedElectronID_Summer16_80X_V1_medium)

        print("This is the point after the selector is declared...")
        
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

                print("Analyzing electron: ",i)
                passSelection = selectElectron( electron, event )

                print(passSelection,type(passSelection))

                if passSelection:
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
    electron_fwlite(sys.argv)



