#!/bin/bash

GPHOCS_EXE="/c/Users/ronvis/Dropbox/Thesis/G-PhoCS/code/G-PhoCS/bin/G-PhoCS-1-2-3.exe"
MODEL_COMPARE_PY="/C/Users/ronvis/Dropbox/Thesis/ModelCompare/model_compare/model_compare.py"


# $1 - control-file path
function run_gphocs {
	echo "Running G-PhoCS on Control file: "$1;
	$GPHOCS_EXE $1;
}

# $1 - simulation name
function run_model_compare {
	echo "Running Model_Compare on simulation: "$1;
	python $MODEL_COMPARE_PY $1;
}

# $var - simulation names
main() {
	for var;
	do
		ctl_file="./simulations/$var/control-file.ctl"
		if [ -f $ctl_file ]; then
			run_gphocs $ctl_file &
		else
			echo "ERROR: Target control-file " $ctl_file " is not a valid file"  >&2
		fi;
	done

	wait

	for var;
	do
		simulation=$var
		run_model_compare $simulation &
	done

	wait
	
	echo "DONE"
}
 
main "$@"