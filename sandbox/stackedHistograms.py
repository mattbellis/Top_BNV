import topbnv_tools as tbt

import numpy as np
import matplotlib.pylab as plt

import ROOT
import sys

#import lichen.lichen as lch

import pickle

################################################################################
def main():

    lumi_file_name = 'lumi_info.pkl'
    lumi_info = pickle.load( open( lumi_file_name, "rb" ))

    filenames = sys.argv[1:]

    MCfiles = []
    DATAfiles = []
    for filename in filenames:
        filename2 = filename.split('/')[-1]
        if filename2.split('DATASET')[0] == 'MC_':
            #print('**********************************')
            MCfiles.append(filename)
        else:
            DATAfiles.append(filename)
    
    for filename in MCfiles:
        print('MC: ', filename)
    for filename in DATAfiles:
        print('DATA: ', filename)
                
    print("Will open files:")
    for f in filenames:
        print(f)

    data,tot_lumi = tbt.chain_pickle_files(DATAfiles,lumi_info)
    mcdata, tot_lumiMC = tbt.chain_pickle_files(MCfiles)
    print("tot_lumi: ",tot_lumi)

    topmassDATA = data['topmass']
    wmassDATA  = data['wmass']
    csvsDATA  = data['csvs']
    anglesDATA = data['angles']
    dRsDATA  = data['dRs']
    #njets = data['njets']
    njetsDATA  = data['njets']

    topmassMC = mcdata['topmass']
    wmassMC  = mcdata['wmass']
    csvsMC  = mcdata['csvs']
    anglesMC = mcdata['angles']
    dRsMC  = mcdata['dRs']
    #njets = mcdata['njets']
    njetsMC  = mcdata['njets']

    ################################################################################
    bins = 100 
    
    plt.figure()
    plt.subplot(3,3,1)
    plt.hist([topmassDATA,topmassMC], bins, stacked=True)
    #lch.hist_err(topmass,bins=100,range=(0,600),color='k')
    plt.xlabel('Top Mass (GeV)')

    plt.subplot(3,3,2)
    #lch.hist_err(wmass,bins=100,range=(0,300),color='k')
    plt.xlabel('W Mass (GeV)')

    plt.subplot(3,3,3)
    #lch.hist_err(csvs,bins=110,range=(0,1.1),color='k')
    plt.xlabel('Isolation Variable')

    plt.subplot(3,3,4)
    #lch.hist_err(angles,bins=100,range=(0, 3.2),color='k')
    plt.xlabel('Angles')

    plt.subplot(3,3,5)
    #plt.plot(wmass,angles,'.',markersize=0.5,alpha=0.2)
    #lch.hist_2D(wmass,angles,xbins=100,ybins=100,xrange=(0,300),yrange=(0,3.14))
    plt.xlim(50,150)
    plt.ylim(0, 3.2)
    plt.xlabel('W Mass')
    plt.ylabel('Angles')

    plt.subplot(3,3,6)
    #lch.hist_err(dRs,bins=100,range=(0, 3.2),color='k')
    plt.xlabel('dRs')

    plt.subplot(3,3,7)
    #lch.hist_2D(dRs,angles,xbins=100,ybins=100,xrange=(0,6.28),yrange=(0,3.14))
    plt.xlabel('dRs')
    plt.ylabel('Angles')


    ################################################################################
    # Cut on the wmass
    #index = wmass>70.0
    #index *= wmass<95.0

    plt.figure()
    plt.title('W Mass Cuts')
    plt.subplot(3,3,1)
    #lch.hist_err(topmass[index],bins=100,range=(0,600),color='k')
    plt.xlabel('Top Mass (GeV)')

    plt.subplot(3,3,2)
    #lch.hist_err(wmass[index],bins=100,range=(0,300),color='k')
    plt.xlabel('W Mass (GeV)')

    plt.subplot(3,3,4)
    #lch.hist_err(angles[index],bins=100,range=(0,3.2),color='k')
    plt.xlabel('Angles')

    plt.subplot(3,3,5)
    #plt.plot(wmass[index],angles[index],'.',markersize=0.5,alpha=0.2)
    #lch.hist_2D(wmass[index],angles[index],xbins=100,ybins=100,xrange=(0,300),yrange=(0,3.14))
    plt.xlim(50,150)
    plt.ylim(0, 3.2)
    plt.xlabel('W Mass')
    plt.ylabel('Angles')

    plt.subplot(3,3,6)
    #lch.hist_err(dRs[index],bins=100,range=(0, 3.2),color='k')
    plt.xlabel('dRs')

    plt.subplot(3,3,7)
    #lch.hist_2D(dRs[index],angles[index],xbins=100,ybins=100,xrange=(0,6.28),yrange=(0,3.14))
    plt.xlabel('dRs')
    plt.ylabel('Angles')


    '''
    # For talk
    plt.figure()
    #lch.hist_err(topmass[index],bins=100,range=(0,600),color='k')
    plt.hist(topmass[index],bins=100,range=(0,600),color='grey',alpha=0.2)
    plt.xlabel(r'Top candidate with W-mass cut (GeV/c$^2$)',fontsize=14)
    plt.tight_layout()
    plt.savefig('top.png')

    plt.figure()
    #lch.hist_err(wmass,bins=100,range=(0,300),color='k')
    plt.hist(wmass,bins=100,range=(0,300),color='grey',alpha=0.2)
    plt.xlabel(r'W candidate (GeV/c$^2$)',fontsize=14)
    plt.tight_layout()
    plt.savefig('W.png')

    plt.figure()
    #lch.hist_err(csvs,bins=110,range=(0,1.1),color='k')
    plt.hist(csvs,bins=100,range=(0,1.1),color='grey',alpha=0.2)
    plt.xlabel(r'CSVv2 variable',fontsize=14)
    plt.tight_layout()
    plt.savefig('csvv2.png')
    '''

    plt.show()

    return data


################################################################################
if __name__=="__main__":
    main()
