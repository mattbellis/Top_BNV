set infile = $1
@ number = 6 

while ( $number < 7 )

    set outfile = "TMP_"`basename $infile .py`"_"$number.py

    echo $outfile

    cat $infile | sed s/NUMBERTORUN/$number/ > $outfile

    crab submit -c $outfile

    @ number += 1

end
