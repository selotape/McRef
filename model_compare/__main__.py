import numpy as np
import pandas as pd
import configparser

### SETUP ###

def main():
    set_pandas()

    config = configparser.ConfigParser()
    config.read('config.ini')
    simulation_name = config.get('Simulation', 'name')
    theta_column_name = config.get('Simulation','theta_column')
    print_factor = config.getfloat('Simulation','print_factor')


    flat_stats_path = '..\\simulations\\' + simulation_name + '\\gphocs\\data.flatStats.tsv'
    flat_stats = pd.read_csv(flat_stats_path, sep='\t')

    trace_path = '..\\simulations\\' + simulation_name + '\\gphocs\\data.trace.tsv'
    trace = pd.read_csv(trace_path, sep='\t')

    flat_stats[theta_column_name] = trace[theta_column_name]


    flat_stats = flat_stats[['logPrior', 'coalStatFlat', 'numCoalFlat', theta_column_name, 'genealogyLogLikelihood']]
    flat_stats.columns = ['logPrior', 'time_stats', 'num_coal', theta_column_name, 'P_Z_ϴM']

    flat_stats[theta_column_name] /= print_factor

    thetas = flat_stats[theta_column_name]
    num_coal = flat_stats['num_coal']
    time_stats = flat_stats['time_stats']

    flat_stats['P_Z_ϴM0'] = P_Z_ϴM0(thetas, num_coal, time_stats)


    # print to make sense
    flat_stats[['P_Z_ϴM0', 'P_Z_ϴM']].plot()
    print(flat_stats.head())






def set_pandas():
    pd.set_option('display.mpl_style', 'default')
    pd.set_option('display.width', 5000)
    pd.set_option('display.max_columns', 60)

def P_Z_ϴM0(theta, num_coal, time_stats):
    result = num_coal*np.log(2.0/theta) - (time_stats/theta)
    return result


if __name__ == "__main__":
    main()