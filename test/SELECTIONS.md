# Jets

Odd strucuture in CSV2 b-tagging variable at 0.55-ish is the result of low-momentum "jets" being created. This is referred to as 
*pileup jets*, though we're not sure why. They can be cut out by requiring the pT of the jets to be greater than 20 or 30 GeV/c.



Use "loose" jets
https://twiki.cern.ch/twiki/bin/view/CMS/JetID13TeVRun2016


Jet Energy Corrections
https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC


# Pile-up
Will need to use this type of file

https://github.com/cmsb2g/B2GDAS/blob/master/test/makepu_fwlite.py

to generate purw.root for pileup reweighting. 


