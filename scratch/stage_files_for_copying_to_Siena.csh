# 2016
# python copyfiles.py T3_US_FNALLPC CONDOR_output_files_2019/MC/2016/SingleElectron local /uscms_data/d1/mbellis/CONDOR_output_files_2019/MC/2016/SingleElectron -p xrootd --depth 10
# python copyfiles.py T3_US_FNALLPC CONDOR_output_files_2019/MC/2016/SingleMuon local /uscms_data/d1/mbellis/CONDOR_output_files_2019/MC/2016/SingleMuon -p xrootd --depth 10
#
# python copyfiles.py T3_US_FNALLPC CONDOR_output_files_2019/Data/2016/SingleElectron local /uscms_data/d1/mbellis/CONDOR_output_files_2019/Data/2016/SingleElectron -p xrootd --depth 10
# python copyfiles.py T3_US_FNALLPC CONDOR_output_files_2019/Data/2016/SingleMuon local /uscms_data/d1/mbellis/CONDOR_output_files_2019/Data/2016/SingleMuon -p xrootd --depth 10
#
# # 2017
# python copyfiles.py T3_US_FNALLPC CONDOR_output_files_2019/MC/2017/SingleElectron local /uscms_data/d1/mbellis/CONDOR_output_files_2019/MC/2017/SingleElectron -p xrootd --depth 10
# python copyfiles.py T3_US_FNALLPC CONDOR_output_files_2019/MC/2017/SingleMuon local /uscms_data/d1/mbellis/CONDOR_output_files_2019/MC/2017/SingleMuon -p xrootd --depth 10
#

#set dataMC = 'Data'
set dataMC = 'MC'

#set year = '2016'
set year = '2017'
#set year = '2018'

set trigger = 'SingleMuon'
#set trigger = 'SingleElectron'
#set trigger = 'EGamma'

echo "Will be copying files to "
echo "/uscms_data/d1/mbellis/CONDOR_output_files_2019/$dataMC/$year/$trigger"
echo 
echo 'Is this OK?'
#exit()

set files = `eosls /store/user/mbellis/CONDOR_output_files_2019/$dataMC/$year/$trigger`

foreach file ( $files )

    echo $file
    set first_char = `echo $file | awk '{print substr($1,1,1)}'`
    echo $first_char

    if ( $first_char == 'T' ) then
    #if ( $first_char != 'T' ) then

        echo python copyfiles.py T3_US_FNALLPC CONDOR_output_files_2019/$dataMC/$year/$trigger/$file local /uscms_data/d1/mbellis/CONDOR_output_files_2019/$dataMC/$year/$trigger/$file -p xrootd --depth 10
             python copyfiles.py T3_US_FNALLPC CONDOR_output_files_2019/$dataMC/$year/$trigger/$file local /uscms_data/d1/mbellis/CONDOR_output_files_2019/$dataMC/$year/$trigger/$file -p xrootd --depth 10

    endif


end


