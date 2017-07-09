import sys
import PSet
files = []
#outfile = file( 'filesToProcess_FOR_CRAB.txt', 'w')
#for ifile in PSet.process.source.fileNames :    
    #outfile.write( ifile + '\n' )
#outfile.close()

sys.argv.append('--input')
sys.argv.append('filesToProcess_FOR_CRAB_TTBAR_SMALL.txt')

sys.argv.append('--isCrabRun')

sys.argv.append('--trigProc')
sys.argv.append('HLT')

sys.argv.append('--disablePileup')

sys.argv.append('--output')
sys.argv.append('output_MC_CRAB.root')

sys.argv.append('--minMuonPt')
sys.argv.append('10')

sys.argv.append('--minElectronPt')
sys.argv.append('10')

sys.argv.append('--minAK4Pt')
sys.argv.append('20')

print sys.argv

from topbnv_fwlite import *

topbnv_fwlite(sys.argv)

