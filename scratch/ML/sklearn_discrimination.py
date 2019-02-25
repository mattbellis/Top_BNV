import numpy as np
import matplotlib.pyplot as plt

import sklearn as sk
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.cross_validation import train_test_split
from sklearn.metrics import roc_curve, auc, accuracy_score

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

outfilename = "CLASSIFICATION_{0}_{1}.pkl".format(infilenames[0].split('.pkl')[0],infilenames[1].split('.pkl')[0])
outfile = open(outfilename,'wb')

dict0 = pickle.load(open(infilenames[0],'rb'))
dict1 = pickle.load(open(infilenames[1],'rb'))

param_labels = list(dict0.keys())

print(param_labels)
toberemoved = ['had_dRPtTop','had_dRPtW']
for a in toberemoved:
    param_labels.remove(a)
print(param_labels)
nparams = len(param_labels)

#exit()

data0 = []
data1 = []

nevents0 = nevents
nevents1 = nevents

if nevents == 0 or nevents > len(dict0[param_labels[0]]):
    nevents0 = len(dict0[param_labels[0]])
print("Will process {0} events for {1}".format(nevents0,infilenames[0]))

if nevents == 0 or nevents > len(dict1[param_labels[0]]):
    nevents1 = len(dict1[param_labels[0]])
print("Will process {0} events for {1}".format(nevents1,infilenames[1]))

#exit()

for pl in param_labels:
    #data0.append(dict0[pl]['values'][0])
    data0.append(dict0[pl][0:nevents0])
    #print(len(dict0[pl]['values'][0]))

for pl in param_labels:
    #data1.append(dict1[pl]['values'][0])
    data1.append(dict1[pl][0:nevents1])
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

X = np.concatenate((data0.transpose(), data1.transpose()))
y = np.concatenate((np.ones(data0.transpose().shape[0]), np.zeros(data1.transpose().shape[0])))
print("X -----------------")
print(type(X),X.shape)
print(type(y),y.shape)
print(X)
print(y)

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

classifier_results["classifier"] = bdt

pickle.dump(classifier_results,outfile)
outfile.close()

plot_results(data0, data1, infilenames[0], infilenames[1], param_labels, bdt)

plt.show()
