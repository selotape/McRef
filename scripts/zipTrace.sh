#!/bin/bash
set -e

TAU=$1
M_AC=$2
M_CA=$3

simName=M3.$TAU.migAC_${M_AC}_${M_CA}
traceName=trace.$simName.tsv
cladeName=clade.$simName.tsv

function cleanup {
    rm -rf $traceName.dwn $cladeName.dwn
}

cd $simName

cleanup
echo ' copying trace files with TAU='$TAU', $M_AC='0.0${M_AC}', $M_CA='0.0${M_CA}
cp $traceName $traceName.dwn
cp $cladeName $cladeName.dwn

echo ' zipping...'
zip $simName.zip $traceName.dwn $cladeName.dwn

echo ' cleaning up...'
cleanup
