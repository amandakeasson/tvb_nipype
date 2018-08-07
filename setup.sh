#!/bin/bash

conda create -n tvbenv python=2
source activate tvbenv
conda install jupyter
pip install Cython
pip install -U tvb-library

mkdir -p input
mkdir -p output

