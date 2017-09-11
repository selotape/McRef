GENERAL-INFO-START

	seq-file	SPECIFY_SEPARATELY	
	trace-file		./trace.tsv
	comb-stats-file		./comb-trace.tsv
	hyp-stats-file		./hyp-trace.tsv
	clade-stats-file	./clade-trace.tsv
	locus-mut-rate		CONST

	num-loci		2000
	burn-in		0
	mcmc-iterations		500000
	mcmc-sample-skip	9
	start-mig		0
	iterations-per-log	100
	logs-per-line		100

	tau-theta-print		10000
	tau-theta-alpha		1
	tau-theta-beta		10000

	mig-rate-print		0.001
	mig-rate-alpha		0.002
	mig-rate-beta		0.00001

	locus-mut-rate		CONST

	find-finetunes		TRUE
	find-finetunes-num-steps	100
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

CURRENT-POPS-END


ANCESTRAL-POPS-START

	POP-START
		name			ANC
		children		A		B
		tau-initial		0.0001
		tau-beta		20000.0	
	POP-END

	POP-START
		name			ROOT
		children		ANC	C
		tau-initial		0.0005
		tau-beta		20000.0	
	POP-END

ANCESTRAL-POPS-END

MIG-BANDS-START
	BAND-START
		source A
		target B
	BAND-END
	BAND-START
		source B
		target A
	BAND-END
	BAND-START
		source A
		target C
	BAND-END
	BAND-START
		source C
		target A
	BAND-END
	BAND-START
		source B
		target C
	BAND-END
	BAND-START
		source C
		target B
	BAND-END
MIG-BANDS-END
