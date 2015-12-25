#!/bin/sh

# setup
[ $# -ge 1 ] && SIM_NAME="$1" || ( echo "Enter simulation name:" && read SIM_NAME )

CTRL_FILE="./$SIM_NAME/gphocs/control-file.ctl"

# run GPhoCS
if [ -f $CTRL_FILE ]; then
	echo "Running G-PhoCS."
	echo "Control file:"$CTRL_FILE
	# ./G-PhoCS-1-2-3.exe $CTRL_FILE_NAME
	/c/Users/ronvis/Dropbox/Thesis/G-PhoCS/code/G-PhoCS/bin/G-PhoCS-1-2-3.exe $CTRL_FILE
else
	echo "ERROR: Target control-file " $CTRL_FILE " is not a valid file"  >&2
fi



# run model compare...
