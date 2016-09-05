#!/bin/bash
set -e
set -o nounset

oxfordDir='/home/rvisbord/dev/gphocs-dev/experiments/oxford'
mc3Dir='.'
mc3='python '$mc3Dir'/run_model_compare.py'

function action {
        TAU=$1
        M_AC=$2
        M_CA=$3

        simName=M3.$TAU.migAC_${M_AC}_${M_CA}

        exp_full_path=$oxfordDir/$simName

	run_mc3 $exp_full_path
}

function run_mc3 {
	expDir=$1
	$mc3 $expDir &
}


taus="01 05 10 15"
migs="1 2 4"
action 00 0 0
for tau in $taus
do
	action $tau 0 0
        for m in $migs
        do
                action $tau $m 0
                action $tau 0 $m
        done
done
wait
