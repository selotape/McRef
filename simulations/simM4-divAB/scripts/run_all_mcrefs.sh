#!/usr/bin/env bash
DIR=`dirname "$0"`
source "${DIR}/env.sh"
set +u && source "${python_venv}/bin/activate"

mcref_install_dir="/home/ron/Dropbox/Thesis/ModelCompare/"
pushd ${mcref_install_dir}

sims=""
for div in "18" "24" "30" ; do #
  for i in "1" "2" ; do #
    for hyp in "AB_C_O" "A_BC_O" "AC_B_O" ; do #
      for seed in "${seed1}" "${seed2}" ; do #

        data_set="M4.divAB_${div}-${i}"
        data_dir="${data_root}/${data_set}"
        results_dir="${data_dir}/results/${hyp}/seed_${seed}"
        sims="${sims} ${results_dir}"

      done
    done
  done
done


for ref in "ABC_COMB" "ROOT_COMB" "ABC_CLADE" "ROOT_CLADE"; do
  
  original_config_ini="${configs_dir}/${ref}_config.ini"
  export original_config_ini
  "${DIR}/create_some_config_ini_files.sh"

  echo "=== Running McRef with ${ref} reference model ==="
  python mcref "$@" ${sims}

done

set -u && deactivate
popd