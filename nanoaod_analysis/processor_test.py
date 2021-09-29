import time

from coffea import hist, util
import coffea.processor as processor
from coffea.nanoevents.methods import nanoaod
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
from coffea.lookup_tools import extractor, dense_lookup
from coffea.btag_tools import BTagScaleFactor
from coffea.analysis_tools import PackedSelection
from coffea.jetmet_tools import CorrectedJetsFactory, JECStack

import awkward1 as ak
import numpy as np
import pickle
import re

# Look at ProcessorABC to see the expected methods and what they are supposed to do
class MyProcessor(processor.ProcessorABC):

    ############################################################################
    def __init__(self, isMC=False, runNum=-1, eventNum=-1, mcEventYields=None, jetSyst='nominal'):

        ################################
        # INITIALIZE COFFEA PROCESSOR
        ################################
        ak.behavior.update(nanoaod.behavior)
    
        self._accumulator = processor.dict_accumulator({
            #'nmuons': processor.defaultdict_accumulator(float),
            'EventCount': processor.value_accumulator(int)
        })

    ############################################################################
    @property
    def accumulator(self):
        return self._accumulator


    def process(self, events):

        output = self.accumulator.identity()
        output['EventCount'] = len(events)

        #output['nmuons'] = ak.num(events.Muons)

        return output


    def postprocess(self, accumulator):
        return accumulator







