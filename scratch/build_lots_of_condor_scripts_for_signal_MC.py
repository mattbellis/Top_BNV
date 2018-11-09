import numpy as np
import sys
import subprocess as sp

import os


# Run as (for example)
# python build_lots_of_condor_scripts_for_signal_MC.py ~/eos_store/signalMC/bnv_ttbar_t2mubc/*.root

infiles = sys.argv[1:]
outfiletag = infiles[0].split("/")[-2]
print(outfiletag)

# Get the eos location of these files
#topdir = infiles[0].split("/")[0:-2].join("/")
#print("topdir: %s" % (topdir))
#os.chdir(topdir)
#topdir_lastname = os.getcwd().split('/')[-1]
#os.chdir(pwd)

outputdir = "/uscms/homes/m/mbellis/eos_store/script_output_files_NEW/{0}".format(outfiletag)

print(outputdir)

#exit(1)



nfiles = len(infiles)

nfiles_to_process = 500

nchunks = int(np.floor(nfiles/nfiles_to_process)) + 1

if nchunks*nfiles_to_process>nfiles:
    nchunks -= 1

print(nchunks)
for i in range(0,nchunks):

    lo = i*nfiles_to_process
    hi = (i+1)*nfiles_to_process
    
    fullnames = infiles[lo:hi]

    outfile = "MC_DATASET_%s_%03d.root" % (outfiletag, i)

    cmd = ['python', 'build_condor_script_for_signal_MC.py', outfile]
    for rootfile in fullnames:
        cmd += [rootfile]
    print(cmd)
    sp.Popen(cmd,0).wait()

