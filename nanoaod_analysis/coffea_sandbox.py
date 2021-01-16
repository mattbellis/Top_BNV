import matplotlib.pylab as plt
import numpy as np
import pandas as pd

from coffea import util, processor
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema

from processor_test import MyProcessor


import awkward1 as ak

import time
tstart = time.time()

import sys

# Create a dictionary of the files
fileset = {}
filenames = sys.argv[1:]
for i,filename in enumerate(filenames):
    fileset['file{0}'.format(i)] = [filename]

print(fileset)



#Run Coffea code using uproot
output = processor.run_uproot_job(
    fileset,
    "Events",
    MyProcessor(isMC=True),
    processor.iterative_executor,
    executor_args={'schema': NanoAODSchema,'workers': 4},
    chunksize=100,
    maxchunks=1,
    )

elapsed = time.time() - tstart
print("Total time: %.1f seconds"%elapsed)
print("Total rate: %.1f events / second"%(output['EventCount'].value/elapsed))

print()
print(output)
print(type(output))

