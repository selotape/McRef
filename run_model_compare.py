import argparse
import os

from model_compare import compare_models
from model_compare.util.general_purpose import timed


@timed
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clade", help="enable clade reference model. ", action="store_true")
    parser.add_argument("simulations", nargs='+', help="space-delimited list of directories containing model_compare experiments")
    args = parser.parse_args()

    for simulation in args.simulations:
        compare_models(simulation, args.clade)


def is_valid_simulation(sim):
    return os.path.isdir(sim) and os.path.isfile(sim + '/' + 'config.ini')


if __name__ == "__main__":
    main()
