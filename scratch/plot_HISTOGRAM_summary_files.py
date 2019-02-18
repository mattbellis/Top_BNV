#import topbnv_tools as tbt

import numpy as np
import matplotlib.pylab as plt

import sys

import lichen.lichen as lch

import pickle

import myhist as mh

from simple_MCinfo import mc_info

from collections import OrderedDict

mcparamsnames = list(mc_info.keys())

#print(mc_info)

data_int_lumi = 37.* (1.0/1e-15) # 35 ifb --> inv barns

print(" {1:15s} {2:12s} {3:12s} {4} {0}".format("Dataset","Weight","# gen","N","cross section"))
for key in mc_info.keys():
    entry = mc_info[key]
    Ngen = entry['completed_events']
    xsec = entry['cross_section']*1e-12 # pb --> barns

    N = xsec * data_int_lumi

    wt = N/Ngen

    mc_info[key]['weight'] = wt

    print(" {1:12.3f} {2:12} {3:12d} {4:12.2e} {0}".format(key,wt,Ngen,int(N),xsec))

#exit()


################################################################################
def combine_bins(h,bin_edges,n=2):

    #print(len(bin_edges)-1/n)

    x = []
    y = [bin_edges[0]]

    for i in range(0,len(h),n):

        v0 = np.sum(h[i:i+n])

        x.append(v0)
        y.append(bin_edges[i+n])

    return x,y
################################################################################

################################################################################
def main(infiles=None):


    colors = ['k','b','r','g','y','m','c','orange']
    names = ['leadmupt', 'hadtopmass','Wmass','jetcsv', 'leadmupt_cut0', 'hadtopmass_cut0', 'Wmass_cut0']
    xaxislabels = [r'leading $\mu$ p_T [GeV/c]', 
                   r'Top candidate mass [GeV/c$^2$]', 
                   r'$W$ candidate mass [GeV/c$^2$]', 
                   r'Jet CSVv2 variable',
                   r'leading $\mu$ p_T [GeV/c]', 
                   r'Top candidate mass [GeV/c$^2$]', 
                   r'$W$ candidate mass [GeV/c$^2$]'
                   ]

    mcdatasets = ["WW","ZZ","WZ","WJets","DYJetsToLL_M-50","DYJetsToLL_M-10to50","TT_Tune","TTGJets"]
    datadatasets = ['Data (2016)']

    plots = OrderedDict()
    dataplots = OrderedDict()
    for name in names:
        plots[name] = OrderedDict()
        dataplots[name] = OrderedDict()
        for dataset in mcdatasets:
            plots[name][dataset] = {'bin_vals':[], 'bin_edges':[]}
        for dataset in datadatasets:
            dataplots[name][dataset] = {'bin_vals':[], 'bin_edges':[]}

    for i,infile in enumerate(infiles):

        wt = 1.0
        for name in mcparamsnames:
            if infile.find(name)>=0:
                wt = mc_info[name]['weight']
        print(wt,infile)

        isData = False

        filedataset = infile.split('DATASET_')[1].split('_NFILES')[0]

        dataset = None

        if infile.find('DATA_DATASET')>=0:
            dataset = "Data (2016)"
            isData = True
        else:
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

                if isData == False:
                    if len(plots[name][dataset]['bin_vals'])==0:
                        plots[name][dataset]['bin_vals'] = bin_vals * wt
                        plots[name][dataset]['bin_edges'] = bin_edges
                    else:
                        plots[name][dataset]['bin_vals'] += bin_vals * wt
                else:
                    if len(dataplots[name][dataset]['bin_vals'])==0:
                        dataplots[name][dataset]['bin_vals'] = bin_vals
                        dataplots[name][dataset]['bin_edges'] = bin_edges
                    else:
                        dataplots[name][dataset]['bin_vals'] += bin_vals

    #print(plots)

    ############################################################################
    plt.figure(figsize=(12,8))

    maxvals = np.zeros(len(names))
    for i,name in enumerate(names):
        for j,dataset in enumerate(plots[name].keys()):
            plt.subplot(3,3,1+i)
            #print(plots[name]['bin_vals'],plots[name]['bin_edges'])
            #x,y = combine_bins(plots[name][dataset]['bin_vals'],plots[name][dataset]['bin_edges'],n=8)
            x,y = plots[name][dataset]['bin_vals'],plots[name][dataset]['bin_edges']

            x = np.array(x); y = np.array(y)
            xbins = (y[0:-1] + y[1:])/2.
            plt.errorbar(xbins, x,yerr=np.sqrt(x),fmt='.',label=dataset,color=colors[j%len(colors)])

        for j,dataset in enumerate(dataplots[name].keys()):
            #x,y = combine_bins(dataplots[name][dataset]['bin_vals'],dataplots[name][dataset]['bin_edges'],n=8)
            x,y = dataplots[name][dataset]['bin_vals'],dataplots[name][dataset]['bin_edges']
            x = np.array(x); y = np.array(y)
            xbins = (y[0:-1] + y[1:])/2.
            plt.errorbar(xbins, x,yerr=np.sqrt(x),fmt='.',label=dataset,color="k")


            '''
            mh.hh(x, y, plt.gca())
            if max(x)>maxvals[i]:
                maxvals[i] = max(x)
            '''
        plt.xlabel(xaxislabels[i],fontsize=18)


    plt.legend()
    plt.tight_layout()

    '''
    for i,name in enumerate(names):
        plt.subplot(3,3,1+i)
        plt.ylim(0,1.1*maxvals[i])
    '''


    ############################################################################
    # Stacked
    ############################################################################

    # Make an empty plot for the legend
    plt.figure(figsize=(5,4),dpi=100)
    for j,dataset in enumerate(plots[name].keys()):
        plt.plot([0,0],[0,0],color=colors[j%len(colors)],label=dataset,linewidth=8)
    plt.axis('off')
    plt.legend(loc='center',fontsize=18)
    plt.tight_layout()
    plt.savefig('plots/legend.png')


    plt.figure(figsize=(12,8))
    for i,name in enumerate(names):
        plt.subplot(3,3,1+i)
        #plt.figure(figsize=(5,4),dpi=100)

        heights,bins = [],[]
        for j,dataset in enumerate(plots[name].keys()):
            #print(dataset)
            if len(plots[name][dataset]['bin_vals'])>0:
                heights.append(plots[name][dataset]['bin_vals'])
                bins.append(plots[name][dataset]['bin_edges'])
                plt.plot([0,0],[0,0],color=colors[j%len(colors)],label=dataset)

        #print(heights)
        #print(bins)
        if len(heights)>0:
            mh.shh(heights,bins,color=colors,ax=plt.gca())

        for j,dataset in enumerate(dataplots[name].keys()):
            #x,y = combine_bins(dataplots[name][dataset]['bin_vals'],dataplots[name][dataset]['bin_edges'],n=8)
            x,y = dataplots[name][dataset]['bin_vals'],dataplots[name][dataset]['bin_edges']
            x = np.array(x); y = np.array(y)
            xbins = (y[0:-1] + y[1:])/2.
            plt.errorbar(xbins, x,yerr=np.sqrt(x),fmt='.',label=dataset,color="k")

        plt.xlabel(xaxislabels[i],fontsize=14)
        #plt.legend()
        plt.tight_layout()

        figname = "plots/fig_{0}.png".format(name)
        plt.savefig(figname)

    plt.show()

    return 1


################################################################################
if __name__=="__main__":
    infiles = sys.argv[1:]
    main(infiles)
