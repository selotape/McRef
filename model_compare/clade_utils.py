import pandas as pd
import os
from model_compare.probability_functions import P_G_Mroot, E_P_G

def get_clades_and_pops():
    clades = []
    pops = ["A", "B", "root"]
    return clades, pops


##############
### CONSTS ###
##############
LIKELIHOODS_PLOT_PATH   = "experiments\\simulations\\seq_X0_mod_M1\\results\\likelihoods_plot.png"
EXPECTATION_PLOT_PATH   = "experiments\\simulations\\seq_X0_mod_M1\\results\\expectation_plot.png"
RESULTS_PATH            = "experiments\\simulations\\seq_X0_mod_M1\\results\\model_compare_results.csv"
SUMMARY_PATH            = "experiments\\simulations\\seq_X0_mod_M1\\results\\model_compare_summary.txt"
DATA_TRACE_PATH = "experiments\\simulations\\seq_X0_mod_M1\\data.trace.tsv"
CLADE_STATS_PATH = "experiments\\simulations\\seq_X0_mod_M1\\data.cladeStats.tsv"

TAIL_LENGTH = 1000

POP_INFFIX = "__pop"
THETA_PREFIX = "theta_"
NUM_COALS_SUFFIX = "_num_coals_total"
COAL_STATS_SUFFIX = "_coal_stats_total"


def func(simulation):

    clades, pops = get_clades_and_pops()

    dataTrace = pd.read_csv(DATA_TRACE_PATH, sep='\t')
    cladeStats = pd.read_csv(CLADE_STATS_PATH, sep='\t')

    thetas = dataTrace[[THETA_PREFIX + p for p in pops]]
    num_coal = cladeStats[[c + NUM_COALS_SUFFIX for c in clades] + [p + POP_INFFIX + NUM_COALS_SUFFIX for p in pops]]
    coal_stats = cladeStats[[c + COAL_STATS_SUFFIX for c in clades] + [p + POP_INFFIX + COAL_STATS_SUFFIX for p in pops]]

    results = pd.DataFrame()
    for pop in pops:
        results[pop + POP_INFFIX] = P_G_Mroot(thetas[THETA_PREFIX + pop], num_coal[ pop + POP_INFFIX + NUM_COALS_SUFFIX ], coal_stats[pop + POP_INFFIX + COAL_STATS_SUFFIX ])
    for clade in clades:
        results[clade] = P_G_Mroot(thetas[THETA_PREFIX + clade], num_coal[clade + NUM_COALS_SUFFIX], coal_stats[clade + COAL_STATS_SUFFIX])

    columns_to_sum = [clade for clade in clades] + [pop + POP_INFFIX for pop in pops]
    results['reference'] = results[columns_to_sum].sum(axis=1)


    results['hypothesis'] = dataTrace['Gene-ld-ln']

    results['E_ratio'] = results['reference'] - results['hypothesis']

    rbf = E_P_G(results['E_ratio'][-TAIL_LENGTH:])


    save_results(LIKELIHOODS_PLOT_PATH, EXPECTATION_PLOT_PATH, results, rbf, simulation)

def save_results(likelihoods_plot_path, expectation_plot_path, results, rbf, simulation):

    save_plot(results[-TAIL_LENGTH:][['reference', 'hypothesis']], likelihoods_plot_path, simulation)
    save_plot(results[-TAIL_LENGTH:][['E_ratio']], expectation_plot_path, simulation)

    results.to_csv(RESULTS_PATH)

    f = open(SUMMARY_PATH, 'w')
    f.write("rbf={0}\n".format(rbf))


def save_plot(data_frame, plot_save_path, plot_name=''):
    plot = data_frame.plot(title=plot_name)
    figure = plot.get_figure()
    figure.savefig(plot_save_path)
