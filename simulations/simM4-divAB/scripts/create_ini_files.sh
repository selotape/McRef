#!/usr/bin/env bash
DIR=`dirname "$0"`
source "${DIR}/env.sh"

for div in  "15" "18" "21" "24" "27" "30" ; do 
  for i in "1" "2" ; do
    data_set="M4.divAB_${div}-${i}"
    data_dir="${data_root}/${data_set}"
    pushd "${data_dir}"
    for seed in "${seed1}" "${seed2}" ; do
      new_ctl="${data_set}_${seed}.ctl"
      cp ${template_ctl} ${new_ctl}
      sed -i "s/RANDOM_SEED/${seed}/g" ${new_ctl}
      sed -i "s/DATA_SET/${data_set}/g" ${new_ctl}
    done
    popd
  done 
done


#while test $# != 0
#do
#    case "$1" in
#    -p) echo "Purging old control files."
#        rm ./M4.divAB* ;;
#    esac
#    shift
#done
