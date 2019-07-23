# Much of this is from the B2G data analysis school code
#####################################################################################
import fwlite_tools

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

    # NEED HLT2 for 80x 2016 (maybe only TTBar?
    # https://twiki.cern.ch/twiki/bin/view/CMS/TopTrigger#Summary_for_2016_Run2016B_H_25_n
    # https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD2016#Trigger
    triggerBits, triggerBitLabel = Handle("edm::TriggerResults"), ("TriggerResults","", "HLT")
    #trigPrescalesHandle = Handle( "std::vector<int>")
    #trigPrescalesLabel = ("TriggerUserData", "triggerPrescaleTree")
    #triggerPrescales, triggerPrescalesLabel = Handle("pat::PackedTriggerPrescales"), ("PackedTriggerPrescales","", "HLT")
    triggerPrescales, triggerPrescalesLabel  = Handle("pat::PackedTriggerPrescales"), "patTrigger"



    f = ROOT.TFile(options.output, "RECREATE")
    f.cd()

    outtree = ROOT.TTree("T", "Our tree of everything")

    ############################################################################
    # Vertex 
    ############################################################################
    trigdata = {}
    trigdata['ntrig_muon'] = ['trig_muon']
    trigdata['ntrig_electron'] = ['trig_electron']
    trigdata['ntrig_dilepmue'] = ['trig_dilepmue']
    trigdata['ntrig_dilepemu'] = ['trig_dilepemu']
    trigdata['ntrig_dilepmumu'] = ['trig_dilepmumu']
    trigdata['ntrig_dilepee'] = ['trig_dilepee']

    outdata = {}
    for key in trigdata.keys():
        print(key)
        outdata[key] = array('i', [-1])
        outtree.Branch(key, outdata[key], key+"/I")

        for branch in trigdata[key]:
            # Save them as integers
            outdata[branch] = array('i', 8*[-1])
            outtree.Branch(branch, outdata[branch], '{0}[{1}]/I'.format(branch,key))

    trigger_tree_branches = {
        "SingleMuon":outdata['trig_muon'],
        "SingleElectron":outdata['trig_electron'],
        "DileptonMuE":outdata['trig_dilepmue'],
        "DileptonEMu":outdata['trig_dilepemu'],
        "DileptonMuMu":outdata['trig_dilepmumu'],
        "DileptonEE":outdata['trig_dilepee']
    }

    '''
    njet = array('i', [-1])
    outtree.Branch('njet', njet, 'njet/I')

    jetpt = array('f', 16*[-1.])
    outtree.Branch('jetpt', jetpt, 'jetpt[njet]/F')
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

        event.getByLabel(triggerBitLabel, triggerBits)
        event.getByLabel(triggerPrescalesLabel, triggerPrescales )

        trigger_names = event.object().triggerNames(triggerBits.product())

        FLAG_passed_trigger = fwlite_tools.process_triggers(triggerBits, triggerPrescales, trigger_names, trigger_tree_branches, outdata, options, verbose=options.verbose)

        # Should do this early. We shouldn't analyze events that don't
        # pass any of the relevant triggers
        if FLAG_passed_trigger is False:
            return 0


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



