import sys
import numpy as np
import matplotlib.pylab as plt

import hepfile

################################################################################
def get_4vecs(data,idx):

    e = data['jet/e'][idx]
    px = data['jet/px'][idx]
    py = data['jet/py'][idx]
    pz = data['jet/pz'][idx]

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

wpm = invmass([q11,q12])
wmm = invmass([q21,q22])

tm = invmass([b1,q11,q12])
tbarm = invmass([b2,q21,q22])

plt.figure()

plt.subplot(2,2,1)
plt.hist(wpm,bins=50,range=(0,300))

plt.subplot(2,2,2)
plt.hist(wmm,bins=50,range=(0,300))

plt.subplot(2,2,3)
plt.hist(tm,bins=50,range=(0,500))

plt.subplot(2,2,4)
plt.hist(tbarm,bins=50,range=(0,500))

plt.savefig('image_from_h5.png')

plt.show()
