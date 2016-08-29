GENERAL-INFO-START

	seq-file            sims/simM2.10/data.seqs
	trace-file          experiments/simM2.10/data.trace.tsv
#	flat-stats-file		experiments/simM2.10/data.flatStats.tsv
	clade-stats-file	experiments/simM2.10/data.cladeStats.tsv
#	num-pop-partitions	1
	locus-mut-rate		CONST

	num-loci			5000
	mcmc-iterations		50000
	iterations-per-log	5
	logs-per-line		10


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
		samples		1 h 2 h 3 h 4 h 5 h 6 h 7 h 8 h
	POP-END

	POP-START
		name		B
		samples		9 h 10 h 11 h 12 h 13 h 14 h 15 h 16 h
	POP-END

	POP-START
		name		C
		samples		17 h 18 h 19 h 20 h 21 h 22 h 23 h 24 h
	POP-END
	
CURRENT-POPS-END

#!! ROOT population must be placed last!
ANCESTRAL-POPS-START

	POP-START
		name			AB
		children		A		B
		tau-initial		0.00005
		tau-beta		20000.0	
		finetune-tau	0.0000008
	POP-END

	POP-START
		name			root
		children		AB	C
		tau-initial		0.0003
		tau-beta		20000.0	
		finetune-tau	0.00000286
	POP-END

ANCESTRAL-POPS-END

#MIG-BANDS-START	
#
#	BAND-START		
#		name    C->B
#		source  C
#		target  B
#		mig-rate-print 0.1
#	BAND-END
#
#MIG-BANDS-END
