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
                    "heuristic_backtracking_search", with_history=True)
measure_performance(1, "magic_square_problem", magic_square_problem,
                    "heuristic_backtracking_search", inference=csp.forward_check, with_history=True)
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
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "ac3_magic_square_problem", ac3_magic_square_problem,
                        "heuristic_backtracking_search", inference=csp.forward_check, with_history=True)
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
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "ac4_magic_square_problem", ac4_magic_square_problem,
                        "heuristic_backtracking_search", inference=csp.forward_check, with_history=True)
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
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "pc2_magic_square_problem", pc2_magic_square_problem,
                        "heuristic_backtracking_search", inference=csp.forward_check, with_history=True)
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
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "two_consistency_magic_square_problem", two_consistency_magic_square_problem,
                        "heuristic_backtracking_search", inference=csp.forward_check, with_history=True)
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


# /////////////////////////////////////////////////////// PERFORMANCE RESULTS /////////////////////////////////////////////////////////////////////
###################################################################################################################################################
# displaying performance results of solver: 'backtracking_search' with problem: 'magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [56757465]
# time results (seconds): [379.9375]
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search_with_forward_checking' with problem: 'magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [56757465]
# time results (seconds): [1758.96875]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search' with problem: 'magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [45]
# time results (seconds): [1.828125]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search_with_forward_checking' with problem: 'magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [45]
# time results (seconds): [0.21875]
# #################################################################################################################################################
# displaying performance results of solver: 'naive_cycle_cutset' with problem: 'magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [9]
# solution lengths (number of assignment and unassignment actions): [0]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'min_conflicts' with problem: 'magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [2, 2]
# solution lengths (number of assignment and unassignment actions): [200018, 200018]
# time results (seconds): [87.375, 87.40625]
# #################################################################################################################################################
# displaying performance results of solver: 'constraints_weighting' with problem: 'magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [9, 9]
# solution lengths (number of assignment and unassignment actions): [20000, 20000]
# time results (seconds): [31.40625, 31.421875]
# #################################################################################################################################################
# displaying performance results of solver: 'simulated_annealing' with problem: 'magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [0, 0]
# time results (seconds): [46.8125, 25.640625]
# #################################################################################################################################################
# displaying performance results of solver: 'random_restart_first_choice_hill_climbing' with problem: 'magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [0, 1]
# time results (seconds): [41.8125, 95.71875]
# #################################################################################################################################################
# displaying performance results of solver: 'genetic_local_search' with problem: 'general_genetic_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [1, 1]
# time results (seconds): [180.265625, 195.375]
#
#
# -------------------------------------------------------------------------------------------------------------------------------------------------
# using ac3 as a preprocessing stage which took 0.078125 seconds
# -------------------------------------------------------------------------------------------------------------------------------------------------
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search' with problem: 'ac3_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [63022473]
# time results (seconds): [414.375]
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search_with_forward_checking' with problem: 'ac3_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [63022473]
# time results (seconds): [1664.9375]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search' with problem: 'ac3_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [65]
# time results (seconds): [1.9375]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search_with_forward_checking' with problem: 'ac3_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [65]
# time results (seconds): [0.296875]
# #################################################################################################################################################
# displaying performance results of solver: 'naive_cycle_cutset' with problem: 'ac3_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [9]
# solution lengths (number of assignment and unassignment actions): [0]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'min_conflicts' with problem: 'ac3_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [3, 3]
# solution lengths (number of assignment and unassignment actions): [200018, 200018]
# time results (seconds): [84.859375, 85.25]
# #################################################################################################################################################
# displaying performance results of solver: 'constraints_weighting' with problem: 'ac3_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [9, 8]
# solution lengths (number of assignment and unassignment actions): [20000, 20000]
# time results (seconds): [31.828125, 31.90625]
# #################################################################################################################################################
# displaying performance results of solver: 'simulated_annealing' with problem: 'ac3_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [1, 0]
# time results (seconds): [107.984375, 1.8125]
# #################################################################################################################################################
# displaying performance results of solver: 'random_restart_first_choice_hill_climbing' with problem: 'ac3_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [1, 1]
# time results (seconds): [96.359375, 95.78125]
# #################################################################################################################################################
# displaying performance results of solver: 'genetic_local_search' with problem: 'general_genetic_ac3_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [1, 1]
# time results (seconds): [19.640625, 19.6875]
#
#
# -------------------------------------------------------------------------------------------------------------------------------------------------
# using ac4 as a preprocessing stage which took 0.015625 seconds
# -------------------------------------------------------------------------------------------------------------------------------------------------
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search' with problem: 'ac4_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [56062539]
# time results (seconds): [358.40625]
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search_with_forward_checking' with problem: 'ac4_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [56062539]
# time results (seconds): [1911.171875]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search' with problem: 'ac4_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [35]
# time results (seconds): [1.71875]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search_with_forward_checking' with problem: 'ac4_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [35]
# time results (seconds): [0.171875]
# #################################################################################################################################################
# displaying performance results of solver: 'naive_cycle_cutset' with problem: 'ac4_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [9]
# solution lengths (number of assignment and unassignment actions): [0]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'min_conflicts' with problem: 'ac4_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [1, 2]
# solution lengths (number of assignment and unassignment actions): [200018, 200018]
# time results (seconds): [81.71875, 81.21875]
# #################################################################################################################################################
# displaying performance results of solver: 'constraints_weighting' with problem: 'ac4_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [8, 7]
# solution lengths (number of assignment and unassignment actions): [20000, 20000]
# time results (seconds): [30.359375, 30.328125]
# #################################################################################################################################################
# displaying performance results of solver: 'simulated_annealing' with problem: 'ac4_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [0, 0]
# time results (seconds): [18.46875, 6.796875]
# #################################################################################################################################################
# displaying performance results of solver: 'random_restart_first_choice_hill_climbing' with problem: 'ac4_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [1, 1]
# time results (seconds): [95.5, 102.53125]
# #################################################################################################################################################
# displaying performance results of solver: 'genetic_local_search' with problem: 'general_genetic_ac4_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [3, 4]
# time results (seconds): [18.46875, 17.796875]
#
#
# -------------------------------------------------------------------------------------------------------------------------------------------------
# using 2-consistency as a preprocessing stage which took 1.625 seconds
# -------------------------------------------------------------------------------------------------------------------------------------------------
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search' with problem: 'two_consistency_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [27706725]
# time results (seconds): [262.15625]
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search_with_forward_checking' with problem: 'two_consistency_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [27706725]
# time results (seconds): [977.09375]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search' with problem: 'two_consistency_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [53]
# time results (seconds): [1.109375]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search_with_forward_checking' with problem: 'two_consistency_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [53]
# time results (seconds): [0.453125]
# #################################################################################################################################################
# displaying performance results of solver: 'naive_cycle_cutset' with problem: 'two_consistency_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [9]
# solution lengths (number of assignment and unassignment actions): [0]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'min_conflicts' with problem: 'two_consistency_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [1, 4]
# solution lengths (number of assignment and unassignment actions): [200018, 200018]
# time results (seconds): [158.078125, 134.734375]
# #################################################################################################################################################
# displaying performance results of solver: 'constraints_weighting' with problem: 'two_consistency_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [8, 9]
# solution lengths (number of assignment and unassignment actions): [20000, 20000]
# time results (seconds): [32.296875, 31.765625]
# #################################################################################################################################################
# displaying performance results of solver: 'simulated_annealing' with problem: 'two_consistency_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [0, 1]
# time results (seconds): [121.46875, 653.296875]
# #################################################################################################################################################
# displaying performance results of solver: 'random_restart_first_choice_hill_climbing' with problem: 'two_consistency_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [0, 0]
# time results (seconds): [258.015625, 78.578125]
# #################################################################################################################################################
# displaying performance results of solver: 'genetic_local_search' with problem: 'general_genetic_two_consistency_magic_square_problem'
# unsatisfied_constraints_amounts out of 9 overall constraints: [1, 2]
# time results (seconds): [269.578125, 246.65625]
#
# Process finished with exit code 0
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////