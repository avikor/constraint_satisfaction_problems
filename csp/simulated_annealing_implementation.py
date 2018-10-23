from copy import deepcopy
from math import exp
from random import uniform
from csp.constraint_problem import ConstraintProblem
from csp.hill_climbing_implementations import StartStateGenerator, ScoreCalculator, SuccessorGenerator, \
    generate_start_state_randomly, consistent_constraints_amount, alter_random_variable_value_pair


def simulated_annealing(constraint_problem: ConstraintProblem, max_steps: int, temperature: float, cooling_rate: float,
                        generate_start_state: StartStateGenerator = generate_start_state_randomly,
                        generate_successor: SuccessorGenerator = alter_random_variable_value_pair,
                        calculate_score: ScoreCalculator = consistent_constraints_amount) -> ConstraintProblem:
    generate_start_state(constraint_problem)
    if constraint_problem.is_completely_consistently_assigned():
        return constraint_problem
    max_steps -= 1

    best_score = calculate_score(constraint_problem)
    best_score_problem = deepcopy(constraint_problem)
    for i in range(max_steps):
        if constraint_problem.is_completely_consistently_assigned():
            return constraint_problem

        curr_score = calculate_score(constraint_problem)
        if best_score < curr_score:
            best_score = curr_score
            best_score_problem = deepcopy(constraint_problem)

        successor = generate_successor(constraint_problem)
        successor_score = calculate_score(successor)
        delta = successor_score - curr_score
        if delta > 0 or uniform(0, 1) < exp(delta / temperature):
            constraint_problem = successor
        temperature *= cooling_rate

    return best_score_problem
