#!/usr/bin/env bash
DIR=`dirname "$0"`
source "${DIR}/env.sh"

original_config_ini="${configs_dir}/ROOT_COMB_config.ini"


for div in "18" "24" "30" ; do
  for i in "1" "2" ; do
    for hyp in "AB_C_O" "A_BC_O" "AC_B_O"; do
      for seed in "${seed1}" "${seed2}" ; do

        data_set="M4.divAB_${div}-${i}"
        data_dir="${data_root}/${data_set}"
        results_dir="${data_dir}/results/${hyp}/seed_${seed}"

        cp "${original_config_ini}" "${results_dir}/config.ini"

      done
    done
  done
done