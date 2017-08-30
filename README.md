# McRef User Guide



McRef is a **Relative Bayesian Algorithm for Phylogenetic-Population-Model Comparison**, through post-processing of the [G-PhoCS](http://compgen.cshl.edu/GPhoCS/) markov-chain monte-carlo samples.



### Quick Start
The quickest, surest way to run McRef is:
```bash
git clone https://github.com/selotape/Population-Model-Compare mcref
cd ./mcref
pip3 install -r requirements.txt  # or better yet - create a virtual environment!
python3 ./run_model_compare.py -h
python3 ./run_model_compare.py ./simulations/experiments/sample
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
To make emit GPhoCS emit comb and clade statistics, add the following configurations to the gphocs control file:

```
GENERAL-INFO-START
...
    comb-stats-file     out/comb-trace.tsv
    clade-stats-file    out/clade-trace.tsv
    hyp-stats-file      out/hyp-trace.tsv
...
```
For a full explanation on G-PhoCS configuration and execution, see  [G-PhoCS Homepage](http://compgen.cshl.edu/GPhoCS/) and [G-PhoCS Manual](http://compgen.cshl.edu/GPhoCS/GPhoCS_Manual.pdf)


### Contact Us!
For questions or suggestions please contact us - RonVisbord at Gmail dot com || Ilan Gronau at IDC dot AC dot IL

**McRef is powered by - <img src="http://www.faculty.idc.ac.il/igronau/images/research/gphocs-logo.png"  width="130"/>

