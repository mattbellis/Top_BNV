import numpy as np
import matplotlib.pylab as plt
import uproot
import awkward as ak

import vector

import sys

vector.register_awkward()


infilename = sys.argv[1]

infile = uproot.open(infilename)


'''
muon_branch_arrays = infile["Events"].arrays(filter_name="Muon_*")
electron_branch_arrays = infile["Events"].arrays(filter_name="Electron_*")

muons = ak.zip({
    "pt": muon_branch_arrays["Muon_pt"],
    "phi": muon_branch_arrays["Muon_phi"],
    "eta": muon_branch_arrays["Muon_eta"],
    "mass": muon_branch_arrays["Muon_mass"],
    "charge": muon_branch_arrays["Muon_charge"],
}, with_name="Momentum4D")
electrons = ak.zip({
    "pt": electron_branch_arrays["Electron_pt"],
    "phi": electron_branch_arrays["Electron_phi"],
    "eta": electron_branch_arrays["Electron_eta"],
    "mass": electron_branch_arrays["Electron_mass"],
    "charge": electron_branch_arrays["Electron_charge"],
}, with_name="Momentum4D")

quads = ak.combinations(muons, 4)
quad_charge = quads["0"].charge + quads["1"].charge + quads["2"].charge + quads["3"].charge
mu1, mu2, mu3, mu4 = ak.unzip(quads[quad_charge == 0])
plt.hist(ak.flatten((mu1 + mu2 + mu3 + mu4).mass), bins=100, range=(0, 200));


plt.show()
'''
