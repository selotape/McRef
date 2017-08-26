import argparse
import os
from concurrent.futures import ProcessPoolExecutor
from functools import partial

from model_compare import compare_models, Result
from model_compare.util.general_purpose import timed
from model_compare.util.log import configure_logging


@timed
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clade", help="enable clade reference model", action="store_true")
    parser.add_argument("simulations", nargs='+', help="space-delimited list of directories containing model_compare experiments")
    args = parser.parse_args()

    configured_compare_models = partial(compare_models, is_clade=args.clade)

    with ProcessPoolExecutor() as executor:
        results = executor.map(configured_compare_models, args.simulations)
        _print_results(results)


def _print_results(results):
    print(','.join(Result._fields))
    for result in results:
        print(','.join(str(f) for f in result))


def is_valid_simulation(sim):
    return os.path.isdir(sim) and os.path.isfile(sim + '/' + 'config.ini')


if __name__ == "__main__":
    configure_logging('DEBUG', 'model_compare.log')
    main()
