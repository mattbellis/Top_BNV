import sys

import pandas as pd

import numpy as np
import matplotlib.pylab as plt

#import h5hep as hp
import hepfile

# For CMS-style plotting
#import mplhep
#plt.style.use(mplhep.style.CMS)

plot_defs = {}
plot_defs['ml/bnv_dR12_lab'] = {"xlabel":r"BNV dR$_{12}$ lab", "ylabel":r"# E","range":(0,4),'nbins':50}
plot_defs['ml/bnv_dR13_lab'] = {"xlabel":r"BNV dR$_{13}$ lab", "ylabel":r"# E","range":(0,4),'nbins':50}
plot_defs['ml/bnv_dR1_23_lab'] = {"xlabel":r"BNV dR$_{1(23)}$ lab", "ylabel":r"# E","range":(0,4),'nbins':50}
plot_defs['ml/bnv_dR23_lab'] = {"xlabel":r"BNV dR$_{23}$ lab", "ylabel":r"# E","range":(0,4),'nbins':50}
plot_defs['ml/bnv_dTheta12_rest'] = {"xlabel":r"BNV d$\theta$$_{12}$ rest", "ylabel":r"# E","range":(-0.5,3.5),'nbins':50}
plot_defs['ml/bnv_dTheta13_rest'] = {"xlabel":r"BNV d$\theta$$_{13}$ rest", "ylabel":r"# E","range":(-0.5,3.5),'nbins':50}
plot_defs['ml/bnv_dTheta1_23_rest'] = {"xlabel":r"BNV d$\theta$$_{1(23)}$ rest", "ylabel":r"# E","range":(-0.5,3.5),'nbins':50}
plot_defs['ml/bnv_dTheta23_rest'] = {"xlabel":r"BNV d$\theta$$_{23}$ rest", "ylabel":r"# E","range":(-0.5,3.5),'nbins':50}
plot_defs['ml/bnv_j12_m'] = {"xlabel":r"BNV m$_{12}$ (GeV/c$^2$)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['ml/bnv_j13_m'] = {"xlabel":r"BNV m$_{13}$ (GeV/c$^2$)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['ml/bnv_j1_btag'] = {"xlabel":r"BNV b-tag$_1$ (GeV/c$^2$)", "ylabel":r"# E","range":(-2,2),'nbins':50}
plot_defs['ml/bnv_j23_m'] = {"xlabel":r"BNV m$_{23}$ (GeV/c$^2$)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['ml/bnv_j2_btag'] = {"xlabel":r"BNV b-tag$_2$ (GeV/c$^2$)", "ylabel":r"# E","range":(-2,2),'nbins':50}
plot_defs['ml/bnv_m'] = {"xlabel":r"BNV $t$-cand (GeV/c$^2$)", "ylabel":r"# E","range":(0,400),'nbins':50}
plot_defs['ml/bnv_lep_pt'] = {"xlabel":r"BNV lepton p$_T$ (GeV/c)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['ml/had_dR12_lab'] = {"xlabel":r"hadronic dR$_{12}$ lab", "ylabel":r"# E","range":(0,4),'nbins':50}
plot_defs['ml/had_dR13_lab'] = {"xlabel":r"hadronic dR$_{13}$ lab", "ylabel":r"# E","range":(0,4),'nbins':50}
plot_defs['ml/had_dR1_23_lab'] = {"xlabel":r"hadronic dR$_{1(23)}$ lab", "ylabel":r"# E","range":(0,4),'nbins':50}
plot_defs['ml/had_dR23_lab'] = {"xlabel":r"hadronic dR$_{23}$ lab", "ylabel":r"# E","range":(0,4),'nbins':50}
plot_defs['ml/had_dTheta12_rest'] = {"xlabel":r"hadronic d$\theta_{12}$ rest", "ylabel":r"# E","range":(-0.5,3.5),'nbins':50}
plot_defs['ml/had_dTheta13_rest'] = {"xlabel":r"hadronic d$\theta_{13}$ rest", "ylabel":r"# E","range":(-0.5,3.5),'nbins':50}
plot_defs['ml/had_dTheta1_23_rest'] = {"xlabel":r"hadronic d$\theta_{1(23)}$ rest", "ylabel":r"# E","range":(-0.5,3.5),'nbins':50}
plot_defs['ml/had_dTheta23_rest'] = {"xlabel":r"hadronic d$\theta_{23}$ rest", "ylabel":r"# E","range":(-0.5,3.5),'nbins':50}
plot_defs['ml/had_j12_m'] = {"xlabel":r"hadronic m$_{12}$ (GeV/c$^2$)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['ml/had_j13_m'] = {"xlabel":r"hadronic m$_{13}$ (GeV/c$^2$)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['ml/had_j1_btag'] = {"xlabel":r"hadronic b-tag$_1$ (GeV/c$^2$)", "ylabel":r"# E","range":(-2,2),'nbins':50}
plot_defs['ml/had_j23_m'] = {"xlabel":r"hadronic m$_{23}$ (GeV/c$^2$)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['ml/had_j2_btag'] = {"xlabel":r"hadronic b-tag$_2$ (GeV/c$^2$)", "ylabel":r"# E","range":(-2,2),'nbins':50}
plot_defs['ml/had_j3_btag'] = {"xlabel":r"hadronic b-tag$_3$ (GeV/c$^2$)", "ylabel":r"# E","range":(-2,2),'nbins':50}
plot_defs['ml/had_m'] = {"xlabel":r"hadronic $t$-cand (GeV/c$^2$)", "ylabel":r"# E","range":(0,400),'nbins':50}
plot_defs['ml/num'] = {"xlabel":r"# of candidates", "ylabel":r"# E","range":(0,60),'nbins':60}
plot_defs['ml/num_combos'] = {"xlabel":r"# of combos", "ylabel":r"# E","range":(0,60),'nbins':60}
plot_defs['ml/ttbar_angle'] = {"xlabel":r"$\cos\theta$ $t\bar{t}$ candidates", "ylabel":r"# E","range":(-1.2,1.2),'nbins':70}


alldata = {}
alldata2 = {}

##############################################################################
# Get the data 
##############################################################################
#df = pd.read_hdf(sys.argv[1])
names = []
for i,infilename in enumerate(sys.argv[1:]):
    #infilename = sys.argv[1]
    data, event = hepfile.load(infilename, verbose=False)  # ,subset=10000)

    for key in event.keys():
        print(key)
        if key[0:2]=='ml':
            if i==0:
                names.append(key)
                alldata[key] = data[key].tolist()
            else:
                #alldata[key] += data[key].tolist()
                # Do this if there are two data types
                alldata2[key] = data[key].tolist()
#exit()

#exit()

fig1plots = ['ml/bnv_dR12_lab',
'ml/bnv_dR13_lab',
'ml/bnv_dR23_lab',
'ml/bnv_dR1_23_lab',
'ml/bnv_dTheta12_rest',
'ml/bnv_dTheta13_rest',
'ml/bnv_dTheta23_rest',
'ml/bnv_dTheta1_23_rest',
'ml/bnv_j12_m',
'ml/bnv_j13_m',
'ml/bnv_j23_m',
'ml/bnv_m',
'SKIP',
'ml/bnv_j1_btag',
'ml/bnv_j2_btag',
'ml/bnv_lep_pt',
]

fig2plots = ['ml/had_dR12_lab',
'ml/had_dR13_lab',
'ml/had_dR23_lab',
'ml/had_dR1_23_lab',
'ml/had_dTheta12_rest',
'ml/had_dTheta13_rest',
'ml/had_dTheta23_rest',
'ml/had_dTheta1_23_rest',
'ml/had_j12_m',
'ml/had_j13_m',
'ml/had_j23_m',
'ml/had_m',
'SKIP',
'ml/had_j1_btag',
'ml/had_j2_btag',
'ml/had_j3_btag',
]

fig3plots = ['ml/num','ml/num_combos', 'ml/ttbar_angle'] 

print(f"# of plots: {len(names)}")

for pidx,plots in enumerate([fig1plots, fig2plots, fig3plots]):
    if pidx < 2:
        plt.figure(figsize=(12,8))
    else:
        plt.figure(figsize=(9,3))

    for i,name in enumerate(plots):
        if name=='SKIP':
            continue

        print(i,name)
        tag = 'BNV'
        if name.find('had')>=0:
            tag = 'hadronic'

        if pidx<2:
            plt.subplot(4,4,i%16+1)
        else:
            plt.subplot(1,3,i%16+1)

        nbins = plot_defs[name]['nbins']
        xlabel = plot_defs[name]['xlabel']
        ylabel = plot_defs[name]['ylabel']
        plotrange = plot_defs[name]['range']

        plt.hist(alldata[name],bins=nbins,range=plotrange,density=True,alpha=0.9,label=r'$t\bar{t}$ '+tag)
        if len(sys.argv)>2:
            plt.hist(alldata2[name],bins=nbins,range=plotrange,density=True,alpha=0.9,label=r'$t\bar{t}$ '+tag)


        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        if name=='ml/bnv_m' or name=='ml/had_m':
            plt.plot([173, 173], plt.gca().get_ylim(),'k--',label='top mass')
        elif name=='ml/had_j12_m':
            plt.plot([83, 83], plt.gca().get_ylim(),'k--',label=r'$W$ mass')
        
        plt.legend()

    plt.tight_layout()

plt.show()
