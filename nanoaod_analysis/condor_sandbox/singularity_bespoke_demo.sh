#!/usr/bin/env bash

echo "Untarring the virtual environment"
# Do this *not* verbose
tar -zxf myenv.tgz
echo

echo "Activating our virtual environment"
source myenv/bin/activate
echo

echo "Running our python example!"
python singularity_bespoke_demo.py 
echo

echo "All done!"

