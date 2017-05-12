import sys
import logging
import os
from model_compare.model_compare import model_compare


def main(simulations):
    if len(simulations) < 1:
        print_usage_and_exit()
        
    for simulation in simulations:
        if is_valid_simulation(simulation):
            model_compare(simulation)


def print_usage_and_exit():
    print(r"Usage: >>> python .\run_model_compare.py .\path\to\gphocs\results")
    exit()


def is_valid_simulation(sim):
    return os.path.isdir(sim), "\"%s\" is not a directory" % sim


if __name__ == "__main__":
    logging.basicConfig(filename='model_compare.log', level=logging.INFO)  # TODO - move to file config
    logging.info("Starting model_compare...")

    main(sys.argv[1:])

    logging.info("Done!")
