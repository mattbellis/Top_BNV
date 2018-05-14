import topbnv_tools as tbt

import numpy as np
import matplotlib.pylab as plt

import ROOT
import sys

import lichen.lichen as lch

import pickle

################################################################################
def main():

    #lumi_file_name = 'lumi_info.pkl'
    #lumi_info = pickle.load( open( lumi_file_name, "rb" ) )

    filenames = sys.argv[1:]


    #data,tot_lumi = tbt.chain_pickle_files(filenames,lumi_info)
    #print("tot_lumi: ",tot_lumi)

    T = ROOT.TChain("T")
    print("Will open files:")
    for f in filenames:
        print(f)
        T.Add(f)

    ntops = []
    topmass = []
    wmass = []
    csvs = []
    angles = []
    dRs = []
    wH = []
    njets = []
    leadmupt = []
    leadmueta = []
    subleadmupt = []
    subleadmueta = []
    metpt = []
    triggers = [[], [], [], []]

    nentries = T.GetEntries()
    for i in range(nentries):
        T.GetEntry(i)

        njets.append(T.njet)
        ntop = T.ntop
        ntops.append(ntop)
        for n in range(ntop):
            topmass.append(T.topmass[n])
            wmass.append(T.wmass[n])
            dRs.append(T.wdR[n])
            wH.append(T.wH[n])
            angles.append(T.wangle[n])

        for n in range(T.njet):
            csvs.append(T.jetcsv[n])

        leadmupt.append(T.leadmupt)
        leadmueta.append(T.leadmueta)
        subleadmupt.append(T.subleadmupt)
        subleadmueta.append(T.subleadmueta)
        metpt.append(T.METpt)

        triggers[0].append(T.trig_HLT_IsoMu24_accept)
        triggers[1].append(T.trig_HLT_IsoTkMu24_accept)
        triggers[2].append(T.trig_HLT_IsoMu22_eta2p1_accept)
        triggers[3].append(T.trig_HLT_IsoTkMu22_eta2p1_accept)


    ntops = np.array(ntops)
    topmass = np.array(topmass)
    wmass = np.array(wmass)
    csvs = np.array(csvs)
    angles = np.array(angles)
    dRs = np.array(dRs)
    wH = np.array(wH)
    njets = np.array(njets)
    leadmupt = np.array(leadmupt)
    leadmueta = np.array(leadmueta)
    subleadmupt = np.array(subleadmupt)
    subleadmueta = np.array(subleadmueta)
    metpt = np.array(metpt)
    triggers[0] = np.array(triggers[0])
    triggers[1] = np.array(triggers[1])
    triggers[2] = np.array(triggers[2])
    triggers[3] = np.array(triggers[3])


    '''
    for a in zip(topmass, wmass, csvs, angles, dRs, njets):
        print(a)
        a = np.array(a)
    '''






    ################################################################################
    plt.figure()
    plt.subplot(3,3,1)
    lch.hist_err(topmass,bins=100,range=(0,600),color='k')
    plt.xlabel('Top Mass (GeV)')

    plt.subplot(3,3,2)
    lch.hist_err(wmass,bins=100,range=(0,300),color='k')
    plt.xlabel('W Mass (GeV)')

    plt.subplot(3,3,3)
    lch.hist_err(csvs,bins=110,range=(0,1.1),color='k')
    plt.xlabel('CSV variable')

    plt.subplot(3,3,4)
    lch.hist_err(angles,bins=100,range=(0, 3.2),color='k')
    plt.xlabel('Angles')

    plt.subplot(3,3,5)
    #plt.plot(wmass,angles,'.',markersize=0.5,alpha=0.2)
    lch.hist_2D(wmass,angles,xbins=100,ybins=100,xrange=(0,300),yrange=(0,3.14))
    plt.xlim(50,150)
    plt.ylim(0, 3.2)
    plt.xlabel('W Mass')
    plt.ylabel('Angles')

    plt.subplot(3,3,6)
    lch.hist_err(dRs,bins=100,range=(0, 3.2),color='k')
    plt.xlabel('dRs')

    plt.subplot(3,3,7)
    lch.hist_2D(dRs,angles,xbins=100,ybins=100,xrange=(0,6.28),yrange=(0,3.14))
    plt.xlabel('dRs')
    plt.ylabel('Angles')

    plt.subplot(3,3,8)
    lch.hist_err(wH,bins=100,range=(0,250),color='k')
    plt.xlabel('scalar H')

    plt.subplot(3,3,9)
    lch.hist_err(ntops,bins=6,range=(0,6),color='k')
    plt.xlabel('ntops')

    plt.tight_layout()


    ################################################################################
    # Cut on the wmass
    index = wmass>70.0
    index *= wmass<95.0
    #index = (np.abs(angles - dRs)<=0.45)

    plt.figure()
    plt.title('W Mass Cuts')
    plt.subplot(3,3,1)
    lch.hist_err(topmass[index],bins=100,range=(0,600),color='k')
    plt.xlabel('Top Mass (GeV)')

    plt.subplot(3,3,2)
    lch.hist_err(wmass[index],bins=100,range=(0,300),color='k')
    plt.xlabel('W Mass (GeV)')

    plt.subplot(3,3,4)
    lch.hist_err(angles[index],bins=100,range=(0,3.2),color='k')
    plt.xlabel('Angles')

    plt.subplot(3,3,5)
    #plt.plot(wmass[index],angles[index],'.',markersize=0.5,alpha=0.2)
    lch.hist_2D(wmass[index],angles[index],xbins=100,ybins=100,xrange=(0,300),yrange=(0,3.14))
    plt.xlim(50,150)
    plt.ylim(0, 3.2)
    plt.xlabel('W Mass')
    plt.ylabel('Angles')

    plt.subplot(3,3,6)
    lch.hist_err(dRs[index],bins=100,range=(0, 3.2),color='k')
    plt.xlabel('dRs')

    plt.subplot(3,3,7)
    lch.hist_2D(dRs[index],angles[index],xbins=100,ybins=100,xrange=(0,6.28),yrange=(0,3.14))
    plt.xlabel('dRs')
    plt.ylabel('Angles')

    plt.subplot(3,3,8)
    lch.hist_err(wH[index],bins=100,range=(0,250),color='k')
    plt.xlabel('scalar H')

    plt.tight_layout()

    ############################################################################
    # Muons
    ############################################################################
    plt.figure()
    plt.subplot(3,3,1)
    lch.hist_err(leadmupt,bins=100,range=(0,250),color='k')
    plt.xlabel(r'Leading muon p$_{T}$ (GeV/c)')

    plt.subplot(3,3,2)
    lch.hist_err(leadmueta,bins=100,range=(-3.0,3.0),color='k')
    plt.xlabel(r'Leading muon $\eta$ (GeV/c)')

    plt.subplot(3,3,4)
    lch.hist_err(subleadmupt,bins=100,range=(0,250),color='k')
    plt.xlabel(r'Sub-leading muon p$_{T}$ (GeV/c)')

    plt.subplot(3,3,5)
    lch.hist_err(subleadmueta,bins=100,range=(-3.0,3.0),color='k')
    plt.xlabel(r'Sub-leading muon $\eta$ (GeV/c)')

    plt.subplot(3,3,7)
    lch.hist_err(metpt,bins=100,range=(0.0,100.0),color='k')
    plt.xlabel(r'Missing E$_T$ (GeV)')

    plt.tight_layout()
    '''
    # For talk
    plt.figure()
    lch.hist_err(topmass[index],bins=100,range=(0,600),color='k')
    plt.hist(topmass[index],bins=100,range=(0,600),color='grey',alpha=0.2)
    plt.xlabel(r'Top candidate with W-mass cut (GeV/c$^2$)',fontsize=14)
    plt.tight_layout()
    plt.savefig('top.png')

    plt.figure()
    lch.hist_err(wmass,bins=100,range=(0,300),color='k')
    plt.hist(wmass,bins=100,range=(0,300),color='grey',alpha=0.2)
    plt.xlabel(r'W candidate (GeV/c$^2$)',fontsize=14)
    plt.tight_layout()
    plt.savefig('W.png')

    plt.figure()
    lch.hist_err(csvs,bins=110,range=(0,1.1),color='k')
    plt.hist(csvs,bins=100,range=(0,1.1),color='grey',alpha=0.2)
    plt.xlabel(r'CSVv2 variable',fontsize=14)
    plt.tight_layout()
    plt.savefig('csvv2.png')
    '''

    ############################################################################
    # Triggers
    ############################################################################
    plt.figure()
    plt.subplot(5,4,1)
    lch.hist_err(triggers[0],bins=2,range=(0,2),color='k')
    plt.xlabel(r'Trigger 0')

    plt.subplot(5,4,2)
    lch.hist_err(triggers[1],bins=2,range=(0,2),color='k')
    plt.xlabel(r'Trigger 1')

    plt.subplot(5,4,3)
    lch.hist_err(triggers[2],bins=2,range=(0,2),color='k')
    plt.xlabel(r'Trigger 2')

    plt.subplot(5,4,4)
    lch.hist_err(triggers[3],bins=2,range=(0,2),color='k')
    plt.xlabel(r'Trigger 3')

    for i in range(0,4):
        for j in range(0,4):
            plt.subplot(5,4,5+i*4 + j)
            lch.hist_err(triggers[i][triggers[j]==1],bins=2,range=(0,2))

    plt.tight_layout()


    plt.show()

    #return data


################################################################################
if __name__=="__main__":
    main()
