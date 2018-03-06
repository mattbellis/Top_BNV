import ROOT, sys
import topbnv_tools as tbt

MCinfo = tbt.csvtodict('MCinfo.csv')

for i in range(len(MCinfo)):
    print(MCinfo[i]['Tag'])
    print(MCinfo[i]['cross_section'])
