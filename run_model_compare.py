import argparse
from concurrent.futures import ProcessPoolExecutor
from functools import partial

from tqdm import tqdm

from model_compare import compare_models, Result
from model_compare.util.general_purpose import timed
from model_compare.util.log import module_logger, tee_log

_log = module_logger(__name__)


@timed
def main():
    args = _parse_arguments()

    configured_compare_models = partial(compare_models, is_clade=args.clade)

    with ProcessPoolExecutor(max_workers=args.max_workers) as executor:
        results = executor.map(configured_compare_models, args.simulations)
        _print_results(results, args.simulations)


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clade", help="enable clade reference model", action="store_true")
    parser.add_argument("--max-workers", help="maximum number of processes to spawn. Default is #available-cpu", type=int, default=None)
    parser.add_argument("simulations", nargs='+', help="space-delimited list of directories containing model_compare experiments")
    return parser.parse_args()


def _print_results(results, simulations):
    simulation_results = [ret for ret in tqdm(results, total=len(simulations))]

    header = ','.join(Result._fields)
    print("Summary:")
    print(header)
    for sim_res in simulation_results:
        tee_log(_log.info, ','.join(str(f) for f in sim_res))


if __name__ == "__main__":
    main()
