from itertools import chain

from thesis_pseudo_code.phylogenetic_tree import is_leaf

num_coals_from_gphocs = intervals_from_gphocs = calculate_coal_stats = emit = lambda x: x


def merge_sort(*sequences):
    return sorted(list(chain(*sequences)))


def recursive_coal_stats(pop):
    pop_intervals = intervals_from_gphocs(pop)

    if is_leaf(pop):
        return pop_intervals

    left_intervals = recursive_coal_stats(pop.left)
    right_intervals = recursive_coal_stats(pop.right)
    merged_intervals = merge_sort(left_intervals, right_intervals)

    clade_intervals = merged_intervals.append(pop_intervals)

    clade_coal_stats = calculate_coal_stats(clade_intervals)
    emit(clade_coal_stats)

    return clade_intervals


def recursive_num_coals(pop):
    pop_num_coals = num_coals_from_gphocs(pop)

    if is_leaf(pop):
        return pop_num_coals

    left_num_coals = recursive_num_coals(pop.left)
    right_num_coals = recursive_num_coals(pop.right)

    current_num_coals = pop_num_coals + left_num_coals + right_num_coals
    emit(current_num_coals)

    return current_num_coals
