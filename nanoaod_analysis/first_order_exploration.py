import numpy as np
import awkward as ak
import uproot as uproot

import matplotlib.pylab as plt

import sys

import hepfile

from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import nanoaod_analysis_tools as nat

import time

infilename = sys.argv[1]
print("Reading in {0}".format(infilename))
dataset_type, mc_type, trigger, topology, year = nat.extract_dataset_type_and_trigger_from_filename(infilename)
if trigger==None:
    trigger = 'SingleMuon'
print(f"input file information:   {dataset_type} {mc_type} {trigger} {topology} {year}")
################################################################################

TRUTH = False
if len(sys.argv)>2:
    print(sys.argv[2])
    data = np.load(sys.argv[2],allow_pickle=False)
    event_truth_indices = data['event_truth_indices']
    truth_indices = data['truth_indices']
    TRUTH = True

print("Reading in {0}".format(infilename))

################################################################################
data = hepfile.initialize()
hepfile.create_group(data,'jet',counter='njet')
hepfile.create_dataset(data,['pt'],group='jet',dtype=float)

hepfile.create_group(data,'muon',counter='nmuon')
hepfile.create_dataset(data,['pt'],group='muon',dtype=float)

output_data_ML = nat.define_ML_output_data()
hepfile.create_group(data,'ml',counter='num')
hepfile.create_dataset(data,list(output_data_ML.keys()),group='ml',dtype=float)
event = hepfile.create_single_bucket(data)

################################################################################

events = NanoEventsFactory.from_root(infilename, schemaclass=NanoAODSchema).events()
print(len(events))

if len(sys.argv)>2:
    print("# events in file passing truth requirements: ",len(events[event_truth_indices]))
    events = events[event_truth_indices]

################################################################################
# Before we mask everything, we create an index for each of the GenPart, and Jets,
# and Muons, and GenJets
print("Making the Indices field idx....")
print("Applying the trigger mask and extracting jets, muons, and electrons...")
jets = events.Jet
genjets = events.GenJet
muons = events.Muon
electrons = events.Electron
genparts = events.GenPart
for pat in [jets, genjets, muons, electrons]:
    print(pat)
    num = ak.num(pat)
    all_idx = []
    for n in num:
        idx = np.arange(0,n,dtype=int)
        all_idx.append(idx)
    pat['idx'] = all_idx
    print("Made the pat idx....")
print("Made all the idx fields...")

# Also precalculate the GenPart pdgId for the reconstructed leptons
electrons['matched_gen_pdgId'] = electrons.matched_gen.pdgId
muons['matched_gen_pdgId'] = muons.matched_gen.pdgId

################################################################################

print(f"Applying the trigger mask...assume year {year}")
HLT = events.HLT
event_mask = None
#event_mask = nat.trigger_mask(HLT, trigger=trigger, year=year)
print("# events in file:                              ",len(events))
print("# events in file passing trigger requirements: ",len(events[event_mask]))
print("Mask is calculated!")

# If we want a mask with everything
event_mask = np.ones(len(events),dtype=bool)
################################################################################

print("Applying the trigger mask and extracting jets, muons, and electrons...")
#alljets_temp = events[event_mask].Jet
#allgenjets_temp = events[event_mask].GenJet
#allmuons_temp = events[event_mask].Muon
#allelectrons_temp = events[event_mask].Electron
#allgenparts = events[event_mask].GenPart
alljets_temp = jets
allgenjets_temp = genjets
allmuons_temp = muons
allelectrons_temp = electrons
allgenparts = genparts
met = events[event_mask].MET
print("Extracted jets, muons, and electrons!")

################################################################################

print("Calculating Cartesian 4-vectors...")
allgenparts['px'],allgenparts['py'],allgenparts['pz'] = nat.etaphipt2xyz(allgenparts)
allgenparts['e'] = nat.energyfrommasspxpypz(allgenparts)
allgenparts['btagDeepB'] = allgenparts['e'] # This is just a placeholder, since genPart doesn't have the b-tagging variable
allgenparts['charge'] = allgenparts['pdgId'] # This is just a placeholder, since genPart doesn't have the b-tagging variable

alljets_temp['px'],alljets_temp['py'],alljets_temp['pz'] = nat.etaphipt2xyz(alljets_temp)
alljets_temp['e'] = nat.energyfrommasspxpypz(alljets_temp)

allelectrons_temp['px'],allelectrons_temp['py'],allelectrons_temp['pz'] = nat.etaphipt2xyz(allelectrons_temp)
allelectrons_temp['e'] = nat.energyfrommasspxpypz(allelectrons_temp)

allmuons_temp['px'],allmuons_temp['py'],allmuons_temp['pz'] = nat.etaphipt2xyz(allmuons_temp)
allmuons_temp['e'] = nat.energyfrommasspxpypz(allmuons_temp)

print(allgenparts['mass'])

maxnjets = 7
#maxnleps = 2
# For gen part stuff
maxnleps = 7

'''
event_topology_indices = []
for truth in truth_indices:
    t = [(truth[0],truth[1],truth[2]), (truth[3], truth[4]), truth[5]]
    event_topology_indices.append(t)
'''

#genpart = ak.flatten(genpart)[truth_indices]
#print(genpart)

if TRUTH:
    print(len(allgenparts), len(truth_indices), len(alljets_temp))
nmatched_jets_and_leptons = 0
# Do jet matching
#'''
matched_reco_indices = []
# First 5 are jets and the last is the lepton
matched_final_state_idx = [-999,-999,-999,-999,-999,-999]
#for alljets,allgenjets,allleptons,genparts,idx in zip(alljets_temp,allgenjets_temp,allelectrons_temp,allgenparts,truth_indices):
icount = 0
if TRUTH:
    for alljets,allgenjets,allleptons,genparts,idx in zip(alljets_temp,allgenjets_temp,allmuons_temp,allgenparts,truth_indices):

        if icount%100==0:
            print(f"{icount}")

        # First 5 are jets and the last is the lepton
        matched_final_state_idx = [-999,-999,-999,-999,-999,-999]
        gp = genparts[idx]
        pdgId = gp.pdgId
        #print(pdgId)
        #print("----------------------------")
        for i,p in enumerate(pdgId):
            if i==5:
                continue # Skip the lepton matching
            #print("----")
            #print(i,p)
            for j,jet in enumerate(alljets[alljets.partonFlavour==p]):
                #print(jet.idx, jet,jet.partonFlavour, allgenjets[allgenjets.idx==jet.genJetIdx].partonFlavour)
                #if jet.partonFlavour == p:
                if 1:
                    dR = gp[i].delta_r(jet)
                    #print(dR)
                    if dR<0.4:
                        matched_final_state_idx[i] = jet.idx

        # Match the leptons
        #'''
        i = 5
        p = gp[i].pdgId # pdgId for the electron, do we need this?
        for j,lep in enumerate(allleptons):
            #print(p,j,lep,lep.pdgId)
            #if lep.pt>0:
            # We precalculated this so it doesn't have to look through everything
            #print("---")
            #print(j,p)
            if lep.matched_gen_pdgId == p:
                #matched_final_state_idx[i] = lep.idx
                dR = gp[i].delta_r(lep)
                ##print(dR)
                if dR<0.4:
                    matched_final_state_idx[i] = lep.idx
        #'''

        #print(matched_final_state_idx)

        matched_reco_indices.append(matched_final_state_idx)
        if sum(matched_final_state_idx)>=0:
            nmatched_jets_and_leptons += 1

        icount += 1
print(f"nmatched_jets_and_leptons : {nmatched_jets_and_leptons}")
#'''


################################################################################
# Matched jets and leptons
#'''
icount = 0
#matched_final_state_idx
event_topology_indices = [[(0, 1, 2), (3 ,4), 0]]
if not TRUTH:
    maxnjets = 7
    maxnleps = 2
    all_event_topology_indices = nat.generate_all_event_topology_indices(maxnjets=maxnjets,maxnleps=maxnleps,verbose=False)

# TRUTH
#for alljets,allleptons,idx in zip(alljets_temp,allelectrons_temp,matched_reco_indices):
for alljets,allleptons,idx in zip(alljets_temp,allmuons_temp,matched_reco_indices):
# NOT TRUTH
#for alljets,allleptons in zip(alljets_temp,allmuons_temp):

    if not TRUTH:
        njets = len(alljets)
        nleps = len(allmuons)
        nbjets= len(alljets[jets.btagDeepB>0.5])
        #print(njets,nleps,nbjets)
        if nleps>maxnleps or njets>maxnjets or nbjets<1:
            continue

        event_topology_indices = all_event_topology_indices[njets][nleps]

    # Skip if we didn't match everyone
    #print(idx)
    if TRUTH:
        if sum(idx)<0:
            continue

    #print("flavours =================")
    #print(alljets[idx[0:5]].partonFlavour, allleptons[idx[5]].pdgId)
    keep_order = True
    # Pass in the leptons as a list because there is just 1
    x = nat.event_hypothesis(alljets[idx[0:5]],[allleptons[idx[5]]],verbose=True, bjetcut=0.25, ML_data=output_data_ML,maxnjets=maxnjets,maxnleps=maxnleps,event_topology_indices=event_topology_indices, keep_order=keep_order)

    hepfile.pack(data,event)
    icount += 1

    #print(output_data_ML)
#'''
################################################################################
################################################################################
# GenPart
'''
event_topology_indices = [[(0, 1, 2), (3 ,4), 5]]
icount = 0
for gens,idx in zip(allgenparts,truth_indices):
    #print(gens.pdgId)
    #print(len(gens.pdgId))
    #print(idx)
    #print(icount,gens[idx].pdgId)
    keep_order = True
    x = nat.event_hypothesis(gens[idx],gens[idx],verbose=True, ML_data=output_data_ML,maxnjets=maxnjets,maxnleps=maxnleps,event_topology_indices=event_topology_indices, keep_order=keep_order)
    hepfile.pack(data,event)
    icount += 1

    #print(output_data_ML)
'''
################################################################################


################################################################################

print("Calculating the muon mask...")
# Muon processing
muon_ptcut = 20
muon_isoflag = 1
muon_flag = 'loose'
muon_mask = nat.muon_mask(allmuons_temp,ptcut=muon_ptcut,isoflag=muon_isoflag,flag=muon_flag)

print("Calculating the jet mask...")
jet_mask = nat.jet_mask(alljets_temp,ptcut=25)

print("Applying the jet mask...")
print(len(alljets_temp))
alljets = alljets_temp[jet_mask]
print(len(alljets))
allmuons = allmuons_temp[muon_mask]

################################################################################
# Numbers cut
################################################################################
print(len(alljets), len(allmuons))
mask_num = (ak.num(alljets)>=5) & (ak.num(allmuons)==1)
alljets = alljets[mask_num]
allmuons = allmuons[mask_num]
print(len(alljets), len(allmuons))

################################################################################
data['muon/nmuon'] = ak.to_numpy(ak.num(allmuons.pt))
data['muon/pt'] = ak.to_numpy(ak.flatten(allmuons.pt))
data['jet/njet'] = ak.to_numpy(ak.num(alljets.pt))
data['jet/pt'] = ak.to_numpy(ak.flatten(alljets.pt))
data['_SINGLETONS_GROUP_/COUNTER'] = np.zeros(len(data['muon/nmuon']))

for key in output_data_ML.keys():
    if key != 'num_combos':
        data['ml/'+key] = output_data_ML[key]
print( output_data_ML['num_combos'])
data['ml/num'] = output_data_ML['num_combos']

outfilename = f"FIRST_LOOK_{infilename.split('/')[-1].split('.root')[0]}.h5"
#outfilename = f"FIRST_LOOK_GENPART_{infilename.split('/')[-1].split('.root')[0]}.h5"
#outfilename = f"FIRST_LOOK_GENPART_FIRST_INSTANCE_{infilename.split('/')[-1].split('.root')[0]}.h5"
hdfile = hepfile.write_to_file(outfilename,data,comp_type='gzip',comp_opts=9,verbose=True)

exit()
################################################################################

################################################################################

plt.figure()
plt.subplot(2,3,1)
plt.hist(ak.num(alljets),bins=20,range=(0,20))
plt.xlabel('# of jets')

plt.subplot(2,3,2)
plt.hist(ak.to_numpy(ak.flatten(alljets.pt)),bins=25,range=(0,300))
plt.xlabel(r'$p_T$ jets (GeV/c)')
#nbjets= len(jets[jets.btagDeepB>0.5])

plt.subplot(2,3,3)
plt.hist(ak.to_numpy(ak.max(alljets.pt,1)),bins=25,range=(0,300))
plt.xlabel(r'$p_T$ jets (GeV/c)')

# Second highest momentum, assuming that they are ordered
plt.subplot(2,3,4)
plt.hist(alljets[ak.num(alljets)>1][:,1].pt,bins=25,range=(0,300))
plt.xlabel(r'$p_T$ jets (GeV/c)')

# Second highest momentum versus the highest momentum, assuming that they are ordered
plt.subplot(2,3,5)
plt.plot(alljets[ak.num(alljets)>1][:,0].pt, alljets[ak.num(alljets)>1][:,1].pt,'.',alpha=0.2)
plt.xlabel(r'$p_T$ jets (GeV/c)')

plt.tight_layout()
##########################################################

plt.figure()
plt.subplot(2,2,1)
plt.hist(ak.num(allmuons),bins=5,range=(0,5))
plt.xlabel('# of muons')

plt.subplot(2,2,2)
plt.hist(ak.to_numpy(ak.flatten(allmuons.pt)),bins=25,range=(0,300))
plt.xlabel(r'$p_T$ muons (GeV/c)')

plt.tight_layout()
##########################################################
##########################################################

plt.figure()
plt.subplot(2,2,1)
plt.hist(met.pt,bins=25,range=(0,100))
plt.xlabel('MET pt')

plt.tight_layout()

#plt.show()











