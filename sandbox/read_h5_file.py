import numpy as np
import sys

import topbnv_tools as tbt

import h5hep
import h5py as h5

filenames = sys.argv[1:]

for filename in filenames:
    f = h5.File(filename,'r+')

    keys = f.keys()

    print(keys)
    for key in keys:
        x = f[key]
        print(key,type(x),len(x))

    '''
    #datah5 = h5hep.initialize()
    outfile = filename.split('.pkl')[0] + ".h5"
    hdoutfile = h5.File(outfile,'w')

    keys = data.keys()

    for key in keys:

        x = data[key]

        #create_dataset(datah5,['e','px','py','pz'],group='muons',dtype=float)

        dset = hdoutfile.create_dataset(key, \
                                data = x, \
                                compression='gzip', \
                                compression_opts=9)


    '''
    f.close()






