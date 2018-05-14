import topbnv_tools as tbt

import numpy as np
import matplotlib.pylab as plt

import ROOT
import sys

import lichen.lichen as lch

import pickle

################################################################################
def weights_for_histos(weights,vals):
    hweights = []
    for w,d in zip(weights,vals):
        print('weighting: ',w,len(d))
        hweights.append(w*np.ones(len(d)))
    return hweights

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
    '''
    for filename in MCfiles:
        print('MC: ', filename)
    for filename in DATAfiles:
        print('DATA: ', filename)
    '''            
    mcdata = []
    #print("Will open files:")
    mcInfo = tbt.csvtodict("MCinfo.csv")
    weights = []
    mcEvents = []
    crosssection = []

    data,tot_lumi = tbt.chain_pickle_files(DATAfiles,lumi_info)
    print("tot_lumi: ",tot_lumi)
   

    for f in MCfiles:
        #print('f', f)
        mcdataTMP, tot_lumiMC = tbt.chain_pickle_files(f)
        mcdata.append(mcdataTMP) 
        fnew = f.split('DATASET_crab_')[1].split('_NFILES')[0]
        nfiles = int(f.split('NFILES_')[1].split('_')[1].split('.')[0]) - int(f.split('NFILES_')[1].split('_')[0])
        crosssection = 1000*(float(mcInfo[fnew]['cross_section'])) # Convert from pb to fb
        mcEvents = (float(mcInfo[fnew]['total_events']))
        print("crosssection: ",crosssection)
        print("MCEvents/crosssection: ",mcEvents/crosssection)
        print("MCEvents: ",mcEvents)
        print("tot_lumi: ",tot_lumi)
        print("nfiles: ",nfiles)
        print("nfiles_tot: ",mcInfo[fnew]['nfiles'])
        weights.append((crosssection * tot_lumi) / (nfiles*mcEvents/float(mcInfo[fnew]['nfiles'])))

    topmassDATA = data['topmass']
    wmassDATA  = data['wmass']
    csvsDATA  = data['csvs']
    anglesDATA = data['angles']
    dRsDATA  = data['dRs']
    #njets = data['njets']
    njetsDATA  = data['njets']
    leadmuptDATA  = data['leadmupt']
    leadmuetaDATA  = data['leadmueta']

    topmassMC = [] 
    wmassMC  = []
    csvsMC  = []
    anglesMC = []
    dRsMC  = []
    #njets = []
    njetsMC  = []
    leadmuptMC  = []
    leadmuetaMC  = []
    

    for mc in mcdata:
        topmassMC.append(mc['topmass'])
        wmassMC.append(mc['wmass'])
        csvsMC.append(mc['csvs'])
        anglesMC.append(mc['angles'])
        dRsMC.append(mc['dRs'])
        #njets.append(mc['njets'])
        njetsMC.append(mc['njets'])
        leadmuptMC.append(mc['leadmupt'])
        leadmuetaMC.append(mc['leadmueta'])

    print('Weights', weights)
    
    bins = 100 

    hweights = []
    for w,d in zip(weights,[topmassMC[0],topmassMC[1]]):
        print('weighting: ',w,len(d))
        hweights.append(w*np.ones(len(d)))

    plt.figure()
    vals = [topmassMC[0],topmassMC[1]]
    hw = weights_for_histos(weights,vals)
    plt.hist(vals, bins, range=(0,1600), weights=hw,stacked=True)
    lch.hist_err(topmassDATA, bins, range=(0,1600))

    plt.figure()
    vals = [leadmuptMC[0],leadmuptMC[1]]
    hw = weights_for_histos(weights,vals)
    plt.hist(vals, bins, range=(0,200), weights=hw,stacked=True)
    lch.hist_err(leadmuptDATA, bins, range=(0,200))

    plt.figure()
    vals = [leadmuetaMC[0],leadmuetaMC[1]]
    hw = weights_for_histos(weights,vals)
    plt.hist(vals, bins, range=(-3,3), weights=hw,stacked=True)
    lch.hist_err(leadmuetaDATA, bins, range=(-3,3))

    print(mcdata[0].keys())
    plt.figure()
    plt.subplot(2,2,1)
    plt.hist(mcdata[0]["trig_HLT_IsoMu24_accept"])
    plt.subplot(2,2,2)
    plt.hist(mcdata[0]["trig_HLT_IsoTkMu24_accept"])
    plt.subplot(2,2,3)
    plt.hist(mcdata[0]["trig_HLT_IsoMu22_eta2p1_accept"])
    plt.subplot(2,2,4)
    plt.hist(mcdata[0]["trig_HLT_IsoTkMu22_eta2p1_accept"])

    '''
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
    '''
    
    ################################################################################
    # Cut on the wmass
    #index = wmass>70.0
    #index *= wmass<95.0
    '''
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
