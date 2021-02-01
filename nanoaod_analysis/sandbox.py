from itertools import combinations
import numpy as np

import sys

njets = int(sys.argv[1])
nleps = int(sys.argv[2])

jetindices = np.arange(njets,dtype=int)
lepindices = np.arange(nleps,dtype=int)

x = combinations(jetindices,3)

#print(x)
for had in x:
    #print("-------")
    #print(had)
    # Remove those indices
    remaining = np.delete(jetindices, np.argwhere( (jetindices==had[0]) | (jetindices==had[1]) | (jetindices==had[2]) ))
    bnv = combinations(remaining,2)
    for b in bnv:
        for lep in lepindices:
            print(had,b,lep)
    #for j in arr:
        #print(j)
