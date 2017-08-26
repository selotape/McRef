import argparse
from concurrent.futures import ProcessPoolExecutor
from functools import partial

from model_compare import compare_models, Result
from model_compare.util.general_purpose import timed
from model_compare.util.log import module_logger, tee_log

log = module_logger(__name__)


@timed
def main():
    args = parse_arguments()

    configured_compare_models = partial(compare_models, is_clade=args.clade)

    with ProcessPoolExecutor() as executor:
        results = executor.map(configured_compare_models, args.simulations)
        _print_results(results)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clade", help="enable clade reference model", action="store_true")
    parser.add_argument("simulations", nargs='+', help="space-delimited list of directories containing model_compare experiments")
    return parser.parse_args()


def _print_results(results):
    header = ','.join(Result._fields)

    print("Summary:")
    print(header)
    for result in results:
        tee_log(log.info, ','.join(str(f) for f in result))


if __name__ == "__main__":
    main()
