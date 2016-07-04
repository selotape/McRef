import sys
from model_compare import model_compare
from model_compare import clade_utils

if __name__ == "__main__":
    simulation_names = sys.argv[1:]
    for simulation_name in simulation_names:
        model_compare.model_compare(simulation_name)
        # clade_utils.func(simulation)