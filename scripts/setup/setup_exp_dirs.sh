#!/usr/bin/env bash
set -x
set -o errexit
set -o nounset

pushd /home/rvisbord/experiments/comb 
  
for sim in  M3.20.migAC_0_0   M3.25.migAC_0_0   M3.29.migAC_0_0 ; do 

  rm -rf ${sim}
  mkdir -p ${sim}
  pushd ${sim}

  cp /home/igronau/share/sims/simM3/${sim}/seqs.txt.gz ./
  gunzip ./seqs.txt.gz

  for hyp in AB_C BC_A AC_B ; do 
   
    rm -rf ${hyp} 
    mkdir -p ${hyp};
    pushd ${hyp}

    cp ../../M3.15.migAC_0_0/with_clade_and_mem_fix_without_assertions/${hyp}/${hyp}_control-file.ctl ./
    sed -i -e "s/\/home\/igronau\/share\/sims\/simM3\/M3.15.migAC_0_0\/seqs.txt/ \/home\/rvisbord\/experiments\/comb\/${sim}\/seqs.txt /g" ./${hyp}_control-file.ctl;

    echo `pwd`
    nohup G-PhoCS ./${hyp}_control-file.ctl &
    
    popd

  done;

  popd

done
popd
