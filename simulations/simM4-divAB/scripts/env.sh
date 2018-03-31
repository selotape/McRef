#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

DIR=`dirname "$0"`


#root_dir="/home/ron/Desktop/data_sets"
configs_dir="${DIR}/../config_files"
data_root="/home/ron/Desktop/data_sets"
template_ctl="${configs_dir}/template.ctl"

seed1="12345"
seed2="54321"

