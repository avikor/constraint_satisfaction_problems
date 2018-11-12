from typing import FrozenSet, Callable, Deque, Tuple, Any, Optional, Union, Dict, Iterator
from collections import deque
from csp.variable import Variable
from csp.constraint_problem import ConstraintProblem
from csp.domain_sorters import least_constraining_value
from csp.unassigned_variable_selectors import minimum_remaining_values, degree_heuristic


SelectUnassignedVariables = Callable[[ConstraintProblem, Optional[FrozenSet[Variable]]], FrozenSet[Variable]]
SortDomain = Callable[[ConstraintProblem, Variable], list]
Inference = Callable[[ConstraintProblem, Variable], bool]


__actions_history = deque()


def backtracking_search(constraint_problem: ConstraintProblem, inference: Optional[Inference] = None,
                        find_all_solutions: bool = False, with_history: bool = False) \
        -> Union[None, Deque[Tuple[Variable, Any]], Iterator[Dict[Variable, Any]]]:
    __actions_history.clear()
    if find_all_solutions and with_history:
        with_history = False

    if not find_all_solutions:
        next(__backtrack(constraint_problem, inference, find_all_solutions, with_history))
        if with_history:
            return __actions_history
        return

    return __backtrack(constraint_problem, inference, find_all_solutions, with_history)


def __backtrack(constraint_problem: ConstraintProblem, inference: Optional[Inference] = None,
                find_all_solutions: bool = False, with_history: bool = False) -> Optional[Dict[Variable, Any]]:
    variable, *_ = constraint_problem.get_unassigned_variables()
    for value in variable.domain:
        variable.assign(value)
        if with_history:
            __actions_history.append((variable, value))

        if inference is not None and not inference(constraint_problem, variable):
            variable.unassign()
            if with_history:
                __actions_history.append((variable, None))
            continue

        if constraint_problem.is_completely_assigned():
            if constraint_problem.is_consistently_assigned():
                if find_all_solutions:
                    yield constraint_problem.get_current_assignment()
                else:
                    yield None

            variable.unassign()
            if with_history:
                __actions_history.append((variable, None))
            continue

        if constraint_problem.is_consistently_assigned():
            for solution_assignment in __backtrack(constraint_problem, inference, find_all_solutions, with_history):
                yield solution_assignment

        variable.unassign()
        if with_history:
            __actions_history.append((variable, None))


def heuristic_backtracking_search(constraint_problem: ConstraintProblem,
                                  primary_select_unassigned_vars: SelectUnassignedVariables = minimum_remaining_values,
                                  secondary_select_unassigned_vars: Optional[SelectUnassignedVariables] =
                                  degree_heuristic,
                                  sort_domain: SortDomain = least_constraining_value,
                                  inference: Optional[Inference] = None,
                                  find_all_solutions: bool = False,
                                  with_history: bool = False) \
        -> Union[None, Deque[Tuple[Variable, Any]], Iterator[Dict[Variable, Any]]]:
    __actions_history.clear()
    if find_all_solutions and with_history:
        with_history = False

    if not find_all_solutions:
        next(__heuristic_backtrack(constraint_problem, primary_select_unassigned_vars,
                                   secondary_select_unassigned_vars, sort_domain, inference, find_all_solutions,
                                   with_history))
        if with_history:
            return __actions_history
        return

    return __heuristic_backtrack(constraint_problem, primary_select_unassigned_vars,
                                 secondary_select_unassigned_vars, sort_domain, inference, find_all_solutions,
                                 with_history)


def __heuristic_backtrack(constraint_problem: ConstraintProblem,
                          primary_select_unassigned_vars: SelectUnassignedVariables = minimum_remaining_values,
                          secondary_select_unassigned_vars: SelectUnassignedVariables = degree_heuristic,
                          sort_domain: SortDomain = least_constraining_value,
                          inference: Optional[Inference] = None,
                          find_all_solutions: bool = False,
                          with_history: bool = False) -> Optional[Dict[Variable, Any]]:
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
            continue

        if constraint_problem.is_completely_assigned():
            if constraint_problem.is_consistently_assigned():
                if find_all_solutions:
                    yield constraint_problem.get_current_assignment()
                else:
                    yield None

            selected_variable.unassign()
            if with_history:
                __actions_history.append((selected_variable, None))
            continue

        if constraint_problem.is_consistently_assigned():
            for solution_assignment in __heuristic_backtrack(constraint_problem, primary_select_unassigned_vars,
                                                             secondary_select_unassigned_vars, sort_domain, inference,
                                                             find_all_solutions, with_history):
                yield solution_assignment

        selected_variable.unassign()
        if with_history:
            __actions_history.append((selected_variable, None))


def forward_checking_backtracking_search(constraint_problem: ConstraintProblem, find_all_solutions: bool = False,
                                         with_history: bool = False) \
        -> Union[None, Deque[Tuple[Variable, Any]], Iterator[Dict[Variable, Any]]]:
    """ Optimized backtracking with forward checking. Instead of implementing forward checking as an Inference,
        It is written here directly.
        Advantage: saves the need to make a function call for forward checking, thus increasing performance.
        Disadvantage: violates DRY, makes the code less modular which might proof harder to maintain. """

    __actions_history.clear()
    if find_all_solutions and with_history:
        with_history = False

    if not find_all_solutions:
        next(__forward_checking_backtrack(constraint_problem, find_all_solutions, with_history))
        if with_history:
            return __actions_history
        return

    return __forward_checking_backtrack(constraint_problem, find_all_solutions, with_history)


def __forward_checking_backtrack(constraint_problem: ConstraintProblem, find_all_solutions: bool = False,
                                 with_history: bool = False) -> Optional[Dict[Variable, Any]]:
    variable, *_ = constraint_problem.get_unassigned_variables()
    for value in variable.domain:
        variable.assign(value)
        if with_history:
            __actions_history.append((variable, value))

        unassigned_neighbors_frozenset = constraint_problem.get_unassigned_neighbors(variable)
        unsatisfiable_neighbors = filter(lambda unassigned_neighbor:
                                         not constraint_problem.get_consistent_domain(unassigned_neighbor),
                                         unassigned_neighbors_frozenset)
        if any(unsatisfiable_neighbors):
            variable.unassign()
            if with_history:
                __actions_history.append((variable, None))
            continue

        if constraint_problem.is_completely_assigned():
            if constraint_problem.is_consistently_assigned():
                if find_all_solutions:
                    yield constraint_problem.get_current_assignment()
                else:
                    yield None

            variable.unassign()
            if with_history:
                __actions_history.append((variable, None))
            continue

        if constraint_problem.is_consistently_assigned():
            for solution_assignment in __forward_checking_backtrack(constraint_problem, find_all_solutions,
                                                                    with_history):
                yield solution_assignment

        variable.unassign()
        if with_history:
            __actions_history.append((variable, None))


def optimized_heuristic_backtracking_search(constraint_problem: ConstraintProblem,
                                            find_all_solutions: bool = False, with_history: bool = False) \
        -> Union[None, Deque[Tuple[Variable, Any]], Iterator[Dict[Variable, Any]]]:
    """ Optimized heuristic_backtracking_search. Instead of implementing Minimum Remaining Values, Degree Heuristic,
        and Least Constraining Value as functions, they are written here directly.
        Minimum Remaining Values as a primary selector, Degree Heuristic as a secondary selector.
        Also doesn't allow to add an Inference, such as forward checking or AC3.
        Advantage: saves the need to make function calls, thus increasing performance.
        Disadvantage: makes the code less modular which might proof harder to maintain, doesn't allow users to
                      implement their own heuristics, or change the order of existing heuristics.
                      Does not allow for inferences. """
    __actions_history.clear()
    if find_all_solutions and with_history:
        with_history = False

    if not find_all_solutions:
        next(__optimized_heuristic_backtrack(constraint_problem, find_all_solutions, with_history))
        if with_history:
            return __actions_history
        return

    return __optimized_heuristic_backtrack(constraint_problem, find_all_solutions, with_history)


def __optimized_heuristic_backtrack(constraint_problem: ConstraintProblem, find_all_solutions: bool = False,
                                    with_history: bool = False):
    unassigned_variables = constraint_problem.get_unassigned_variables()
    min_variable = min(unassigned_variables, key=lambda var: len(constraint_problem.get_consistent_domain(var)))
    min_remaining_values = len(constraint_problem.get_consistent_domain(min_variable))
    min_variables = filter(lambda var: len(constraint_problem.get_consistent_domain(var)) == min_remaining_values,
                           unassigned_variables)
    selected_unassigned_vars = frozenset(min_variables)
    if len(selected_unassigned_vars) > 1:
        selected_variable = max(selected_unassigned_vars,
                                key=lambda var: len(constraint_problem.get_unassigned_neighbors(var)))
    else:
        selected_variable, *_ = selected_unassigned_vars

    unassigned_neighbors = constraint_problem.get_unassigned_neighbors(selected_variable)

    def neighbors_consistent_domain_lengths(val) -> int:
        selected_variable.assign(val)
        consistent_domain_lengths = map(lambda neighbor: len((constraint_problem.get_consistent_domain(neighbor))),
                                        unassigned_neighbors)
        selected_variable.unassign()
        return sum(consistent_domain_lengths)

    sorted_domain = sorted(constraint_problem.get_consistent_domain(selected_variable),
                           key=neighbors_consistent_domain_lengths, reverse=True)

    for value in sorted_domain:
        selected_variable.assign(value)
        if with_history:
            __actions_history.append((selected_variable, value))

        if constraint_problem.is_completely_assigned():
            if constraint_problem.is_consistently_assigned():
                if find_all_solutions:
                    yield constraint_problem.get_current_assignment()
                else:
                    yield None

            selected_variable.unassign()
            if with_history:
                __actions_history.append((selected_variable, None))
            continue

        if constraint_problem.is_consistently_assigned():
            for solution_assignment in __optimized_heuristic_backtrack(constraint_problem, find_all_solutions,
                                                                       with_history):
                yield solution_assignment

        selected_variable.unassign()
        if with_history:
            __actions_history.append((selected_variable, None))


def classic_backtracking_search(constraint_problem: ConstraintProblem, inference: Optional[Inference] = None,
                                with_history: bool = False) -> Optional[Deque[Tuple[Variable, Any]]]:
    """ Backtracking which finds a single solution and quits. """
    __actions_history.clear()
    __classic_backtrack(constraint_problem, inference, with_history)
    if with_history:
        return __actions_history


def __classic_backtrack(constraint_problem: ConstraintProblem, inference: Optional[Inference] = None,
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

        if __classic_backtrack(constraint_problem, inference, with_history):
            return True

        selected_variable.unassign()
        if with_history:
            __actions_history.append((selected_variable, None))

    return False


def classic_heuristic_backtracking_search(constraint_problem: ConstraintProblem,
                                          primary_select_unassigned_vars: SelectUnassignedVariables =
                                          minimum_remaining_values,
                                          secondary_select_unassigned_vars: Optional[SelectUnassignedVariables] =
                                          degree_heuristic,
                                          sort_domain: SortDomain = least_constraining_value,
                                          inference: Optional[Inference] = None,
                                          with_history: bool = False) -> Optional[Deque[Tuple[Variable, Any]]]:
    """ Heuristic Backtracking which finds a single solution and quits. """
    __actions_history.clear()
    __classic_heuristic_backtrack(constraint_problem, primary_select_unassigned_vars,
                                  secondary_select_unassigned_vars, sort_domain, inference, with_history)
    if with_history:
        return __actions_history


def __classic_heuristic_backtrack(constraint_problem: ConstraintProblem,
                                  primary_select_unassigned_vars: SelectUnassignedVariables = minimum_remaining_values,
                                  secondary_select_unassigned_vars: SelectUnassignedVariables = degree_heuristic,
                                  sort_domain: SortDomain = least_constraining_value,
                                  inference: Optional[Inference] = None,
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

        if __classic_heuristic_backtrack(constraint_problem, primary_select_unassigned_vars,
                                         secondary_select_unassigned_vars, sort_domain, inference, with_history):
            return True

        selected_variable.unassign()
        if with_history:
            __actions_history.append((selected_variable, None))

    return False
