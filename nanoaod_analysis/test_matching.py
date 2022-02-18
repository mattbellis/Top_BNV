import numpy as np
import awkward as ak
import uproot as uproot

import matplotlib.pylab as plt

import sys

from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import nanoaod_analysis_tools as nat

import hepfile

import time

import argparse

# Argparse
parser = argparse.ArgumentParser(description='Process some data.')
parser.add_argument('--nevents', dest='maxevents',  type=int, default=None,
                    help='Max events to process')
parser.add_argument('--event-range', dest='event_range', type=str,
                    default=None, help='Range of events to process.')
parser.add_argument('infilename')

args = parser.parse_args()
print(args)

if args.maxevents is not None and args.event_range is not None:
    print("Can't set both max events and event range.")
    exit()

infilename = args.infilename
events = NanoEventsFactory.from_root(infilename, schemaclass=NanoAODSchema).events()

genpart = events.GenPart
jets = events.Jet

mask = abs(genpart.pdgId) == 5

print(genpart[mask].pdgId)
