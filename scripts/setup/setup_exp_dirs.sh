#!/usr/bin/env bash
set -x
set -o errexit
set -o nounset

pushd /home/rvisbord/experiments/comb 
  
for sim in  M3.20.migAC_0_0   M3.25.migAC_0_0   M3.29.migAC_0_0 ; do 

  rm -rf ${sim}
  mkdir -p ${sim}
  pushd ${sim}

  for hyp in AB_C BC_A AC_B ; do 
   
    rm -rf ${hyp} 
    mkdir -p ${hyp};
    pushd ${hyp}

    # copy a ready-made control file and edit it
    old_control_file=${hyp}_control-file.ctl
    current_control_file=${sim}__${hyp}_control-file.ctl
    cp ../../M3.15.migAC_0_0/with_clade_and_mem_fix_without_assertions/${hyp}/${old_control_file} ${current_control_file}
    #sed -i -e "s/\/home\/igronau\/share\/sims\/simM3\/M3.15.migAC_0_0\/seqs.txt/ \/home\/rvisbord\/experiments\/comb\/${sim}\/seqs.txt /g" ./${hyp}_control-file.ctl;
    sed -i -e "s/M3.15.migAC_0_0/${sim}/g" ${current_control_file}

    # run gphocs
    nohup G-PhoCS ${current_control_file} &
    
    popd

  done;

  popd

done
popd
