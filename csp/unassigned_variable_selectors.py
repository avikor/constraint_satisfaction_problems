from typing import FrozenSet, Optional
from csp.variable import Variable
from csp.constraint_problem import ConstraintProblem


def first_encountered_unassigned_variable(constraint_problem: ConstraintProblem) -> FrozenSet[Variable]:
    first_unassigned_variable, *_ = constraint_problem.get_unassigned_variables()
    return frozenset({first_unassigned_variable})


def minimum_remaining_values(constraint_problem: ConstraintProblem,
                             variables: Optional[FrozenSet[Variable]] = None) -> FrozenSet[Variable]:
    if variables is not None:  # then we're using minimum_remaining_values as secondary key
        min_variable = min(variables, key=lambda variable: len(constraint_problem.get_consistent_domain(variable)))
        return frozenset({min_variable})

    unassigned_variables = constraint_problem.get_unassigned_variables()
    min_variable = min(unassigned_variables, key=lambda var: len(constraint_problem.get_consistent_domain(var)))
    min_remaining_values = len(constraint_problem.get_consistent_domain(min_variable))
    min_variables = filter(lambda var: len(constraint_problem.get_consistent_domain(var)) == min_remaining_values,
                           unassigned_variables)
    return frozenset(min_variables)


def degree_heuristic(constraint_problem: ConstraintProblem,
                     variables: Optional[FrozenSet[Variable]] = None) -> FrozenSet[Variable]:
    if variables is not None:  # then we're using degree_heuristic as secondary key
        max_variable = max(variables, key=lambda var: len(constraint_problem.get_unassigned_neighbors(var)))
        return frozenset({max_variable})

    unassigned_variables = constraint_problem.get_unassigned_variables()
    max_variable = max(unassigned_variables, key=lambda var: len(constraint_problem.get_unassigned_neighbors(var)))
    max_degree = len(constraint_problem.get_unassigned_neighbors(max_variable))
    max_variables = filter(lambda var: len(constraint_problem.get_unassigned_neighbors(var)) == max_degree,
                           unassigned_variables)
    return frozenset(max_variables)
