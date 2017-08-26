#!/usr/bin/env bash

cd ~/dev/modelcompare
rm nohup.out

for sim in migAC_1 migAC_0
do
    echo "=== ${sim} ==="
    for hyp in AB_C_migal AB_C_nomig AB_C_migCA BC_A_nomig BC_A_migal AC_B_migal AC_B_nomig
    do
        vim ~/experiments/post_france/M3.15/${sim}/${hyp}/config.ini
        nohup python ./run_model_compare.py ~/experiments/post_france/M3.15/${sim}/${hyp} &
    done


    for job in `jobs -p`
    do
    echo ${job}
        wait ${job}
    done
    echo; echo; echo; echo
done
