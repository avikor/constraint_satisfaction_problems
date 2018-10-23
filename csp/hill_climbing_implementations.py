from copy import deepcopy
from random import choice
from typing import Callable
from csp.constraint_problem import ConstraintProblem


StartStateGenerator = Callable[[ConstraintProblem], None]
ScoreCalculator = Callable[[ConstraintProblem], int]
SuccessorGenerator = Callable[[ConstraintProblem], ConstraintProblem]


def generate_start_state_randomly(constraint_problem: ConstraintProblem) -> None:
    constraint_problem.unassign_all_variables()
    for var in constraint_problem.get_variables():
        var.assign(choice(var.domain))


def consistent_constraints_amount(constraint_problem: ConstraintProblem) -> int:
    return len(constraint_problem.get_consistent_constraints())


def alter_random_variable_value_pair(constraint_problem: ConstraintProblem) -> ConstraintProblem:
    successor = deepcopy(constraint_problem)
    random_var = choice(tuple(successor.get_variables()))
    old_val = random_var.value
    random_var.unassign()
    possible_values = random_var.domain
    if len(possible_values) > 1:
        possible_values.remove(old_val)
    random_var.assign(choice(possible_values))
    return successor


def random_restart_first_choice_hill_climbing(constraint_problem: ConstraintProblem, max_restarts: int,
                                              max_steps: int, max_successors: int,
                                              generate_start_state: StartStateGenerator = generate_start_state_randomly,
                                              generate_successor: SuccessorGenerator = alter_random_variable_value_pair,
                                              calculate_score: ScoreCalculator = consistent_constraints_amount
                                              ) -> ConstraintProblem:
    generate_start_state(constraint_problem)
    if constraint_problem.is_completely_consistently_assigned():
        return constraint_problem
    max_restarts -= 1

    best_score = calculate_score(constraint_problem)
    best_score_problem = deepcopy(constraint_problem)
    for i in range(max_restarts):
        generate_start_state(constraint_problem)
        for j in range(max_steps):
            if constraint_problem.is_completely_consistently_assigned():
                return constraint_problem

            current_score = calculate_score(constraint_problem)
            if best_score < current_score:
                best_score = current_score
                best_score_problem = deepcopy(constraint_problem)

            for k in range(max_successors):
                successor = generate_successor(constraint_problem)
                successor_score = calculate_score(successor)
                if current_score < successor_score:
                    constraint_problem = successor
                    break

    return best_score_problem
