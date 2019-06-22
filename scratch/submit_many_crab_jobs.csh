set infile = $1
@ number = 4 

set trigger = "SingleMuon"
#set trigger = "SingleElectron"

set year = "2016"
#set year = "2017"
#set year = "2018"

while ( $number < 5 )

    set outfile = "TMP_"`basename $infile .py`"_"$number.py

    echo $outfile

    cat $infile | sed s/NUMBERTORUN/$number/ | sed s/TRIGGERGOESHERE/$trigger/ | sed s/YEARGOESHERE/$year/ > $outfile

    crab submit -c $outfile

    @ number += 1

end
