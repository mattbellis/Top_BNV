import sys
import os

import subprocess as sp

import commands

# Testing with
# python build_lots_of_condor_scripts.py ~/eos_store/SingleMuon

def write_out_build_file(list_of_files,topdir,s0,s1,s2):

    lo = list_of_files[0].split('_')[-1].split('.root')[0]
    hi = list_of_files[-1].split('_')[-1].split('.root')[0]
    tag = "NFILES_%s_%s" % (lo,hi)

    #outfile = "%s_%s_%s_%s.pkl" % (s0,s1,s2, tag)
    outfile = "DATA_DATASET_%s_%s.root" % (s0, tag)
    if topdir.find('SingleMuon')>=0:
        outfile = "DATA_DATASET_%s_%s.root" % (s0, tag)
    else:
        outfile = "MC_DATASET_%s_%s.root" % (s0, tag)

    print("OUTFILE:")
    print(outfile)
    print()

    #startdir = topdir.split('/')[-2:]
    fullnames = []
    for f in list_of_files:
        newname = "%s/%s/%s/%s/%s" % (topdir,s0,s1,s2,f)
        fullnames.append(newname)

    print(list_of_files)
    print(fullnames)

            
    cmd = ['python', 'build_condor_script.py', outfile]
    for rootfile in fullnames:
        cmd += [rootfile]
    print(cmd)
    sp.Popen(cmd,0).wait()
    

    #exit()


files_at_a_time = 100

pwd = os.getcwd()
# This should be something like eos_store/SingleMuon (for the data)
topdir = sys.argv[1]
print("topdir: %s" % (topdir))
os.chdir(topdir)
topdir_lastname = os.getcwd().split('/')[-1]
os.chdir(pwd)

subdirs0 = os.listdir(topdir)
print(subdirs0)
print(topdir_lastname)

#################################################################
# Make the output directory because we know where this will go
outputdir = "/uscms/homes/m/mbellis/eos_store/script_output_files_NEW/{0}".format(topdir_lastname)

print("Making output directory;")
print(outputdir)
cmds = ['mkdir',outputdir]
#print(cmds)
sp.Popen(cmds,0).wait()
#################################################################


#exit()

for s0 in subdirs0:

    path = "%s/%s" % (topdir,s0)

    # I DON'T WANT TO RUN ON THE OLD STUFF FOR NOW
    if path.find('crab_SingleMuon')>0:
        print("Skipping....")
        print(path)
        continue 


    print("Processing....")
    print(path)
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
                # For MC
                #if '.root' in f and 'TRIGGER' in f:
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

                # For MC
                #tempfile = "TRIGGER_APPLIED_out_file_%d.root" % (i+1)
                tempfile = "output_%d.root" % (i+1)

                if tempfile in rootfiles:
                    list_of_files.append(tempfile)
                
                if (i+1)%files_at_a_time==0:
                    #print(i)

                    #print(len(list_of_files))

                    if len(list_of_files)>0:
                        write_out_build_file(list_of_files,topdir,s0,s1,s2)
                        list_of_files[:] = []

            if len(list_of_files)>0:
                write_out_build_file(list_of_files,topdir,s0,s1,s2)

            
    #exit()


print(topdir)
