import sys
import pickle as pkl

infilename = sys.argv[1]

dataset = pkl.load(open(infilename,'rb'))

print(dataset)

for i,d in enumerate(dataset):
    print(i,d)
    print(dataset[d])
