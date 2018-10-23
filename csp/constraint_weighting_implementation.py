from typing import Dict, Any, Tuple, Deque, FrozenSet, Optional
from collections import deque
from itertools import filterfalse
from csp.constraint import Constraint
from csp.variable import Variable
from csp.constraint_problem import ConstraintProblem


def constraints_weighting(constraint_problem: ConstraintProblem, max_tries: int, with_history: bool = False) \
        -> Optional[Deque[Tuple[Variable, Any]]]:
    actions_history = None
    if with_history:
        actions_history = deque()
    constraints_weights = {constraint: 1 for constraint in constraint_problem.get_constraints()}
    read_only_variables = constraint_problem.get_assigned_variables()

    for i in range(max_tries):
        constraint_problem.assign_variables_with_random_values(read_only_variables)
        last_reduction = float("inf")
        while 0 < last_reduction:
            if constraint_problem.is_completely_consistently_assigned():
                return actions_history

            reduction, variable, value = __get_best_reduction_variable_value(constraint_problem, constraints_weights,
                                                                             read_only_variables)
            variable.unassign()
            if with_history:
                actions_history.append((variable, None))
            variable.assign(value)
            if with_history:
                actions_history.append((variable, value))
            last_reduction = reduction

            for unsatisfied_constraint in constraint_problem.get_unsatisfied_constraints():
                constraints_weights[unsatisfied_constraint] += 1

        if i != max_tries - 1:
            constraint_problem.unassign_all_variables(read_only_variables)

    return actions_history


def __get_best_reduction_variable_value(constraint_problem: ConstraintProblem,
                                        constraints_weights: Dict[Constraint, int],
                                        read_only_variables: FrozenSet[Variable]) -> Tuple[int, Variable, Any]:
    pairs_to_weight_reduction = dict()
    weight = __calculate_weight(constraint_problem, constraints_weights)
    original_assignment = constraint_problem.get_current_assignment()
    constraint_problem.unassign_all_variables()
    for variable in constraint_problem.get_variables() - read_only_variables:
        for value in variable.domain:
            variable.assign(value)
            curr_weight = __calculate_weight(constraint_problem, constraints_weights)
            pairs_to_weight_reduction[(variable, value)] = weight - curr_weight
            variable.unassign()

    constraint_problem.unassign_all_variables()
    constraint_problem.assign_variables_from_assignment(original_assignment)
    max_variable, max_value = max(pairs_to_weight_reduction, key=pairs_to_weight_reduction.get)
    return pairs_to_weight_reduction[(max_variable, max_value)], max_variable, max_value


def __calculate_weight(constraint_problem: ConstraintProblem, constraints_weights: Dict[Constraint, int]) -> int:
    weight = 0
    for variable in constraint_problem.get_variables():
        unsatisfied_constraints = filterfalse(None, constraint_problem.get_constraints_containing_variable(variable))
        for unsatisfied_const in unsatisfied_constraints:
            weight += constraints_weights[unsatisfied_const]
    return weight
