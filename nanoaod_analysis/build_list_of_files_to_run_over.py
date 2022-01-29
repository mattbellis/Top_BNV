import subprocess
from sample_definitions import samples
import os

outfilename = "datasets_and_files.json"

my_env = os.environ.copy()

print("\n---------------------\n")

output = "{"

for iyear,year in enumerate(['2016', '2017','2018']):

    # Make sure we don't have a trailing comma at the end
    if iyear!=0: # Put a comma *before* the key
        output += ',"'+year+'\": {\n'
    else:
        output += '"'+year+'\": {\n'

        
    print("------ "+year+" ------\n")

    sorted_keys = list(samples['MC'].keys())
    sorted_keys.sort()
    ikey = 0
    #for key in sorted_keys[:5]:
    for key in sorted_keys[:]:
        if key in ['2016', '2017', '2018']:
            continue 

        s = samples['MC'][year][key]

        #output += '\"'+key+'\":"'+s+'",\n'
        # Do this to avoid a trailing comma at the end, otherwise it won't 
        # parse as JSON
        if ikey!=0:
            output += ","
        output += '"'+key+'\":{"dataset":"'+s+'",\n'

        # To list the dataset
        cmd = ['dasgoclient', '-dasmaps', './das_maps_dbs_prod.js',  '-query', 'file dataset='+s, '--json']

        process = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True,env=my_env).communicate()

        # To list the dataset
        print("here")
        print(process)
        print("\n")
        output += '"files":\n'
        output += process[0]
        # Get a list of all the json output
        #values = process[0].split('\n')[1:-3]

        '''
        output += '"files": [\n'
        for entry in values:
            print(entry)
            print("\n")
            # There is a comma at the end of each entry we want to remove
            output += entry[:-1]
            output += "\n"
        '''

        #output += "]\n"
        # Make sure I don't have a comma after the curly bracket. Otherwise it won't parse as JSON
        # because it is the last entry
        output += "}\n"
        ikey += 1

    output += "}\n"
output += "}\n"
           


#############################################################
outfile = open(outfilename,'w')
outfile.write(output)
outfile.close()
