#!/bin/bash

echo "Running scripts..."

for lag in $(seq 4 12);
do python train.py --lag=$lag
done