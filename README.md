Relative Bayesian model comparison framework through post-processing of G-PhoCS traces

## Usage:

> \>\>\> .\main.py .\path\to\gphocs\results

## Requirements:

1. Anaconda3 (in your environment PATH)
2. G-PhoCS executable in your PATH
3. Precomputed G-PhoCS Trace and CladeStats files

## Configuration:

* The main configuration file is "*config.ini*":
	* Config.ini should reside in the same directory as main.py
	* The main user mandated configurations are 'clades', 'pops' and 'mig_bands'. For further explanation see config file
* For G-PhoCS configuration and execution see the [G-PhoCS Homepage](http://compgen.cshl.edu/GPhoCS/) and the [G-PhoCS Manual](http://compgen.cshl.edu/GPhoCS/GPhoCS_Manual.pdf)

## Todo:
	* add default option to read pops and mig_bands from gphocs ctl file
	* create three seperate algorithms: flat, clade and harmonic_mean
	* manage large data files in lfg

For any question or suggestion feel free to contact me - Ron dot Visbord at Gmail dot com
