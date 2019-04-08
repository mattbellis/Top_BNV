import ROOT
import sys

def main():
    file1 = ROOT.TFile(sys.argv[1])
    file2 = ROOT.TFile(sys.argv[2])

    file1.ls()
    file2.ls()

    h1 = file1.Get("pileup")
    h2 = file2.Get("pileup")
    h3 = h1.Clone("h3")


    c1 = ROOT.TCanvas("c1","c1",900,300)
    c1.Divide(3,1)
    c1.cd(1)
    h1.Draw()
    ROOT.gPad.Update()

    c1.cd(2)
    h2.Draw()
    ROOT.gPad.Update()


    h3.Sumw2()
    h3.Scale(1.0 / h3.Integral() )
    h2.Sumw2()
    h2.Scale(1.0 / h2.Integral() )

    h3.Divide(h2)

    c1.cd(3)
    h3.Draw()
    ROOT.gPad.Update()

    #f3.cd()
    #h1.Write()
    #f3.Close()

    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = raw_input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]


if __name__ == "__main__":
    main()
