import csv
import numpy as np
import pickle

import sys
import os

filename = sys.argv[1]

info = {}

first = True

csvReader = csv.reader(open(filename), delimiter=',', quotechar='|')
for row in csvReader:
    if not first:
        print(row)
        info[row[0]] = {'dataset':row[1],
            'prepid':row[2],
            'requested_events':row[3],
            'completed_events':row[4],
            'crosssection':row[5],
            'luminosity':row[6]}
    else:
        first = False

with open('MCInfo_2017.pkl', 'wb') as fp:
    pickle.dump(info, fp)


