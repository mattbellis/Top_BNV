# Producing lists of datasets and files

Create a dictionary of datasets and shorter names in 
```
 sample_definitions.py
```
There are some examples of how to use this file and pass the arguments
to `dasgoclient` in a python script, such that you can manipulate the 
output in python.
```
test_sample_definitions.py
```

Run the following to build a JSON file of the datasets and the files
in those datasets. 
```
build_list_of_files_to_run_over.py
```
This JSON file is pretty big (around 10 Mb) because it contains much of
the output from the `dasgoclient` data dump. The name of the file
it produces is `datasets_and_files.json`.

To dump a summary of these datasets and files, with total events in each 
dataset, run
```
python build_summary_list_of_datasets_and_files.py datasets_and_files.json
```


