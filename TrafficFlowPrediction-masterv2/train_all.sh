#!/bin/bash

echo "Running scripts..."

data_file='../Data/data/'
echo $data_file
for entry in `ls $data_file`; 
do python train.py --file_name=$entry
done