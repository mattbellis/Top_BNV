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

# Getting some of this from here
# https://betatim.github.io/posts/sklearn-for-TMVA-users/

################################################################################
def plot_corr_matrix(ccmat,labels,title="Correlation matrix"):
    fig1 = plt.figure()
    ax1 = plt.subplot(1,1,1)
    opts = {'cmap': plt.get_cmap("RdBu"), 'vmin': -1, 'vmax': +1}
    heatmap1 = ax1.pcolor(ccmat, **opts)
    plt.colorbar(heatmap1, ax=ax1)
    ax1.set_title(title)

    for ax in (ax1,):
        # shift location of ticks to center of the bins
        ax.set_xticks(np.arange(len(labels))+0.5, minor=False)
        ax.set_yticks(np.arange(len(labels))+0.5, minor=False)
        ax.set_xticklabels(labels, minor=False, ha='right', rotation=70)
        ax.set_yticklabels(labels, minor=False)

    plt.tight_layout()
    plt.savefig("plots/{0}.png".format(title.replace(' ','_').replace('.pkl','').replace('(','').replace(')','')))
    
    return fig1,ax1
################################################################################
################################################################################
def compare_train_test(clf, X_train, y_train, X_test, y_test, bins=30):
    decisions = []

    if hasattr(clf,"decision_function"):
        for X,y in ((X_train, y_train), (X_test, y_test)):
            d1 = clf.decision_function(X[y>0.5]).ravel()
            d2 = clf.decision_function(X[y<0.5]).ravel()
            decisions += [d1, d2]
    else:
        for X,y in ((X_train, y_train), (X_test, y_test)):
            d1 = clf.predict_proba(X[y>0.5]).ravel()
            d2 = clf.predict_proba(X[y<0.5]).ravel()
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
 


################################################################################
################################################################################
def plot_results(data0, data1, dataset0name, dataset1name, param_labels, bdt, show=False):

    if len(dataset0name)>24:
        dataset0name = dataset0name[0:24]

    if len(dataset1name)>24:
        dataset1name = dataset1name[0:24]

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
        fig,ax = plot_corr_matrix(corrcoefs,param_labels,title=title)

    ################################################################################
    # Plot data
    ################################################################################

    plt.figure(figsize=(14,11))
    for i in range(len(param_labels)):
        plt.subplot(4,5,1+i)
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
    # Difference detailed here
    # https://stackoverflow.com/questions/36543137/whats-the-difference-between-predict-proba-and-decision-function-in-scikit-lear
    # 
    # Search for relevant code in this example
    # https://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html
    print(X_test.shape, X_train.shape)
    if hasattr(bdt, "decision_function"):
        print("HAS DECISION FUNCTION!")
        decisionsTest = bdt.decision_function(X_test)
        decisionsTrain = bdt.decision_function(X_train)
    else:
        print("DOES NOT HAVE DECISION FUNCTION!")
        decisionsTest = bdt.predict_proba(X_test)
        decisionsTrain = bdt.predict_proba(X_train)
    
    y_pred = bdt.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy (train) for %s: %0.1f%% " %("BDT", accuracy * 100))

    y_predicted = bdt.predict(X_test)
    print(classification_report(y_test, y_predicted, target_names=["background", "signal"]))
    print(y_test.shape, decisionsTest.shape)
    decisionsTest = [x[0] for x in decisionsTest]
    decisionsTest = np.array(decisionsTest)
    print(y_test.shape, decisionsTest.shape)
    print("Area under ROC curve: %.4f"%(roc_auc_score(y_test, decisionsTest)))

    y_predicted = bdt.predict(X_train)
    print(classification_report(y_train, y_predicted, target_names=["background", "signal"]))
    decisionsTrain = [x[0] for x in decisionsTrain]
    decisionsTrain = np.array(decisionsTrain)
    print("Area under ROC curve: %.4f"%(roc_auc_score(y_train, decisionsTrain)))

    ################################################################################
    # ROC curve
    ################################################################################
    # Compute ROC curve and area under the curve
    fpr, tpr, thresholds = roc_curve(y_test, decisionsTest)
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

    # What features are most important?
    feature_importances = bdt.feature_importances_
    estimators = bdt.estimators_
    print(len(feature_importances))
    for f,pl in zip(feature_importances, param_labels):
        print(f,pl)
    
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

    print("Number of events in file: ", results["nevents"])

    plot_results(data0,data1,dataset0name,dataset1name,param_labels,bdt,show=True)


