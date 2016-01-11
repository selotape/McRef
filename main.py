import sys
from model_compare import model_compare

if __name__ == "__main__":
    simulation_names = sys.argv[1:]
    for simulation in simulation_names:
        model_compare.model_compare(simulation)