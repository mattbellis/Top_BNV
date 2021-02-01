import awkward1 as ak
#from coffea.nanoaod import NanoEventsFactory
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema

from coffea.lookup_tools import extractor


#fname = "https://github.com/CoffeaTeam/coffea/raw/master/tests/samples/nano_dy.root"
fname = "nano_dy.root"
#events = NanoEvents.from_file(fname)
events = NanoEventsFactory.from_root(fname, schemaclass=NanoAODSchema).events()


################################################################################
# b-tag scale factor
################################################################################
ext = extractor()
ext.add_weight_sets(["testBTag * data/testBTagSF.btag.csv"])
ext.finalize()

evaluator = ext.make_evaluator()

print("available evaluator keys:")
for i, key in enumerate(evaluator.keys()):
    print("\t", key)
    if i > 5:
        print("\t ...")
        break
print("testBTagCSVv2_1_comb_up_0:", evaluator["testBTagCSVv2_1_comb_up_0"])
print( "type of testBTagCSVv2_1_comb_up_0:", type(evaluator["testBTagCSVv2_1_comb_up_0"]))


scalefactor = evaluator['testBTagCSVv2_1_comb_up_0'](events.Jet.eta, events.Jet.pt, events.Jet.btagCSVV2)
print(scalefactor)


################################################################################
# JES and Unc
################################################################################
ext = extractor()
ext.add_weight_sets([
        "* * data/Fall17_17Nov2017_V32_MC_L2Relative_AK4PFPuppi.jec.txt",
            "* * data/Fall17_17Nov2017_V32_MC_Uncertainty_AK4PFPuppi.junc.txt",
            ])
ext.finalize()

evaluator = ext.make_evaluator()

print("available evaluator keys:")
for key in evaluator.keys():
    print("\t", key)

print()
print("Fall17_17Nov2017_V32_MC_L2Relative_AK4PFPuppi:")
print(evaluator['Fall17_17Nov2017_V32_MC_L2Relative_AK4PFPuppi'])
print("type of Fall17_17Nov2017_V32_MC_L2Relative_AK4PFPuppi:")
print(type(evaluator['Fall17_17Nov2017_V32_MC_L2Relative_AK4PFPuppi']))
print()
print("Fall17_17Nov2017_V32_MC_Uncertainty_AK4PFPuppi:")
print(evaluator['Fall17_17Nov2017_V32_MC_Uncertainty_AK4PFPuppi'])
print("type of Fall17_17Nov2017_V32_MC_Uncertainty_AK4PFPuppi:")
print(type(evaluator['Fall17_17Nov2017_V32_MC_Uncertainty_AK4PFPuppi']))


################################################################################
# Jet energy scale transformation
################################################################################
from coffea.analysis_objects import JaggedCandidateArray
from coffea.jetmet_tools import FactorizedJetCorrector, JetCorrectionUncertainty
from coffea.jetmet_tools import JetTransformer

ext = extractor()
ext.add_weight_sets([
    "* * data/Fall17_17Nov2017_V32_MC_L2Relative_AK4PFPuppi.jec.txt",
    "* * data/Fall17_17Nov2017_V32_MC_Uncertainty_AK4PFPuppi.junc.txt",
])
ext.finalize()

evaluator = ext.make_evaluator()

print(dir(evaluator))
print()

jets = JaggedCandidateArray.candidatesfromcounts(
        #events.Jet.counts,
        #pt=(events.Jet.pt * (1 - events.Jet.rawFactor)).flatten(),
        #eta=events.Jet.y.flatten(),
        #phi=events.Jet.z.flatten(),
        #mass=(events.Jet.mass * (1 - events.Jet.rawFactor)).flatten(),
    ak.num(events.Jet),
    pt=ak.flatten((events.Jet.pt * (1 - events.Jet.rawFactor))),
    eta=ak.flatten(events.Jet.y),
    phi=ak.flatten(events.Jet.z),
    mass=ak.flatten((events.Jet.mass * (1 - events.Jet.rawFactor))),
)
jets.add_attributes(ptRaw=jets.pt, massRaw=jets.mass)

corrector = FactorizedJetCorrector(
    Fall17_17Nov2017_V32_MC_L2Relative_AK4PFPuppi=evaluator['Fall17_17Nov2017_V32_MC_L2Relative_AK4PFPuppi'],
)
uncertainties = JetCorrectionUncertainty(
    Fall17_17Nov2017_V32_MC_Uncertainty_AK4PFPuppi=evaluator['Fall17_17Nov2017_V32_MC_Uncertainty_AK4PFPuppi']
)

transformer = JetTransformer(jec=corrector, junc=uncertainties)
### more possibilities are available if you send in more pieces of the JEC stack
# mc2016_ak8_jxform = JetTransformer(jec=MC_AK8JEC2016,junc=MC_AK8JUNC2016
#                                    jer=MC_AK8JER2016,jersf=MC_AK8JERSF2016)

print()
print('starting columns:',jets.columns)
print()

print('untransformed pt ratios',jets.pt/jets.ptRaw)
print('untransformed mass ratios',jets.mass/jets.massRaw)

transformer.transform(jets)

print('transformed pt ratios',jets.pt/jets.ptRaw)
print('transformed mass ratios',jets.mass/jets.massRaw)

print()
print('transformed columns:',jets.columns)
print()

print('JES UP pt ratio',jets.pt_jes_up/jets.ptRaw)
print('JES DOWN pt ratio',jets.pt_jes_down/jets.ptRaw)



################################################################################
# CMS b-tagging corrections
################################################################################
from coffea.btag_tools import BTagScaleFactor

btag_sf = BTagScaleFactor("data/DeepCSV_102XSF_V1.btag.csv.gz", "medium")

print("SF:", btag_sf.eval("central", events.Jet.hadronFlavour, abs(events.Jet.eta), events.Jet.pt))
print("systematic +:", btag_sf.eval("up", events.Jet.hadronFlavour, abs(events.Jet.eta), events.Jet.pt))
