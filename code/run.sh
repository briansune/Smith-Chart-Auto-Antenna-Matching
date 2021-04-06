#!/usr/bin/env sh

source /c/Anaconda/etc/profile.d/conda.sh

conda activate py3p8_test

conda env list

python ./main.py
