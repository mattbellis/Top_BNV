import sys
import PSet
files = []
outfile = file( 'files_to_process.txt', 'w')
for ifile in PSet.process.source.fileNames :    
    outfile.write( ifile + '\n' )
outfile.close()

sys.argv.append('--input')
sys.argv.append('files_to_process.txt')

sys.argv.append('--isCrabRun')

#sys.argv.append('--trigType')
#sys.argv.append('SingleMuon')

print sys.argv

from topbnv_fwlite import *

topbnv_fwlite(sys.argv)

