import ROOT, sys
import topbnv_tools as tbt

MCinfo = tbt.csvtodict('MCinfo.csv')

print(MCinfo['DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD']['cross_section'])


#for i in range(len(MCinfo)):
    #print(MCinfo[i]['Tag'])
    #print(MCinfo[i]['cross_section'])
