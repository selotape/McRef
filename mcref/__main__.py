import argparse
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from typing import List

from tabulate import tabulate
from tqdm import tqdm

sys.path.append(os.getcwd())

from mcref.model_compare import run_simulation, Result
from mcref.util.general_purpose import timed
from mcref.util.log import module_logger, tee_log


_log = module_logger(__name__)



@timed
def main():
    args = _parse_arguments()

    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        futures = executor.map(run_simulation, args.simulations)
        results = list(tqdm(futures, total=len(args.simulations)))
        _print_results(results)


def _parse_arguments():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--purge-results", help="Delete all previous simulation results", action="store_true") # TODO
    parser.add_argument("simulations", nargs='+', help="space-delimited list of directories containing model_compare experiments")
    return parser.parse_args()


def _print_results(results: List[Result]):
    results_table = tabulate(results, headers=Result._fields)
    tee_log(_log.info, '\n' + results_table)


if __name__ == "__main__":
    main()
