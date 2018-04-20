#!/usr/bin/env bash
set -euo pipefail

DIR=`dirname "$0"`
python_venv="/home/ron/.virtualenvs/modelcompare"

configs_dir="${DIR}/../config_files"
data_root="/home/ron/Desktop/data_sets"
template_ctl="${configs_dir}/template.ctl"

seed1="12345"
seed2="54321"