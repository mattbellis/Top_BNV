import sys
import os

import subprocess as sp

import commands


def make_directory(outputdir):
    #outputdir = "/uscms/homes/m/mbellis/eos_store/CONDOR_output_files_2019/{0}/{1}/{2}".format(mc_or_data,year,trigger)
    print("\nMaking directory................")
    print(outputdir)
    cmds = ['mkdir','-p',outputdir]
    print(cmds)
    sp.Popen(cmds,0).wait()
    print('\n')

# Testing with
# For data
# python build_lots_of_condor_scripts.py ~/eos_store/SingleMuon

def write_out_build_file(list_of_files,topdir,s0,s1,s2,s3):

    lo = list_of_files[0].split('_')[-1].split('.root')[0]
    hi = list_of_files[-1].split('_')[-1].split('.root')[0]
    tag = "NFILES_%s_%s" % (lo,hi)

    print("-------")
    print(topdir)
    print(s0,s1,s2)
    print(list_of_files[0])
    destinationdir = '{0}/{1}/{2}/{3}'.format(topdir,s1,s2,s3)

    #outfile = "%s_%s_%s_%s.pkl" % (s0,s1,s2, tag)
    outfile = "DATA_DATASET_%s_%s.root" % (s0, tag)
    #if topdir.find('SingleMuon_Run')>=0:
    if topdir.find('Run2016')>=0 or s0.find('Run2016')>0 or s1.find('Run2016')>0 or s2.find('Run2016')>0:
        outfile = "DATA_DATASET_%s_%s.root" % (s0, tag)
    else:
        outfile = "MC_DATASET_%s_%s.root" % (s0, tag)

    print("OUTFILE:")
    print(outfile)
    print()
    #exit()

    #startdir = topdir.split('/')[-2:]
    fullnames = []
    for f in list_of_files:
        newname = "{0}/{1}/{2}/{3}/{4}".format(topdir,s1,s2,s3,f)
        fullnames.append(newname)

    #print(list_of_files)
    #print(fullnames)


    #topdirlastdir = topdir.split('/')[-1]
    #if topdir[-1]=='/':
        #topdirlastdir = topdir.split('/')[-2]
            
    cmd = ['python', 'build_condor_script.py', destinationdir, outfile]
    for rootfile in fullnames:
        cmd += [rootfile]
    print(cmd)
    sp.Popen(cmd,0).wait()
    

    #exit()


#files_at_a_time = 100
files_at_a_time = 10
#files_at_a_time = 3
#files_at_a_time = 1

pwd = os.getcwd()
# This should be something like eos_store/SingleMuon (for the data)
#topdir = sys.argv[1]
mc_or_data_options = ['MC','Data']
years_and_triggers = {'2016':['SingleMuon','SingleElectron'], 
                      '2017':['SingleMuon','SingleElectron'], 
                      '2018':['SingleMuon','EGamma']
                      }

mc_or_data = mc_or_data_options[0]
year = '2016'
trigger = years_and_triggers[year][0]

topdir = '/uscms/homes/m/mbellis/eos_store/{0}/{1}/{2}'.format(mc_or_data, year, trigger)
#if mc_or_data=='Data':
#    topdir = '/uscms/homes/m/mbellis/eos_store/{0}/{1}/{2}/{2}'.format(mc_or_data, year, trigger)

print("topdir: %s" % (topdir))
os.chdir(topdir)
topdir_lastname = os.getcwd().split('/')[-1]
os.chdir(pwd)

subdirs0 = os.listdir(topdir)
#print(subdirs0)
#print(topdir_lastname)

#################################################################
# Make the output directory because we know where this will go
outputtopdir = "/uscms/homes/m/mbellis/eos_store/CONDOR_output_files_2019/".format(mc_or_data,year,trigger)
outputtopsubdir = "{0}/{1}/{2}".format(mc_or_data,year,trigger)
outputdir = "{0}/{1}".format(outputtopdir, outputtopsubdir)
make_directory(outputdir)
#print("Making output directory;")
#print(outputdir)
#cmds = ['mkdir','-p',outputdir]
#print(cmds)
#sp.Popen(cmds,0).wait()
#exit()
#################################################################

print('\n')
print("==============\nPhysics processes....\n=======================")
print(subdirs0)

#exit()

for s0 in subdirs0:

    # I DON'T WANT TO RUN ON CERTAIN ONES
    #if s0.find('WW')<0:
    if 0:
        print("Skipping....")
        print(s0)
        continue 

    path = "%s/%s" % (topdir,s0)


    # The TTX files take a long time to run so only run on 1 file
    # at a time
    if s0.find('TT')>=0:
        files_at_a_time = 1
    else:
        files_at_a_time = 10
    #outputsubdir = "{0}/{1}".format(outputtopsubdir,s0)
    #outputdir = "{0}/{1}".format(outputdir, s0)
    #make_directory(outputdir)


    print("----------\nDatasets of that process\n--------------")
    print(path+'\n')
    subdirs1 = os.listdir(path)
    print(subdirs1)

    for s1 in subdirs1:

        outputsubdir = "{0}/{1}".format(outputtopsubdir,s0)
        print("OUTPUTSUBDIR: ", outputsubdir)
        #outputdir = "{0}/{1}/{2}".format(outputdir, s0, s1)
        #make_directory(outputdir)

        # This should get us the 180122, stuff
        path = "%s/%s/%s" % (topdir,s0,s1)
        print("----------\nSubdirectories of crab processing\n--------------")
        print(path+'\n')

        subdirs2 = os.listdir(path)
        print(subdirs2)

        for s2 in subdirs2:

            # This should get us the 0000, 0001 stuff
            path = "%s/%s/%s/%s" % (topdir,s0,s1,s2)
            print("----------\nSub-Subdirectories of crab processing\n--------------")
            print(path+'\n')

            subdirs3 = os.listdir(path)
            print(subdirs3)

            for s3 in subdirs3:

                outputdir = "{0}/{1}/{2}/{3}/{4}/{5}".format(outputtopdir, outputtopsubdir, s0, s1, s2, s3)
                make_directory(outputdir)

                # This should get us the outfiles!
                path = "%s/%s/%s/%s/%s" % (topdir,s0,s1,s2,s3)
                print("----------\nOutput directories that have the root files\n--------------")
                print(path+'\n')

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
                            write_out_build_file(list_of_files,outputsubdir,s0,s1,s2,s3)
                            list_of_files[:] = []

                if len(list_of_files)>0:
                    write_out_build_file(list_of_files,outputsubdir,s0,s1,s2,s3)

                
        #exit()


print(topdir)
