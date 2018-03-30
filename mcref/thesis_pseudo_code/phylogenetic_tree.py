from attr import attrs, attrib
from attr.validators import instance_of, optional


@attrs(hash=True)
class Population:
    name = attrib(validator=instance_of(str))
    father = attrib(default=None, repr=False, hash=False)  # type: Population
    left = attrib(default=None, repr=False, hash=False)  # type: Population
    right = attrib(default=None, repr=False, hash=False)  # type: Population


@attrs
class Event:
    time = attrib(validator=instance_of(float))
    left = attrib(default=None, repr=False)  # type: Event
    right = attrib(default=None, repr=False)  # type: Event
    lca_pop = attrib(validator=optional(instance_of(Population)), default=None, repr=False)  # type: Population


def lca(node1, node2):
    ancestors1 = list(ancestors(node1))
    ancestors2 = list(ancestors(node2))

    return first_intersection(ancestors1, ancestors2)


def ancestors(node):
    while node is not None:
        yield node
        node = node.father


def descendants(node):
    if node is not None:
        yield from descendants(node.left)
        yield from descendants(node.right)
        yield node


def first_intersection(l1, l2):
    return next((item for item in l1 if item in l2), None)


def is_leaf(node):
    return node.left is None and node.right