from collections import defaultdict
from math import isclose

import pytest
from attr import attrs, attrib
from attr.validators import instance_of, optional


def ancestors(node):
    while node is not None:
        yield node
        node = node.father


class BadTreeError(Exception):
    pass


def lca(left_pop, right_pop):
    if left_pop is right_pop:
        return left_pop

    left_ancestors = list(ancestors(left_pop))
    right_ancestors = list(ancestors(right_pop))

    for pop in left_ancestors:
        if pop in right_ancestors:
            return pop

    raise BadTreeError("left and right pop did not share a common ancestor")


def _find_bounds_rec(event, tau_bounds):
    if event.lca_pop is not None:  # event is leaf
        tau_bounds[event.lca_pop.name] = event.time
        return

    _find_bounds_rec(event.left, tau_bounds)
    _find_bounds_rec(event.right, tau_bounds)

    event.lca_pop = lca(event.left.lca_pop, event.right.lca_pop)

    tau_bounds[event.lca_pop.name] = min(tau_bounds[event.lca_pop.name], event.time)


def find_tau_bounds(root_event):
    tau_bounds = defaultdict(lambda: float('Inf'))

    _find_bounds_rec(root_event, tau_bounds)

    return tau_bounds


@attrs
class Population:
    name = attrib(validator=instance_of(str))
    father = attrib(default=None)


@attrs
class Event:
    time = attrib(validator=instance_of(float))
    left = attrib(default=None)
    right = attrib(default=None)
    lca_pop = attrib(validator=optional(instance_of(Population)), default=None)


def test_ancestors():
    c = Population(name='c')
    b = Population(name='b', father=c)
    a = Population(name='a', father=b)

    assert list(ancestors(a)) == [a, b, c]


def test_lca():
    AB = Population(name='AB')
    A = Population(name='A', father=AB)
    B = Population(name='B', father=AB)

    assert lca(A, B) is AB


def test_tau_bounds_sanity():
    ROOT = Population(name='ROOT')
    A = Population(name='A', father=ROOT)
    B = Population(name='B', father=ROOT)
    a = Event(time=0.0, lca_pop=A)
    b = Event(time=0.0, lca_pop=B)
    r = Event(time=1.0, left=a, right=b)
    tau_bounds = find_tau_bounds(r)

    assert isclose(tau_bounds['ROOT'], 1.0, rel_tol=0.001)


def test_tau_bounds():
    ROOT = Population(name='ROOT')

    AB = Population(name='AB', father=ROOT)
    A = Population(name='A', father=AB)
    B = Population(name='B', father=AB)

    CD = Population(name='CD', father=ROOT)
    C = Population(name='C', father=CD)
    D = Population(name='D', father=CD)

    a = Event(time=0.0, lca_pop=A)
    b = Event(time=0.0, lca_pop=B)
    ab = Event(time=0.5, left=a, right=b)

    c = Event(time=0.0)
    d = Event(time=0.0)
    cd = Event(time=0.6, left=c, right=d)

    r = Event(time=1.0, left=ab, right=cd)

    tau_bounds = find_tau_bounds(r, (A, B, C, D, AB, CD, ROOT))

    for pop, event in ((A, a), (B, b), (C, c), (D, d), (AB, ab), (CD, cd), (ROOT, r)):
        assert isclose(tau_bounds[pop.name], event.time)


if __name__ == '__main__':
    pytest.main()
