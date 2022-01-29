#!/bin/bash
set -x
# Sleep
sleep $1
echo "##### HOST DETAILS #####"
echo "I slept for $1 seconds on:"
hostname
date
