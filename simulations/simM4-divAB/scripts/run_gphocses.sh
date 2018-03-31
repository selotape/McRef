#!/usr/bin/env bash
DIR=`dirname "$0"`
source "${DIR}/env.sh"

echo "I'm disabled!" && exit

core=""

while test $# != 0
do
    case "$1" in
    --with-cpu-affinity) core=0;;
    esac
    shift
done


for div in "15" "21" "27" ; do
  for i in "1" "2" ; do
    data_set="M4.divAB_${div}-${i}"
    data_dir="${data_root}/${data_set}"

    for hyp in "AB_C_O" "A_BC_O" "AC_B_O"; do
      main_ctl="${ctl_dir}/${hyp}.ctl"
      for seed in "${seed1}" "${seed2}" ; do
        secondary_ctl="${data_dir}/${data_set}_${seed}.ctl"  
        results_dir="${data_dir}/results/${hyp}/seed_${seed}"
        rm -rf "${results_dir}"
        mkdir -p "${results_dir}"
        echo
        pushd "${results_dir}"
        
        if [ "${core}" ]; then
#          nohup taskset -c ${core} G-PhoCS ${main_ctl} ${secondary_ctl} &
          core=$((core+1))
        else 
#          nohup G-PhoCS ${main_ctl} ${secondary_ctl} &
        fi
        
        popd
      done
    done
  done
done

