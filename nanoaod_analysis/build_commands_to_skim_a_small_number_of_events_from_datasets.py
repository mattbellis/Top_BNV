import subprocess
from sample_definitions import samples
import os

my_env = os.environ.copy()

print("\n---------------------\n")

for year in ['2016', '2017','2018']:
        
    print("------ "+year+" ------\n")

    sorted_keys = list(samples['MC'].keys())
    sorted_keys.sort()
    for key in sorted_keys:
        if key in ['2016', '2017', '2018']:
            continue 

        s = samples['MC'][year][key]

        # To list the dataset
        cmd = ['dasgoclient', '-dasmaps', './das_maps_dbs_prod.js',  '-query', 'file dataset='+s, '--format', 'plain', '--verbose', '0']

        process = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True,env=my_env).communicate()

        # To list the dataset
        #print(process)
        files = process[0].split('\n')

        command = "python skim_nanoaod_file_and_write_to_eos.py "+key+" "+year+" "+files[0]
        #print(len(files),files[0])
        print(command)
