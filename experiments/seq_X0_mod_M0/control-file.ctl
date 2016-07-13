GENERAL-INFO-START

	seq-file            sims\M0\sequences.seqs
	trace-file          experiments\seq_X0_mod_M0\data.trace.tsv
	flat-stats-file		experiments\seq_X0_mod_M0\data.flatStats.tsv
	clade-stats-file	experiments\seq_X0_mod_M0\data.cladeStats.tsv
#	num-pop-partitions	1
	locus-mut-rate		CONST

	num-loci 			10
	mcmc-iterations	  	5000
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
		samples		1 h 2 h 3 h 4 h 5 h 6 h 7 h 8 h 9 h 10 h 11 h 12 h 13 h 14 h 15 h
	POP-END
	
	POP-START
		name		B
		samples		16 h
	POP-END

CURRENT-POPS-END

ANCESTRAL-POPS-START

	POP-START
		name			root
		children		A B
		tau-initial		0.000000000001
		tau-beta		20000.0	
		finetune-tau	0.00000286
	POP-END

ANCESTRAL-POPS-END
