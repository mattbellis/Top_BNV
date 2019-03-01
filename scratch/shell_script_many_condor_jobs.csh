foreach dir(~/eos_store/SingleMuon ~/eos_store/SingleElectron ~/eos_store/MC/SingleMuon/* ~/eos_store/MC/SingleElectron/* )
    python build_lots_of_condor_scripts.py $dir
end
