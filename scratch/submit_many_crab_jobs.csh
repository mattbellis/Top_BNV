set infile = $1
@ number = 38

while ( $number < 39 )

    set outfile = "TMP_"`basename $infile .py`"_"$number.py

    echo $outfile

    cat $infile | sed s/NUMBERTORUN/$number/ > $outfile

    crab submit -c $outfile

    @ number += 1

end
