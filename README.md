# McRef User Guide



McRef is a **Relative Bayesian Algorithm for Phylogenetic-Population-Model Comparison**, through post-processing of the [G-PhoCS](http://compgen.cshl.edu/GPhoCS/) markov-chain monte-carlo samples.



### Quick Start
The quickest, surest way to run McRef is:
```bash
git clone https://github.com/selotape/Population-Model-Compare mcref
cd ./mcref
pip3 install -r requirements.txt  # or better yet - use [Pipenv](https://docs.pipenv.org/)!
python3 mcref -h
python3 mcref ./simulations/experiments/sample
```


### Config Files
*McRef* takes It's parameters from config file**s**. It looks for files called *config.ini* in the current directory and in the experiment directory. 
   * See further documentation in [./config.ini](https://github.com/selotape/Population-Model-Compare/blob/master/config.ini).


### Common Experiment Setup
1. Run G-PhocS with comb enabled (see next section). Save data in *"hyp/comb/clade-trace.tsv"* and *"trace.tsv"* files. Put files in an *experiment directory*
2. Create a *config.ini* file in the *experiment directory*. Set your reference model and any other non-default parameter you may require.
3. run `python3 ./run_model_compare.py [/path/to/experiment1 ...]`
4. ...
5. see results in directory */path/to/experiment/results/${time-stamp}* 

### Running GPhoCS with mcref enabled
To make GPhoCS emit comb and clade statistics, add the following configurations to the gphocs control file:

```
GENERAL-INFO-START
...
    comb-stats-file     out/comb-trace.tsv
    clade-stats-file    out/clade-trace.tsv
    hyp-stats-file      out/hyp-trace.tsv
    tau-bounds-file      out/tau-bounds.tsv
...
```
For a full explanation on G-PhoCS configuration and execution, see  [G-PhoCS Homepage](http://compgen.cshl.edu/GPhoCS/) and [G-PhoCS Manual](http://compgen.cshl.edu/GPhoCS/GPhoCS_Manual.pdf)


### Configuring mcref

Below is an example configuration file with inline comments explaining each value. 
Copy this config, edit it to your hearts content and put it in the "experiment directory" - 


```yaml
[ReferenceModel]
### Note - this is the main (and hopefully only) thing you should configure!
### This configuration (comb/clade) must form a valid reference model.
### See PLACE-LINK-HERE for explanation of a reference model.

### configure clade XOR comb
#clade = ABC
#clade_mig_bands =
#comb = ABC
#comb_leaves = A,B,C
#comb_mig_bands =

#hyp_pops = root,D
#hyp_mig_bands = D->B

[Input]
#trace_file = /path/to/sample-trace.tsv
#comb_stats_file = /path/to/sample-comb-trace.tsv
#clade_stats_file = /path/to/sample-clade-trace.tsv
#hyp_stats_file = /path/to/sample-hyp-trace.tsv
#tau_bounds_file = ./tau-bounds.tsv

#tau-theta-print=10000.0
#tau-theta-alpha=1.0
#tau-theta-beta=10000.0
#mig-rate-print=0.001

[Output]
# results_name = results.csv
# summary_name = summary.txt
# results_directory = results
# debug_directory = debug
# likelihoods_plot_name = hyp_and_ref_plot
# expectation_plot_name = rbf_plot
# harmonic_mean_plot_name = harmonic_mean_plot
# save_data = true  # uncomment to save all the pandas data


[Data]
#skip_rows = 100
#number_of_rows = 1000


[Debug]
# enabled = true
## when debug is enabled, mcref reconstructs the original hypothesis likelihoods using these fields
# hypothesis_pops = A,B,C,D,AB,ABC,root
# hypothesis_migbands = D->B
```


### Contact Us!
For questions or suggestions please contact us - RonVisbord at Gmail dot com || Ilan Gronau at IDC dot AC dot IL

**McRef is powered by - <img src="http://www.faculty.idc.ac.il/igronau/images/research/gphocs-logo.png"  width="130"/>

