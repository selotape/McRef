import os
import sys

from model_compare import compare_models, clade_compare_models


def main(args):
    simulation, is_clade = _parse_args(args)

    if is_clade:
        clade_compare_models(simulation)
    else:
        compare_models(simulation)


def _parse_args(args):
    is_clade = False
    simulation = None
    if len(args) == 0 or not is_valid_simulation(args[0]):
        print_usage_and_exit()
    else:
        simulation = args[0]
    if len(args) == 2:
        if args[1] != '--clade':
            print_usage_and_exit()
        else:
            is_clade = True
    return simulation, is_clade


def print_usage_and_exit():
    print(r"Usage: >>> python .\run_model_compare.py .\path\to\config_dir [--clade]")
    exit()


def is_valid_simulation(sim):
    return os.path.isdir(sim), "\"%s\" is not a directory" % sim


if __name__ == "__main__":
    main(sys.argv[1:])
