import numpy as np
import sys

import topbnv_tools as tbt

import h5hep
import h5py as h5

filenames = sys.argv[1:]

for filename in filenames:
    print(filename)
    data = tbt.read_dictionary_file(filename)

    #print(data.keys())

    #datah5 = h5hep.initialize()
    outfile = filename.split('.pkl')[0] + ".h5"
    hdoutfile = h5.File(outfile,'w')

    keys = data.keys()

    for key in keys:

        x = data[key]
        #print(key,type(x))

        #create_dataset(datah5,['e','px','py','pz'],group='muons',dtype=float)

        dset = hdoutfile.create_dataset(key, \
                                data = x, \
                                compression='gzip', \
                                compression_opts=9)


    '''
    print(hdoutfile.keys())
    for key in hdoutfile.keys():
        print(key)
    '''
    hdoutfile.close()

    del data
    del hdoutfile






