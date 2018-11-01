#!/bin/bash
echo "Starting job on " `date` #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
echo "System software: `cat /etc/redhat-release`" #Operating System on that node
source /cvmfs/cms.cern.ch/cmsset_default.sh  ## if a tcsh script, use .csh instead of .sh
export SCRAM_ARCH=slc6_amd64_gcc630
eval `scramv1 project CMSSW CMSSW_9_3_2`
cd CMSSW_9_3_2/src/
pwd
ls -l 
echo "HERE"
ls -l ../
echo "THERE"
ls -l ../../
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo "CMSSW: "$CMSSW_BASE
echo "Arguments passed to this script are: for 1: $*"


cp ../../copy_and_cut_file.py .

ls -ltr 
echo
echo python copy_and_cut_file.py "${@:2}"
     python copy_and_cut_file.py "${@:2}"
#xrdcp nameOfOutputFile.root root://cmseos.fnal.gov//store/user/username/nameOfOutputFile.root
echo
ls -ltr 

#echo "Removing original files." 
#xrdfs rm ${*}

echo "Setting out dir"
outdir=$1
echo $outdir


#xrdcp --force TRIGGER*.root root://cmseos.fnal.gov//store/user/mbellis/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD/180222_151710/0001//.
xrdcp --force TRIGGER*.root $outdir

### remove the output file if you don't want it automatically transferred when the job ends
#rm *.pkl
cd ${_CONDOR_SCRATCH_DIR}
rm -rf CMSSW_9_3_2

