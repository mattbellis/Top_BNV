# Top_BNV
CMS analysis tools for searches for baryon-number violating decays of the top quark. 


# The first time you are checking out/cloning this directory
*Taken from B2GDAS...*


To run :

`export SCRAM_ARCH=slc6_amd64_gcc530` *if using BASH*

`setenv SCRAM_ARCH slc6_amd64_gcc530` *if using TCSH*

`cmsrel CMSSW_8_0_20`

`cd CMSSW_8_0_20/src`

`git clone https://github.com/mattbellis/Top_BNV.git Analysis/Top_BNV`

`cd Analysis/B2GDAS`

`scram b -j 10`

`cd test`

`voms-proxy-init`

`python b2gdas_fwlite.py --input=inputfiles/rsgluon_ttbar_2TeV.txt --output=rsgluon_ttbar_2TeV.root --maxevents 10000 --trigProc=HLT2`
