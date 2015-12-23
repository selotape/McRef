#!/bin/sh

# setup
[ $# -ge 1 ] && SIM_NAME="$1" || read SIM_NAME

CTRL_FILE_NAME="./$SIM_NAME/gphocs/control-file.ctl"

echo $CTRL_FILE_NAME

# run GPhoCS
if [ -f $CTRL_FILE_NAME ]; then
	echo "Running G-PhoCS."
	echo "Control file:"$CTRL_FILE_NAME
	./G-PhoCS-1-2-3.exe $CTRL_FILE_NAME
else
	echo "ERROR: Target control-file " $CTRL_FILE_NAME "is not a valid file"  >&2
fi



# run model compare