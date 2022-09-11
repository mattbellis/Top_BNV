import sys
import json

infilename = sys.argv[1]
inyear = sys.argv[2]
indataset = sys.argv[3]

data = json.load(open(infilename))

print("------\n"+inyear+"\n-------\n")
print("------\n"+indataset+"\n-------\n")
datasets = data[inyear]

keys = datasets.keys()
sorted_keys = list(keys)
sorted_keys.sort()

#print(keys)

totalevents = 0
totalsize = 0
fulldatasetname = datasets[indataset]['dataset']
files = datasets[indataset]['files']
output = ""
for file in files:
    name = file['file'][0]['name']
    nevents = int(file['file'][0]['nevents'])
    size = float(file['file'][0]['size'])

    totalevents += nevents
    totalsize += size

    output += str(nevents) + "\t" + str(size) + "\t" + name + "\n"
    print(output)
    #print(name)

 # Prepend the full dataset info
#output = str(totalevents) + " " + str(totalsize) + " " + dataset + " " + fulldatasetname + "\n" + output
output = "\ndataset: " + "{0:10d}  {1}".format(totalevents, indataset) #+ " " + fulldatasetname
print(output)




