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


def lca(left_node, right_node):
    left_ancestors = list(ancestors(left_node))
    right_ancestors = list(ancestors(right_node))

    return first_intersection(left_ancestors, right_ancestors)


def ancestors(node):
    while node is not None:
        yield node
        node = node.father


def first_intersection(l1, l2):
    for item in l1:
        if item in l2:
            return item


@attrs(hash=True)
class Population:
    name = attrib(validator=instance_of(str))
    father = attrib(default=None)  # type: Population


@attrs
class Event:
    time = attrib(validator=instance_of(float))
    left = attrib(default=None)  # type: Event
    right = attrib(default=None)  # type: Event
    lca_pop = attrib(validator=optional(instance_of(Population)), default=None)
