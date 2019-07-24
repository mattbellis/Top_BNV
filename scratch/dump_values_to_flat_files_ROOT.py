import numpy as np

import ROOT
import sys

################################################################################
def prepare_histogram_for_output(name,bin_vals,bin_edges,xlabel="x label",ylabel="y label"):

    output = "{0}\t".format(name)
    for i in bin_vals:
        output += "{0} ".format(i)
    output += "\n"
    output += "{0}\t".format(name)
    for i in bin_edges:
        output += "{0} ".format(i)
    output += "\n"
    output += "{0}\t".format(name)
    output += "{0}\n".format(xlabel)
    output += "{0}\t".format(name)
    output += "{0}\n".format(ylabel)

    return output

################################################################################
def main(infiles=None,outfilename=None):


    plotvars = {}
    plotvars["ncand"] = {"values":[], "weights":[], "xlabel":r"# candidates []", "ylabel":r"# entries","range":(0,100), "bins":100}
    plotvars["leadmupt"] = {"values":[], "weights":[], "xlabel":r"Leading $\mu$ $p_{\rm T}$ [GeV/c]", "ylabel":r"# entries","range":(0,400), "bins":400}
    plotvars["leadelectronpt"] = {"values":[], "weights":[], "xlabel":r"Leading $e$ $p_{\rm T}$ [GeV/c]", "ylabel":r"# entries","range":(0,400), "bins":400}
    plotvars["hadtopmass"] = {"values":[], "weights":[], "xlabel":r"Hadronic op candidate mass [GeV/c$^{\rm 2}$]", "ylabel":r"# entries","range":(0,800), "bins":800}
    plotvars["bnvtopmass"] = {"values":[], "weights":[], "xlabel":r"BNV top candidate mass [GeV/c$^{\rm 2}$]", "ylabel":r"# entries","range":(0,800), "bins":800}
    plotvars["Wmass"] = {"values":[], "weights":[], "xlabel":r"$W$ candidate mass [GeV/c$^{\rm 2}$]", "ylabel":r"# entries","range":(0,400), "bins":400}
    plotvars["metpt"] = {"values":[], "weights":[], "xlabel":r"$E_{T}^{\rm miss}$ [GeV]", "ylabel":r"# entries","range":(0,200), "bins":200}
    plotvars["pu_wt"] = {"values":[], "weights":[], "xlabel":r"Pileup weight []", "ylabel":r"# entries","range":(0,2), "bins":200}

    cuts = []
    ncuts = 5
    for n in range(ncuts):
        for key in plotvars.keys():
            plotvars[key]["values"].append([])
            plotvars[key]["weights"].append([])


    #filenames = sys.argv[1:]

    treename = "Tskim"
    t = ROOT.TChain(treename)

    for filename in sys.argv[1:]:
        t.AddFile(filename)


    leadmupt = []
    hadtopmass = []
    Wmass = []
    #ncand = []

    leadmupt_cut0 = []
    hadtopmass_cut0 = []
    Wmass_cut0 = []
    #ncand_cut0 = []

    leadmupt_cut1 = []
    hadtopmass_cut1 = []
    Wmass_cut1 = []
    #ncand_cut1 = []

    jetcsv = []
    njet = []
    #nbjet = []
    nmuon = []

    wts = []

    nentries = t.GetEntries()
    print("Nentries: {0}".format(nentries))


    for i in range(nentries):

        t.GetEntry(i)

        if i%100000==0:
            print("{0} out of {1} entries".format(i,nentries))

        if i>1000000000:
            break

        #print(data[b'nmuon'][i])

        ncand = t.ncand
        metpt = t.metpt
        leadmupt = t.leadmupt
        leadelectronpt = t.leadelectronpt
        bnvtopmass = t.bnvtopmass
        hadtopmass = t.hadtopmass
        Wmass = t.Wmass
        hadtopjet0idx = t.hadtopjet0idx
        hadtopjet1idx = t.hadtopjet1idx
        hadtopjet2idx = t.hadtopjet2idx
        jetpt = t.jetpt
        pu_wt = t.pu_wt

        wts.append(pu_wt)

        #for n in range(ncand):
        #hadtopmass = data[b'hadtopmass'][i]

        # Make some cuts and the like
        cut1 = leadmupt>25

        cuts = [1, cut1]

        for n in range(ncand):

            tbnvm = bnvtopmass[n]
            thm = hadtopmass[n]
            wm = Wmass[n]

            pt0 = jetpt[hadtopjet0idx[n]]
            pt1 = jetpt[hadtopjet1idx[n]]
            pt2 = jetpt[hadtopjet2idx[n]]

            cut2 = pt0>30 and pt1>30 and pt2>30
            cut3 = wm>70 and wm<95
            cuts = [1, cut1, cut1*cut2, cut1*cut2*cut3]

            for icut,cut in enumerate(cuts):
                if cut:
                    plotvars["bnvtopmass"]["values"][icut].append(tbnvm)
                    plotvars["bnvtopmass"]["weights"][icut].append(pu_wt)
                    plotvars["hadtopmass"]["values"][icut].append(thm)
                    plotvars["hadtopmass"]["weights"][icut].append(pu_wt)
                    plotvars["Wmass"]["values"][icut].append(wm)
                    plotvars["Wmass"]["weights"][icut].append(pu_wt)
                    plotvars["pu_wt"]["values"][icut].append(pu_wt)
                    plotvars["pu_wt"]["weights"][icut].append(pu_wt)


            ncuts = len(cuts)

        # Variables that don't depend on the above cuts
        for icut in range(ncuts):
            plotvars["ncand"]["values"][icut].append(ncand)
            plotvars["ncand"]["weights"][icut].append(pu_wt)
            plotvars["leadmupt"]["values"][icut].append(leadmupt)
            plotvars["leadmupt"]["weights"][icut].append(pu_wt)
            plotvars["leadelectronpt"]["values"][icut].append(leadelectronpt)
            plotvars["leadelectronpt"]["weights"][icut].append(pu_wt)
            plotvars["metpt"]["values"][icut].append(metpt)
            plotvars["metpt"]["weights"][icut].append(pu_wt)
        

    '''
    leadmupt = np.array(leadmupt)
    hadtopmass = np.array(hadtopmass)
    Wmass = np.array(Wmass)
    jetcsv = np.array(jetcsv)
    njet = np.array(njet)
    #nbjet = np.array(nbjet)
    ncand = np.array(ncand)
    nmuon = np.array(nmuon)
    '''


    if outfilename == None:
        outfilename = "/data/physics/bellis/CMS/HISTOGRAM_FILES_2019/{0}_HISTOGRAMS.txt".format(infiles[0].split('/')[-1].split('.')[0])
        #outfilename = "{0}_HISTOGRAMS.txt".format(infiles[0].split('/')[-1].split('.')[0])
        #outfilename = "TEST_HIST.txt"
    print(outfilename)
    #exit()
    outfile = open(outfilename,'w')

    output = ""
    for key in plotvars.keys():
        for n in range(ncuts):
            vals = plotvars[key]['values'][n]
            #print(vals)
            bins = plotvars[key]['bins']
            r = plotvars[key]['range']
            xlabel = plotvars[key]['xlabel']
            ylabel = plotvars[key]['ylabel']

            # With weights
            h,bin_edges = np.histogram(vals,bins=bins,range=r,weights=plotvars[key]['weights'][n])
            name = "{0}_WEIGHTS_cut{1}".format(key,n)
            print(name,bins,r)
            output += prepare_histogram_for_output(name,h,bin_edges,xlabel,ylabel)

            # With NO weights
            #h,bin_edges = np.histogram(vals,bins=bins,range=r)
            #name = "{0}_cut{1}".format(key,n)
            #print(name,bins,r)
            #output += prepare_histogram_for_output(name,h,bin_edges,xlabel,ylabel)


    '''
    h,bin_edges = np.histogram(leadmupt,bins=400,range=(0,400))
    output += prepare_histogram_for_output("leadmupt",h,bin_edges)

    h,bin_edges = np.histogram(hadtopmass,bins=400,range=(0,800))
    output += prepare_histogram_for_output("hadtopmass",h,bin_edges)

    h,bin_edges = np.histogram(Wmass,bins=400,range=(0,800))
    output += prepare_histogram_for_output("Wmass",h,bin_edges)

    h,bin_edges = np.histogram(jetcsv,bins=440,range=(-20,2))
    output += prepare_histogram_for_output("jetcsv",h,bin_edges)

    h,bin_edges = np.histogram(leadmupt_cut0,bins=400,range=(0,400))
    output += prepare_histogram_for_output("leadmupt_cut0",h,bin_edges)

    h,bin_edges = np.histogram(hadtopmass_cut0,bins=400,range=(0,800))
    output += prepare_histogram_for_output("hadtopmass_cut0",h,bin_edges)

    h,bin_edges = np.histogram(Wmass_cut0,bins=400,range=(0,800))
    output += prepare_histogram_for_output("Wmass_cut0",h,bin_edges)
    '''

    outfile.write(output)

    return 1


################################################################################
if __name__=="__main__":
    infiles = sys.argv[1:]
    main(infiles)
