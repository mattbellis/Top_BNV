import numpy as np
import sys
import subprocess as sp

#infile_directory = "crab_SingleMuon_Run2016C-03Feb2017-v1"

infiles = sys.argv[1:]

cmd = "universe = vanilla\n"
cmd += "Executable = execute_python_script_to_copy_and_cut.sh\n"
cmd += "Should_Transfer_Files = YES\n"
cmd += "WhenToTransferOutput = ON_EXIT\n"
cmd += "Transfer_Input_Files = copy_and_cut_file.py\n"
cmd += "Output = condor_log_files/bellis_%s_$(Cluster)_$(Process).stdout\n" % ("copy_and_cut")
cmd += "Error = condor_log_files/bellis_%s_$(Cluster)_$(Process).stderr\n" % ("copy_and_cut")
cmd += "Log = condor_log_files/bellis_%s_$(Cluster)_$(Process).log\n" % ("copy_and_cut")
cmd += "notify_user = mbellis@FNAL.GOV\n"
cmd += "x509userproxy = /tmp/x509up_u47418 \n"
cmd += "Arguments = "
for infile in infiles:
    #prepend = "root://cmsxrootd.fnal.gov//store/user/mbellis"
    prepend = "root://cmseos.fnal.gov//store/user/mbellis"
    #postpend = infile.split('mbellis')[1]
    postpend = infile.split('eos_store')[1]
    filename = "%s/%s " % (prepend, postpend)
    cmd += filename 
cmd += "\n"
cmd += "Queue 1\n"

print(cmd)

outfilename = "cdr_temp_%s.jdl" % ("cut_and_count")
outfile = open(outfilename,'w')
outfile.write(cmd)
outfile.close()

# Submit it
condor_cmd = ['condor_submit', outfilename]
sp.Popen(condor_cmd,0).wait()

