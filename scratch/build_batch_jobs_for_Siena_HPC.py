import numpy as np
import subprocess as sp

import sys

###############################################################################
def write_output_file(infile, tag, batchfilename):

    output = ""
    output += "#!/bin/bash -l\n"
    output += "#$ -cwd\n"
    output += "#$ -V\n"
    output += "#$ -N bellis_%s\n" % (tag)
    output += "#$ -j y\n"
    output += "#$ -o bellis_$JOB_ID_%s.log\n"% (tag)
    output += "#$ -q sos.q\n"
    #output += "#$ -q allsmp.q\n"
    output += "\n"
    output += "# To run the simulation do from the command line:\n"
    output += "# qsub <thisfilename>\n"
    output += "\n"
    #output += "source /etc/profile.d/modules.sh\n"
    output += "\n"
    output += "module load Python3\n"
    output += "\n"
    output += "# REMINDER! This is all in bash\n"
    output += "\n"
    output += "date\n"
    output += "echo $SHELL\n"
    output += "\n"
    output += "pwd\n"
    output += "\n"
    output += "tag=\"%s\"\n" % (tag)
    output += "\n"
    #output += "outputfilename=$tag\"_\"$infile1_tag\"_\"$infile2_tag\"_ranges_\"$range1\"_\"$range2\".dat\"\n"
    output += "\n"
    #output += "echo \"outputfile: \" $outputfilename\n"
    output += "\n"
    output += "cd /home/mbellis//Top_BNV/scratch/ \n"
    output += "python dump_values_to_flat_files_UPROOT.py \\\n"
    output += "\t{0}\n".format(infile)
    output += "\n"
    output += "date \n"
    output += " \n"
    output += "echo \"Job $JOB_ID is complete.\" | sendmail mbellis@siena.edu \n"

    #print output

    outfile = open(batchfilename,'w')
    outfile.write(output)
    outfile.close()



################################################################################
# Main function
################################################################################
def main():

    infiles = sys.argv[1:]

    mastertag = "cms"

    for infile in infiles:

        infile_tag = infile.split('/')[-1].split(',root')[0]

        tag = "{0}_{1}".format(mastertag,infile_tag)

        batchfilename = "batch_%s.sh" % (tag)

        write_output_file(infile,tag,batchfilename)
        
        print(batchfilename)

        cmd = ['qsub', batchfilename]
        print(cmd)

        sp.Popen(cmd,0).wait()

################################################################################
################################################################################
if __name__=='__main__':
	main()
