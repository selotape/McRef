#!/usr/bin/env bash
DIR=`dirname "$0"`
source "${DIR}/env.sh"

mcref_install_dir="/home/ron/Dropbox/Thesis/ModelCompare/"

sims=""

for div in "18" ; do # "24" "30"
  for i in "1" ; do #  "2"
    for hyp in "AB_C_O" ; do # "A_BC_O" "AC_B_O"
      for seed in "${seed1}" ; do # "${seed2}"

        data_set="M4.divAB_${div}-${i}"
        data_dir="${data_root}/${data_set}"
        results_dir="${data_dir}/results/${hyp}/seed_${seed}"
        sims="${sims} ${results_dir}"
      done
    done
  done
done

pushd ${mcref_install_dir}
set +u && source "${python_venv}/bin/activate"
python mcref ${sims}
set -u && deactivate
popd