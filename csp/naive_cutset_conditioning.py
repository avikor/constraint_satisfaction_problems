from collections import deque
from itertools import product
from typing import Deque, Tuple, Any, Dict, List, Set, Optional, FrozenSet
from random import choice
from csp.variable import Variable
from csp.constraint import Constraint
from csp.constraint_problem import ConstraintProblem
from csp.tree_csp_solver_implementation import tree_csp_solver


# ///////////////////////////////////////// cutset conditioning algorithm /////////////////////////////////////////
# 1. find a cycle cutset, i.e. a set of variables that once removed from the constraint graph, the graph becomes a tree.
# 2. for each possible assignment to the cycle cutset variables which is consistent within their constraints:
#   a. remove from the domains of the remaining variables any values that are inconsistent with the partial assignment.
#   b. if the remaining CSP has a solution, return it together with the assignment for cycle cutset.
#
#
# how to find cycle cutset? finding a minimal cycle cutset is NP-hard. iterative compression might be the best option.
# but we don't require a minimal cycle cutset, just a cycle cutset.
# ergo a naive algorithm is implemented:
# 1. sort constrains by their lengths in descending order (longer to shorter).
# 2. find all the variables of the first (longest) constraint.
# 3. remove these variables from the graph, and see if it becomes a tree.
# 4. if it is a tree:
# 5.    go to step 2 in the aforementioned (upper) algorithm
# 6. else:
# 7.    repeat steps 2 and 3, but this time for first and second longest constraints, and so on...
# NOTE: this naive algorithm is incomplete (does not guarantee to find a solution).
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def naive_cycle_cutset(constraint_problem: ConstraintProblem, with_history: bool = False) \
        -> Optional[Deque[Tuple[Variable, Any]]]:
    actions_history = None
    if with_history:
        actions_history = deque()
    variables = constraint_problem.get_variables()
    read_only_variables = constraint_problem.get_assigned_variables()
    constraints = list(constraint_problem.get_constraints())
    constraints.sort(key=lambda constraint: len(constraint.variables), reverse=True)
    constraint_graph = constraint_problem.get_constraint_graph_as_adjacency_list()

    for i in range(1, len(constraints)):
        cutset_constraints = constraints[:i]
        cutset_variables = set()
        for cutset_const in cutset_constraints:
            cutset_variables.update(cutset_const.variables)
        reduced_graph = {var: neighbors for var, neighbors in constraint_graph.items() if var not in cutset_variables}
        for var in reduced_graph:
            reduced_graph[var] -= cutset_variables

        if __is_tree(reduced_graph):
            consistent_assignments_list = __get_consistent_assignments(cutset_variables, cutset_constraints,
                                                                       read_only_variables)
            non_cutset_variables = variables - cutset_variables
            non_cutset_vars_to_original_domains_map = {var: var.domain for var in non_cutset_variables}

            for consist_assignment in consistent_assignments_list:
                for var, value in zip(cutset_variables, consist_assignment):
                    if var not in read_only_variables:
                        var.assign(value)
                        if with_history:
                            actions_history.append((var, value))
                for non_cutset_var in non_cutset_variables:
                    if non_cutset_var not in read_only_variables:
                        non_cutset_var.domain = list(constraint_problem.get_consistent_domain(non_cutset_var))

                tree_csp_action_history = tree_csp_solver(constraint_problem, with_history)
                if with_history:
                    actions_history.extend(tree_csp_action_history)
                if constraint_problem.is_completely_consistently_assigned():
                    return actions_history

                for var in variables:
                    if var not in read_only_variables:
                        var.unassign()
                        if with_history:
                            actions_history.append((var, None))
                for var in non_cutset_vars_to_original_domains_map:
                    if var not in read_only_variables:
                        var.domain = non_cutset_vars_to_original_domains_map[var]

    return actions_history


__visited = set()


def __is_tree(reduced_graph: Dict[Variable, Set[Variable]]) -> bool:
    __visited.clear()
    if not reduced_graph:
        return False
    root = choice(tuple(reduced_graph.keys()))
    if __is_cyclic(reduced_graph, root, None):
        return False
    all_nodes = set()
    for node, neighbor in reduced_graph.items():
        all_nodes.add(node)
        all_nodes.update(reduced_graph[node])
    return len(__visited) == len(all_nodes)


def __is_cyclic(reduced_graph: Dict[Variable, Set[Variable]], node: Variable, parent: Optional[Variable]) -> bool:
    __visited.add(node)
    for neighbor in reduced_graph[node]:
        if neighbor not in __visited:
            if __is_cyclic(reduced_graph, neighbor, node):
                return True
        elif neighbor != parent:
            return True
    return False


def __get_consistent_assignments(cutset_variables: Set[Variable], cutset_constraints: List[Constraint],
                                 read_only_variables: FrozenSet[Variable]) -> list:
    domains = [var.domain for var in cutset_variables]
    consistent_assignments = list()
    for assignment in product(*domains):
        for var, value in zip(cutset_variables, assignment):
            if var not in read_only_variables:
                var.assign(value)
        if all(cutset_constraints):
            consistent_assignments.append(assignment)
        for var in cutset_variables:
            if var not in read_only_variables:
                var.unassign()
    return consistent_assignments
