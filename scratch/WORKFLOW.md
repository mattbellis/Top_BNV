# Step 1
## Crab jobs
```topbnv_fwlite.py```
Filters out basic information about 
* jets (AK4)
* muons
* electrons
* MET
* Pileup information (weighting)

**crab files used**

Check out this code!

```
sh myscript_that_is_one_line_whatever.sh
```

### Skim the data

This will run ```topbnv_fwlite.py``` over all the data. 

Make sure there is a directory for the trigger for data.
```
/uscms/homes/m/mbellis/CMSSW_8_0_26/src/Analysis/Top_BNV/scratch/SingleMuon

/uscms/homes/m/mbellis/CMSSW_8_0_26/src/Analysis/Top_BNV/scratch/SingleMuon

```
The files of interest to this next part are

```
submit_many_crab_jobs.csh
crab_submit_data.py

execute_for_crab_data.sh
execute_for_crab_data.py
```

As of now, the file ```crab_submit_data.py``` has the trigger hard coded in the dataset name. For example

```
/SingleMuon/Run2016B-03Feb2017_ver2-v2/MINIAOD
```

You want to edit ```submit_many_crab_jobs.csh``` so that it starts and ends with whichever
datasets in ```crab_submit-data.py``` you want to submit. 

Make sure that in the ```crab_project``` subdirectory, there are no directories
with the same naming as what we're about to do. 

Then you can run

```
csh submit_many_crab_jobs.csh crab_submit_data.py
```





# Step 2
## Run on LPC cluster with condor
```top_reconstruction_to_run_at_FNAL_over_grid_job_output.py```

Produces things like
* top candidate mass
* W candidate mass
* Highest muon pT

# Step 3

Copy the output from condor to Siena HPC


# Step 4

Various scripts to run over this. Can do this one of two different ways.

## Exploratory
These are scripts that just run over the files producing plots

## Massive cluster work on Siena's HPC

Produces text files of histogram entries. 

