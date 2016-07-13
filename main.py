import sys
from model_compare import model_compare

if __name__ == "__main__":
    simulation_names = sys.argv[1:]
    for simulation_name in simulation_names:
        print(" Starting simulation " + simulation_name)
        model_compare.model_compare(simulation_name)
        print(" Finished " + simulation_name)
    print("Done!")