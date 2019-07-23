# Much of this is from the B2G data analysis school code

import ROOT, copy, sys, logging
from array import array
from DataFormats.FWLite import Events, Handle
from DataFormats.FWLite import Events, Handle

from fwlite_tools import jet_energy_corrections, jet_energy_correction_GT_for_MC, DataJEC

import fwlite_tools

# NEED THIS FOR DEEP CSV STUFF?
from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection


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

    options = fwlite_tools.getUserOptions(argv)
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
    jetdata = {}
    jetdata['njet'] = ['jetpt', 'jeteta', 'jetphi', 'jete', 'jetpx', 'jetpy', 'jetpz']
    jetdata['njet'] += ['jetbtag0', 'jetbtag1', 'jetbtagsum']
    jetdata['njet'] += ['jetarea', 'jetjec', 'jetNHF', 'jetNEMF', 'jetCHF', 'jetCHM', 'jetMUF', 'jetCEMF']
    jetdata['njet'] += ['jetNumConst', 'jetNumNeutralParticles']

    outJets = {}
    for key in jetdata.keys():

        outJets[key] = array('i', [-1])
        outtree.Branch(key, outJets[key], key+"/I")

        for branch in jetdata[key]:
            outJets[branch] = array('f', 16*[-1.])
            outtree.Branch(branch, outJets[branch], '{0}[{1}]/F'.format(branch,key))

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
    # Pileup

    pudata = ['pu_wt']

    outPileup = {}
    for key in pudata:
        outPileup[key] = array('f', [-1])
        outtree.Branch(key, outPileup[key], key+"/F")

    '''
    njet = array('i', [-1])
    outtree.Branch('njet', njet, 'njet/I')
    jetpt = array('f', 16*[-1.])
    outtree.Branch('jetpt', jetpt, 'jetpt[njet]/F')
    '''

    purw = None # pileup reweighting histogram
    if options.isMC and not options.disablePileup:
        pileupReweightFile = ROOT.TFile('purw_{0}.root'.format(options.year), 'READ')
        #pileupReweightFile = ROOT.TFile('PileupHistogram-goldenJSON-13tev-{0}.root'.format(options.year), 'READ')
        purw = pileupReweightFile.Get('pileup')


    #################################################################################
    #################################################################################
    # Trigger

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

    #################################################################################
    #################################################################################
    # Vertex

    vertexdata = {}
    vertexdata['nvertex'] = ['vertexX', 'vertexY', 'vertexZ', 'vertexndof']

    outVertex = {}
    for key in vertexdata.keys():
        outVertex[key] = array('i', [-1])
        outtree.Branch(key, outVertex[key], key+"/I")

        for branch in vertexdata[key]:
            outVertex[branch] = array('f', 64*[-1.])
            outtree.Branch(branch, outVertex[branch], '{0}[{1}]/F'.format(branch,key))
    


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
        jecAK4 = fwlite_tools.createJEC('JECs/'+options.year+'/'+jet_energy_correction_GT_for_MC[options.year], ['L1FastJet', 'L2Relative', 'L3Absolute'], 'AK4PFchs')
        jecUncAK4 = ROOT.JetCorrectionUncertainty(ROOT.std.string('JECs/'+options.year+'/'+jet_energy_correction_GT_for_MC[options.year]+'_Uncertainty_AK4PFchs.txt'))
    else:
        # CHANGE THIS FOR DATA
        DataJECs = DataJEC(jet_energy_corrections[options.year], options.year)
    
    
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
        # Trigger
        event.getByLabel(triggerBitLabel, triggerBits)
        event.getByLabel(triggerPrescalesLabel, triggerPrescales )

        trigger_names = event.object().triggerNames(triggerBits.product())

        FLAG_passed_trigger = fwlite_tools.process_triggers(triggerBits, triggerPrescales, trigger_names, trigger_tree_branches, outTriggers, options, verbose=options.verbose)

        # Should do this early. We shouldn't analyze events that don't
        # pass any of the relevant triggers
        if FLAG_passed_trigger is False:
            return 0

        ###########################################################################
        # If trigger test is passed, process event

        ###########################################################################
        # Vertex
        event.getByLabel(vertexLabel, vertices)
        PV,NPV = fwlite_tools.process_vertices(vertices, outVertex, verbose=options.verbose)

        # Should do this first. We shouldn't analyze events that don't have a
        # good primary vertex
        if PV is None:
            return 0

        ###########################################################################
        # Muons
        event.getByLabel (muonLabel, muons)
        fwlite_tools.process_muons(muons, outMuons, verbose=options.verbose)

        ###########################################################################
        # Electrons
        event.getByLabel (electronLabel, electrons)
        fwlite_tools.process_electrons(electrons, outElectrons, verbose=options.verbose)
        
        ###########################################################################
        # Pileup
        if options.isMC:
            event.getByLabel(pileuplabel, pileups)
            fwlite_tools.process_pileup(pileups, outPileup, purw, options, verbose=options.verbose)

        ###########################################################################
        # MET
        event.getByLabel( metLabel, mets )
        fwlite_tools.process_mets(mets, outMET, verbose=options.verbose)
        
        ###########################################################################
        # Rhos
        event.getByLabel(rhoLabel, rhos)
        rho = fwlite_tools.process_rhos(rhos, verbose=options.verbose)
        if rho is None:
            return 0
        
        ###########################################################################
        # Jets
        runnumber = event.eventAuxiliary().run()
        event.getByLabel(vertexLabel, vertices)
        event.getByLabel (jetLabel, jets)

        if options.isMC:
            fwlite_tools.process_jets(jets, outJets, options, jecAK4=jecAK4, jecUncAK4=jecUncAK4, runnumber=runnumber, rho=rho, NPV=NPV, verbose=options.verbose)
        else:
            fwlite_tools.process_jets(jets, outJets, options, DataJECs=DataJECs, runnumber=runnumber, rho=rho, NPV=NPV, verbose=options.verbose)

        
        
        genOut = "Event %d\n" % (iev)

        if options.verbose:
            print( "\nProcessing %d: run %6d, lumi %4d, event %12d" % \
                  (iev,event.eventAuxiliary().run(), \
                  event.eventAuxiliary().luminosityBlock(), \
                  event.eventAuxiliary().event()))



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


