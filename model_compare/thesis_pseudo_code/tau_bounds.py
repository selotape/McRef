from collections import defaultdict

from thesis_pseudo_code.phylogenetic_tree import lca, descendants


def find_tau_bounds(genealogy_root):
    tau_bounds = defaultdict(lambda: float('Inf'))

    _find_tau_bounds_rec(genealogy_root, tau_bounds)

    return tau_bounds


def _find_tau_bounds_rec(event, tau_bounds):
    if event.lca_pop is not None:  # event is a leaf
        tau_bounds[event.lca_pop] = event.time
        return

    _find_tau_bounds_rec(event.left, tau_bounds)
    _find_tau_bounds_rec(event.right, tau_bounds)

    event.lca_pop = lca(event.left.lca_pop, event.right.lca_pop)

    for pop in descendants(event.lca_pop):
        tau_bounds[pop] = min(tau_bounds[pop], event.time)
