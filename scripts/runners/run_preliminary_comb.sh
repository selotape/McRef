#!/usr/bin/env bash
model_compare="python /home/rvisbord/dev/modelcompare/run_model_compare.py"

for exp in 'AB_C' 'BC_A' 'AC_B'; 
do 
    sim_dir="simulations/experiments/preliminary_comb/M3.15.migAC_0_0/${exp}"
    time nohup $model_compare ${sim_dir} &
    disown -a
done

