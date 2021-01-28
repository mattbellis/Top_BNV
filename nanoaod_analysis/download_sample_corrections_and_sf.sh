# download some sample correction sources
mkdir -p data
pushd data
PREFIX=https://raw.githubusercontent.com/CoffeaTeam/coffea/master/tests/samples
curl -Os $PREFIX/testSF2d.histo.root
curl -Os $PREFIX/testBTagSF.btag.csv
curl -Os $PREFIX/EIDISO_WH_out.histo.json
curl -Os $PREFIX/Fall17_17Nov2017_V32_MC_L2Relative_AK4PFPuppi.jec.txt
curl -Os $PREFIX/Fall17_17Nov2017_V32_MC_Uncertainty_AK4PFPuppi.junc.txt
curl -Os $PREFIX/DeepCSV_102XSF_V1.btag.csv.gz
#popd
