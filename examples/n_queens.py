import time
import copy
import csp
from examples.performance_testing import measure_performance


# SOLVING N-QUEENS PROBLEM:
# Each variable represent a column in the n x n sized board.
# Each variable's domain is (1, ..., n), and it represent a possible queen row-coordinate location in the column i.
# For the queens not to attack each other, the constraints ara:
#   1. No single row hold two queens: all variables are (pair-wise) all-different.
#   2. The queens don't attack each other horizontally.
#   3. The queens don't attack each other diagonally.


n = 8


name_to_variable_map = {col: csp.Variable(range(n)) for col in range(n)}


def get_not_attacking_constraint(columns_difference: int) -> csp.ConstraintEvaluator:
    def not_attacking_constraint(values: tuple) -> bool:
        if len(values) < 2:
            return True
        row1, row2 = values
        return row1 != row2 and abs(row1 - row2) != columns_difference
    return not_attacking_constraint


not_attacking_constraints = dict()
for i in range(1, n):
    not_attacking_constraints[i] = get_not_attacking_constraint(i)


constraints = set()
for col1 in range(n):
    for col2 in range(n):
        if col1 < col2:
            constraints.add(csp.Constraint((name_to_variable_map[col1], name_to_variable_map[col2]),
                                           not_attacking_constraints[abs(col1 - col2)]))

n_queens_problem = csp.ConstraintProblem(constraints)


# /////////////////////////////////////////////// USAGE EXAMPLE ///////////////////////////////////////////////
# csp.heuristic_backtracking_search(n_queens_problem)
# for name in name_to_variable_map:
#    print(name, ":", name_to_variable_map[name].value)
#
# 0 : 3
# 1 : 6
# 2 : 2
# 3 : 7
# 4 : 1
# 5 : 4
# 6 : 0
# 7 : 5
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////


measure_performance(1, "n_queens_problem", n_queens_problem,
                    "backtracking_search", with_history=True)
measure_performance(1, "n_queens_problem", n_queens_problem,
                    "backtracking_search", inference=csp.forward_check, with_history=True)
measure_performance(1, "n_queens_problem", n_queens_problem,
                    "heuristic_backtracking_search", inference=None, with_history=True)
measure_performance(1, "n_queens_problem", n_queens_problem,
                    "heuristic_backtracking_search", with_history=True)
measure_performance(1, "n_queens_problem", n_queens_problem,
                    "naive_cycle_cutset", with_history=True)
measure_performance(2, "n_queens_problem", n_queens_problem,
                    "min_conflicts", 100000, with_history=True)
measure_performance(2, "n_queens_problem", n_queens_problem,
                    "constraints_weighting", 10000, with_history=True)
measure_performance(2, "n_queens_problem", n_queens_problem,
                    "simulated_annealing", 100000, 0.5, 0.99999)
measure_performance(2, "n_queens_problem", n_queens_problem,
                    "random_restart_first_choice_hill_climbing", 100, 100, 10)
general_genetic_n_queens_problem = csp.GeneralGeneticConstraintProblem(n_queens_problem, 0.1)
measure_performance(2, "n_queens_problem", general_genetic_n_queens_problem,
                    "genetic_local_search", 100, 100, 0.1)


ac3_n_queens_problem = copy.deepcopy(n_queens_problem)
ac3_n_queens_problem.unassign_all_variables()
ac3_start_time = time.process_time()
ac3_is_arc_consistent = csp.ac3(ac3_n_queens_problem)
ac3_end_time = time.process_time()
if ac3_is_arc_consistent:
    print()
    print()
    print("-" * 145)
    print("using ac3 as a preprocessing stage which took", ac3_end_time - ac3_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "ac3_n_queens_problem", ac3_n_queens_problem,
                        "backtracking_search", with_history=True)
    measure_performance(1, "ac3_n_queens_problem", ac3_n_queens_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "ac3_n_queens_problem", ac3_n_queens_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True)
    measure_performance(1, "ac3_n_queens_problem", ac3_n_queens_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "ac3_n_queens_problem", ac3_n_queens_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "ac3_n_queens_problem", ac3_n_queens_problem,
                        "min_conflicts", 100000, with_history=True)
    measure_performance(2, "ac3_n_queens_problem", ac3_n_queens_problem,
                        "constraints_weighting", 10000, with_history=True)
    measure_performance(2, "ac3_n_queens_problem", ac3_n_queens_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "ac3_n_queens_problem", ac3_n_queens_problem,
                        "random_restart_first_choice_hill_climbing", 100, 100, 10)
    general_genetic_n_queens_problem = csp.GeneralGeneticConstraintProblem(ac3_n_queens_problem, 0.1)
    measure_performance(2, "ac3_n_queens_problem", general_genetic_n_queens_problem,
                        "genetic_local_search", 100, 100, 0.1)


ac4_n_queens_problem = copy.deepcopy(n_queens_problem)
ac4_n_queens_problem.unassign_all_variables()
ac4_start_time = time.process_time()
ac4_is_arc_consistent = csp.ac4(ac4_n_queens_problem)
ac4_end_time = time.process_time()
if ac4_is_arc_consistent:
    print()
    print()
    print("-" * 145)
    print("using ac4 as a preprocessing stage which took", ac4_end_time - ac4_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "ac4_n_queens_problem", ac4_n_queens_problem,
                        "backtracking_search", with_history=True)
    measure_performance(1, "ac4_n_queens_problem", ac4_n_queens_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "ac4_n_queens_problem", ac4_n_queens_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True)
    measure_performance(1, "ac4_n_queens_problem", ac4_n_queens_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "ac4_n_queens_problem", ac4_n_queens_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "ac4_n_queens_problem", ac4_n_queens_problem,
                        "min_conflicts", 100000, with_history=True)
    measure_performance(2, "ac4_n_queens_problem", ac4_n_queens_problem,
                        "constraints_weighting", 10000, with_history=True)
    measure_performance(2, "ac4_n_queens_problem", ac4_n_queens_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "ac4_n_queens_problem", ac4_n_queens_problem,
                        "random_restart_first_choice_hill_climbing", 100, 100, 10)
    general_genetic_n_queens_problem = csp.GeneralGeneticConstraintProblem(ac4_n_queens_problem, 0.1)
    measure_performance(2, "ac4_n_queens_problem", general_genetic_n_queens_problem,
                        "genetic_local_search", 100, 100, 0.1)


pc2_n_queens_problem = copy.deepcopy(n_queens_problem)
pc2_n_queens_problem.unassign_all_variables()
pc2_start_time = time.process_time()
pc2_is_path_consistent = csp.pc2(pc2_n_queens_problem)
pc2_end_time = time.process_time()
if pc2_is_path_consistent:
    print()
    print()
    print("-" * 145)
    print("using pc2 as a preprocessing stage which took", pc2_end_time - pc2_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "pc2_n_queens_problem", pc2_n_queens_problem,
                        "backtracking_search", with_history=True)
    measure_performance(1, "pc2_n_queens_problem", pc2_n_queens_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "pc2_n_queens_problem", pc2_n_queens_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True)
    measure_performance(1, "pc2_n_queens_problem", pc2_n_queens_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "pc2_n_queens_problem", pc2_n_queens_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "pc2_n_queens_problem", pc2_n_queens_problem,
                        "min_conflicts", 100000, with_history=True)
    measure_performance(2, "pc2_n_queens_problem", pc2_n_queens_problem,
                        "constraints_weighting", 10000, with_history=True)
    measure_performance(2, "pc2_n_queens_problem", pc2_n_queens_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "pc2_n_queens_problem", pc2_n_queens_problem,
                        "random_restart_first_choice_hill_climbing", 100, 100, 10)
    general_genetic_n_queens_problem = csp.GeneralGeneticConstraintProblem(pc2_n_queens_problem, 0.1)
    measure_performance(2, "pc2_n_queens_problem", general_genetic_n_queens_problem,
                        "genetic_local_search", 100, 100, 0.1)


two_consistency_n_queens_problem = copy.deepcopy(n_queens_problem)
two_consistency_n_queens_problem.unassign_all_variables()
two_consistency_start_time = time.process_time()
is_two_consistent = csp.i_consistency(two_consistency_n_queens_problem, 2)
two_consistency_end_time = time.process_time()
if is_two_consistent:
    print()
    print()
    print("-" * 145)
    print("using 2-consistency as a preprocessing stage which took",
          two_consistency_end_time - two_consistency_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "two_consistency_n_queens_problem", two_consistency_n_queens_problem,
                        "backtracking_search", with_history=True)
    measure_performance(1, "two_consistency_n_queens_problem", two_consistency_n_queens_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "two_consistency_n_queens_problem", two_consistency_n_queens_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True)
    measure_performance(1, "two_consistency_n_queens_problem", two_consistency_n_queens_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "two_consistency_n_queens_problem", two_consistency_n_queens_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "two_consistency_n_queens_problem", two_consistency_n_queens_problem,
                        "min_conflicts", 100000, with_history=True)
    measure_performance(2, "two_consistency_n_queens_problem", two_consistency_n_queens_problem,
                        "constraints_weighting", 10000, with_history=True)
    measure_performance(2, "two_consistency_n_queens_problem", two_consistency_n_queens_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "two_consistency_n_queens_problem", two_consistency_n_queens_problem,
                        "random_restart_first_choice_hill_climbing", 100, 100, 10)
    general_genetic_n_queens_problem = \
        csp.GeneralGeneticConstraintProblem(two_consistency_n_queens_problem, 0.1)
    measure_performance(2, "two_consistency_n_queens_problem", general_genetic_n_queens_problem,
                        "genetic_local_search", 100, 100, 0.1)



# /////////////////////////////////////////////////////// PERFORMANCE RESULTS /////////////////////////////////////////////////////////////////////
###################################################################################################################################################
# displaying performance results of solver: 'backtracking_search' with problem: 'n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [864816]
# time results (seconds): [10.1875]
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search_with_forward_checking' with problem: 'n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [864816]
# time results (seconds): [37.328125]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search' with problem: 'n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [8]
# time results (seconds): [0.109375]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search_with_forward_checking' with problem: 'n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [8]
# time results (seconds): [0.09375]
# #################################################################################################################################################
# displaying performance results of solver: 'naive_cycle_cutset' with problem: 'n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [28044]
# time results (seconds): [7.765625]
# #################################################################################################################################################
# displaying performance results of solver: 'min_conflicts' with problem: 'n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0, 0]
# solution lengths (number of assignment and unassignment actions): [104, 64]
# time results (seconds): [0.078125, 0.03125]
# #################################################################################################################################################
# displaying performance results of solver: 'constraints_weighting' with problem: 'n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [4, 5]
# solution lengths (number of assignment and unassignment actions): [20000, 20000]
# time results (seconds): [32.109375, 33.65625]
# #################################################################################################################################################
# displaying performance results of solver: 'simulated_annealing' with problem: 'n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0, 0]
# time results (seconds): [0.484375, 0.40625]
# #################################################################################################################################################
# displaying performance results of solver: 'random_restart_first_choice_hill_climbing' with problem: 'n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0, 0]
# time results (seconds): [4.4375, 4.28125]
# #################################################################################################################################################
# displaying performance results of solver: 'genetic_local_search' with problem: 'n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [1, 1]
# time results (seconds): [3.578125, 3.78125]
#
#
# -------------------------------------------------------------------------------------------------------------------------------------------------
# using ac3 as a preprocessing stage which took 0.015625 seconds
# -------------------------------------------------------------------------------------------------------------------------------------------------
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search' with problem: 'ac3_n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [7686]
# time results (seconds): [0.09375]
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search_with_forward_checking' with problem: 'ac3_n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [7686]
# time results (seconds): [0.390625]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search' with problem: 'ac3_n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [22]
# time results (seconds): [0.046875]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search_with_forward_checking' with problem: 'ac3_n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [22]
# time results (seconds): [0.046875]
# #################################################################################################################################################
# displaying performance results of solver: 'naive_cycle_cutset' with problem: 'ac3_n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [2974]
# time results (seconds): [0.125]
# #################################################################################################################################################
# displaying performance results of solver: 'min_conflicts' with problem: 'ac3_n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0, 0]
# solution lengths (number of assignment and unassignment actions): [52, 32]
# time results (seconds): [0.015625, 0.015625]
# #################################################################################################################################################
# displaying performance results of solver: 'constraints_weighting' with problem: 'ac3_n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0, 0]
# solution lengths (number of assignment and unassignment actions): [1136, 108]
# time results (seconds): [1.078125, 0.109375]
# #################################################################################################################################################
# displaying performance results of solver: 'simulated_annealing' with problem: 'ac3_n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0, 0]
# time results (seconds): [0.015625, 1.21875]
# #################################################################################################################################################
# displaying performance results of solver: 'random_restart_first_choice_hill_climbing' with problem: 'ac3_n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0, 0]
# time results (seconds): [2.125, 2.046875]
# #################################################################################################################################################
# displaying performance results of solver: 'genetic_local_search' with problem: 'ac3_n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0, 0]
# time results (seconds): [0.046875, 0.0]
#
#
# -------------------------------------------------------------------------------------------------------------------------------------------------
# using ac4 as a preprocessing stage which took 0.03125 seconds
# -------------------------------------------------------------------------------------------------------------------------------------------------
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search' with problem: 'ac4_n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [1864]
# time results (seconds): [0.015625]
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search_with_forward_checking' with problem: 'ac4_n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [1864]
# time results (seconds): [0.078125]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search' with problem: 'ac4_n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [12]
# time results (seconds): [0.03125]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search_with_forward_checking' with problem: 'ac4_n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [12]
# time results (seconds): [0.046875]
# #################################################################################################################################################
# displaying performance results of solver: 'naive_cycle_cutset' with problem: 'ac4_n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [1044]
# time results (seconds): [0.0625]
# #################################################################################################################################################
# displaying performance results of solver: 'min_conflicts' with problem: 'ac4_n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0, 0]
# solution lengths (number of assignment and unassignment actions): [18, 80]
# time results (seconds): [0.0, 0.03125]
# #################################################################################################################################################
# displaying performance results of solver: 'constraints_weighting' with problem: 'ac4_n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0, 0]
# solution lengths (number of assignment and unassignment actions): [110, 166]
# time results (seconds): [0.109375, 0.15625]
# #################################################################################################################################################
# displaying performance results of solver: 'simulated_annealing' with problem: 'ac4_n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0, 0]
# time results (seconds): [0.71875, 0.375]
# #################################################################################################################################################
# displaying performance results of solver: 'random_restart_first_choice_hill_climbing' with problem: 'ac4_n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0, 0]
# time results (seconds): [2.078125, 2.09375]
# #################################################################################################################################################
# displaying performance results of solver: 'genetic_local_search' with problem: 'ac4_n_queens_problem'
# unsatisfied_constraints_amounts out of 28 overall constraints: [0, 0]
# time results (seconds): [0.015625, 0.03125]
#
# Process finished with exit code 0

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////