#!/bin/bash
echo "Starting job on " `date` #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
echo "System software: `cat /etc/redhat-release`" #Operating System on that node
source /cvmfs/cms.cern.ch/cmsset_default.sh  ## if a tcsh script, use .csh instead of .sh
export SCRAM_ARCH=slc6_amd64_gcc630
#eval `scramv1 project CMSSW CMSSW_9_3_2`
eval `scramv1 project CMSSW CMSSW_8_0_26`
cd CMSSW_8_0_26/src/
pwd
ls -l 
echo "HERE"
ls -l ../
echo "THERE"
ls -l ../../
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo "CMSSW: "$CMSSW_BASE
echo "Arguments passed to this script are: for 1: $*"


cp ../../top_reconstruction_to_run_at_FNAL_over_grid_job_output.py .
cp ../../topbnv_tools.py .

ls -ltr 
echo
echo python top_reconstruction_to_run_at_FNAL_over_grid_job_output.py ${*}
     python top_reconstruction_to_run_at_FNAL_over_grid_job_output.py ${*}
#xrdcp nameOfOutputFile.root root://cmseos.fnal.gov//store/user/username/nameOfOutputFile.root
echo
ls -ltr 

########################################################################################
# Figure out which subdir to copy stuff over
# This is dependent on how things are being copied over and the directory is
# currently created in the build_lots_of_condor_scripts.py
########################################################################################
# Making use of xrdcp
# https://uscms.org/uscms_at_work/computing/LPC/additionalEOSatLPC.shtml
subdir=`echo $3 | awk -F"/" '{print $9}'`

echo "subdir: "$subdir

#if ( ! -d  root://cmseos.fnal.gov//store/user/mbellis/script_output_files_NEW/$subdir ) then
#echo xrdfs root://cmseos.fnal.gov//store/user/mbellis/script_output_files_NEW/$subdir mkdir
     #xrdfs root://cmseos.fnal.gov//store/user/mbellis/script_output_files_NEW/$subdir mkdir
#echo xrdfs root://cmseos.fnal.gov//store/user/mbellis/script_output_files_NEW/$subdir/$2 rm 
     #xrdfs root://cmseos.fnal.gov//store/user/mbellis/script_output_files_NEW/$subdir/$2 rm 

# This directory has to already exist
echo xrdcp $2 root://cmseos.fnal.gov//store/user/mbellis/script_output_files_NEW/$subdir/.
     xrdcp $2 root://cmseos.fnal.gov//store/user/mbellis/script_output_files_NEW/$subdir/.

#/eos/uscms/store/user/mbellis
### remove the output file if you don't want it automatically transferred when the job ends
rm *.root
cd ${_CONDOR_SCRATCH_DIR}
rm -rf CMSSW_8_0_26

