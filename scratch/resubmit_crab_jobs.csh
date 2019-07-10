foreach file(crab_projects/MC/2016/**)

    echo 
    echo "========================================"
    echo
    echo $file
    echo
    echo "========================================"

    echo 
    echo "---------- RESUBMIT ---------"
    crab resubmit -d $file
    echo 
    echo

end
