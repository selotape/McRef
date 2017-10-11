from collections import defaultdict

from attr import attrs, attrib
from attr.validators import instance_of, optional


def find_tau_bounds(root_event):
    tau_bounds = defaultdict(lambda: float('Inf'))

    _find_tau_bounds_rec(root_event, tau_bounds)

    return tau_bounds


def _find_tau_bounds_rec(event, tau_bounds):
    if event.lca_pop is not None:  # event is leaf
        tau_bounds[event.lca_pop] = event.time
        return

    _find_tau_bounds_rec(event.left, tau_bounds)
    _find_tau_bounds_rec(event.right, tau_bounds)

    event.lca_pop = lca(event.left.lca_pop, event.right.lca_pop)

    tau_bounds[event.lca_pop] = min(tau_bounds[event.lca_pop], event.time)


def ancestors(node):
    while node is not None:
        yield node
        node = node.father


def lca(left_node, right_node):
    if left_node is right_node:
        return left_node

    left_ancestors = list(ancestors(left_node))
    right_ancestors = list(ancestors(right_node))

    for node in left_ancestors:
        if node in right_ancestors:
            return node

    raise BadTreeError("left and right nodes did not share a common ancestor")


@attrs(hash=True)
class Population:
    name = attrib(validator=instance_of(str))
    father = attrib(default=None)


@attrs
class Event:
    time = attrib(validator=instance_of(float))
    left = attrib(default=None)
    right = attrib(default=None)
    lca_pop = attrib(validator=optional(instance_of(Population)), default=None)


class BadTreeError(Exception):
    pass
