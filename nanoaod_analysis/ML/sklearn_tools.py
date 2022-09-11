import numpy as np
import matplotlib.pyplot as plt


import sklearn as sk
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.metrics import roc_curve, auc, accuracy_score

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.neural_network import MLPClassifier

import hepfile

import pandas as pd
import sys
import pickle

# Getting some of this from here
# https://betatim.github.io/posts/sklearn-for-TMVA-users/

################################################################################
def read_in_pickle_files(infiles):
    dict0 = pickle.load(open(infile[0],'rb'))
################################################################################

################################################################################
def read_in_files_and_return_dataframe(infilenames):

    #infilenames = sys.argv[1:]
    if len(infilenames) != 2:
        print("Wrong number of input files!")
        print("Should be 2!")
        exit()

    df0,df1 = None,None
    if infilenames[0].find('.csv')>=0:
        df0 = pd.read_csv(infilenames[0])
        df1 = pd.read_csv(infilenames[1])
    elif infilenames[0].find('.h5')>=0 or infilenames[0].find('.hdf')>=0:
        #df0 = pd.read_hdf(infilenames[0])
        #df1 = pd.read_hdf(infilenames[1])
        df0,df1 = None,None
        for i in range(0,2):
            data,event = hepfile.load(infilenames[i])
            keys = data.keys()
            d = {}
            for key in keys:
                # Need to catch ml/nml and ml/nml_INDEX
                if key[0:6] == 'ml/nml':
                    continue

                if key[0:3]=='ml/':
                    d[key[3:]] = data[key]

            # Create an index for the dataframe
            idx = []
            for j,a in enumerate(data['ml/nml']):
                idx += (j*np.ones(a,dtype=int)).tolist()
                        
            d['event_idx'] = np.array(idx)
            df = pd.DataFrame.from_dict(d)
            if i==0:
                df0 = df.copy()
            elif i==1:
                df1 = df.copy()

    return df0, df1

################################################################################
def format(df, columns_to_drop=None, className=None):
    if columns_to_drop is not None:
        df = df.drop(columns=columns_to_drop, errors='ignore') # remove specified columns
        #df = df.drop([0]) # drop feature (column) labels
        #if columns_to_drop is not None:
        #    df = df.drop(columns=columns_to_drop) # drop correct columns

    # add column with class name
    labels = [className] * len(df) #list of labels is the length of the df
    df['Class'] = labels # creates new class column

    return df # returns data frame with new class and reformatted

################################################################################
def changeClassName(df, oldName, newName):
  df["Class"].replace({oldName: newName}, inplace=True) #replaces old name with new name
  return df

################################################################################
def mergeDataframes(dfs):
  mergedDFs = pd.DataFrame()

  for df in dfs:
    mergedDFs = pd.concat([mergedDFs, df])

  # Get rid of nans
  mergedDFs.dropna(0,inplace=True)

  return mergedDFs


################################################################################
def preprocess(df, class_string='Class', test_size=0.20):
  #X = df.iloc[:, 0:xCols] # all features except label
  #y = df.iloc[:, xCols+1:xCols+2] # column with label
  X = df.drop(class_string,axis=1) # all features except label
  y = df[[class_string]] # column with label

  # convert categories into numerical labels
  le = preprocessing.LabelEncoder()
  y = y.apply(le.fit_transform)

  # split sets into training and test sets to minimize over fitting
  # test_size is fraction reserved for testing
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = test_size)

  return X, X_train, X_test, y, y_train, y_test

################################################################################
# train neural net that can make predictions
# initialize mlp w/ 2 parameters:
# *
# hidden_layer_sizes: set size of hidden layers
# this creates 3 layers of 10 nodes each
# try different combinations of layers/nodes to see what works best
# *
#  max_iter: number of epochs/iterations neural net will execute
################################################################################
def train(X_train, y_train, hidden_layers_num = 5, iter_num = 1000, verbose=True):

  mlp = MLPClassifier(hidden_layer_sizes=(hidden_layers_num), max_iter=iter_num, verbose=verbose)

  # fit function: trains algorithm on training data
  model = mlp.fit(X_train, y_train.values.ravel())

  return mlp, model

################################################################################
#Key to Code:
#*   y = dataset w/ id # and class name
#*   X = dataset w/ id #, momentum, energy...
#*   X_train = training set w/ energy, momentum...
#*   y_train = training set w/ class names
#
# returns dictionary with all the df, X, Y, all the training/test sets, mlp, model, and predictions
################################################################################
def learn(myDict, hidden_layers = 5, iterations = 1000):
  df = myDict['df'] # the dataframe
  
  #preprocess
  X, X_train, X_test, y, y_train, y_test = preprocess(df, xCols = len(df.columns)-2)

  myDict['X'] = X
  myDict['y'] = y
  myDict['y_train'] = y_train
  myDict['y_test'] = y_test

  #feature scaling
  #_train, X_test = featureScaling(X_train, X_test)

  myDict['X_train'] = X_train
  myDict['X_test'] = X_test

  #train
  mlp, model = train(X_train, y_train, hidden_layers, iterations)

  myDict['mlp'] = mlp
  myDict['model'] = model

  #predict
  predict_X_test = mlp.predict_proba(X_test)[:,1]

  myDict['predict_X_test'] = predict_X_test

  return myDict
################################################################################


################################################################################
def graphROC(predict_X_test):

  plt.gcf()
  plt.gca()

  decisions = predict_X_test
  # Compute ROC curve and area under the curve
  fpr, tpr, thresholds = roc_curve(y_test, decisions)
  roc_auc = auc(fpr, tpr)

  plt.plot(fpr, tpr, lw=1, label='ROC (area = %0.2f)'%(roc_auc))

  plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')
  plt.xlim([-0.05, 1.05])
  plt.ylim([-0.05, 1.05])
  plt.xlabel('False Positive Rate', color = 'k')
  plt.ylabel('True Positive Rate', color = 'k')
  plt.title('Receiver operating characteristic', color = 'k')
  plt.legend(loc="lower right")
  plt.grid()
  plt.tick_params(axis='x', colors='k')
  plt.tick_params(axis='y', colors='k')

################################################################################
def graphROCfromDict(myDict, ax):

  decisions = myDict['predict_X_test']
  y_test = myDict['y_test']

  # Compute ROC curve and area under the curve
  fpr, tpr, thresholds = roc_curve(y_test, decisions)
  roc_auc = auc(fpr, tpr)

  ax.plot(fpr, tpr, lw=1, label='ROC (area = %0.2f)'%(roc_auc))

  # print(fpr)
  # print(tpr)
  # print("thresh: " , thresholds)

  # print(len(fpr))
  # print(len(tpr))

  ax.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')
  ax.set_xlim([-0.05, 1.05])
  ax.set_ylim([-0.05, 1.05])
  ax.set(xlabel = 'False Positive Rate', ylabel = 'True Positive Rate')
  ax.xaxis.label.set_color('black')
  ax.yaxis.label.set_color('black')
  ax.set_title('Receiver operating characteristic of ' +myDict['title'], color = 'k')
  ax.legend(loc="lower right")
  ax.grid()
  ax.tick_params(axis='x', colors='k')
  ax.tick_params(axis='y', colors='k')

################################################################################

################################################################################
def compare_train_test(model, X_train, y_train, X_test, y_test, bins=30,tag='default'):
    decisions = []

    mask0, mask1, mask2, mask3 = None, None, None, None
    if type(y_test) == np.ndarray:
        mask0 = y_test.ravel()<0.5
        mask1 = y_test.ravel()>0.5
        mask2 = y_train.ravel()<0.5
        mask3 = y_train.ravel()>0.5

    else:
        mask0 = y_test.values.ravel()<0.5
        mask1 = y_test.values.ravel()>0.5
        mask2 = y_train.values.ravel()<0.5
        mask3 = y_train.values.ravel()>0.5

    predictions0 = model.predict(X_test[mask0])
    predictions1 = model.predict(X_test[mask1])
    predictions2 = model.predict(X_train[mask2])
    predictions3 = model.predict(X_train[mask3])

    decisions = [predictions0, predictions1, predictions2, predictions3]
        
    low = min(np.min(d) for d in decisions)
    high = max(np.max(d) for d in decisions)
    low_high = (low,high)

    #plt.figure(figsize=(6,6))
    
    plt.hist(decisions[0],
             color='r', alpha=0.5, range=low_high, bins=bins,
             histtype='stepfilled', density=True,
             label='Background (train)')
    plt.hist(decisions[1],
             color='b', alpha=0.5, range=low_high, bins=bins,
             histtype='stepfilled', density=True,
             label='Signal (train)')

    hist, bins = np.histogram(decisions[2],
                              bins=bins, range=low_high, density=True)
    scale = len(decisions[2]) / sum(hist)
    err = np.sqrt(hist * scale) / scale
    
    width = (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.errorbar(center, hist, yerr=err, fmt='o', c='r', label='Background (test)')
    
    hist, bins = np.histogram(decisions[3],
                              bins=bins, range=low_high, density=True)
    scale = len(decisions[2]) / sum(hist)
    err = np.sqrt(hist * scale) / scale

    plt.errorbar(center, hist, yerr=err, fmt='o', c='b', label='Signal (test)')

    plt.xlabel("Model output", color = 'k')
    plt.ylabel("Arbitrary units", color = 'k')
    plt.legend(loc='best')
    plt.title('Compare Train Test', color = 'k')
    plt.tick_params(axis='x', colors='k')
    plt.tick_params(axis='y', colors='k')

    filename = 'compare_train_test_{0}.png'.format(tag)
    plt.savefig(filename)
    
def graphOvertrainingCheckFromDict(myDict, ax, bins = 30):
    y_test = myDict['y_test']
    y_train = myDict['y_train']
    mlp = myDict['mlp']
    X_test = myDict['X_test']
    X_train = myDict['X_train']
    
    decisions = []

    mask0 = y_test.values.ravel()<0.5
    mask1 = y_test.values.ravel()>0.5
    mask2 = y_train.values.ravel()<0.5
    mask3 = y_train.values.ravel()>0.5

    predictions0 = mlp.predict_proba(X_test[mask0])[:,1]
    predictions1 = mlp.predict_proba(X_test[mask1])[:,1]
    predictions2 = mlp.predict_proba(X_train[mask2])[:,1]
    predictions3 = mlp.predict_proba(X_train[mask3])[:,1]

    decisions = [predictions0, predictions1, predictions2, predictions3]
        
    low = min(np.min(d) for d in decisions)
    high = max(np.max(d) for d in decisions)
    low_high = (low,high)

    #plt.figure(figsize=(6,6))
    
    ax.hist(decisions[0],
             color='r', alpha=0.5, range=low_high, bins=bins,
             histtype='stepfilled', density=True,
             label='Class 0 (train)')
    ax.hist(decisions[1],
             color='b', alpha=0.5, range=low_high, bins=bins,
             histtype='stepfilled', density=True,
             label='Class 1 (train)')

    hist, bins = np.histogram(decisions[2],
                              bins=bins, range=low_high, density=True)
    scale = len(decisions[2]) / sum(hist)
    err = np.sqrt(hist * scale) / scale
    
    width = (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    ax.errorbar(center, hist, yerr=err, fmt='o', c='r', label='Class 0 (test)')
    
    hist, bins = np.histogram(decisions[3],
                              bins=bins, range=low_high, density=True)
    scale = len(decisions[2]) / sum(hist)
    err = np.sqrt(hist * scale) / scale

    ax.errorbar(center, hist, yerr=err, fmt='o', c='b', label='Class 1 (test)')

    ax.set(xlabel="MLP output", ylabel="Arbitrary units")
    ax.legend(loc='best')
    ax.set_title('Compare Train Test of '+myDict['title'], color = 'k')
    ax.tick_params(axis='x', colors='k')
    ax.tick_params(axis='y', colors='k')
    ax.xaxis.label.set_color("black")
    ax.yaxis.label.set_color("black")
################################################################################

################################################################################
def tablesReportFromDict(myDict):
  y_test = myDict['y_test']
  X_test = myDict['X_test']
  mlp = myDict['mlp']

  predictBinary_X_test = mlp.predict(X_test)

  #show table report first
  print("----------------------------------------------------------------------")
  print("Confusion Matrix from " + myDict['title'] + ": \n")
  print(confusion_matrix(y_test, predictBinary_X_test))
  print('')
  print("----------------------------------------------------------------------")
  print("Classification Report " + myDict['title'] + ": \n")
  print(classification_report(y_test,predictBinary_X_test))
  print('')
  print("----------------------------------------------------------------------")
  
################################################################################


################################################################################
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix

# for binary classifications (0 or 1)
def graphPredictions(predict_X_test, mlp, X_test, y_test, oneClass, zeroClass):
  
  #show table report first
  print("----------------------------------------------------------------------")
  print("Confusion Matrix: \n")
  print(confusion_matrix(y_test, predict_X_test))
  print('')
  print("----------------------------------------------------------------------")
  print("Classification Report: \n")
  print(classification_report(y_test,predict_X_test))
  print('')
  print("----------------------------------------------------------------------")
  
  #then graphic report
  mask0 = y_test.values.ravel()<0.5
  mask1 = y_test.values.ravel()>0.5

  predictions0 = mlp.predict(X_test[mask0])
  predictions1 = mlp.predict(X_test[mask1])

  #plt.figure(figsize=(8,5))
  plt.hist([predictions0, predictions1], bins= 2, stacked = True)
  plt.ylabel('# Occurences', color = 'k')
  plt.xlabel('Prediction', color = 'k')
  plt.legend([(zeroClass + ' (prediction should be 0)'), (oneClass + ' (prediction should be 1)')])
  plt.title('Stacked Histogram of Predictions of Test Data', color = "y", size = 18)
  plt.tick_params(axis='x', colors='k')
  plt.tick_params(axis='y', colors='k')

def graphPredictionsFromDict(myDict, ax):
  y_test = myDict['y_test']
  X_test = myDict['X_test']
  X_train = myDict['X_train']
  y_train = myDict['y_train']
  mlp = myDict['mlp']
  predict_X_test = myDict['predict_X_test']
  zeroClass = myDict['zeroClass']
  oneClass = myDict['oneClass']

  #then graphic report----------------------------------------------------------

  # these mask sgo through the y_test values and return True or False 
  # mask0 returns true if y_test is less than 0.5 (0)
  # mask1 returns true if y_test is greater than 0.5 (1)
  mask0 = y_test.values.ravel()<0.5
  mask1 = y_test.values.ravel()>0.5

  # X_test[mask0] returns X_test data whose true label is 0
  # X_test[mask1] returns X_test data whose true label is 1
  # predictions0 makes predictions on X_test data that should be 0
  # predictions1 makes predicitons on X_test data that should be 1
  predictions0 = mlp.predict_proba(X_test[mask0])[:,1]
  predictions1 = mlp.predict_proba(X_test[mask1])[:,1]

  #plt.figure(figsize=(8,5))
  ax.hist([predictions0, predictions1], bins= 200, stacked = True, density=True)
  ax.set(xlabel='Prediction', ylabel='# Occurences')
  ax.legend([(zeroClass + ' (prediction should be 0)'), (oneClass + ' (prediction should be 1)')])
  ax.set_title('Predictions of ' + myDict['title'], color = "k")
  ax.tick_params(axis='x', colors='k')
  ax.tick_params(axis='y', colors='k')  
  ax.xaxis.label.set_color("black")
  ax.yaxis.label.set_color("black")


################################################################################
def graphicReport(myDict):
  fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15,4))
  fig.suptitle(myDict['title'], color = 'black', size = '18')

  graphPredictionsFromDict(myDict,ax1)
  graphROCfromDict(myDict, ax2)
  graphOvertrainingCheckFromDict(myDict, ax3, bins=30)

################################################################################


























################################################################################
def plot_corr_matrix(df,title="Correlation matrix",figsize=None):

    print("Plotting the correlation matrices!")

    classes = np.unique(df['Class'])

    figs,axes = [], []
    for cl in classes:
        print("For class " + cl)
        keys = list(df.keys())
        if 'Class' in list(keys):
            keys.remove('Class')
        ccmat = []
        mask = df['Class']==cl
        for i in range(len(keys)):
            ccmat.append([])
            for j in range(len(keys)):
                #print(keys[i], keys[j])
                x = df[keys[i]][mask]
                y = df[keys[j]][mask]
                ccmat[i].append(np.corrcoef(x,y)[0][1])


        fig = plt.figure(figsize=figsize)
        ax = plt.subplot(1,1,1)
        opts = {'cmap': plt.get_cmap("RdBu"), 'vmin': -1, 'vmax': +1}
        heatmap1 = ax.pcolor(ccmat, **opts)
        plt.colorbar(heatmap1, ax=ax)
        ax.set_title("{0} {1}".format(title,cl))

        #for ax in (ax1,):
        if 1:
            # shift location of ticks to center of the bins
            ax.set_xticks(np.arange(len(keys))+0.5, minor=False)
            ax.set_yticks(np.arange(len(keys))+0.5, minor=False)
            ax.set_xticklabels(keys, minor=False, ha='right', rotation=70)
            ax.set_yticklabels(keys, minor=False)

        plt.tight_layout()
        plt.savefig("plots/{0}.png".format(cl))
        figs.append(fig)
        axes.append(ax)

    print("Plotted the correlation matrices!")
    return figs,axes
################################################################################
################################################################################
'''
def compare_train_test(clf, X_train, y_train, X_test, y_test, bins=30):
    decisions = []
    for X,y in ((X_train, y_train), (X_test, y_test)):

        if hasattr(clf, "decision_function"):
            d1 = clf.decision_function(X[y>0.5]).ravel()
            d2 = clf.decision_function(X[y<0.5]).ravel()
        else:
            print("NO DECISION FUNCTION")
            #decisions = bdt.predict_proba(X_test)
            d1 = clf.predict_proba(X[y>0.5]).ravel()
            d2 = clf.predict_proba(X[y<0.5]).ravel()
        #d1 = clf.decision_function(X[y>0.5]).ravel()
        #d2 = clf.decision_function(X[y<0.5]).ravel()

        decisions += [d1, d2]
     
    low = min(np.min(d) for d in decisions)
    high = max(np.max(d) for d in decisions)
    low_high = (low,high)
 
    fig = plt.figure()
    plt.hist(decisions[0],
            color='r', alpha=0.5, range=low_high, bins=bins,
            histtype='stepfilled', density=True,
            label='S (train)')
    plt.hist(decisions[1],
            color='b', alpha=0.5, range=low_high, bins=bins,
            histtype='stepfilled', density=True,
            label='B (train)')

    hist, bins = np.histogram(decisions[2],
                            bins=bins, range=low_high, density=True)
    scale = len(decisions[2]) / sum(hist)
    err = np.sqrt(hist * scale) / scale
 
    width = (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.errorbar(center, hist, yerr=err, fmt='o', c='r', label='S (test)')
 
    hist, bins = np.histogram(decisions[3],
                            bins=bins, range=low_high, density=True)
    scale = len(decisions[2]) / sum(hist)
    err = np.sqrt(hist * scale) / scale

    plt.errorbar(center, hist, yerr=err, fmt='o', c='b', label='B (test)')

    plt.xlabel("BDT output")
    plt.ylabel("Arbitrary units")
    plt.legend(loc='best')

    plt.savefig("plots/BDT_output.png")
    return fig
'''
 


################################################################################
################################################################################
def plot_results(data0, data1, dataset0name, dataset1name, param_labels, bdt, show=False):

    nparams = len(data0)
    ################################################################################
    # Plot the correlation matrices
    ################################################################################
    for idx,data in enumerate([data0,data1]):
        corrcoefs = []
        #plt.figure()
        for i in range(nparams):
            corrcoefs.append([])
            for j in range(nparams):
                #plt.subplot(nparams,nparams,1+i+nparams*j)
                x = data[i]
                y = data[j]
                #plt.plot(x,y,'.',markersize=1)
                #plt.xlim(0,2)
                #plt.ylim(0,2)
                #plt.xlabel(param_labels[i],fontsize=10)
                #plt.ylabel(param_labels[j],fontsize=10)

                corrcoefs[i].append(np.corrcoef(x,y)[0][1])

        #plt.tight_layout()

        #print(corrcoefs)

        #fig,ax = plot_corr_matrix(corrcoefs,param_labels,title="Correlation matrix ({0})".format(infilenames[idx]))
        if idx==0:
            title = title="Correlation matrix ({0})".format(dataset0name)
        else:
            title = title="Correlation matrix ({0})".format(dataset1name)
        #fig,ax = plot_corr_matrix(corrcoefs,param_labels,title=title)
        fig,ax = plot_corr_matrix(corrcoefs,param_labels,title='tmp')

    ################################################################################
    # Plot data
    ################################################################################

    plt.figure(figsize=(14,11))
    for i in range(len(param_labels)):
        plt.subplot(5,5,1+i)
        x0 = data0[i]
        x1 = data1[i]
        lo0,hi0 = min(x0),max(x0)
        lo1,hi1 = min(x1),max(x1)
        lo = lo0
        if lo1<lo0:
            lo = lo1
        hi = hi0
        if hi1>hi0:
            hi = hi1

        if param_labels[i]=='ncharged' or param_labels[i]=='nphot':
            plt.hist(x0, color='r', alpha=0.5, range=(0,25), bins=25, histtype='stepfilled', density=True, label=dataset0name)
            plt.hist(x1, color='b', alpha=0.5, range=(0,25), bins=25, histtype='stepfilled', density=True, label=dataset1name)
        else:
            plt.hist(x0, color='r', alpha=0.5, range=(lo,hi), bins=50, histtype='stepfilled', density=True, label=dataset0name)
            plt.hist(x1, color='b', alpha=0.5, range=(lo,hi), bins=50, histtype='stepfilled', density=True, label=dataset1name)
        plt.xlabel(param_labels[i],fontsize=14)
        plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig("plots/BDT_data.png")

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

    X_dev,X_eval, y_dev,y_eval = train_test_split(X, y, test_size=0.33, random_state=42)
    X_train,X_test, y_train,y_test = train_test_split(X_dev, y_dev, test_size=0.33, random_state=492)

    ################################################################################
    # Fit/Classify
    ################################################################################
    
    #bdt.fit(X_train, y_train)

    probas = bdt.predict_proba(X_test)
    print("probas")
    print(probas)
    print(y_test)
    #plt.figure()
    #plt.plot(y_test,probas,'.')
    
    # The order is because we said that the signal was 1 earlier and the background was 0 (labels).
    # So those are the columns they get put in for the probabilities.
    probbkg,probsig = probas.transpose()[:]
    xpts = []
    ypts0 = []
    ypts1 = []
    for i in np.linspace(0,1.0,10000):
        xpts.append(i)
        ypts0.append(len(probsig[(probsig>i)*(y_test==1)]))
        ypts1.append(len(probsig[(probsig>i)*(y_test==0)]))
    #print(xpts)
    #print(ypts)
    
    n0 = float(len(y_test[y_test==1]))
    n1 = float(len(y_test[y_test==0]))
    ypts0 = np.array(ypts0)
    ypts1 = np.array(ypts1)

    plt.figure(figsize=(8,8))
    plt.subplot(2,2,1)
    plt.plot(xpts,ypts0)
    plt.xlabel("Cut on probability of being signal")
    plt.ylabel("# of signal remaining")

    plt.subplot(2,2,2)
    plt.plot(xpts,ypts1)
    plt.xlabel("Cut on probability of being signal")
    plt.ylabel("# of background remaining")

    plt.subplot(2,2,3)
    plt.plot(ypts1/n1,ypts0/n0)
    plt.xlabel("Fraction of background remaining")
    plt.ylabel("Fraction of signal remaining")

    # For Punzi calculation
    a = 4.0
    B0 = 100.0

    sig_eps = ypts0/n0
    bkg_eps = ypts1/n1

    fom = sig_eps/((a/2.0) + np.sqrt(bkg_eps*B0))

    #plt.subplot(2,2,4)
    plt.figure(figsize=(6,5))
    plt.plot(sig_eps, fom)
    plt.xlabel("Fraction of signal remaining",fontsize=14)
    plt.ylabel("Punzi figure of merit",fontsize=14)
    plt.tight_layout()
    plt.savefig("plots/BDT_fom.png")


    plt.tight_layout()

    ################################################################################
    # Performance
    ################################################################################
    y_pred = bdt.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy (train) for %s: %0.1f%% " % ("BDT", accuracy * 100))

    y_predicted = bdt.predict(X_test)
    print(classification_report(y_test, y_predicted, target_names=["background", "signal"]))
    #print("Area under ROC curve: %.4f"%(roc_auc_score(y_test, bdt.decision_function(X_test))))

    y_predicted = bdt.predict(X_train)
    print(classification_report(y_train, y_predicted, target_names=["background", "signal"]))
    #print("Area under ROC curve: %.4f"%(roc_auc_score(y_train, bdt.decision_function(X_train))))

    ################################################################################
    # ROC curve
    ################################################################################
    if hasattr(bdt, "decision_function"):
        #decisions = bdt.decision_function(X_test)
        decisionsTest = bdt.decision_function(X_test)
        decisionsTrain = bdt.decision_function(X_train)
    else:
        print("NO DECISION FUNCTION")
        #decisions = bdt.predict_proba(X_test)
        decisionsTest = bdt.predict_proba(X_test)
        decisionsTrain = bdt.predict_proba(X_train)
    #decisions = bdt.decision_function(X_test)
    # Compute ROC curve and area under the curve
    #fpr, tpr, thresholds = roc_curve(y_test, decisions)
    print(y_test.shape)
    print(decisionsTest.shape)
    print(decisionsTest[0:4])
    #fpr, tpr, thresholds = roc_curve(y_test, decisionsTest)
    fpr, tpr, thresholds = roc_curve(y_test, decisionsTest.transpose()[1])
    roc_auc = auc(fpr, tpr)
    
    plt.figure()
    plt.plot(fpr, tpr, lw=1, label='ROC (area = %0.2f)'%(roc_auc))
    
    plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.grid()
    plt.savefig("plots/roc_curve.png")
    
    figctt = compare_train_test(bdt, X_train, y_train, X_test, y_test)
    print("HERE AFTER COMPARE")
    
    if show:
        plt.show()

    return 0

################################################################################
    
################################################################################
if __name__=="__main__":
    infilename = sys.argv[1]
    results = pickle.load(open(infilename,'rb'))
    data0 = results["data0"]
    data1 = results["data1"]
    param_labels = results["param_labels"]
    bdt = results["classifier"]
    dataset0name = results["dataset0"]
    dataset1name = results["dataset1"]

    plot_results(data0,data1,dataset0name,dataset1name,param_labels,bdt,show=True)


