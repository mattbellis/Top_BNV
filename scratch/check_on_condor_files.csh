set topdir = '/store/user/mbellis/CONDOR_output_files_2019'

set infile = $1

set v = `cat $infile`

set i = 1
while ( $i < = $#v )
    #echo $v[$i]
    set filename_to_check = $topdir"/"$v[$i]
    #echo $filename_to_check
    #eosls -l $filename_to_check
    set bytes = `eosls -l $filename_to_check | awk '{print $5}'`
    #echo $bytes
    if ( `echo $bytes | egrep '[:alpha:]|[:cntrl:]|[:graph:]|[:punct:]'` ) then
        # variable's not numeric 
        echo "Variable $bytes is NOT numeric"
        echo $filename_to_check
        #else
        #1
        # It's numeric (or null, you'll need to test for that too)
        #echo "Variable $bytes is numeric."
    endif
    @ i = $i + 1
    #echo $i
end

