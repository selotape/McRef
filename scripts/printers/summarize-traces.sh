#!/usr/bin/env bash
# summarize div traces
# traces=`ls M3.divs/divAB_??/*/trace.tsv`

# summarize mig traces
traces=`ls M3.15/migAC_?/*/trace.tsv`

for trace in $traces
do
	newname=`echo $trace | tr "/" "-" | sed 's/tsv$/txt/'`
	# echo $newname
	cp -a $trace traces/$newname
done

# copy M3.15 traces from mig runs

for model in AB_C AC_B BC_A
do
	cp -a M3.15/migAC_0/${model}_nomig/trace.tsv traces/M3.divs-divAB_15-${model}-trace.txt
done


tail -n2 traces/M3.15-*-trace.txt |cut -f1 | tr "\n" "\t" | tr ">" "\n" | sort -k3,3n
