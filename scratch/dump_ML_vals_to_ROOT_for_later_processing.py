import numpy as np
import matplotlib.pylab as plt

import uproot
import sys

import topbnv_tools as tbt

import h5hep 

import sklearn as sk
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.cross_validation import train_test_split
from sklearn.metrics import roc_curve, auc, accuracy_score

import pickle

from itertools import combinations

################################################################################
# RUN THIS OVER THE OUTPUT FROM CONDOR  
################################################################################

################################################################################
def main(infiles=None,ml_file=None,outfilename=None):

    dec_funcs = []

    output_data = tbt.define_ML_output_data()
    output_data_keys = list(output_data.keys())
    output_data_keys.append('classifier_output')

    ml_results = pickle.load(open(ml_file,'rb'))
    bdt = ml_results["classifier"]
    param_labels = ml_results["param_labels"]

    treename = "Tskim"

    for infile in infiles:

        tree = uproot.open(infile)[treename]
        print("keys")
        print(tree.keys())

        nentries = tree.numentries
        print(nentries)

        nentries = 100

        branches = ["njet", "jete", "jetpx", "jetpy", "jetpz", "jetpt", "jeteta", "jetphi", "jetcsv"]
        branches += ["nmuon", "muone", "muonpx", "muonpy", "muonpz", "muonpt", "muoneta", "muonphi"]
        branches += ["nelectron", "electrone", "electronpx", "electronpy", "electronpz", "electronpt", "electroneta", "electronphi"]
        branches += ["metpt", "ntrigger", "trigger", "ev_wt", "pu_wt", "gen_wt"]

        data = tree.arrays(branches)
        #print(type(data))
        #print(data)

        ########################################################
        # h5hep stuff
        ########################################################
        # Create a data container
        h5data = h5hep.initialize()

        # Create some groups and datasets
        # Datasets are like data members of an the group/object
        h5hep.create_group(h5data,'jet',counter='njet')
        h5hep.create_dataset(h5data,['e','px','py','pz','pt','eta','phi','csv'],group='jet',dtype=float)

        h5hep.create_group(h5data,'muon',counter='nmuon')
        h5hep.create_dataset(h5data,['e','px','py','pz','pt','eta','phi'],group='muon',dtype=float)

        h5hep.create_group(h5data,'electron',counter='nelectron')
        h5hep.create_dataset(h5data,['e','px','py','pz','pt','eta','phi'],group='electron',dtype=float)

        h5hep.create_group(h5data,'trigger',counter='ntrigger')
        h5hep.create_dataset(h5data,['val'],group='trigger',dtype=float)

        h5hep.create_group(h5data,'hypothesis',counter='nhypothesis')
        h5hep.create_dataset(h5data,output_data_keys,group='hypothesis',dtype=float)

        h5hep.create_dataset(h5data,['metpt','ev_wt','pu_wt','gen_wt'],group=None,dtype=float)

        # Create a single event bucket for us to fill
        event = h5hep.create_single_event(h5data)

        wts = []
        for i in range(nentries):

            h5hep.clear_event(event)

            if i%10==0:
                print("{0} out of {1} entries".format(i,nentries))

            if i>1000000000:
                break

            pu_wt = data[b'pu_wt'][i]
            wts.append(pu_wt)

            alljets = []
            allmuons = []
            allelectrons = []

            event['metpt'] = data[b'metpt'][i]
            event['pu_wt'] = data[b'pu_wt'][i]
            event['ev_wt'] = data[b'ev_wt'][i]
            event['gen_wt'] = data[b'gen_wt'][i]

            event['trigger/ntrigger'] = data[b'ntrigger'][i]
            for n in range(data[b'ntrigger'][i]):
                event['trigger/val'] = data[b'trigger'][i][n]

            njet = data[b'njet'][i]
            event['jet/njet'] = njet
            for n in range(njet):
                jet = [data[b'jete'][i][n]]
                jet.append(data[b'jetpx'][i][n])
                jet.append(data[b'jetpy'][i][n])
                jet.append(data[b'jetpz'][i][n])
                jet.append(data[b'jetpt'][i][n])
                jet.append(data[b'jeteta'][i][n])
                jet.append(data[b'jetphi'][i][n])
                jet.append(data[b'jetcsv'][i][n])

                alljets.append(jet)

                event['jet/e'].append(data[b'jete'][i][n])
                event['jet/px'].append(data[b'jetpx'][i][n])
                event['jet/py'].append(data[b'jetpy'][i][n])
                event['jet/pz'].append(data[b'jetpz'][i][n])
                event['jet/pt'].append(data[b'jetpt'][i][n])
                event['jet/eta'].append(data[b'jeteta'][i][n])
                event['jet/phi'].append(data[b'jetphi'][i][n])
                event['jet/csv'].append(data[b'jetcsv'][i][n])

            nmuon = data[b'nmuon'][i]
            event['muon/nmuon'] = nmuon
            for n in range(nmuon):
                muon = [data[b'muone'][i][n]]
                muon.append(data[b'muonpx'][i][n])
                muon.append(data[b'muonpy'][i][n])
                muon.append(data[b'muonpz'][i][n])
                muon.append(data[b'muonpt'][i][n])
                muon.append(data[b'muoneta'][i][n])
                muon.append(data[b'muonphi'][i][n])

                allmuons.append(muon)

                event['muon/e'].append(data[b'muone'][i][n])
                event['muon/px'].append(data[b'muonpx'][i][n])
                event['muon/py'].append(data[b'muonpy'][i][n])
                event['muon/pz'].append(data[b'muonpz'][i][n])
                event['muon/pt'].append(data[b'muonpt'][i][n])
                event['muon/eta'].append(data[b'muoneta'][i][n])
                event['muon/phi'].append(data[b'muonphi'][i][n])

            nelectron = data[b'nelectron'][i]
            event['electron/nelectron'] = nelectron
            for n in range(nelectron):
                electron = [data[b'electrone'][i][n]]
                electron.append(data[b'electronpx'][i][n])
                electron.append(data[b'electronpy'][i][n])
                electron.append(data[b'electronpz'][i][n])
                electron.append(data[b'electronpt'][i][n])
                electron.append(data[b'electroneta'][i][n])
                electron.append(data[b'electronphi'][i][n])

                allelectrons.append(electron)

                event['electron/e'].append(data[b'electrone'][i][n])
                event['electron/px'].append(data[b'electronpx'][i][n])
                event['electron/py'].append(data[b'electronpy'][i][n])
                event['electron/pz'].append(data[b'electronpz'][i][n])
                event['electron/pt'].append(data[b'electronpt'][i][n])
                event['electron/eta'].append(data[b'electroneta'][i][n])
                event['electron/phi'].append(data[b'electronphi'][i][n])

            ####################################################################
            # ML stuff
            ####################################################################
            tmpjets = alljets.copy()
            #print(len(tmpjets))

            output_data = tbt.define_ML_output_data()

            combos = 0
            #print(len(tmpjets),len(allmuons),len(allelectrons))

            if len(tmpjets)>=5:
                for j0,j1,j2 in combinations(tmpjets,3):
                    tmp2jets = tmpjets.copy()
                    tmp2jets.remove(j0)
                    tmp2jets.remove(j1)
                    tmp2jets.remove(j2)
                    for j3,j4 in combinations(tmp2jets,2):
                        j3 = np.array(j3)
                        j4 = np.array(j4)
                        for lep in allmuons:
                            lep = np.array(lep)
                            tbt.vals_for_ML_training([j0,j1,j2],output_data,tag='had')
                            tbt.vals_for_ML_training([j3,j4,lep],output_data,tag='bnv')
                            hadtopp4 = j0[0:4] + j1[0:4] + j2[0:4]
                            #print(lep[0:4],type(lep[0:4]))
                            bnvtopp4 = j3[0:4]+j4[0:4]+lep[0:4]
                            a = tbt.angle_between_vectors(hadtopp4[1:4],bnvtopp4[1:4],transverse=True)
                            output_data['ttbar_angle'].append(np.cos(a))
                            combos += 1

            if len(output_data['had_m'])>0:
                data0 = []
                for pl in param_labels:
                    #print(pl,len(output_data[pl]))
                    data0.append(output_data[pl])
                data0 = np.array(data0)


                #print(data0)
                #probas = bdt.predict_proba(data0.transpose())
                #probbkg,probsig = probas.transpose()
                # This only works with BDT
                # Will need something else for NN
                dec_func = bdt.decision_function(data0.transpose())
                dec_funcs += dec_func.tolist()
                #print(probas)
                #print(dec_func)
                print(max(dec_func))
                for key in output_data_keys:
                    if key != 'classifier_output':
                        key_tot = 'hypothesis/{0}'.format(key)
                        event[key_tot] += output_data[key]
                    else:
                        key_tot = 'hypothesis/{0}'.format('classifier_output')
                        event[key_tot] += dec_func.tolist()



            


            h5hep.pack(h5data,event)

    plt.figure()
    plt.hist(dec_funcs,bins=50)

    plt.show()

    if outfilename == None:
        #outfilename = "/data/physics/bellis/CMS/HISTOGRAM_FILES_FEB2019/{0}_HISTOGRAMS.txt".format(infiles[0].split('/')[-1].split('.')[0])
        outfilename = "{0}_WITH_ML_VALS.hdf5".format(infiles[0].split('/')[-1].split('.')[0])
    print(outfilename)

    h5hep.write_to_file(outfilename,h5data,comp_type='gzip',comp_opts=9)
    
    return 1


################################################################################
if __name__=="__main__":

    infiles = sys.argv[1:-1]
    ml_file = sys.argv[-1]

    main(infiles,ml_file)
