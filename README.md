# McRef User Guide



McRef is an **Relative Bayesian algorithm for Phylogenetic-Population-Model Comparison**, through post-processing of the [G-PhoCS](http://compgen.cshl.edu/GPhoCS/) markov-chain monte-carlo samples.

Below is the minimal documentation required to execute McRef.

### Directory structure
Inside the repo are several important directories:
0. **root (./)**: In the root dir lie the module runner (*run_model_compare.py*) and the default config file.
1. **scripts**: This directory contains bash scripts for bulk experiment executions and other misc development tools
2. **model_compare**: This is **the** python module. all python source code is here.
3. **experiments & sims**: Where, during development, we placed seq-gen data, gphocs traces and McRef results.



### Execution Guide
The quickest, surest way to run McRef would look as such:
```bash
$ cd ./modelcompare
$ python ./run_model_compare.py ./experiments/sample
```

Now that we got that out of the way, let's get on with a full explanation.

A common experiment setup would be:
1. Run G-PhocS w/ clade. Save data in *"data.cladestats.tsv"* & *"data.trace.tsv"* files. Put files in an *experiment directory*
    * For further explanation on G-PhoCS configuration and execution, see  [G-PhoCS Homepage](http://compgen.cshl.edu/GPhoCS/) and [G-PhoCS Manual](http://compgen.cshl.edu/GPhoCS/GPhoCS_Manual.pdf)
2. Create a *config.ini* file (in the *experiment directory*) with the following attributes:
    * *clade_stats_file_name & trace_file_name*
    * *pops, clades & mig_bands*
    * *burn_in, trim_percentile, dilute_factor & bootstrap_iterations*
3. `$ python ./run_model_compare.py /path/to/experiment_directory`
4. Results will appear in directory */path/to/experiment_directory/results/##time-stamp##* 

### The Config File
*McRef* takes It's parameters from config file**s**.
The majority of attributes, mainly the "static" ones, are preset by the config in the root directory. For experiment-specific configuration, place in the experiment directory a new config file with relevant attributes. Any attribute set in the experiment-specific config will override the defaults.

#### Config File Attributes
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
  * *theta_print_factor* - the print factor used in the gphocs execution
  * *mig_rate_print_factor* - see above
  * *pop_inffix* - column name formatting in gphocs clade stats (used to parse gphocs output)
  * *theta_prefix* - see above
  * *num_coals_suffix* - see above
  * *coal_stats_suffix* - see above
  * *mig_rate_prefix* - see above
  * *num_migs_suffix* - see above
  * *mig_stats_suffix* - see above
* [Input]
  * **trace_file_name** - location of trace file (relative to experiment dir)
  * **clade_stats_file_name** - see above
* [Output]
  * *results_directory* = results - name of directory in which to save results
  * *likelihoods_plot_name* = hyp_and_ref_plot - plot names
  * *expectation_plot_name* = rbf_plot - see above
  * *harmonic_mean_plot_name* = harmonic_mean_plot - see above
  * *summary_name* = summary.txt - where to save experiment textual summary 
  * *save_data* = [yes/no] - whether to save to disk all statistics used in the final computations
  * *results_name* = results.csv - if save_data=yes, where to save statistics


### Installation

#### Prerequisites
1. install python 3.X along with packages *matplotlib, numpy & pandas*.
Best ways to setup requirements are either via pip (`$ pip install -r model_compare/requirements.txt`) or by directrly  [installing anaconda](https://docs.continuum.io/anaconda/install#linux-install)
2. install git 
``` bash
$ sudo apt-get update
$ sudo apt-get install git
```

#### Installing McRef
1. Get latest release from bitbucket - `$ git clone https://my_user_name@bitbucket.org/gphocsdev/modelcompare.git`
2. Test project on with sample config & data - `$ python run_model_compare.py experiments/sample`
3. Assert output is a comma-seperated set of results:

    | experiment name  | clades | pops         | mig_bands | rbf_boot   | rbf_mean   | hm_boot   | hm_mean  |
    | ---------------- | :----: | ------------ | --------- | ---------- | ---------- | --------- | -------- |
    |experiments\sample| AB     | C&ABC&D&root |           | 0.06183... | -4.1527... | 1.4149... | 14011... | 
4. Success!!

### Contact Us!
For questions or suggestions please contact us - RonVisbord at Gmail dot com || Ilan Gronau at IDC dot AC dot IL

**McRef is powered by - <img src="http://www.faculty.idc.ac.il/igronau/images/research/gphocs-logo.png"  width="130"/>
