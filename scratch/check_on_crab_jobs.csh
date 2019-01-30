#foreach file(crab_projects/*)
foreach file($*)

    echo 
    echo "========================================"
    echo $file
    echo "---------- STATUS ---------"
    crab status $file
    #echo "---------- RESUBMIT ---------"
    #crab resubmit $file
    #echo 
    #echo "---------- REPORT ---------"
    #crab report $file
    #echo
    echo

end
