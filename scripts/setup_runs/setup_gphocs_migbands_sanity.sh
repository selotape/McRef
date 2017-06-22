#!/usr/bin/env bash
set -o errexit
set -o nounset

root=/home/rvisbord/experiments/comb_with_migs
mkdir -p ${root}
pushd ${root}
  
for sim in  M3.05.migAC_0_1  M3.05.migAC_0_2  M3.05.migAC_0_4  M3.10.migAC_0_1  M3.10.migAC_0_2  M3.10.migAC_0_4  M3.15.migAC_0_1  M3.15.migAC_0_2  M3.15.migAC_0_4 ; do

  rm -rf ${sim}
  mkdir -p ${sim}
  pushd ${sim}

  for hyp in AB_C BC_A AC_B ; do 

    mig_hyp="${hyp}__C->A"
    rm -rf ${mig_hyp}
    mkdir -p ${mig_hyp};
    pushd ${mig_hyp}

    # copy a ready-made control file and edit it
    old_control_file=/home/rvisbord/experiments/comb/M3.15.migAC_0_4/${mig_hyp}/control-file.ctl
    control_file=${sim}__${mig_hyp}_control-file.ctl
    cp ${old_control_file} ./${control_file}
    sed -i -e "s/M3.15.migAC_0_4/${sim}/g" ${control_file}

    # run gphocs
    echo "nohup G-PhoCS ${control_file} &"
          nohup G-PhoCS ${control_file} &
    
    popd


  done

  popd

done
popd
