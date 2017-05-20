import sys
import logging
import os
from model_compare import compare_models


def main(simulations):
    if len(simulations) < 1:
        print_usage_and_exit()

    for simulation in simulations:
        if is_valid_simulation(simulation):
            compare_models(simulation)


def print_usage_and_exit():
    print(r"Usage: >>> python .\run_model_compare.py .\path\to\gphocs\results")
    exit()


def is_valid_simulation(sim):
    return os.path.isdir(sim), "\"%s\" is not a directory" % sim


def setup_logging():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='model_compare.log',
                        filemode='w')


if __name__ == "__main__":
    setup_logging()
    logging.info("Starting model_compare...")

    main(sys.argv[1:])

    logging.info("Done!")
