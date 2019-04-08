import numpy as np
import matplotlib.pyplot as plt

import random

import sklearn as sk
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.cross_validation import train_test_split
from sklearn.metrics import roc_curve, auc, accuracy_score
from sklearn import cross_validation, grid_search

import sys
import pickle

from sklearn_plot_results import plot_results

import argparse 
# Getting some of this from here
# https://betatim.github.io/posts/sklearn-for-TMVA-users/

################################################################################

#-db DATABSE -u USERNAME -p PASSWORD -size 20

parser = argparse.ArgumentParser(description='Process some files for scikit learning algorithms.')
parser.add_argument('--events', dest='nevents', default=0, help='Number of events you want to process.',type=int)
parser.add_argument('infiles', action='append', nargs='*', help='Input file name(s)')
args = parser.parse_args()

infilenames = args.infiles[0]
nevents = args.nevents

print(infilenames,nevents)





'''
if sys.argv[1] == "--events":
    nevents = int(sys.argv[2])
    infilenames = sys.argv[3:]
else:
    nevents = 0
    infilenames = sys.argv[1:]
'''

if len(infilenames) != 2:
    print("Wrong number of input files!")
    print("Should be 2!")
    exit()

outfilename = "AdaBoost_CLASSIFICATION_{0}_{1}.pkl".format(infilenames[0].split('.pkl')[0],infilenames[1].split('.pkl')[0])
outfile = open(outfilename,'wb')

dict0 = pickle.load(open(infilenames[0],'rb'))
dict1 = pickle.load(open(infilenames[1],'rb'))

param_labels = list(dict0.keys())

print("original")
print(param_labels)
toberemoved = ['had_dRPtTop','had_dRPtW', 'bnv_dRPtTop','bnv_dRPtW']
toberemoved += ['bnv_j12_m', 'bnv_j13_m', 'bnv_j23_m']
toberemoved += ['bnv_dR12_lab', 'bnv_dR13_lab', 'bnv_dR23_lab', 'bnv_dR1_23_lab']
toberemoved += ['bnv_dTheta12_rest','bnv_dTheta13_rest','bnv_dTheta23_rest']

for a in toberemoved:
    print('Removing {0} from variables to use in training'.format(a))
    param_labels.remove(a)
print("After removal")
print(param_labels)
nparams = len(param_labels)

#exit()

data0 = []
data1 = []

nevents0 = nevents
nevents1 = nevents

print(len(dict0[param_labels[0]]))
print(len(dict1[param_labels[0]]))

if nevents == 0 or nevents > len(dict0[param_labels[0]]):
    nevents0 = len(dict0[param_labels[0]])
print("Will process {0} events for {1}".format(nevents0,infilenames[0]))

if nevents == 0 or nevents > len(dict1[param_labels[0]]):
    nevents1 = len(dict1[param_labels[0]])
print("Will process {0} events for {1}".format(nevents1,infilenames[1]))

#exit()

# To randomize the selection of events.
index0 = np.arange(0,len(dict0[param_labels[0]]))
index1 = np.arange(0,len(dict1[param_labels[0]]))

random.shuffle(index0)
random.shuffle(index1)

for pl in param_labels:
    #data0.append(dict0[pl]['values'][0])
    print(pl,len(dict0[pl]))
    #print(len(dict0[pl][0:nevents0]),pl)
    data0.append([dict0[pl][x] for x in index0[0:nevents0]])
    #print(len(dict0[pl]['values'][0]))

for pl in param_labels:
    #data1.append(dict1[pl]['values'][0])
    print(pl,len(dict1[pl]))
    data1.append([dict1[pl][x] for x in index1[0:nevents1]])
    #print(len(dict1[pl]['values'][0]))
#exit()


classifier_results = {}

data0 = np.array(data0)
data1 = np.array(data1)

classifier_results["data0"] = data0
classifier_results["data1"] = data1
classifier_results["param_labels"] = param_labels
classifier_results["dataset0"] = infilenames[0]
classifier_results["dataset1"] = infilenames[1]
classifier_results["nevents"] = nevents 

################################################################################
# Train test split
################################################################################

print(data0.shape,data1.shape)
X = np.concatenate((data0.transpose(), data1.transpose()))
y = np.concatenate((np.ones(data0.transpose().shape[0]), np.zeros(data1.transpose().shape[0])))
print("X -----------------")
print(type(X),X.shape)
print(type(y),y.shape)
#print(X)
#print(y)

skdataset = {"data":X,"target":y,"target_names":param_labels}

# Might want to look at Tim's second post about how to use the X_eval dataset for 
# cross-validation
# https://betatim.github.io/posts/advanced-sklearn-for-TMVA/
X_dev,X_eval, y_dev,y_eval = train_test_split(X, y, test_size=0.33, random_state=42)
X_train,X_test, y_train,y_test = train_test_split(X_dev, y_dev, test_size=0.33, random_state=492)

################################################################################
# Fit/Classify
################################################################################

#dt = DecisionTreeClassifier(max_depth=3, min_samples_leaf=0.05*len(X_train))
dt = DecisionTreeClassifier(max_depth=3)

bdt = AdaBoostClassifier(dt, algorithm='SAMME', n_estimators=800, learning_rate=0.5)
bdt.fit(X_train, y_train)

scores = cross_validation.cross_val_score(bdt,
                                          X_dev, y_dev,
                                          scoring="roc_auc",
                                          n_jobs=6,
                                          cv=3)

print("Accuracy: %0.5f (+/- %0.5f)" %(scores.mean(), scores.std()))

classifier_results["classifier"] = bdt

# Dump all the info to file
pickle.dump(classifier_results,outfile)
outfile.close()

# Perform grid search over all combinations
# of these hyper-parameters
param_grid = {"n_estimators": [50,200,400,1000],
        #"max_depth": [3, 4, 5],
              'learning_rate': [0.1, 0.2, 1.]}

clf = grid_search.GridSearchCV(bdt,
                               param_grid,
                               cv=3,
                               scoring='roc_auc',
                               n_jobs=8)
_ = clf.fit(X_dev, y_dev)

print("Best parameter set found on development set:")
print(clf.best_estimator_)
print("")
print("Grid scores on a subset of the development set:")
for params, mean_score, scores in clf.grid_scores_:
    print("%0.4f (+/-%0.04f) for %r" % (mean_score, scores.std(), params))
print("")
print("With the model trained on the full development set:")

y_true, y_pred = y_dev, clf.decision_function(X_dev)
print("  It scores %0.4f on the full development set" % roc_auc_score(y_true, y_pred))
y_true, y_pred = y_eval, clf.decision_function(X_eval)
print("  It scores %0.4f on the full evaluation set" % roc_auc_score(y_true, y_pred))



plot_results(data0, data1, infilenames[0], infilenames[1], param_labels, bdt)

plt.show()
