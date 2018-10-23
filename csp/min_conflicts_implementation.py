from random import choice
from typing import Any, Deque, Tuple, FrozenSet, Optional
from collections import deque
from csp.variable import Variable
from csp.constraint_problem import ConstraintProblem


__tabu_queue = deque()


def min_conflicts(constraint_problem: ConstraintProblem, max_steps: int, tabu_size: int = -1,
                  with_history: bool = False) -> Optional[Deque[Tuple[Variable, Any]]]:
    __tabu_queue.clear()
    read_only_variables = constraint_problem.get_assigned_variables()

    if tabu_size == -1:
        tabu_size = 0
    assert tabu_size + len(read_only_variables) < len(constraint_problem.get_variables()), \
        "tabu_size + len(read_only_variables) is equal or bigger than constraint_problem's variables amount."
    if tabu_size == 0:
        tabu_size = -1

    actions_history = None
    if with_history:
        actions_history = deque()
    rand_assignmt_history = constraint_problem.assign_variables_with_random_values(read_only_variables, actions_history)
    if with_history:
        actions_history.extend(rand_assignmt_history)

    best_min_conflicts = len(constraint_problem.get_unsatisfied_constraints())
    best_min_conflicts_assignment = constraint_problem.get_current_assignment()
    for i in range(max_steps):
        if constraint_problem.is_completely_consistently_assigned():
            return actions_history

        conflicted_variable = __get_random_conflicted_variable(constraint_problem, read_only_variables, tabu_size)
        conflicted_variable.unassign()
        if with_history:
            actions_history.append((conflicted_variable, None))
        min_conflicts_value = __get_min_conflicts_value(constraint_problem, conflicted_variable)
        conflicted_variable.assign(min_conflicts_value)
        if with_history:
            actions_history.append((conflicted_variable, min_conflicts_value))

        if len(__tabu_queue) == tabu_size:
            __tabu_queue.popleft()
        if __tabu_queue:
            __tabu_queue.append(conflicted_variable)

        curr_conflicts_count = len(constraint_problem.get_unsatisfied_constraints())
        if curr_conflicts_count < best_min_conflicts:
            best_min_conflicts = curr_conflicts_count
            best_min_conflicts_assignment = constraint_problem.get_current_assignment()

    constraint_problem.unassign_all_variables()
    constraint_problem.assign_variables_from_assignment(best_min_conflicts_assignment)
    return actions_history


def __get_random_conflicted_variable(constraint_problem: ConstraintProblem, read_only_variables: FrozenSet[Variable],
                                     tabu_size: int) -> Variable:
    conflicted_variables = set()
    for constraint in constraint_problem.get_unsatisfied_constraints():
        conflicted_variables.update(constraint.variables)
    conflicted_variables -= read_only_variables
    if tabu_size != -1:
        untabued_conflicted_variables = conflicted_variables - set(__tabu_queue)
        return choice(tuple(untabued_conflicted_variables))
    return choice(tuple(conflicted_variables))


def __get_min_conflicts_value(constraint_problem: ConstraintProblem, conflicted_variable: Variable) -> Any:
    min_conflicts_count = float("inf")
    min_conflicting_values = list()
    for value in conflicted_variable.domain:
        conflicted_variable.assign(value)
        conflicts_count = len(constraint_problem.get_unsatisfied_constraints())
        if conflicts_count < min_conflicts_count:
            min_conflicts_count = conflicts_count
            min_conflicting_values.clear()
            min_conflicting_values.append(value)
        elif conflicts_count == min_conflicts_count:
            min_conflicting_values.append(value)
        conflicted_variable.unassign()

    return choice(min_conflicting_values)

