#!/usr/bin/env bash
#                          year trigger
# The crab script will pass these in as year=2016, so we need to do
# some manipulation. 
#
# Also the first command-line input is the job number
#
year=`echo $2 | awk -F"=" '{print $2}'`
trigger=`echo $3 | awk -F"=" '{print $2}'`

echo "In execute_for_crab.sh...."
echo $year
echo $trigger

python execute_for_crab_data.py --year $year --trigType $trigger


#python execute_for_crab_data.py
