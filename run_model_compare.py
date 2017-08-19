import os
import sys

from model_compare import compare_models


def main(args):
    simulation, is_clade = _parse_args(args)
    compare_models(simulation, is_clade)


def _parse_args(args):
    is_clade = False
    simulation = None
    if len(args) == 0:
        print_usage_and_exit()
    else:
        simulation = args[0]
    if len(args) == 2:
        if args[1] != '--clade':
            print_usage_and_exit(err_msg="'%s' is not a valid argument" % args[1])
        else:
            is_clade = True

    if not is_valid_simulation(simulation):
        print_usage_and_exit(err_msg="'%s' is not a valid simulation dir" % simulation)

    return simulation, is_clade


def print_usage_and_exit(err_msg=''):
    if err_msg: print(err_msg, file=sys.stderr)
    print(r"Usage: >>> python ./run_model_compare.py ./path/to/config_dir [--clade]")
    exit()


def is_valid_simulation(sim):
    return os.path.isdir(sim) and os.path.isfile(sim + '/' + 'config.ini')


if __name__ == "__main__":
    main(sys.argv[1:])
