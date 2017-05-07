import sys

import logging

from model_compare import model_compare
import os


def main(argv):
    logging.basicConfig(filename='model_compare.log', level=logging.INFO)
    logging.info("Starting model_compare...")

    simulations = argv[1:]
    if len(simulations) < 1:
        print_usage_and_exit()
    for simulation in simulations:
        validate_simulation(simulation)
        model_compare.model_compare(simulation)
    logging.info("Done!")


def print_usage_and_exit():
    print(r"Usage: >>> python .\run_model_compare.py .\path\to\gphocs\results")
    exit()


def validate_simulation(sim):
    assert os.path.isdir(sim), "\"%s\" is not a directory" % sim
    logging.info("Validated simulation %s", sim)






if __name__ == "__main__":
    main(sys.argv)
