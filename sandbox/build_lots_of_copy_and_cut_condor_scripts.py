import sys
import os

import subprocess as sp

# Testing with
# python build_lots_of_copy_and_cut_condor_scripts.py  ~/eos_store/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/

def write_out_build_file(list_of_files,topdir,s0,s1,s2):

    lo = list_of_files[0].split('_')[-1].split('.root')[0]
    hi = list_of_files[-1].split('_')[-1].split('.root')[0]
    tag = "NFILES_%s_%s" % (lo,hi)

    #arguments = "%s_%s_%s_%s.pkl" % (s0,s1,s2, tag)
    #arguments = "DATA_DATASET_%s_%s.pkl" % (s0, tag)
    #if topdir.find('SingleMuon')>=0:
        #arguments = "DATA_DATASET_%s_%s.pkl" % (s0, tag)
    #else:
        #arguments = "MC_DATASET_%s_%s.pkl" % (s0, tag)

    #print(arguments)

    #startdir = topdir.split('/')[-2:]
    fullnames = []
    for f in list_of_files:
        newname = "%s/%s/%s/%s/%s" % (topdir,s0,s1,s2,f)
        fullnames.append(newname)

    print(list_of_files)
    print(fullnames)

    copybackdirectory = "root://cmseos.fnal.gov/%s/%s/%s/%s/." % (topdir,s0,s1,s2)
    print()
    print(copybackdirectory)
    print()

    #cmd = ['python', 'build_copy_and_cut_condor_script.py', copybackdirectory, arguments]
    cmd = ['python', 'build_copy_and_cut_condor_script.py', copybackdirectory]
    for rootfile in fullnames:
        cmd += [rootfile]
    print(cmd)
    sp.Popen(cmd,0).wait()

    #exit()


files_at_a_time = 10

pwd = os.getcwd()
# This should be something like eos_store/SingleMuon (for the data)
topdir = sys.argv[1]
print("topdir: %s" % (topdir))
os.chdir(topdir)
topdir_lastname = os.getcwd().split('/')[-1]
os.chdir(pwd)

subdirs0 = os.listdir(topdir)
print(subdirs0)

for s0 in subdirs0:

    path = "%s/%s" % (topdir,s0)

    # This should get us the 180122, stuff
    subdirs1 = os.listdir(path)
    print(subdirs1)

    for s1 in subdirs1:

        path = "%s/%s/%s" % (topdir,s0,s1)

        # This should get us the 0000, 0001 stuff
        subdirs2 = os.listdir(path)
        print(subdirs2)

        
        for s2 in subdirs2:

            path = "%s/%s/%s/%s" % (topdir,s0,s1,s2)

            # This should get us the outfiles!
            files = os.listdir(path)
            rootfiles = []
            for f in files:
                if '.root' in f:
                    rootfiles.append(f)

            rootfiles.sort()
            #print(rootfiles)

            nfiles = len(rootfiles)
            print("nfiles: %d" % (nfiles))

            maxnum = -1
            minnum = 1e6
            for rootfile in rootfiles:
                testnum = int(rootfile.split('_')[-1].split('.root')[0])
                if testnum>maxnum:
                    maxnum = testnum
                if testnum<minnum:
                    minnum = testnum

            print("maxnum is %d" % (maxnum))

            i=0
            list_of_files = []
            for i in range(minnum-1,maxnum):

                tempfile = "out_file_%d.root" % (i+1)

                if tempfile in rootfiles:
                    list_of_files.append(tempfile)
                
                if (i+1)%files_at_a_time==0:
                    print(i)

                    if len(list_of_files)>0:
                        write_out_build_file(list_of_files,topdir,s0,s1,s2)
                        list_of_files[:] = []

            if len(list_of_files)>0:
                write_out_build_file(list_of_files,topdir,s0,s1,s2)

            
    # Comment this out when we want to run over everything
    #exit()


print(topdir)
