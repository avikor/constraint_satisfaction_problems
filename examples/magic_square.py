import time
import copy
import csp
from examples.performance_testing import measure_performance


# number of variables: n x n
# domain of each variable: 1, ..., n x n
# constraints:
#   1. global all different.
#   2. the values of all rows sum up to magic sum.
#   3. the values of all columns sum up to magic sum.
#   4. the values of both diagonals sum up to magic sum.

n = 3
order = n**2
magic_sum = n * int((order + 1) / 2)


name_to_variable_map = {square: csp.Variable(range(1, order + 1)) for square in range(1, order + 1)}

constraints = set()
constraints.add(csp.Constraint(name_to_variable_map.values(), csp.all_different))

exact_magic_sum = csp.ExactLengthExactSum(n, magic_sum)

for row in range(1, order + 1, n):
    constraints.add(csp.Constraint((name_to_variable_map[i] for i in range(row, row + n)),
                                   exact_magic_sum))

for column in range(1, n + 1):
    constraints.add(csp.Constraint((name_to_variable_map[i] for i in range(column, order + 1, n)),
                                   exact_magic_sum))

constraints.add(csp.Constraint((name_to_variable_map[diag] for diag in range(1, order + 1, n + 1)),
                               exact_magic_sum))
constraints.add(csp.Constraint((name_to_variable_map[diag] for diag in range(n, order, n - 1)),
                               exact_magic_sum))

magic_square_problem = csp.ConstraintProblem(constraints)


# /////////////////////////////////////////////// USAGE EXAMPLE ///////////////////////////////////////////////
# csp.heuristic_backtracking_search(magic_square_problem)
# for name in name_to_variable_map:
#    print(name, ":", name_to_variable_map[name].value)
#
# 1 : 2
# 2 : 7
# 3 : 6
# 4 : 9
# 5 : 5
# 6 : 1
# 7 : 4
# 8 : 3
# 9 : 8
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////


measure_performance(1, "magic_square_problem", magic_square_problem,
                    "backtracking_search", with_history=True)
measure_performance(1, "magic_square_problem", magic_square_problem,
                    "backtracking_search", inference=csp.forward_check, with_history=True)
measure_performance(1, "magic_square_problem", magic_square_problem,
                    "heuristic_backtracking_search", inference=None, with_history=True)
measure_performance(1, "magic_square_problem", magic_square_problem,
                    "heuristic_backtracking_search", with_history=True)
measure_performance(1, "magic_square_problem", magic_square_problem,
                    "naive_cycle_cutset", with_history=True)
measure_performance(2, "magic_square_problem", magic_square_problem,
                    "min_conflicts", 100000, with_history=True)
measure_performance(2, "magic_square_problem", magic_square_problem,
                    "constraints_weighting", 10000, with_history=True)
measure_performance(2, "magic_square_problem", magic_square_problem,
                    "simulated_annealing", 200000, 0.5, 0.99999)
measure_performance(2, "magic_square_problem", magic_square_problem,
                    "random_restart_first_choice_hill_climbing", 100, 100, 10)
general_genetic_magic_square_problem = csp.GeneralGeneticConstraintProblem(magic_square_problem, 0.1)
measure_performance(2, "general_genetic_magic_square_problem", general_genetic_magic_square_problem,
                    "genetic_local_search", 1000, 1000, 0.1)


ac3_magic_square_problem = copy.deepcopy(magic_square_problem)
ac3_magic_square_problem.unassign_all_variables()
ac3_start_time = time.process_time()
ac3_is_arc_consistent = csp.ac3(ac3_magic_square_problem)
ac3_end_time = time.process_time()
if ac3_is_arc_consistent:
    print()
    print()
    print("-" * 145)
    print("using ac3 as a preprocessing stage which took", ac3_end_time - ac3_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "ac3_magic_square_problem", ac3_magic_square_problem,
                        "backtracking_search", with_history=True)
    measure_performance(1, "ac3_magic_square_problem", ac3_magic_square_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "ac3_magic_square_problem", ac3_magic_square_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True)
    measure_performance(1, "ac3_magic_square_problem", ac3_magic_square_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "ac3_magic_square_problem", ac3_magic_square_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "ac3_magic_square_problem", ac3_magic_square_problem,
                        "min_conflicts", 100000, with_history=True)
    measure_performance(2, "ac3_magic_square_problem", ac3_magic_square_problem,
                        "constraints_weighting", 10000, with_history=True)
    measure_performance(2, "ac3_magic_square_problem", ac3_magic_square_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "ac3_magic_square_problem", ac3_magic_square_problem,
                        "random_restart_first_choice_hill_climbing", 100, 100, 10)
    general_genetic_ac3_magic_square_problem = csp.GeneralGeneticConstraintProblem(ac3_magic_square_problem, 0.1)
    measure_performance(2, "general_genetic_ac3_magic_square_problem", general_genetic_ac3_magic_square_problem,
                        "genetic_local_search", 1000, 100, 0.1)

ac4_magic_square_problem = copy.deepcopy(magic_square_problem)
ac4_magic_square_problem.unassign_all_variables()
ac4_start_time = time.process_time()
ac4_is_arc_consistent = csp.ac4(ac4_magic_square_problem)
ac4_end_time = time.process_time()
if ac4_is_arc_consistent:
    print()
    print()
    print("-" * 145)
    print("using ac4 as a preprocessing stage which took", ac4_end_time - ac4_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "ac4_magic_square_problem", ac4_magic_square_problem,
                        "backtracking_search", with_history=True)
    measure_performance(1, "ac4_magic_square_problem", ac4_magic_square_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "ac4_magic_square_problem", ac4_magic_square_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True)
    measure_performance(1, "ac4_magic_square_problem", ac4_magic_square_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "ac4_magic_square_problem", ac4_magic_square_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "ac4_magic_square_problem", ac4_magic_square_problem,
                        "min_conflicts", 100000, with_history=True)
    measure_performance(2, "ac4_magic_square_problem", ac4_magic_square_problem,
                        "constraints_weighting", 10000, with_history=True)
    measure_performance(2, "ac4_magic_square_problem", ac4_magic_square_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "ac4_magic_square_problem", ac4_magic_square_problem,
                        "random_restart_first_choice_hill_climbing", 100, 100, 10)
    general_genetic_ac4_magic_square_problem = csp.GeneralGeneticConstraintProblem(ac4_magic_square_problem, 0.1)
    measure_performance(2, "general_genetic_ac4_magic_square_problem", general_genetic_ac4_magic_square_problem,
                        "genetic_local_search", 100, 1000, 0.1)

pc2_magic_square_problem = copy.deepcopy(magic_square_problem)
pc2_magic_square_problem.unassign_all_variables()
pc2_start_time = time.process_time()
pc2_is_path_consistent = csp.pc2(pc2_magic_square_problem)
pc2_end_time = time.process_time()
if pc2_is_path_consistent:
    print()
    print()
    print("-" * 145)
    print("using pc2 as a preprocessing stage which took", pc2_end_time - pc2_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "pc2_magic_square_problem", pc2_magic_square_problem,
                        "backtracking_search", with_history=True)
    measure_performance(1, "pc2_magic_square_problem", pc2_magic_square_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "pc2_magic_square_problem", pc2_magic_square_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True)
    measure_performance(1, "pc2_magic_square_problem", pc2_magic_square_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "pc2_magic_square_problem", pc2_magic_square_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "pc2_magic_square_problem", pc2_magic_square_problem,
                        "min_conflicts", 100000, with_history=True)
    measure_performance(2, "pc2_magic_square_problem", pc2_magic_square_problem,
                        "constraints_weighting", 10000, with_history=True)
    measure_performance(2, "pc2_magic_square_problem", pc2_magic_square_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "pc2_magic_square_problem", pc2_magic_square_problem,
                        "random_restart_first_choice_hill_climbing", 100, 100, 10)
    general_genetic_pc2_magic_square_problem = csp.GeneralGeneticConstraintProblem(pc2_magic_square_problem, 0.1)
    measure_performance(2, "general_genetic_pc2_magic_square_problem", general_genetic_pc2_magic_square_problem,
                        "genetic_local_search", 1000, 1000, 0.1)

two_consistency_magic_square_problem = copy.deepcopy(magic_square_problem)
two_consistency_magic_square_problem.unassign_all_variables()
two_consistency_start_time = time.process_time()
is_two_consistent = csp.i_consistency(two_consistency_magic_square_problem, 2)
two_consistency_end_time = time.process_time()
if is_two_consistent:
    print()
    print()
    print("-" * 145)
    print("using 2-consistency as a preprocessing stage which took",
          two_consistency_end_time - two_consistency_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "two_consistency_magic_square_problem", two_consistency_magic_square_problem,
                        "backtracking_search", with_history=True)
    measure_performance(1, "two_consistency_magic_square_problem", two_consistency_magic_square_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "two_consistency_magic_square_problem", two_consistency_magic_square_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True)
    measure_performance(1, "two_consistency_magic_square_problem", two_consistency_magic_square_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "two_consistency_magic_square_problem", two_consistency_magic_square_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "two_consistency_magic_square_problem", two_consistency_magic_square_problem,
                        "min_conflicts", 100000, with_history=True)
    measure_performance(2, "two_consistency_magic_square_problem", two_consistency_magic_square_problem,
                        "constraints_weighting", 10000, with_history=True)
    measure_performance(2, "two_consistency_magic_square_problem", two_consistency_magic_square_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "two_consistency_magic_square_problem", two_consistency_magic_square_problem,
                        "random_restart_first_choice_hill_climbing", 100, 100, 10)
    general_genetic_two_consistency_magic_square_problem = \
        csp.GeneralGeneticConstraintProblem(two_consistency_magic_square_problem, 0.1)
    measure_performance(2, "general_genetic_two_consistency_magic_square_problem",
                        general_genetic_two_consistency_magic_square_problem, "genetic_local_search", 1000, 1000, 0.1)

