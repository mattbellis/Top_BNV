import numpy as np
import matplotlib.pylab as plt
import awkward as ak
import uproot as uproot

import sys

from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import nanoaod_analysis_tools as nat

import time

# https://coffeateam.github.io/coffea/api/coffea.nanoevents.methods.nanoaod.GenParticle.html

infilename = sys.argv[1]


print("Reading in {0}".format(infilename))

events = NanoEventsFactory.from_root(infilename, schemaclass=NanoAODSchema).events()
print(len(events))


jets = events.Jet
muons = events.Muon
electrons = events.Electron

plt.figure(figsize=(8,6))
plt.subplot(3,3,1)
plt.hist(ak.to_numpy(ak.flatten(jets['pt'])),bins=50,range=(0,300))
plt.xlabel(r'p$_T$ (GeV/c)')
plt.subplot(3,3,2)
plt.hist(ak.to_numpy(ak.flatten(jets['eta'])),bins=50,range=(-6,6))
plt.xlabel(r'$\eta$')
plt.subplot(3,3,3)
plt.hist(ak.to_numpy(ak.flatten(jets['phi'])),bins=50,range=(-3.2,3.2))
plt.xlabel(r'$\phi$')

plt.subplot(3,3,4)
plt.hist(ak.to_numpy(ak.flatten(muons['pt'])),bins=50,range=(0,300))
plt.xlabel(r'p$_T$ (GeV/c)')
plt.subplot(3,3,5)
plt.hist(ak.to_numpy(ak.flatten(muons['eta'])),bins=50,range=(-6,6))
plt.xlabel(r'$\eta$')
plt.subplot(3,3,6)
plt.hist(ak.to_numpy(ak.flatten(muons['phi'])),bins=50,range=(-3.2,3.2))
plt.xlabel(r'$\phi$')

plt.subplot(3,3,7)
plt.hist(ak.to_numpy(ak.flatten(electrons['pt'])),bins=50,range=(0,300))
plt.xlabel(r'p$_T$ (GeV/c)')
plt.subplot(3,3,8)
plt.hist(ak.to_numpy(ak.flatten(electrons['eta'])),bins=50,range=(-6,6))
plt.xlabel(r'$\eta$')
plt.subplot(3,3,9)
plt.hist(ak.to_numpy(ak.flatten(electrons['phi'])),bins=50,range=(-3.2,3.2))
plt.xlabel(r'$\phi$')

plt.show()


