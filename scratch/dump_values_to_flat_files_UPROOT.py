import numpy as np

import uproot
import sys

################################################################################
def prepare_histogram_for_output(name,bin_vals,bin_edges):

    output = "{0}\t".format(name)
    for i in bin_vals:
        output += "{0} ".format(i)
    output += "\n"
    output += "{0}\t".format(name)
    for i in bin_edges:
        output += "{0} ".format(i)
    output += "\n"

    return output

################################################################################
def main(infiles=None,outfilename=None):

    #filenames = sys.argv[1:]

    treename = "Tskim"

    leadmupt = []
    topmass = []
    Wmass = []
    ntop = []

    leadmupt_cut0 = []
    topmass_cut0 = []
    Wmass_cut0 = []
    ntop_cut0 = []

    leadmupt_cut1 = []
    topmass_cut1 = []
    Wmass_cut1 = []
    ntop_cut1 = []

    jetcsv = []
    njet = []
    nbjet = []
    nmuon = []

    for infile in infiles:

        tree = uproot.open(infile)[treename]

        nentries = tree.numentries
        print(nentries)

        print(tree.keys())
        print(tree.array('nmuon'))

        data = tree.arrays(["nmuon", "leadmupt", "ntop","topmass","nW","Wmass","nbjet","njet","jetcsv"])
                           
        print(type(data))

        print(data)

        for i in range(nentries):

            #t.GetEntry(i)

            if i%100000==0:
                print("{0} out of {1} entries".format(i,nentries))

            if i>10000000:
                break

            #print(data[b'nmuon'][i])

            nmuon.append(data[b'nmuon'][i])
            leadmupt.append(data[b'leadmupt'][i])
            
            lmupt = data[b'leadmupt'][i]
            if lmupt>25:
                leadmupt_cut0.append(lmupt)

            ntop.append(data[b'ntop'][i])
            for n in range(data[b'ntop'][i]):
                topmass.append(data[b'topmass'][i][n])
                if lmupt>25:
                    topmass_cut0.append(data[b'topmass'][i][n])

            for n in range(data[b'nW'][i]):
                wm = data[b'Wmass'][i][n]
                Wmass.append(wm)
                if lmupt>25:
                    Wmass_cut0.append(wm)

            nbjet.append(data[b'nbjet'][i])

            njet.append(data[b'njet'][i])
            for n in range(data[b'njet'][i]):
                jetcsv.append(data[b'jetcsv'][i][n])

    leadmupt = np.array(leadmupt)
    topmass = np.array(topmass)
    Wmass = np.array(Wmass)
    jetcsv = np.array(jetcsv)
    njet = np.array(njet)
    nbjet = np.array(nbjet)
    ntop = np.array(ntop)
    nmuon = np.array(nmuon)


    if outfilename == None:
        outfilename = "/data/physics/bellis/CMS/HISTOGRAM_FILES/{0}_HISTOGRAMS.txt".format(infiles[0].split('/')[-1].split('.')[0])
    print(outfilename)
    #exit()
    outfile = open(outfilename,'w')

    output = ""
    h,bin_edges = np.histogram(leadmupt,bins=400,range=(0,400))
    output += prepare_histogram_for_output("leadmupt",h,bin_edges)

    h,bin_edges = np.histogram(topmass,bins=400,range=(0,800))
    output += prepare_histogram_for_output("topmass",h,bin_edges)

    h,bin_edges = np.histogram(Wmass,bins=400,range=(0,800))
    output += prepare_histogram_for_output("Wmass",h,bin_edges)

    h,bin_edges = np.histogram(jetcsv,bins=440,range=(-20,2))
    output += prepare_histogram_for_output("jetcsv",h,bin_edges)

    h,bin_edges = np.histogram(leadmupt_cut0,bins=400,range=(0,400))
    output += prepare_histogram_for_output("leadmupt_cut0",h,bin_edges)

    h,bin_edges = np.histogram(topmass_cut0,bins=400,range=(0,800))
    output += prepare_histogram_for_output("topmass_cut0",h,bin_edges)

    h,bin_edges = np.histogram(Wmass_cut0,bins=400,range=(0,800))
    output += prepare_histogram_for_output("Wmass_cut0",h,bin_edges)

    outfile.write(output)
    
    return 1


################################################################################
if __name__=="__main__":
    infiles = sys.argv[1:]
    main(infiles)
