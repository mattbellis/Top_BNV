import numpy as np
import sys

import topbnv_tools as tbt

filenames = sys.argv[1:]

data,tot_lumi = tbt.chain_pickle_files(filenames)




