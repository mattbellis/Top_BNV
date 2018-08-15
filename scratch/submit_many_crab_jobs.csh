set infile = $1
@ number = 3

while ( $number < 16 )

    set outfile = "TMP_"`basename $infile .py`"_"$number.py

    echo $outfile

    cat $infile | sed s/NUMBERTORUN/$number/ > $outfile

    crab submit $outfile

    @ number += 1

end
