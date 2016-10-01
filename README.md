# McRef User Guide

powered by - <img src="http://www.faculty.idc.ac.il/igronau/images/research/gphocs-logo.png" alt="Drawing" style="width: 130px;"/>


McRef is an **Relative Bayesian algorithm for Phylogenetic-Population-Model Comparison**, through post-processing of the [G-PhoCS](http://compgen.cshl.edu/GPhoCS/) markov-chain monte-carlo samples.

Below is the minimal documentation required to execute McRef.

### Directory structure
Inside the repo are several important directories:
0. **root (./)**: In the root dir lie the module runner (*run_model_compare.py*) and the default config file.
1. **scripts**: This directory contains bash scripts for bulk experiment executions and other misc development tools
2. **model_compare**: This is **the** python module. all python source code is here.
3. **experiments & sims**: Where, during development, we placed seq-gen data, gphocs traces and McRef results.



### Ilan Guide
The quickest, surest way to run McRef would look as such:
```bash
>> su my_user_name
>> cd ~/dev/modelcompare
>> python ./run_model_compare.py ./experiments/sample
```

Now that we got that out of the way let's get on with a full explanation.

A common experiment setup would be:
1. Run G-PhocS w/ clade. Save data in *"data.cladestats.tsv"* & *"data.trace.tsv"* files. Put files in an *experiment directory*
    * For further explanation on G-PhoCS configuration and execution, see  [G-PhoCS Homepage](http://compgen.cshl.edu/GPhoCS/) and [G-PhoCS Manual](http://compgen.cshl.edu/GPhoCS/GPhoCS_Manual.pdf)
2. Create a *config.ini* file (in the *experiment directory*) with the following attributes:
    * *clade_stats_file_name & trace_file_name*
    * *pops, clades & mig_bands*
    * *burn_in, trim_percentile, dilute_factor & bootstrap_iterations*
3. `python ./run_model_compare.py /path/to/experiment_directory`
4. Results will appear in  `/path/to/experiment_directory/results/##time-stamp##`

### The config file
*McRef* takes It's parameters from config file**s**.
The majority of attributes, mainly the "static" ones, are preset by the config in the root directory. For experiment-specific configuration, place in the experiment directory a new config file with relevant attributes. Any attribute set in the experiment-specific config will override the defaults.

#### Config attributes
Note - Attributes in **bold** are the most relevant.
* [Clade]
  * **pops** - a comma-seperated list of population names (matching the ones names in to gphocs control file)
  * **clades** - see above
  * **mig_bands** - see above
* [Data]
  * **burn_in** - how many of the initial samples to dump
  * **trim_percentile** - what top and bottom percentile of *Gene-ld-ln* to dump. 
  * **dilute_factor** - by what factor to skip samples
  * **bootstrap_iterations** - how many iteration in the bootstraping calculation
  * *theta_print_factor*
  * *mig_rate_print_factor*
  * *expectation_tail_length*
  * *pop_inffix*
  * *theta_prefix*
  * *num_coals_suffix*
  * *coal_stats_suffix*
  * *mig_rate_prefix*
  * *num_migs_suffix*
  * *mig_stats_suffix*
* [Input]
  * **trace_file_name** - location of trace file (relative to experiment dir)
  * **clade_stats_file_name** - see above
* [Output]
  * *likelihoods_plot_name* = hyp_and_ref_plot
  * *expectation_plot_name* = rbf_plot
  * *harmonic_mean_plot_name* = harmonic_mean_plot
  * *results_directory* = results
  * *results_name* = results.csv
  * *summary_name* = summary.txt
  * *save_data* = no




### XXXX Installation
- get latest release from github...
- test project on with sample config sample data 
- success!!

### XXXX Server Prerequisites
- ...



McRef is a **Relative Bayesian Phylogenetic Population-Model Comparison Algorithm** through post-processing of the [G-PhoCS](http://compgen.cshl.edu/GPhoCS/) markov-chain monte-carlo sampler.

Below is the minimal documentation required to execute McRef.

### Directory structure
Inside the repo are several important directories:
0. **root (./)**: In the root dir lie the module runner (*run_model_compare.py*) and the default config file.
1. **scripts**: This directory contains bash scripts for bulk experiment executions and other misc development tools
2. **model_compare**: This is **the** python module. all python source code is here.
3. **experiments & sims**: Where, during development, we placed seq-gen data, gphocs traces and McRef results.



### Ilan Guide
The surest way to run McRef would look as such:
```bash
>> su my_user_name
>> cd ~/dev/modelcompare
>> python ./run_model_compare.py ./experiments/sample
```

The experiment directory should contain a config file with all the experiment details. Below is a chapter explaining the config file. attributes in **bold** are most relevant to you.

A common experiment presetup would be:
1. Run G-PhocS w/ clade. Save data in *"data.cladestats.tsv"* & *"data.trace.tsv"* files.
    * For further explanation on G-PhoCS configuration and execution, see  [G-PhoCS Homepage](http://compgen.cshl.edu/GPhoCS/) and [G-PhoCS Manual](http://compgen.cshl.edu/GPhoCS/GPhoCS_Manual.pdf)
2. Create a *config.ini* file (in the same dir as the trace files) with the following attributes:
    * *clade_stats_file_name & trace_file_name*
    * *pops, clades & mig_bands*
    * *burn_in, trim_percentile, dilute_factor & bootstrap_iterations*
3. `python ./run_model_compare.py /path/to/config/directory`

### The config file
*McRef* takes It's parameters from config file**s**.
The majority of attributes, mainly the "static" ones, are preset by the config in the root directory. For experiment-specific configuration, place in the experiment directory a new config file with relevant attributes. Any attribute set in the experiment-specific config will override the defaults.

#### Config attributes
* [Clade]
  * **pops** - a comma-seperated list of population names (matching the ones names in to gphocs control file)
  * **clades** - see above
  * **mig_bands** - see above
* [Data]
  * **burn_in** - how many of the initial samples to dump
  * **trim_percentile** - what top and bottom percentile of *Gene-ld-ln* to dump. 
  * **dilute_factor** - by what factor to skip samples
  * **bootstrap_iterations** - how many iteration in the bootstraping calculation
  * *theta_print_factor*
  * *mig_rate_print_factor*
  * *expectation_tail_length*
  * *pop_inffix*
  * *theta_prefix*
  * *num_coals_suffix*
  * *coal_stats_suffix*
  * *mig_rate_prefix*
  * *num_migs_suffix*
  * *mig_stats_suffix*
* [Input]
  * **trace_file_name** - location of trace file (relative to experiment dir)
  * **clade_stats_file_name** - see above
* [Output]
  * *likelihoods_plot_name* = hyp_and_ref_plot
  * *expectation_plot_name* = rbf_plot
  * *harmonic_mean_plot_name* = harmonic_mean_plot
  * *results_directory* = results
  * *results_name* = results.csv
  * *summary_name* = summary.txt
  * *save_data* = no




### XXXX Installation
- get latest release from github...
- test project on with sample config sample data 
- success!!

### XXXX Server Prerequisites
- ...



For questions or suggestions please contact me - RonVisbord at Gmail dot com
