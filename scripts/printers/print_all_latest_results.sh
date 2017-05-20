#!/usr/bin/env bash


function print_latest_results {
    dir=$1
    last_experiment=(`ls -l "$dir/results" | awk '{print $9}' | sort -r | head -n 1`)
    last_summary_path="$dir/results/$last_experiment/summary.txt"
    cat "$last_summary_path"
}


for dir in `ls`; 
do 
    print_latest_results $dir;
done;

