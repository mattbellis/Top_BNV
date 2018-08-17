import topbnv_tools as tbt

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


    names = ['leadmupt']

    plots = {}
    for name in names:
        plots[name] = {'bin_vals':[], 'bin_edges':[]}


    for i,infile in enumerate(infiles):

        f = open(infile)

        while(1):

            vals = f.readline().split()
            if len(vals)==0:
                break

            print(vals)

            name = vals[0]

            if name in names:

                bin_vals = vals[1:]
                vals = f.readline().split()
                bin_edges = vals[1:]

                bin_vals = np.array(bin_vals).astype(float)
                bin_edges = np.array(bin_edges).astype(float)

                if len(plots[name]['bin_vals'])==0:
                    plots[name]['bin_vals'] = bin_vals
                    plots[name]['bin_edges'] = bin_edges
                else:
                    plots[name]['bin_vals'] += bin_vals
                    plots[name]['bin_edges'] += bin_edges

    print(plots)

    plt.figure(figsize=(12,8))

    plt.subplot(2,3,1)
    print("HERE")
    print(plots['leadmupt']['bin_vals'],plots['leadmupt']['bin_edges'])
    x,y = combine_bins(plots['leadmupt']['bin_vals'],plots['leadmupt']['bin_edges'],n=4)
    x = np.array(x); y = np.array(y)
    print(x)
    print(y)
    #plt.hist(x,y)
    plt.errorbar((y[0:-1] + y[1:])/2, x,yerr=np.sqrt(x),fmt='.')
    #plt.hist(plots['leadmupt']['bin_vals'],plots['leadmupt']['bin_edges'])

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
