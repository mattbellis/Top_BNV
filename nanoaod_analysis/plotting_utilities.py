import numpy as np
import awkward as ak

import matplotlib.pylab as plt

plot_defs = {}

plot_defs['bnv_dR12_lab'] = {"xlabel":r"BNV dR$_{12}$ lab", "ylabel":r"# E","range":(0,6),'nbins':50}
plot_defs['bnv_dR13_lab'] = {"xlabel":r"BNV dR$_{13}$ lab", "ylabel":r"# E","range":(0,6),'nbins':50}
plot_defs['bnv_dR23_lab'] = {"xlabel":r"BNV dR$_{23}$ lab", "ylabel":r"# E","range":(0,6),'nbins':50}
plot_defs['bnv_dR1_23_lab'] = {"xlabel":r"BNV dR$_{1(23)}$ lab", "ylabel":r"# E","range":(0,6),'nbins':50}
plot_defs['bnv_dR3_12_lab'] = {"xlabel":r"BNV dR$_{3(12)}$ lab", "ylabel":r"# E","range":(0,6),'nbins':50}
plot_defs['bnv_dTheta12_CMtop'] = {"xlabel":r"BNV d$\theta$$_{12}$ CM$_{\rm top}$", "ylabel":r"# E","range":(-0.5,3.5),'nbins':50}
plot_defs['bnv_dTheta13_CMtop'] = {"xlabel":r"BNV d$\theta$$_{13}$ CM$_{\rm top}$", "ylabel":r"# E","range":(-0.5,3.5),'nbins':50}
plot_defs['bnv_dTheta23_CMtop'] = {"xlabel":r"BNV d$\theta$$_{23}$ CM$_{\rm top}$", "ylabel":r"# E","range":(-0.5,3.5),'nbins':50}
plot_defs['bnv_dTheta1_23_CMtop'] = {"xlabel":r"BNV d$\theta$$_{1(23)}$ CM$_{\rm top}$", "ylabel":r"# E","range":(-0.5,3.5),'nbins':50}
plot_defs['bnv_dTheta3_12_CMtop'] = {"xlabel":r"BNV d$\theta$$_{3(12)}$ CM$_{\rm top}$", "ylabel":r"# E","range":(-0.5,3.5),'nbins':50}
plot_defs['bnv_j1_pt_lab'] = {"xlabel":r"BNV $j_1$ p$_T$ lab (GeV/c)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['bnv_j2_pt_lab'] = {"xlabel":r"BNV $j_2$ p$_T$ lab (GeV/c)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['bnv_j3_pt_lab'] = {"xlabel":r"BNV $j_3$ p$_T$ lab (GeV/c)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['bnv_j1_pt_CMtop'] = {"xlabel":r"BNV $j_1$ p$_T$ CM$_{\rm top}$ (GeV/c)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['bnv_j2_pt_CMtop'] = {"xlabel":r"BNV $j_2$ p$_T$ CM$_{\rm top}$ (GeV/c)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['bnv_j3_pt_CMtop'] = {"xlabel":r"BNV $j_3$ p$_T$ CM$_{\rm top}$ (GeV/c)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['bnv_j1_mag_lab'] = {"xlabel":r"BNV $j_1$ $|p|$ lab (GeV/c)", "ylabel":r"# E","range":(0,400),'nbins':50}
plot_defs['bnv_j2_mag_lab'] = {"xlabel":r"BNV $j_2$ $|p|$ lab (GeV/c)", "ylabel":r"# E","range":(0,400),'nbins':50}
plot_defs['bnv_j3_mag_lab'] = {"xlabel":r"BNV $j_3$ $|p|$ lab (GeV/c)", "ylabel":r"# E","range":(0,400),'nbins':50}
plot_defs['bnv_j1_mag_CMtop'] = {"xlabel":r"BNV $j_1$ $|p|$ CM$_{\rm top}$ (GeV/c)", "ylabel":r"# E","range":(0,400),'nbins':50}
plot_defs['bnv_j2_mag_CMtop'] = {"xlabel":r"BNV $j_2$ $|p|$ CM$_{\rm top}$ (GeV/c)", "ylabel":r"# E","range":(0,400),'nbins':50}
plot_defs['bnv_j3_mag_CMtop'] = {"xlabel":r"BNV $j_3$ $|p|$ CM$_{\rm top}$ (GeV/c)", "ylabel":r"# E","range":(0,400),'nbins':50}
plot_defs['bnv_j12_m'] = {"xlabel":r"BNV m$_{12}$ (GeV/c$^2$)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['bnv_j13_m'] = {"xlabel":r"BNV m$_{13}$ (GeV/c$^2$)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['bnv_j1_btag'] = {"xlabel":r"BNV b-tag$_1$ (GeV/c$^2$)", "ylabel":r"# E","range":(-2,2),'nbins':400}
plot_defs['bnv_j23_m'] = {"xlabel":r"BNV m$_{23}$ (GeV/c$^2$)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['bnv_j2_btag'] = {"xlabel":r"BNV b-tag$_2$ (GeV/c$^2$)", "ylabel":r"# E","range":(-2,2),'nbins':400}
plot_defs['bnv_top_m'] = {"xlabel":r"BNV $t$-cand (GeV/c$^2$)", "ylabel":r"# E","range":(0,400),'nbins':100}
plot_defs['bnv_top_pt'] = {"xlabel":r"BNV $t$-cand p$_T$  (GeV/c)", "ylabel":r"# E","range":(0,800),'nbins':100}
plot_defs['bnv_top_mag'] = {"xlabel":r"BNV $t$-cand $|p|$ (GeV/c)", "ylabel":r"# E","range":(0,800),'nbins':100}
plot_defs['bnv_lep_pt'] = {"xlabel":r"BNV lepton p$_T$ (GeV/c)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['had_dR12_lab'] = {"xlabel":r"hadronic dR$_{12}$ lab", "ylabel":r"# E","range":(0,6),'nbins':50}
plot_defs['had_dR13_lab'] = {"xlabel":r"hadronic dR$_{13}$ lab", "ylabel":r"# E","range":(0,6),'nbins':50}
plot_defs['had_dR23_lab'] = {"xlabel":r"hadronic dR$_{23}$ lab", "ylabel":r"# E","range":(0,6),'nbins':50}
plot_defs['had_dR1_23_lab'] = {"xlabel":r"hadronic dR$_{1(23)}$ lab", "ylabel":r"# E","range":(0,6),'nbins':50}
plot_defs['had_dR3_12_lab'] = {"xlabel":r"hadronic dR$_{3(12)}$ lab", "ylabel":r"# E","range":(0,6),'nbins':50}
plot_defs['had_dTheta12_CMtop'] = {"xlabel":r"hadronic d$\theta_{12}$ CM$_{\rm top}$", "ylabel":r"# E","range":(-0.5,3.5),'nbins':50}
plot_defs['had_dTheta13_CMtop'] = {"xlabel":r"hadronic d$\theta_{13}$ CM$_{\rm top}$", "ylabel":r"# E","range":(-0.5,3.5),'nbins':50}
plot_defs['had_dTheta23_CMtop'] = {"xlabel":r"hadronic d$\theta_{23}$ CM$_{\rm top}$", "ylabel":r"# E","range":(-0.5,3.5),'nbins':50}
plot_defs['had_dTheta1_23_CMtop'] = {"xlabel":r"hadronic d$\theta_{1(23)}$ CM$_{\rm top}$", "ylabel":r"# E","range":(-0.5,3.5),'nbins':50}
plot_defs['had_dTheta3_12_CMtop'] = {"xlabel":r"hadronic d$\theta_{3(12)}$ CM$_{\rm top}$", "ylabel":r"# E","range":(-0.5,3.5),'nbins':50}
plot_defs['had_j1_pt_lab'] = {"xlabel":r"hadronic $j_1$ p$_T$ lab (GeV/c)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['had_j2_pt_lab'] = {"xlabel":r"hadronic $j_2$ p$_T$ lab (GeV/c)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['had_j3_pt_lab'] = {"xlabel":r"hadronic $j_3$ p$_T$ lab (GeV/c)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['had_j1_pt_CMtop'] = {"xlabel":r"hadronic $j_1$ p$_T$ CM$_{\rm top}$ (GeV/c)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['had_j2_pt_CMtop'] = {"xlabel":r"hadronic $j_2$ p$_T$ CM$_{\rm top}$ (GeV/c)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['had_j3_pt_CMtop'] = {"xlabel":r"hadronic $j_3$ p$_T$ CM$_{\rm top}$ (GeV/c)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['had_j1_mag_lab'] = {"xlabel":r"hadronic $j_1$ $|p|$ lab (GeV/c)", "ylabel":r"# E","range":(0,400),'nbins':50}
plot_defs['had_j2_mag_lab'] = {"xlabel":r"hadronic $j_2$ $|p|$ lab (GeV/c)", "ylabel":r"# E","range":(0,400),'nbins':50}
plot_defs['had_j3_mag_lab'] = {"xlabel":r"hadronic $j_3$ $|p|$ lab (GeV/c)", "ylabel":r"# E","range":(0,400),'nbins':50}
plot_defs['had_j1_mag_CMtop'] = {"xlabel":r"hadronic $j_1$ $|p|$ CM$_{\rm top}$ (GeV/c)", "ylabel":r"# E","range":(0,400),'nbins':50}
plot_defs['had_j2_mag_CMtop'] = {"xlabel":r"hadronic $j_2$ $|p|$ CM$_{\rm top}$ (GeV/c)", "ylabel":r"# E","range":(0,400),'nbins':50}
plot_defs['had_j3_mag_CMtop'] = {"xlabel":r"hadronic $j_3$ $|p|$ CM$_{\rm top}$ (GeV/c)", "ylabel":r"# E","range":(0,400),'nbins':50}
plot_defs['had_j12_m'] = {"xlabel":r"hadronic m$_{12}$ (GeV/c$^2$)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['had_j13_m'] = {"xlabel":r"hadronic m$_{13}$ (GeV/c$^2$)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['had_j1_btag'] = {"xlabel":r"hadronic b-tag$_1$ (GeV/c$^2$)", "ylabel":r"# E","range":(-2,2),'nbins':400}
plot_defs['had_j23_m'] = {"xlabel":r"hadronic m$_{23}$ (GeV/c$^2$)", "ylabel":r"# E","range":(0,200),'nbins':50}
plot_defs['had_j2_btag'] = {"xlabel":r"hadronic b-tag$_2$ (GeV/c$^2$)", "ylabel":r"# E","range":(-2,2),'nbins':400}
plot_defs['had_j3_btag'] = {"xlabel":r"hadronic b-tag$_3$ (GeV/c$^2$)", "ylabel":r"# E","range":(-2,2),'nbins':400}
plot_defs['had_top_m'] = {"xlabel":r"hadronic $t$-cand (GeV/c$^2$)", "ylabel":r"# E","range":(0,400),'nbins':100}
plot_defs['had_top_pt'] = {"xlabel":r"hadronic $t$-cand p$_T$ (GeV/c)", "ylabel":r"# E","range":(0,800),'nbins':100}
plot_defs['had_top_mag'] = {"xlabel":r"hadronic $t$-cand $|p|$ (GeV/c)", "ylabel":r"# E","range":(0,800),'nbins':100}
plot_defs['num'] = {"xlabel":r"# of candidates", "ylabel":r"# E","range":(0,60),'nbins':60}
plot_defs['num_combos'] = {"xlabel":r"# of combos", "ylabel":r"# E","range":(0,60),'nbins':60}
plot_defs['ttbar_cosangle'] = {"xlabel":r"$\cos\theta_T$ $t\bar{t}$ candidates", "ylabel":r"# E","range":(-1.2,1.2),'nbins':70}

################################################################################

################################################################################
def plot_some_variables(values, keys, axes=None, nrows=1, ncols=1, figsize=None, label=None, mask=None, do_unique=False, ml_prepend=True):

    if axes is None:
        if figsize is None:
            figsize = (6,6)
        fig,axes = plt.subplots(1,1,figsize=figsize)
        
    for i,key in enumerate(keys):

        if key=='SKIP':
            continue

        plot_def_key = str(key)
        if key[0:3] != 'ml/':
            key = f"ml/{key}"

        #print(key,plot_def_key)

        x = values[key]

        if type(x) == ak.highlevel.Array:
            x = values[key].to_numpy()
        x[x==-np.inf] = -999
        x[x==np.inf] = -999

        nbins = plot_defs[plot_def_key]['nbins']
        xlabel = plot_defs[plot_def_key]['xlabel']
        ylabel = f"#/bin" #plot_defs[plot_def_key]['ylabel']
        prange = plot_defs[plot_def_key]['range']

        row,col = 1,1
        ax = None
        if nrows==1 or ncols==1:
            ax = axes[i]
        else:
            row = int(np.floor(i/ncols))
            col = i%ncols
            ax = axes[row][col]
        
        #print(i,ncols,nrows,i%ncols,row,col)

        #print(i,row,col)

        xvar = None
        if mask is not None:
            xvar = x[mask]
        else:
            xvar = x

        #print(f"{key}   {len(xvar)}")#  {len(x)}")
        if do_unique:
            xvar = np.unique(xvar)
        #print(f"{key}   {len(xvar)}")#  {len(x)}")

        ax.hist(xvar[xvar==xvar],bins=nbins,range=prange, density=True, alpha=0.5, label=label)
        ax.set_xlabel(xlabel,fontsize=18)
        ax.set_ylabel(ylabel,fontsize=18)

        #if key.find('top_m')>=0:
        #    ax.plot([173, 173], [0, ax.get_ylim()[1]],'k--', label="Top quark mass")

        #if label is not None:
        #    ax.legend()
        
    plt.tight_layout();

    
    return 0
