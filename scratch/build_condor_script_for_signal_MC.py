import numpy as np
import sys
import subprocess as sp

import os

# Make the log file directory
if not os.path.exists('./condor_log_files'):
    os.makedirs('./condor_log_files')

#infile_directory = "crab_SingleMuon_Run2016C-03Feb2017-v1"

outfile = sys.argv[1]
infiles = sys.argv[2:]

cmd = "universe = vanilla\n"
cmd += "Executable = execute_python_on_condor_fwlite_for_signal_MC.sh\n"
cmd += "Should_Transfer_Files = YES\n"
cmd += "WhenToTransferOutput = ON_EXIT\n"
cmd += "Transfer_Input_Files = topbnv_tools.py, topbnv_fwlite.py, FrameworkJobReport.xml, JECs, execute_for_condor_signal_MC.py, execute_python_on_condor_fwlite_for_signal_MC.sh, PSet.py\n"
cmd += "Output = condor_log_files/bellis_%s_$(Cluster)_$(Process).stdout\n" % (outfile.split('.root')[0])
cmd += "Error = condor_log_files/bellis_%s_$(Cluster)_$(Process).stderr\n" % (outfile.split('.root')[0])
cmd += "Log = condor_log_files/bellis_%s_$(Cluster)_$(Process).log\n" % (outfile.split('.root')[0])
cmd += "notify_user = mbellis@FNAL.GOV\n"
# No longer need this line 
# https://uscms.org/uscms_at_work/computing/setup/condor_refactor.shtml
#cmd += "x509userproxy = /tmp/x509up_u47418 \n"
#cmd += "Arguments = --outfile %s " % (outfile)
cmd += "Arguments = %s " % (outfile)
for infile in infiles:
    prepend = "root://cmsxrootd.fnal.gov//store/user/mbellis"
    #postpend = infile.split('mbellis')[1]
    postpend = infile.split('eos_store')[1]
    filename = "%s/%s " % (prepend, postpend)
    cmd += filename 
cmd += "\n"
cmd += "Queue 1\n"

print(cmd)

outfilename = "cdr_temp_%s.jdl" % (outfile.split('.root')[0])
outfile = open(outfilename,'w')
outfile.write(cmd)
outfile.close()

# Submit it
condor_cmd = ['sh', 'condor_submit_script.sh', outfilename]
print(condor_cmd)
sp.Popen(condor_cmd,0).wait()

