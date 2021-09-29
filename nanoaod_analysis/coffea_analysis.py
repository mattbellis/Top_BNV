import matplotlib.pylab as plt
import numpy as np
import pandas as pd

from coffea import util, processor
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema

import awkward as ak

import time
tstart = time.time()

import sys

#Run Coffea code using uproot
output = processor.run_uproot_job(
    fileset,
    "Events",
    TTGammaProcessor(isMC=True),
    processor.iterative_executor,
    executor_args={'schema': NanoAODSchema,'workers': 4},
    chunksize=-1,
    maxchunks=1,
    )

elapsed = time.time() - tstart
print("Total time: %.1f seconds"%elapsed)
print("Total rate: %.1f events / second"%(output['EventCount'].value/elapsed))

