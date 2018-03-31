GENERAL-INFO-START

	seq-file	SPECIFY_SEPARATELY	
	trace-file		./trace.tsv
	comb-stats-file		./comb-trace.tsv
	hyp-stats-file		./hyp-trace.tsv
	clade-stats-file	./clade-trace.tsv
        tau-bounds-file         ./tau-bounds.tsv

	locus-mut-rate		CONST

	num-loci		1000
	burn-in		        0
	mcmc-iterations		1000000
	mcmc-sample-skip	9
#	start-mig		0
	iterations-per-log	100
	logs-per-line		100

	tau-theta-print		10000
	tau-theta-alpha		1
	tau-theta-beta		10000

#	mig-rate-print		0.001
#	mig-rate-alpha		0.002
#	mig-rate-beta		0.00001

	locus-mut-rate		CONST

	find-finetunes	                	TRUE
	find-finetunes-num-steps	        100
	find-finetunes-samples-per-step		100

GENERAL-INFO-END


CURRENT-POPS-START	

	POP-START
		name		A
		samples		1 h 2 h 3 h 4 h
	POP-END

	POP-START
		name		B
		samples		9 h 10 h 11 h 12 h
	POP-END


	POP-START
		name		C
		samples		17 h 18 h 19 h 20 h
	POP-END

	POP-START
		name		O
		samples		25 h 26 h
	POP-END

CURRENT-POPS-END


ANCESTRAL-POPS-START

	POP-START
		name			BC
		children		B		C
		tau-initial		0.0001
		tau-beta		20000.0	
	POP-END


	POP-START
		name			ABC
		children		A	BC
		tau-initial		0.0005
		tau-beta		20000.0	
	POP-END

	POP-START
		name			ROOT
		children		ABC	O
		tau-initial		0.0020
		tau-beta		20000.0	
	POP-END

ANCESTRAL-POPS-END

