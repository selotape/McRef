#!/bin/bash
set -e 
set -o nounset

oxfordDir="/home/rvisbord/dev/gphocs-dev/experiments/oxford"
mc3Dir="."
mc3="python $mc3Dir/run_model_compare.py"


function set_ref {
	conf_file="$1"
	pops="$2"
	clades="$3"
	mig_bands="$4"
	sed -i.bak "s/^clades =.*$/clades = $clades/" "$conf_file"
	sed -i.bak "s/^pops =.*$/pops = $pops/" "$conf_file"
	sed -i.bak "s/^mig_bands =.*$/mig_bands = $mig_bands/" "$conf_file"
}

function run_mc3 {
        expDir="$1"
        $mc3 $expDir &
}

function prep_and_launch {
        simName="$1"
        pops="$2"
        clades="$3"
        mig_bands="$4"
	burn_in="$5"
	expDir="$oxfordDir/$simName"
	conf_file="$oxfordDir/$simName/config.ini"
	set_ref "$conf_file" "$pops" "$clades" "$mig_bands" "$burn_in"
	run_mc3 "$expDir"
}

### choice of clade can improve accuracy

function choice_of_clade {
	pops="C,root"
	clades="AB"
	mig_bands=""
	burn_in="50000"
	prep_and_launch M3.00.migAC_0_0 "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.01.migAC_0_0 "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.05.migAC_0_0 "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.10.migAC_0_0 "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.15.migAC_0_0 "$pops" "$clades" "$mig_bands" "$burn_in"
	wait

	pops=""
	clades="root"
	prep_and_launch M3.00.migAC_0_0 "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.01.migAC_0_0 "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.05.migAC_0_0 "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.10.migAC_0_0 "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.15.migAC_0_0 "$pops" "$clades" "$mig_bands" "$burn_in"
	wait
}

### rbf favors the right model, hyp vs ref
function choice_hyp_vs_ref {

	#M3.00.migAC_0_0/ w root & clade
	#M3.01.migAC_0_0/ w root & clade
	#M3.05.migAC_0_0/ w root & clade
	#M3.10.migAC_0_0/ w root & clade
	#M3.15.migAC_0_0/ w root & clade
	prep_and_launch M3.00_0_0.AB_C "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.01_0_0.AB_C "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.05_0_0.AB_C "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.10_0_0.AB_C "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.15_0_0.AB_C "$pops" "$clades" "$mig_bands" "$burn_in"
	wait
}


### rbfs chooses the right model, hyp1 vs hyp2
function choice_hyp1_vs_hyp2 {
	#M3.00.migAC_0_0/ w root
	prep_and_launch M3.00_0_0.AB_C "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.00_0_0.ACB  "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.00_0_0.BCA  "$pops" "$clades" "$mig_bands" "$burn_in"
	#M3.05.migAC_0_0/ w root
	prep_and_launch M3.05_0_0.AB_C "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.05_0_0.ACB  "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.05_0_0.BCA  "$pops" "$clades" "$mig_bands" "$burn_in"
	#M3.15.migAC_0_0/ w root
	prep_and_launch M3.15_0_0.AB_C "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.15_0_0.ACB  "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.15_0_0.BCA  "$pops" "$clades" "$mig_bands" "$burn_in"
	wait
}


### Migrations 
function choice_of_migration {
	pops=""
	clades="root"
	mig_bands=""
	#M3.05.migAC_0_0/ w root
	prep_and_launch M3.mig.05_0_1.no_mig "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.mig.05_0_2.no_mig "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.mig.05_0_4.no_mig "$pops" "$clades" "$mig_bands" "$burn_in"
	wait
	mig_bands="C->A"
	prep_and_launch M3.05.migAC_0_1      "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.05.migAC_0_2      "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.05.migAC_0_4      "$pops" "$clades" "$mig_bands" "$burn_in"
	wait
	mig_bands="A->C"
	prep_and_launch M3.mig.05_0_0.A-C    "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.mig.05_0_1.A-C    "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.mig.05_0_2.A-C    "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.mig.05_0_4.A-C    "$pops" "$clades" "$mig_bands" "$burn_in"
	wait
	mig_bands="A->C,C->A"
	prep_and_launch M3.mig.05_0_0.A-CC-A "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.mig.05_0_1.A-CC-A "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.mig.05_0_2.A-CC-A "$pops" "$clades" "$mig_bands" "$burn_in"
	prep_and_launch M3.mig.05_0_4.A-CC-A "$pops" "$clades" "$mig_bands" "$burn_in"
	wait
}

function temp {
	prep_and_launch M3.01.migAC_0_0  "" "root" "" "300000"
	prep_and_launch M3.05.migAC_0_0  "" "root" "" "300000"
	wait
	prep_and_launch M3.01.migAC_0_0  "C,root" "AB" "" "300000"
	prep_and_launch M3.05.migAC_0_0  "C,root" "AB" "" "300000"
	wait
}

temp
exit
choice_of_migration
choice_hyp1_vs_hyp2
choice_hyp_vs_ref
choice_of_clade
