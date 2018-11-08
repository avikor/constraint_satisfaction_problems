from typing import FrozenSet, Callable, Deque, Tuple, Any, Optional
from collections import deque
from csp.variable import Variable
from csp.constraint_problem import ConstraintProblem
from csp.domain_sorters import least_constraining_value
from csp.unassigned_variable_selectors import minimum_remaining_values, degree_heuristic
from csp.forward_checking_implementation import forward_check


SelectUnassignedVariables = Callable[[ConstraintProblem, Optional[FrozenSet[Variable]]], FrozenSet[Variable]]
SortDomain = Callable[[ConstraintProblem, Variable], list]
Inference = Callable[[ConstraintProblem, Variable], bool]


__actions_history = deque()


def backtracking_search(constraint_problem: ConstraintProblem, inference: Optional[Inference] = None,
                        with_history: bool = False) -> Optional[Deque[Tuple[Variable, Any]]]:
    __actions_history.clear()
    __backtrack(constraint_problem, inference, with_history)
    if with_history:
        return __actions_history


def __backtrack(constraint_problem: ConstraintProblem, inference: Optional[Inference] = None,
                with_history: bool = False) -> bool:
    if constraint_problem.is_completely_assigned():
        if constraint_problem.is_consistently_assigned():
            return True
        return False

    selected_variable, *_ = constraint_problem.get_unassigned_variables()

    for value in selected_variable.domain:
        selected_variable.assign(value)
        if with_history:
            __actions_history.append((selected_variable, value))

        if inference is not None and not inference(constraint_problem, selected_variable):
            selected_variable.unassign()
            if with_history:
                __actions_history.append((selected_variable, None))
            return False

        if __backtrack(constraint_problem, inference, with_history):
            return True

        selected_variable.unassign()
        if with_history:
            __actions_history.append((selected_variable, None))

    return False


def heuristic_backtracking_search(constraint_problem: ConstraintProblem,
                                  primary_select_unassigned_vars: SelectUnassignedVariables = minimum_remaining_values,
                                  secondary_select_unassigned_vars: Optional[SelectUnassignedVariables] =
                                  degree_heuristic,
                                  sort_domain: SortDomain = least_constraining_value,
                                  inference: Optional[Inference] = None,
                                  with_history: bool = False) -> Optional[Deque[Tuple[Variable, Any]]]:
    __actions_history.clear()
    __heuristic_backtrack(constraint_problem, primary_select_unassigned_vars,
                          secondary_select_unassigned_vars, sort_domain, inference, with_history)
    if with_history:
        return __actions_history


def __heuristic_backtrack(constraint_problem: ConstraintProblem,
                          primary_select_unassigned_vars: SelectUnassignedVariables = minimum_remaining_values,
                          secondary_select_unassigned_vars: SelectUnassignedVariables = degree_heuristic,
                          sort_domain: SortDomain = least_constraining_value,
                          inference: Optional[Inference] = forward_check,
                          with_history: bool = False) -> bool:
    if constraint_problem.is_completely_assigned():
        if constraint_problem.is_consistently_assigned():
            return True
        return False

    selected_unassigned_vars = primary_select_unassigned_vars(constraint_problem, None)
    if secondary_select_unassigned_vars is not None and len(selected_unassigned_vars) > 1:
        selected_unassigned_vars = secondary_select_unassigned_vars(constraint_problem, selected_unassigned_vars)
    selected_variable, *_ = selected_unassigned_vars

    sorted_domain = sort_domain(constraint_problem, selected_variable)
    for value in sorted_domain:
        selected_variable.assign(value)
        if with_history:
            __actions_history.append((selected_variable, value))

        if inference is not None and not inference(constraint_problem, selected_variable):
            selected_variable.unassign()
            if with_history:
                __actions_history.append((selected_variable, None))
            return False

        if __heuristic_backtrack(constraint_problem, primary_select_unassigned_vars,
                                 secondary_select_unassigned_vars, sort_domain, inference, with_history):
            return True

        selected_variable.unassign()
        if with_history:
            __actions_history.append((selected_variable, None))

    return False

