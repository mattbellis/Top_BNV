import numpy as np
import sys
import subprocess as sp

import os

# Make the log file directory
if not os.path.exists('./condor_log_files'):
    os.makedirs('./condor_log_files')


#infile_directory = "crab_SingleMuon_Run2016C-03Feb2017-v1"

#output_destination = '/uscms/homes/m/mbellis/nobackup/CONDOR_output_files_Feb2019/{0}/MC/year/process'.format(topdir)
# This should be the directory path *under*the above output destination
outputsubdir = sys.argv[1]
outfile = sys.argv[2]
infiles = sys.argv[3:]

cmd = "universe = vanilla\n"
cmd += "Executable = execute_python_on_condor.sh\n"
cmd += "Should_Transfer_Files = YES\n"
cmd += "WhenToTransferOutput = ON_EXIT\n"
cmd += "Transfer_Input_Files = topbnv_tools.py, top_reconstruction_to_run_at_FNAL_over_grid_job_output.py\n"
cmd += "Output = condor_log_files/bellis_%s_$(Cluster)_$(Process).stdout\n" % (outfile.split('.root')[0])
cmd += "Error = condor_log_files/bellis_%s_$(Cluster)_$(Process).stderr\n" % (outfile.split('.root')[0])
cmd += "Log = condor_log_files/bellis_%s_$(Cluster)_$(Process).log\n" % (outfile.split('.root')[0])
#cmd += "output_destination = %s/%s\n" % ('/uscms_data/d1/mbellis/CONDOR_output_files_Feb2019/',topdir)
#cmd += "output_destination = file:%s\n" % (output_destination)
#cmd += "transfer_output_files = %s\n" % (outfile)
cmd += "notify_user = mbellis@FNAL.GOV\n"
# No longer need this line 
# https://uscms.org/uscms_at_work/computing/setup/condor_refactor.shtml
#cmd += "x509userproxy = /tmp/x509up_u47418 \n"
cmd += "Arguments = %s --outfile %s " % (outputsubdir,outfile)
for infile in infiles:
    prepend = "root://cmsxrootd.fnal.gov//store/user/mbellis"
    #postpend = infile.split('mbellis')[1]
    #postpend = infile.split('eos_store')[1]
    postpend = infile # This should work with the new system, July 2019
    filename = "%s/%s " % (prepend, postpend)
    cmd += filename 
cmd += "\n"
cmd += "Queue 1\n"

print(cmd)

jdloutfilename = "cdr_temp_%s.jdl" % (outfile.split('.root')[0])
jdloutfile = open(jdloutfilename,'w')
jdloutfile.write(cmd)
jdloutfile.close()

# Submit it
condor_cmd = ['sh', 'condor_submit_script.sh', jdloutfilename]
print(condor_cmd)
sp.Popen(condor_cmd,0).wait()

