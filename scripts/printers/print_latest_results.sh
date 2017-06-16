#!/usr/bin/env bash


function print_latest_results {
    dir=$1
    if [ -d "${dir}" ]; then
        last_experiment=(`ls -l "${dir}/results" | awk '{print $9}' | sort -r | head -n 1`)
        last_summary_path="$dir/results/$last_experiment/summary.txt"
        cat "$last_summary_path"
    fi
}


for dir in `ls $1`; 
do 
    print_latest_results "$1/$dir";
done;

