GENERAL-INFO-START

	seq-file            M0\sequences\sequences.seqs
	trace-file          M0\gphocs\data.trace.tsv
	coal-stats-file		M0\gphocs\data.flatStats.tsv
#	num-pop-partitions	1
	locus-mut-rate		CONST

	num-loci 			10
	mcmc-iterations	  	4000
	iterations-per-log  5
	logs-per-line       10


	find-finetunes		FALSE
	finetune-coal-time	0.01		
	finetune-mig-time	0.3		
	finetune-theta		0.04
	finetune-mig-rate	0.02
	finetune-tau		0.0000008
	finetune-mixing		0.003
#   finetune-locus-rate 0.3
	
	tau-theta-print		10000.0
	tau-theta-alpha		1.0			# for STD/mean ratio of 100%
	tau-theta-beta		10000.0		# for mean of 1e-4

	mig-rate-print		0.001
	mig-rate-alpha		0.002
	mig-rate-beta		0.00001

GENERAL-INFO-END

CURRENT-POPS-START	

	POP-START
		name		A
		samples		1 d 2 d 3 d 4 d 5 d 6 d 7 d 8 d 9 d 10 d 11 d 12 d 13 d 14 d 15 d 16 d
	POP-END
	
	POP-START
		name		B
		samples		17 d
	POP-END

CURRENT-POPS-END

ANCESTRAL-POPS-START

	POP-START
		name			root
		children		A B
		tau-initial		1.0
		tau-beta		20000.0	
		finetune-tau	0.000001
	POP-END

ANCESTRAL-POPS-END
