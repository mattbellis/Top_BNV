foreach file(crab_projects/**)

    echo 
    echo "========================================"
    echo
    echo $file
    echo
    echo "========================================"

    echo 
    echo "---------- STATUS ---------"
    crab status $file
    echo 
    #echo "---------- REPORT ---------"
    #crab report $file
    #echo
    echo

end
