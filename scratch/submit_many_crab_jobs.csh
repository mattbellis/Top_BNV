set infile = $1
@ number = 1

set trigger = "SingleMuon"
#set trigger = "SingleElectron"
#set trigger = "EGamma" # Use this for 2018

#set year = "2016"
#set year = "2017"
set year = "2018"

while ( $number < 48 )

    set outfile = "TMP_"`basename $infile .py`"_"$number$trigger$year.py

    echo $outfile

    cat $infile | sed s/NUMBERTORUN/$number/ | sed s/TRIGGERGOESHERE/$trigger/ | sed s/YEARGOESHERE/$year/ > $outfile

    crab submit -c $outfile

    @ number += 1

end
