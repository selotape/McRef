#!/bin/bash
set -e
set -o nounset

taus="01 05 10 15"
migs="1 2 4"

# handle Mikrei Katze
#./targz_trace.sh 00 0 0asdfasdf
#./targz_trace.sh 00 0 0asdfasdf
#./targz_trace.sh 00 0 0asdfasdf


for tau in $taus
do
	for m in $migs
	do
			./zipTraces.sh $tau $m 0
			./zipTraces.sh $tau 0 $m
	done
done
