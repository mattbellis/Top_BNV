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

Various scripts to run over this. 

