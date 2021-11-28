import sys
import numpy as np
import matplotlib.pylab as plt

import hepfile

################################################################################
def get_4vecs(data,idx,group='jet'):

    e = data[f'{group}/e'][idx]
    px = data[f'{group}/px'][idx]
    py = data[f'{group}/py'][idx]
    pz = data[f'{group}/pz'][idx]

    return (e,px,py,pz)
################################################################################

################################################################################
def invmass(p4s):

    np4s = len(p4s)

    e = p4s[0][0].copy()
    px = p4s[0][1].copy()
    py = p4s[0][2].copy()
    pz = p4s[0][3].copy()

    for i in range(1,np4s):
        e += p4s[i][0]
        px += p4s[i][1]
        py += p4s[i][2]
        pz += p4s[i][3]

    m2 = e*e - (px*px + py*py + pz*pz)

    m = m2

    m[m2<0] = -np.sqrt(-m2[m2<0])
    m[m2>0] = np.sqrt(m2[m2>0])

    return m2
################################################################################


infilename = sys.argv[1]

data,event = hepfile.load(infilename)

nevents = hepfile.get_nbuckets_in_data(data)

topology = "had_had"
topology = "had_TSUE"

if topology == "had_had":
    b1idx = np.arange(0,nevents*6,6)
    q11idx = np.arange(1,nevents*6,6)
    q12idx = np.arange(2,nevents*6,6)
    b2idx = np.arange(3,nevents*6,6)
    q21idx = np.arange(4,nevents*6,6)
    q22idx = np.arange(5,nevents*6,6)

    b1 = get_4vecs(data,b1idx)
    q11 = get_4vecs(data,q11idx)
    q12 = get_4vecs(data,q12idx)
    b2 = get_4vecs(data,b2idx)
    q21 = get_4vecs(data,q21idx)
    q22 = get_4vecs(data,q22idx)

elif topology == "had_TSUE":
    b1idx = np.arange(0,nevents*5,5)
    q11idx = np.arange(1,nevents*5,5)
    q12idx = np.arange(2,nevents*5,5)
    q21idx = np.arange(3,nevents*5,5)
    q22idx = np.arange(4,nevents*5,5)
    lep2idx = np.arange(0,nevents,1)

    b1 = get_4vecs(data,b1idx)
    q11 = get_4vecs(data,q11idx)
    q12 = get_4vecs(data,q12idx)
    q21 = get_4vecs(data,q21idx)
    q22 = get_4vecs(data,q22idx)
    lep2 = get_4vecs(data,lep2idx,'lepton')


    wpm = invmass([q11,q12])
    wmm = invmass([q21,q22])

    tm = invmass([b1,q11,q12])
    tbarm = invmass([lep2,q21,q22])

    plt.figure(figsize=(8,6))

    plt.subplot(2,2,1)
    plt.hist(wpm,bins=50,range=(0,300))
    plt.xlabel(r'$M_{q\bar{q}}, t \rightarrow W \rightarrow q\bar{q}$ (GeV/c$^2$)',fontsize=12)

    plt.subplot(2,2,2)
    plt.hist(wmm,bins=50,range=(0,300))
    plt.xlabel(r'$M_{\bar{q}\bar{q}}, t \rightarrow \ell \bar{q}\bar{q}$ (GeV/c$^2$)',fontsize=12)

    plt.subplot(2,2,3)
    plt.hist(tm,bins=50,range=(0,500))
    plt.xlabel(r'$M_{q_b q\bar{q}}, t \rightarrow q_b W \rightarrow q\bar{q}$ (GeV/c$^2$)',fontsize=12)

    plt.subplot(2,2,4)
    plt.hist(tbarm,bins=50,range=(0,500))
    plt.xlabel(r'$M_{\ell \bar{q}\bar{q}}, t \rightarrow \ell \bar{q}\bar{q}$ (GeV/c$^2$)',fontsize=12)

    plt.tight_layout()

    plt.savefig('image_from_h5.png')

    plt.show()
