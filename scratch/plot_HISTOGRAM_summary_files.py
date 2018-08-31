#import topbnv_tools as tbt

import numpy as np
import matplotlib.pylab as plt

import sys

import lichen.lichen as lch

import pickle


def combine_bins(h,bin_edges,n=2):

    print(len(bin_edges)-1/n)

    x = []
    y = [bin_edges[0]]

    for i in range(0,len(h),n):

        v0 = np.sum(h[i:i+n])

        x.append(v0)
        y.append(bin_edges[i+n])

    return x,y

################################################################################
def main(infiles=None):


    names = ['leadmupt', 'topmass','Wmass','jetcsv']

    mcdatasets = ["WW","ZZ","WZ","WJets","DYJetsToLL_M-50","DYJetsToLL_M-10to50","TT_Tune","TTGJets"]

    plots = {}
    for name in names:
        plots[name] = {}
        for dataset in mcdatasets:
            plots[name][dataset] = {'bin_vals':[], 'bin_edges':[]}

    for i,infile in enumerate(infiles):

        filedataset = infile.split('DATASET_')[1].split('_NFILES')[0]

        dataset = None
        for ds in mcdatasets:
            if filedataset.find(ds)>=0:
                dataset = ds
                break
        if dataset is None:
            print("No dataset for {0}".format(filedataset))



        for key in plots.keys():
            datasetkeys = list(plots[key].keys())
            if dataset not in datasetkeys:
                plots[key][dataset] = {'bin_vals':[], 'bin_edges':[]}

        f = open(infile)

        while(1):

            vals = f.readline().split()
            if len(vals)==0:
                break

            #print(vals)

            name = vals[0]

            if name in names:

                bin_vals = vals[1:]
                vals = f.readline().split()
                bin_edges = vals[1:]

                bin_vals = np.array(bin_vals).astype(float)
                bin_edges = np.array(bin_edges).astype(float)

                if len(plots[name][dataset]['bin_vals'])==0:
                    plots[name][dataset]['bin_vals'] = bin_vals
                    plots[name][dataset]['bin_edges'] = bin_edges
                else:
                    plots[name][dataset]['bin_vals'] += bin_vals
                    #plots[name]['bin_edges'] += bin_edges

    #print(plots)

    plt.figure(figsize=(12,8))

    for i,name in enumerate(names):
        for dataset in plots[name].keys():
            plt.subplot(2,3,1+i)
            #print(plots[name]['bin_vals'],plots[name]['bin_edges'])
            #x,y = combine_bins(plots[name]['bin_vals'],plots[name]['bin_edges'],n=4)
            x,y = plots[name][dataset]['bin_vals'],plots[name][dataset]['bin_edges']
            x = np.array(x); y = np.array(y)
            xbins = (y[0:-1] + y[1:])/2.
            plt.errorbar(xbins, x,yerr=np.sqrt(x),fmt='.',label=dataset)

    plt.legend()

    '''
    plt.subplot(2,3,2)
    lch.hist_err(topmass[topmass<1200],bins=400,alpha=0.2)

    plt.subplot(2,3,3)
    lch.hist_err(Wmass[Wmass<1200],bins=400,range=(0,400),alpha=0.2)

    plt.subplot(2,3,4)
    lch.hist_err(Wmass[(Wmass>40)*(Wmass<150)],bins=100,alpha=0.2)

    plt.subplot(2,3,5)
    lch.hist_err(njet,bins=20,range=(0,20),alpha=0.2)

    plt.subplot(2,3,6)
    lch.hist_err(nbjet,bins=8,range=(0,8),alpha=0.2)

    #lch.hist_err(jetcsv,bins=400)

    plt.figure(figsize=(12,8))
    plt.subplot(2,3,1)
    lch.hist_err(ntop,bins=20,range=(0,20),alpha=0.2)

    plt.subplot(2,3,2)
    lch.hist_err(nmuon,bins=20,range=(0,20),alpha=0.2)
    '''


    plt.show()


    return 1


################################################################################
if __name__=="__main__":
    infiles = sys.argv[1:]
    main(infiles)
