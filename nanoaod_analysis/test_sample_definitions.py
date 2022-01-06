import subprocess
from sample_definitions import samples
import os

my_env = os.environ.copy()
#my_env["PATH"] = "/usr/sbin:/sbin:" + my_env["PATH"]

# Use subrocess.run for python>3.5
# Use subrocess.Popen for python<2.8
'''
process = subprocess.Popen(['dasgoclient', '--help'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True).communicate()

print("here")
print(process)
print("\n")
for p in process:
    print(p)
    print("\n")
'''

print("\n---------------------\n")

for key in samples['MC'].keys():
    if key in ['2016', '2017', '2018']:
        continue 


    s = samples['MC']['2018'][key]
    print(s)
    #cmd = ['dasgoclient', '-dasmaps', './das_maps_dbs_prod.js',  '--query="dataset='+s+'"', '--format', 'plain']

    # To list the dataset
    #cmd = ['dasgoclient', '-dasmaps', './das_maps_dbs_prod.js',  '--query="dataset='+s.replace('/NANOAOD','*/NANOAOD')+'"', '--format', 'plain']
    #cmd = ['dasgoclient', '-dasmaps', './das_maps_dbs_prod.js',  '--query="dataset='+s+'"', '--format', 'plain']

    # To list the dataset
    cmd = ['dasgoclient', '-dasmaps', './das_maps_dbs_prod.js',  '-query', 'file dataset='+s, '--format', 'plain', '--verbose', '0']

    # To count the events
    #cmd = ['dasgoclient', '-dasmaps', './das_maps_dbs_prod.js',  '--query="file' , 'dataset='+s, '|', 'sum(file.nevents)"']

    # To test
    #cmd = ['dasgoclient', '-dasmaps', './das_maps_dbs_prod.js',  '--help']

    #process = subprocess.Popen(['eval', '`scramv1', 'runtime', '-sh`'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True).communicate()
    print('\n')

    process = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True,env=my_env).communicate()
    #subprocess.Popen(my_command, env=my_env)
    print(process)
    print(process[0])
    '''
    for p in process:
        print(p)
    '''

    output = " ".join(cmd)
    print(output)
    print(cmd)
    #cmd = ['dasgoclient', '--help']
