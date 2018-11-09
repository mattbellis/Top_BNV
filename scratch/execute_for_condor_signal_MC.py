import sys
import PSet
files = []
#outfile = file( 'files_to_process_TEMP.txt', 'w')
#outfile = file( 'files_to_process.txt', 'w')
#print(type(outfile))
#print("TESTING THE INFILES -------------------------------")
#for ifile in PSet.process.source.fileNames:    
   #outfile.write( ifile + '\n' )
   #print(ifile)
#outfile.close()

sys.argv.append('--input')
sys.argv.append('files_to_process.txt')

print("TESTING THE FILE TO PROCESS ------------------------------------")
for line in file('files_to_process.txt','r'):
    print(line)

sys.argv.append('--localInputFiles')

sys.argv.append('--isMC')

sys.argv.append('--trigType')
sys.argv.append('SingleMuon')

#sys.argv.append('--output')
#sys.argv.append('output_MC_TESTING.root')

print sys.argv

from topbnv_fwlite import *

topbnv_fwlite(sys.argv)

