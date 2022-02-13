import numpy as np
import awkward as ak
import uproot as uproot

import sys

from coffea.nanoevents import NanoEventsFactory, NanoAODSchema


infilename = sys.argv[1]

events = NanoEventsFactory.from_root(infilename, schemaclass=NanoAODSchema).events()
nevents = len(events)
print(nevents)
print()

# Make a fake array of genparticles I want to pull out
# Suppose I want some random 3 particles out of the first 12 gen particles
truth = np.random.randint(0,12,(nevents,3))

print("Take a quick look at truth")
print(truth.shape)
print(truth[0:10])
print(type(truth), type(truth[0]))
print()

# This seems to work
print(events[0].GenPart[truth[0]])
print(events[0].GenPart[truth[0]].pdgId)
print()

print(events[23].GenPart[truth[23]])
print(events[23].GenPart[truth[23]].pdgId)
print()

# This works too!
print(events.GenPart[truth].pdgId)
print()

#### OK, let's break some stuff!

# I'm going to try to get an subset of events and also a subset
# of our "truth" indices for GenPart

print("Now to break stuff!!!!!")

'''
event_number_subset = np.array([16, 89, 223])

truth_subset = truth[event_number_subset]
print(truth_subset)

events = events[event_number_subset]

print(f"events length: {len(events)}    truth_subset len: {len(truth_subset)}\n")
# This works
print("pdgId of one of the events in the subset")
print(events[1].GenPart[truth_subset[1]].pdgId)

# This doesn't. :(
print(events.GenPart[truth_subset].pdgId)
'''

# Test
for g in events.GenPart[2]:
       print(f"{g.pdgId:4d}  {g.status:3d}  {events.GenPart[0][g.genPartIdxMother].pdgId:4d}  {g.hasFlags(['isPrompt','isLastCopy'])} {g.pt:8.3f} {g.eta:8.3f} {g.phi:8.3f} {g.mass:8.3f}")













