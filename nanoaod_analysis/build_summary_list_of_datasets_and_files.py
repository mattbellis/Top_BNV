import sys
import json

infilename = sys.argv[1]

data = json.load(open(infilename))

for year in ['2016', '2017', '2018']:

    print("------\n"+year+"\n-------\n")
    datasets = data[year]

    keys = datasets.keys()
    sorted_keys = list(keys)
    sorted_keys.sort()

    #print(keys)

    for dataset in sorted_keys:
        totalevents = 0
        totalsize = 0
        fulldatasetname = datasets[dataset]['dataset']
        files = datasets[dataset]['files']
        output = ""
        for file in files:
            name = file['file'][0]['name']
            nevents = int(file['file'][0]['nevents'])
            size = float(file['file'][0]['size'])

            totalevents += nevents
            totalsize += size

            output += str(nevents) + "\t" + str(size) + "\t" + name + "\n"

         # Prepend the full dataset info
        #output = str(totalevents) + " " + str(totalsize) + " " + dataset + " " + fulldatasetname + "\n" + output
        output = "dataset: " + "{0:10d}  {1}".format(totalevents, dataset) #+ " " + fulldatasetname
        print(output)



    
