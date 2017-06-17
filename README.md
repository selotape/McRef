# McRef User Guide



McRef is a **Relative Bayesian Algorithm for Phylogenetic-Population-Model Comparison**, through post-processing of the [G-PhoCS](http://compgen.cshl.edu/GPhoCS/) markov-chain monte-carlo samples.



### Quick Start
The quickest, surest way to run McRef is:
```bash
$ git clone https://github.com/selotape/Population-Model-Compare modelcompare
$ cd ./modelcompare
$ pip install -r requirements.txt
$ python3 ./run_model_compare.py ./simulations/experiments/sample
```


### Config Files
*McRef* takes It's parameters from config file**s**. *McRef* looks for config files called 'config.ini' in the current directory and in the experiment directory.
The majority of attributes are preconfigured by the config in the project root directory. For experiment-specific configuration, place in the experiment directory a new config file with relevant attributes. Any attribute set in the experiment-specific config will override the defaults.


### Common Experiment Setup
1. Run G-PhocS w/ clade. Save data in *"data.cladestats.tsv"* & *"data.trace.tsv"* files. Put files in an *experiment directory*
    * For further explanation on G-PhoCS configuration and execution, see  [G-PhoCS Homepage](http://compgen.cshl.edu/GPhoCS/) and [G-PhoCS Manual](http://compgen.cshl.edu/GPhoCS/GPhoCS_Manual.pdf)
2. Create a *config.ini* file (in the *experiment directory*) with the following attributes:
    * *clade_stats_file_name & trace_file_name*
    * *combs, comb leaves, pops & mig_bands*
    * *skip_rows, number_of_rows, trim_percentile, dilute_factor*
3. run `$ python ./run_model_compare.py [/path/to/experiment1 ...]`
4. see results in directory */path/to/experiment_directory/results/##time-stamp##* 


### Contact Us!
For questions or suggestions please contact us - RonVisbord at Gmail dot com || Ilan Gronau at IDC dot AC dot IL

**McRef is powered by - <img src="http://www.faculty.idc.ac.il/igronau/images/research/gphocs-logo.png"  width="130"/>
