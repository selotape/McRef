#!/usr/bin/env bash
model_compare="/home/rvisbord/dev/modelcompare"
model_compare_exe="python ${model_compare}/run_model_compare.py"
sim_root_dir="${model_compare}/simulations/experiments/preliminary_comb/M3.15.migAC_0_0/with_mem_fix"

for exp in 'AB_C' 'BC_A' 'AC_B'; 
do 
    sim_dir="${sim_root_dir}/${exp}"
    time nohup $model_compare_exe ${sim_dir} &
    disown -a
done

