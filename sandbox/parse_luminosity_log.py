import numpy as np
import pickle

import sys

infilename = 'LUMINOSITY.log'
infile = open(infilename,'r')

lumi_info = {}

while True:

    line = infile.readline()

    if not line:
        break

    if 'crab_projects' in line:
        dataset = line.split('/')[1].strip()
        print(dataset)
        lumi_info[dataset] = {}
        tag = "%s" % (dataset.split('Run')[1])
        tag = tag.replace('-03Feb2017','')
        tag = tag.strip()
        lumi_info[dataset]['tag'] = tag

    if 'nfill' in line:
        line = infile.readline()
        line = infile.readline()
        vals = line.split('|')
        nfill,nrun,nls,ncms,delivered,recorded = vals[1],vals[2],vals[3],vals[4],vals[5],vals[6]

        lumi_info[dataset]['nfill'] = int(nfill)
        lumi_info[dataset]['nrun'] = int(nrun)
        lumi_info[dataset]['nls'] = int(nls)
        lumi_info[dataset]['ncms'] = int(ncms)
        lumi_info[dataset]['delivered'] = float(delivered)/1e9
        lumi_info[dataset]['recorded'] = float(recorded)/1e9
        
        print(nfill,nrun,nls,ncms,delivered,recorded)

print(lumi_info)

tot = 0
for key in lumi_info.keys():
    tag = lumi_info[key]['tag']
    lumi = lumi_info[key]['recorded']
    tot += lumi
    print('{:20}'.format(tag),lumi)

print(tot)

################################################################################
# Now parse the crab completion log
################################################################################

infilename = 'CRAB_COMPLETION.log'
infile = open(infilename,'r')

while True:

    line = infile.readline()

    if not line:
        break

    if 'CRAB project directory' in line:
        dataset = line.split('/')[-1].strip()
        print(dataset)
        failed = 0

    if 'finished' in line:
        finished = int(line.split('(')[1].split('/')[0])
        finished_out_of = int(line.split('/')[1].split(')')[0])
        print(finished,finished_out_of, finished_out_of-finished)

        lumi_info[dataset]['finished_files'] = finished
        lumi_info[dataset]['total_files'] = finished_out_of

print(lumi_info)
pickle.dump( lumi_info, open( "lumi_info.pkl", "wb" ) )

