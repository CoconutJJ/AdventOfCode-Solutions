#!/bin/sh
for ((i=5;i<26;i++))
do
    dir=$1/"day${i}"
    mkdir $dir
    cp template.py $dir/"day${i}.py"
done