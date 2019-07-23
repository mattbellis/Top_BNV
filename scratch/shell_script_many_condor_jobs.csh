#foreach dir(~/eos_store/SingleMuon ~/eos_store/SingleElectron ~/eos_store/MC/SingleMuon/* ~/eos_store/MC/SingleElectron/* )
    #foreach dir(~/eos_store/SingleElectron)
    #foreach dir(~/eos_store/MC/SingleMuon/WZ* )
    foreach dir(~/eos_store/MC/SingleMuon/TTG* )
    python build_lots_of_condor_scripts.py $dir
end
