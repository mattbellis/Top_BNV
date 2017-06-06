import ROOT, sys
import matplotlib.pylab as plt
import lichen.lichen as lch
from math import sqrt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

nentries = tree.GetEntries()

x = []
y = []
z = []
njet = []
notx = []
noty = []
notz = []

xmuon = []
ymuon = []
zmuon = []

for i in range(nentries):
    tree.GetEntry(i)
   
    vertexX = tree.vertexX 
    vertexY = tree.vertexY 
    vertexZ = tree.vertexZ 

    if abs(vertexZ) <= 24.0 and sqrt(vertexX**2 + vertexY**2) <= 2.0:
        x.append(vertexX)
        y.append(vertexY)
        z.append(vertexZ)
    else:
        notx.append(vertexX)
        noty.append(vertexY)
        notz.append(vertexZ)
    #print(x, y, z)
   

x = np.array(x)
y = np.array(y)
z = np.array(z)

print(len(notx))

plt.figure()
ax = plt.axes(projection = '3d')
ax.scatter(x,y,z,c='r')
#ax.scatter(notx,noty,notz,c='b')
#plt.show()

plt.figure()
plt.plot(x,y, '.',alpha=0.1)

plt.figure()
lch.hist_err(x)

plt.figure()
lch.hist_err(y)

plt.figure()
lch.hist_err(z)

plt.show()

