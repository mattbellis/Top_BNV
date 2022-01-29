#!/usr/bin/env bash

#python coffea_EXAMPLE_1.py $1
#pip install hepfile

echo "Here"
echo $SHELL
echo "Here A"
bash
echo "HereBA"
echo $SHELL
echo "Here C"
echo $SHELL
tar -zxvf myenv.tgz
#python -m venv --without-pip --system-site-packages myenv
source myenv/bin/activate
#unlink myenv/lib64 
echo "A"
which python
echo "B"
python coffea_EXAMPLE_1.py 
