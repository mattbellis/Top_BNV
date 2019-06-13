import csv
import numpy as np
import pickle

import sys
import os

filename = sys.argv[1]

f = filename.split('.')

datasets = []

csvReader = csv.reader(open(filename), delimiter=' ', quotechar='|')
for row in csvReader:
    if len(row) > 0:
        r = row[0].split('/')
        v = r[2].split('asymptotic_v3')
        short_name = r[1] + v[-1] 
        datasets.append([short_name,row[0][1:]])

with open(f[0]+'.pkl', 'wb') as fp:
    pickle.dump(datasets, fp)

for data in datasets:
    prepid = os.popen('dasgoclient --query="mcm dataset=/'+data[1]+'"').read()
    data.append(prepid)
'''
with open('datasets.csv', 'w') as myfile:
    wr = csv.writer('datasets.csv', quoting=csv.QUOTE_ALL)
    wr.writerow(datasets)
'''

np.savetxt(f[0]+'COMPLETE.csv', datasets, delimiter=",", fmt='%s')

