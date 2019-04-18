# Much of this is from the B2G data analysis school code

import ROOT, copy, sys, logging
from array import array
from DataFormats.FWLite import Events, Handle

# NEED THIS FOR DEEP CSV STUFF?
from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection


################################################################################
# Pass in a slimmedJets object
################################################################################
def process_jets(jets, outdata, verbose=False): 

    ############################################
    # Get the AK4 jet nearest the lepton:
    ############################################
    print("-------------")
    print("{0:10} {1:10} {2:10} {3:10} {4:10} {5:10}".format("Index", "probb", "probb", "sum", "eta", "pt"))
    sf = []
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




