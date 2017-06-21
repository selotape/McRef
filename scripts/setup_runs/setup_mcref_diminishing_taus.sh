#!/usr/bin/env bash
# set -x
set -o errexit
set -o nounset

root=/home/rvisbord/dev/modelcompare/simulations/experiments/comb
mkdir -p ${root}
pushd ${root}
for sim in  M3.20.migAC_0_0   M3.25.migAC_0_0   M3.29.migAC_0_0 ; do 

  mkdir -p ${sim}
  pushd ${sim}

  for hyp in AB_C BC_A AC_B ; do 
   
    mkdir -p ${hyp};
    pushd ${hyp}

    gphocs_dir=/home/rvisbord/experiments/comb/${sim}/${hyp}
    cp ${gphocs_dir}/trace.tsv ./
    cp ${gphocs_dir}/comb-trace.tsv ./
    # cp ${gphocs_dir}/clade-trace.tsv ./

    # copy a ready-made config file and edit it
    cp ${root}/../preliminary_comb/M3.15.migAC_0_0/${hyp}/config.ini ./
    sed -i -e 's/1000000/25000/g' ./config.ini

    # run model_compare
    pushd /home/rvisbord/dev/modelcompare
    nohup python3 run_model_compare.py ${root}/${sim}/${hyp} &
    popd

 
    popd

  done;

  popd

done
popd
