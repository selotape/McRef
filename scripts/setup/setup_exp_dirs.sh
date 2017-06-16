for hyp in AB_C BC_A AC_B ; do

  pushd /home/rvisbord/experiments/comb 
  for sim in  M3.20.migAC_0_0 M3.25.migAC_0_0 M3.29.migAC_0_0 ; 

  do 

    mkdir -p ${sim}/${hyp};

    cp /home/igronau/share/sims/simM3/${sim}/seqs.txt.gz ./${sim}
    pushd ./${sim}
    gunzip seqs.txt.gz
    popd

    cp M3.15.migAC_0_0/with_clade_and_mem_fix_without_assertions/${hyp}/${hyp}_control-file.ctl ${sim}/${hyp} 
    sed -i -e "s/\/home\/igronau\/share\/sims\/simM3\/M3.15.migAC_0_0\/seqs.txt/ \/home\/rvisbord\/experiments\/comb\/${sim}\/seqs.txt /g" ${sim}/${hyp}/${hyp}_control-file.ctl;

    pushd ./${sim}/${hyp}
    G-PhoCS ./${hyp}_control-file.ctl &
    popd
  done;

done


popd
