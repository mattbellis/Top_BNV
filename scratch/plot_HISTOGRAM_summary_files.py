#import topbnv_tools as tbt

import numpy as np
import matplotlib.pylab as plt

import sys

import lichen.lichen as lch

import pickle

import myhist as mh

#from simple_MCinfo import mc_info

from collections import OrderedDict

#mc_info = pickle.load(open('MCInfo.pkl','rb'))
mc_info = pickle.load(open('MCInfo_2017.pkl','rb'))


#print(mc_info)

data_int_lumi = 37.* (1.0/1e-15) # 35 ifb --> inv barns

print(" {1:15s} {2:15s} {3:15s} {4:8}      {0}".format("Dataset","Weight","# gen","N","cross section"))
keys = list(mc_info.keys())
for key in keys:

    # We need this step because we had to truncate some of the dataset names
    newkey = key
    if len(key)>=50:
        newkey = key[0:50]+'_'+key[-5:]

    entry = mc_info[key]
    Ngen = float(entry['completed_events'])
    xsec = float(entry['crosssection'])*1e-12 # pb --> barns

    N = xsec * data_int_lumi

    wt = N/Ngen

    mc_info[key]['weight'] = wt

    print(" {1:12.3f} {2:15} {3:15d} {4:12.2e}      {0}".format(key,wt,Ngen,int(N),xsec))

    mc_info[newkey] = mc_info.pop(key)
    #del mc_info[key]

mcparamsnames = list(mc_info.keys())
print(mc_info.keys())

#exit()

################################################################################
def combine_bins(h,bin_edges,n=2):

    #print(len(bin_edges)-1/n)

    if len(h)==0 or len(bin_edges)==0:
        return h,bin_edges

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

    colors = ['k','b','r','g','y','m','c','orange', '#fff8dc', '#d2b48c', '#a52a2a']
    #colors = ['k','b','r','g','y','m','c','orange', 'b', 'r', 'g', 'y']
    mcdatasets = ["WW","ZZ","WZ","WJets","DYJetsToLL_M-50","DYJetsToLL_M-10to50","TT_Tune","TTGJets", "TTTo2L2Nu", "TTToHadronic", "TTToSemiLeptonic"]
    datadatasets = ['Data (2016)']
    #datadatasets = ['Data (2017)']

    print("# mcdatasets   {0}".format(len(mcdatasets)))
    print("# datadatasets {0}".format(len(datadatasets)))
    print("# colors       {0}".format(len(colors)))

    #exit()

    # Get the information on the plots from the first infile
    infile = open(infiles[0],'r')
    line = infile.readline()
    names = [] # Names of plots to make
    xlabels = []
    ylabels = []
    while line:
        names.append(line.split()[0])

        line = infile.readline()

        line = infile.readline()
        xlabels.append(' '.join(line.split()[1:]))
        line = infile.readline()
        ylabels.append(' '.join(line.split()[1:]))
        
        line = infile.readline()

    #print(names)
    #print(xlabels)
    #print(ylabels)



    print(names)
    cut_strings = []
    basenames = []
    for name in names:
        cut_string = name.split("_cut")[-1]
        basename = name.split("_cut")[0]
        if cut_string not in cut_strings:
            cut_strings.append(cut_string)
        if basename not in basenames:
            basenames.append(basename)
    print(cut_strings)
    print(basenames)
    #exit()
    
    # Build a dictionary of the histogram information
    plots = OrderedDict()
    dataplots = OrderedDict()
    for name,xlabel,ylabel in zip(names,xlabels,ylabels):
        plots[name] = OrderedDict()
        dataplots[name] = OrderedDict()
        for dataset in mcdatasets:
            plots[name][dataset] = {'bin_vals':[], 'bin_edges':[], 'xlabel':xlabel, 'ylabel':ylabel}
        for dataset in datadatasets:
            dataplots[name][dataset] = {'bin_vals':[], 'bin_edges':[], 'xlabel':xlabel, 'ylabel':ylabel}





    # Loop over the input files
    for i,infile in enumerate(infiles):

        wt = 1.0
        #print("---------")
        #print(infile)
        for name in mcparamsnames:
            #print(name)
            if infile.find(name)>=0:
                wt = mc_info[name]['weight']
        print(i,wt,infile)

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
            #print("==========")
            #print(vals)



            if len(vals)==0:
                break

            #print(vals)

            name = vals[0]

            if name in names:

                #print(name)

                bin_vals = vals[1:]
                vals = f.readline().split()
                bin_edges = vals[1:]

                # Just placeholders here
                xlabels = f.readline().split()
                ylabels = f.readline().split()

                #print("-----")
                #print(xlabels,ylabels)
                #print(bin_edges)
                #print(bin_vals)
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


    for i,name in enumerate(names):
        for j,dataset in enumerate(plots[name].keys()):

            plt.subplot(10,10,1+i)
            
            x,y = combine_bins(plots[name][dataset]['bin_vals'],plots[name][dataset]['bin_edges'],n=2)
            #x,y = plots[name][dataset]['bin_vals'],plots[name][dataset]['bin_edges']

            x = np.array(x); y = np.array(y)
            xbins = (y[0:-1] + y[1:])/2.
            plt.errorbar(xbins, x,yerr=np.sqrt(x),fmt='.',label=dataset,color=colors[j%len(colors)])
            print(dataset,j,j%len(colors),colors[j%len(colors)])

        for j,dataset in enumerate(dataplots[name].keys()):
            x,y = combine_bins(dataplots[name][dataset]['bin_vals'],dataplots[name][dataset]['bin_edges'],n=2)
            #x,y = dataplots[name][dataset]['bin_vals'],dataplots[name][dataset]['bin_edges']
            x = np.array(x); y = np.array(y)
            xbins = (y[0:-1] + y[1:])/2.
            plt.errorbar(xbins, x,yerr=np.sqrt(x),fmt='.',label=dataset,color="k")


            '''
            mh.hh(x, y, plt.gca())
            if max(x)>maxvals[i]:
                maxvals[i] = max(x)
            '''
            plt.xlabel(dataplots[name][dataset]['xlabel'])#,fontsize=18)
            #plt.ylabel(dataplots[name][dataset]['ylabel'])#,fontsize=18)


    #plt.legend()
    #plt.tight_layout()

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
    plt.legend(loc='center')#,fontsize=18)
    #plt.tight_layout()
    plt.savefig('plots/legend.png')


    figs = []
    for i in range(len(cut_strings)):
        figs.append(plt.figure(figsize=(12,8)))

    # Single plots
    single_figs = []
    single_axes = []
    vars_to_plot = ['hadtopmass', 'bnvtopmass', 'leadmupt', 'leadelectronpt','metpt', 'leadmueta', 'leadmuphi', 'leadelectroneta', 'leadelectronphi']
    for i in range(len(cut_strings)):
        single_figs.append([])
        single_axes.append([])
        for j in range(len(vars_to_plot)):
            single_figs[i].append(plt.figure(figsize=(4,4)))
            single_axes[i].append(single_figs[i][j].add_subplot(1,1,1))

    for i,name in enumerate(names):

        cut_string = int(name.split("_cut")[-1])
        basename = name.split("_cut")[0]
        idx = basenames.index(basename)
        print(name,cut_string,idx)

        ax = figs[cut_string].add_subplot(7,7,1+idx)
        plt.sca(ax)
        #plt.figure(figsize=(5,4),dpi=100)

        heights,bins = [],[]
        tempcolors = []
        for j,dataset in enumerate(plots[name].keys()):
            #print(dataset)
            if len(plots[name][dataset]['bin_vals'])>0:
                heights.append(plots[name][dataset]['bin_vals'])
                bins.append(plots[name][dataset]['bin_edges'])
                tempcolors.append(colors[j%len(colors)])
                plt.plot([0,0],[0,0],color=colors[j%len(colors)],label=dataset)

        #print(heights)
        #print(bins)
        if len(heights)>0:
            mh.shh(heights,bins,color=tempcolors,ax=plt.gca())

            # Single plots
            for k in range(len(vars_to_plot)):
                if basename.find(vars_to_plot[k])>=0:
                    mh.shh(heights,bins,color=tempcolors,ax=single_axes[cut_string][k])

        for j,dataset in enumerate(dataplots[name].keys()):
            #x,y = combine_bins(dataplots[name][dataset]['bin_vals'],dataplots[name][dataset]['bin_edges'],n=8)
            x,y = dataplots[name][dataset]['bin_vals'],dataplots[name][dataset]['bin_edges']
            x = np.array(x); y = np.array(y)
            xbins = (y[0:-1] + y[1:])/2.
            plt.errorbar(xbins, x,yerr=np.sqrt(x),fmt='.',label=dataset,color="k")

            #plt.xlabel(xaxislabels[i],fontsize=14)
            plt.xlabel(dataplots[name][dataset]['xlabel'])#,fontsize=18)
            #plt.ylabel(dataplots[name][dataset]['ylabel'])#,fontsize=18)

            # Single plots
            for k in range(len(vars_to_plot)):
                if basename.find(vars_to_plot[k])>=0:
                    plt.sca(single_axes[cut_string][k])
                    plt.errorbar(xbins, x,yerr=np.sqrt(x),fmt='.',label=dataset,color="k")
                    plt.xlabel(dataplots[name][dataset]['xlabel'])#,fontsize=18)

        #plt.legend()
        plt.tight_layout()
        figname = "plots/fig_{0}.png".format(name)
        plt.savefig(figname)

    for i in range(len(cut_strings)):
        for j in range(len(vars_to_plot)):
            plt.sca(single_axes[i][j])
            plt.tight_layout()
            if j==2 or j==3:
                plt.xlim(0,200)
            elif j==4:
                plt.xlim(50,)
            #figname = "plots/SINGLE_ELECTRON_fig_{0}_{1}.png".format(vars_to_plot[j],i)
            figname = "plots/SINGLE_MUON_fig_{0}_{1}.png".format(vars_to_plot[j],i)
            plt.savefig(figname)
    #plt.show()

    return 1


################################################################################
if __name__=="__main__":
    infiles = sys.argv[1:]
    main(infiles)
