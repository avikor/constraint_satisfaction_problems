from typing import Deque, Tuple, Any, List, Optional
from collections import deque, defaultdict
from csp.variable import Variable
from csp.constraint_problem import ConstraintProblem


def tree_csp_solver(constraint_problem: ConstraintProblem, with_history: bool = False) \
        -> Optional[Deque[Tuple[Variable, Any]]]:
    actions_history = None
    if with_history:
        actions_history = deque()
    topological_sorted_unassigned_variables = __kahn_topological_sort(constraint_problem)
    if not topological_sorted_unassigned_variables:
        return actions_history

    for i in range(len(topological_sorted_unassigned_variables) - 1, 0, -1):
        for value in topological_sorted_unassigned_variables[i].domain:
            topological_sorted_unassigned_variables[i].assign(value)
            if not constraint_problem.get_consistent_domain(topological_sorted_unassigned_variables[i-1]):
                topological_sorted_unassigned_variables[i].remove_from_domain(value)
            topological_sorted_unassigned_variables[i].unassign()
        if not topological_sorted_unassigned_variables[i].domain:
            return actions_history

    for variable in topological_sorted_unassigned_variables:
        consistent_domain = constraint_problem.get_consistent_domain(variable)
        if not consistent_domain:
            return actions_history
        value, *_ = consistent_domain
        variable.assign(value)
        if with_history:
            actions_history.append((variable, value))

    return actions_history


def __kahn_topological_sort(constraint_problem: ConstraintProblem) -> List[Variable]:
    variables = constraint_problem.get_unassigned_variables()
    directed_graph = defaultdict(set)
    for var in variables:
        for neighbor in constraint_problem.get_unassigned_neighbors(var):
            if var not in directed_graph[neighbor]:
                directed_graph[var].add(neighbor)

    in_degree = {var: 0 for var in variables}
    for var in variables:
        for neighbor in directed_graph[var]:
            in_degree[neighbor] += 1

    zero_in_degree_variables = set(filter(lambda variable: in_degree[variable] == 0, in_degree.keys()))
    topologically_sorted_unassigned_variables = list()
    while zero_in_degree_variables:
        var = zero_in_degree_variables.pop()
        topologically_sorted_unassigned_variables.append(var)
        for neighbor in directed_graph[var]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                zero_in_degree_variables.add(neighbor)

    if len(topologically_sorted_unassigned_variables) != len(variables):
        return list()
    return topologically_sorted_unassigned_variables
