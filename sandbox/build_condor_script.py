import numpy as np
import sys
import subprocess as sp

#infile_directory = "crab_SingleMuon_Run2016C-03Feb2017-v1"

pickleoutfile = sys.argv[1]
infiles = sys.argv[2:]

cmd = "universe = vanilla\n"
cmd += "Executable = execute_python_script.sh\n"
cmd += "Should_Transfer_Files = YES\n"
cmd += "WhenToTransferOutput = ON_EXIT\n"
cmd += "Transfer_Input_Files = topbnv_tools.py, top_reco_Reza_ROOT_file_factorized.py\n"
cmd += "Output = condor_log_files/bellis_%s_$(Cluster)_$(Process).stdout\n" % (pickleoutfile.split('.pkl')[0])
cmd += "Error = condor_log_files/bellis_%s_$(Cluster)_$(Process).stderr\n" % (pickleoutfile.split('.pkl')[0])
cmd += "Log = condor_log_files/bellis_%s_$(Cluster)_$(Process).log\n" % (pickleoutfile.split('.pkl')[0])
cmd += "notify_user = mbellis@FNAL.GOV\n"
cmd += "x509userproxy = /tmp/x509up_u47418 \n"
cmd += "Arguments = --outfile %s " % (pickleoutfile)
for infile in infiles:
    prepend = "root://cmsxrootd.fnal.gov//store/user/mbellis"
    #postpend = infile.split('mbellis')[1]
    postpend = infile.split('eos_store')[1]
    filename = "%s/%s " % (prepend, postpend)
    cmd += filename 
cmd += "\n"
cmd += "Queue 1\n"

print(cmd)

outfilename = "cdr_temp_%s.jdl" % (pickleoutfile.split('.pkl')[0])
outfile = open(outfilename,'w')
outfile.write(cmd)
outfile.close()

# Submit it
condor_cmd = ['condor_submit', outfilename]
sp.Popen(condor_cmd,0).wait()

