#!/usr/bin/env bash
# set -x
set -o errexit
set -o nounset

root=/home/rvisbord/dev/modelcompare/simulations/experiments/comb
mkdir -p ${root}
pushd ${root}
for sim in  M3.15.migAC_0_4 ; do 

  mkdir -p ${sim}
  pushd ${sim}

  for hyp in AB_C__C-\>A AC_B__C-\>A BC_A__C-\>A ; do 
   
    mkdir -p ${hyp};
    pushd ${hyp}

    gphocs_dir=/home/rvisbord/experiments/comb/${sim}/${hyp}
#    cp ${gphocs_dir}/trace.tsv ./
#    cp ${gphocs_dir}/comb-trace.tsv ./
#    cp ${gphocs_dir}/clade-trace.tsv ./

    # copy a ready-made config file and edit it
#    cp ${root}/M3.20.migAC_0_0/AB_C/config.ini ./
#    sed -i -e 's/mig_bands =/mig_bands = C->A/g' ./config.ini

    # run model_compare
    pushd /home/rvisbord/dev/modelcompare
    nohup python3 run_model_compare.py ${root}/${sim}/${hyp} &
    popd

 
    popd

  done;

  popd

done
popd
