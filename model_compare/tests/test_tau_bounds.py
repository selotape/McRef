from math import isclose

import pytest

from thesis_pseudo_code.tau_bounds import ancestors, lca, find_tau_bounds, Population, Event, descendants


def test_ancestors():
    c = Population(name='c')
    b = Population(name='b', father=c)
    a = Population(name='a', father=b)

    assert list(ancestors(a)) == [a, b, c]


def test_descendants():
    a = Population(name='a')
    b = Population(name='b')
    c = Population(name='c')
    ab = Population(name='ab', left=a, right=b)
    abc = Population(name='abc', left=ab, right=c)

    assert set(descendants(ab)) == {a, b, ab}
    assert set(descendants(abc)) == {a, b, c, ab, abc}


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

    assert isclose(tau_bounds[ROOT], 1.0)


def test_large_pop_tree():
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

    c = Event(time=0.0, lca_pop=C)
    d = Event(time=0.0, lca_pop=D)
    cd = Event(time=0.6, left=c, right=d)

    r = Event(time=1.0, left=ab, right=cd)

    tau_bounds = find_tau_bounds(r)

    for pop, event in ((A, a), (B, b), (C, c), (D, d), (AB, ab), (CD, cd), (ROOT, r)):
        assert isclose(tau_bounds[pop], event.time)


def test_multiple_bounders():
    AB = Population(name='AB')
    A = Population(name='A', father=AB)
    B = Population(name='B', father=AB)

    a = Event(time=0.0, lca_pop=A)
    b = Event(time=0.0, lca_pop=B)
    c = Event(time=0.0, lca_pop=B)
    d = Event(time=0.0, lca_pop=B)
    ab = Event(time=0.5, left=a, right=b)
    abc = Event(time=0.6, left=ab, right=c)
    abcd = Event(time=0.7, left=abc, right=d)

    tau_bounds = find_tau_bounds(abcd)

    assert isclose(tau_bounds[AB], ab.time)


def test_bounder_bounds_multiple_pops():
    ABC = Population(name='ABC')
    AB = Population(name='AB', father=ABC)
    C = Population(name='C', father=ABC)
    A = Population(name='A', father=AB)
    B = Population(name='B', father=AB)
    AB.left, AB.right = A, B
    ABC.left, ABC.right = AB, C

    a = Event(time=0.0, lca_pop=A)
    c = Event(time=0.0, lca_pop=C)
    ac = Event(time=0.5, left=a, right=c)

    tau_bounds = find_tau_bounds(ac)

    assert isclose(tau_bounds[AB], ac.time)
    assert isclose(tau_bounds[ABC], ac.time)


if __name__ == '__main__':
    pytest.main()
