#!/bin/sh

gphocs_exe=/c/Users/ronvis/Dropbox/Thesis/G-PhoCS/code/G-PhoCS/bin/G-PhoCS-1-2-3.exe

function run_gphocs{
	echo "Running G-PhoCS.";
	echo "Control file:"$CTL_FILE;
	$gphocs_exe $CTL_FILE;
}

for var;
do
	CTL_FILE="./simulations/$var/control-file.ctl"
	if [ -f $CTL_FILE ]; then
		run_gphocs $CTL_FILE &
	else
		echo "ERROR: Target control-file " $CTL_FILE " is not a valid file"  >&2
	fi;
done

