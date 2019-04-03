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

This procedure will run ```topbnv_fwlite.py``` over all the data. 

Make sure there is a directory for the trigger for data (either **SingleMuon** or **SingleElectron**).
```
/store/user/mbellis/MC/SingleMuon

/store/user/mbellis/MC/SingleElectron
```


The files of interest to this next part are

```
submit_many_crab_jobs.csh
crab_submit_data.py
crab_submit_data_Electron.py

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

or 

```
csh submit_many_crab_jobs.csh crab_submit_data_Electron.py
```



### Skim the Monte Carlo

Make sure there is a directory for the trigger for data (either **SingleMuon** or **SingleElectron**).
```
/store/user/mbellis/MC/SingleMuon

/store/user/mbellis/MC/SingleElectron
```

The relevant files are

```
submit_many_crab_jobs.csh
crab_submit_MC.py

execute_for_crab.sh
execute_for_crab.py
```
To get the trigger right, you want to edit ```crab_submit_MC.py``` where it says 

```python
#request_name = "bellis_SingleElectron_%s" % (dataset[0])
request_name = "bellis_SingleMuon_%s" % (dataset[0])
```
and
```python
#config.Data.outLFNDirBase = '/store/user/%s/MC/SingleElectron' % (getUsernameFromSiteDB())
config.Data.outLFNDirBase = '/store/user/%s/MC/SingleMuon' % (getUsernameFromSiteDB())
```
Which is where it writes the output. 

You also need to edit ```execute_for_crab.py``` to check what trigger is set. 

```python
sys.argv.append('SingleMuon')
#sys.argv.append('SingleElectron')
```

### Checking on completion of grid jobs 

Can run the following script, passing in the directories in ```crab_projects``` that you want to check on. 

```
csh check_on_crab_jobs.csh crab_projects/crab_bellis_SingleElectron_*
```
The script can be modified to also produce the reports (see script) or resubmit failed jobs.  


# Step 2
## Run on LPC cluster with condor
```top_reconstruction_to_run_at_FNAL_over_grid_job_output.py```

Produces things like
* top candidate mass
* W candidate mass
* Highest muon pT

Start with ```build_lots_of_condor_scripts.py```. For example, to run over the SingleMuon *data*, do

```
python build_lots_of_condor_scripts.py ~/eos_store/SingleMuon
```

Before running, you should decide where you want the output to go. 
There's a line in ```build_lots_of_condor_scripts.py``` that you can edit to set this. 

```
outputdir = "/uscms/homes/m/mbellis/eos_store/CONDOR_output_files_Feb2019/{0}".format(topdir_lastname)
```

There is also a line that controls the number of files that each job will run over

```
files_at_a_time = 100
```

Before running, you should also make sure the following directories exist. They may wind up holding many files,
so I've created them under ```~/nobackup``` and soft-linked them to this directory. 

```
condor_scripts
condor_log_files
```

Calling the above will then call ```build_condor_script.py``` for each job so it's worth checking it out
to make sure it's doing what you want. 

Each condor job will call ```execute_python_on_condor.sh```. This file should be edited to match the same output
directory as in ```build_lots_of_condor_scripts.py```

```
echo xrdcp $2 root://cmseos.fnal.gov//store/user/mbellis/CONDOR_output_files_Feb2019/$subdir/.
     xrdcp $2 root://cmseos.fnal.gov//store/user/mbellis/CONDOR_output_files_Feb2019/$subdir/.
```

It is ```execute_python_on_condor.py``` that will call ```top_reconstruction_to_run_at_FNAL_over_grid_job_output.py```.

## Status

To check on the status of jobs, from the machine where they were submitted, run

```
condor_q
```

***Note***: There are some changes to condor as of Jan 2019 which are addressed [here](https://uscms.org/uscms_at_work/computing/setup/condor_refactor.shtml)



# Step 3

Copy the output from condor to Siena HPC


# Step 4

Various scripts to run over this. Can do this one of two different ways.

## Exploratory
These are scripts that just run over the files producing plots

## Massive cluster work on Siena's HPC

Produces text files of histogram entries. 

