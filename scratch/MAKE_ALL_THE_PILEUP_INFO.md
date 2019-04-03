# Pileup

Getting most of this from here.

https://twiki.cern.ch/twiki/bin/view/CMS/PileupJSONFileforData#2015_Pileup_JSON_Files

as well as from the B2GDAS examples.

# Data 

* Copy over the lumi mask file used to process the data as well as the latest pileup file from CERN.

```
sh copy_over_pileup_files_from_CERN.sh
```

* Generate the ROOT file with a single histogram (pileup) of the # of interactions distribution.

```
sh make_puhists_for_data.sh
```

# MC

* This is overkill, but good for sanity checks. First make text files with lists of files of our MC samples.

```
csh get_lists_of_MC_files_for_pileup.csh
```

* Now we can process them all, though in reality we only need one of them. 

```
csh make_puhists_for_MC.csh
```

* We'll use one of them for our reweighting file.

```
python makepuhist.py --file_data pudata_2016.root --file_mc pumc_TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root --file_out purw.root
```

# Reweighting

Added code to pull the reweighting for the number of interactions out of purw.root and put it in the ROOT tree.
