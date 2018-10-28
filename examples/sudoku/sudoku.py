import math
import copy
import time
import csp
from examples.performance_testing import measure_performance
from examples.sudoku.sudoku_utilities import construct_sudoku_problem, print_solution, SudokuStartStateGenerator, \
    SudokuSuccessorGenerator, sudoku_score_calculator, GeneticSudokuConstraintProblem


sudoku_problem = construct_sudoku_problem("9x9_easy.txt")
ac3_sudoku_problem = copy.deepcopy(sudoku_problem)
ac4_sudoku_problem = copy.deepcopy(sudoku_problem)
pc2_sudoku_problem = copy.deepcopy(sudoku_problem)
two_consistency_sudoku_problem = copy.deepcopy(sudoku_problem)


name_to_var_map = sudoku_problem.get_name_to_variable_map()
tabu_size = int(math.sqrt(math.sqrt(len(name_to_var_map.keys()))))
read_only_variables = sudoku_problem.get_assigned_variables()
read_only_names = set(((i, j) for i, j in name_to_var_map.keys() if name_to_var_map[(i, j)] in read_only_variables))

sudoku_start_state_generator = SudokuStartStateGenerator(read_only_names)
sudoku_successor_generator = SudokuSuccessorGenerator(read_only_names)


# /////////////////////////////////////////////// USAGE EXAMPLE ///////////////////////////////////////////////
# csp.heuristic_backtracking_search(sudoku_problem)  # where sudoku_problem = construct_sudoku_problem("25x25_easy.txt")
# print_solution(name_to_var_map)
#
# 11  3  2 17 23 | 13 12 25  1  4 | 21  7  9 15 16 | 24 22  8 18 20 | 14  6 10 19  5
# 10  5 16  7 24 | 14  2  8 23 18 | 22  3 17 13 12 | 15 21  6  4 19 |  9 20  1 11 25
#  1 22  9 12 19 |  3 15  6 11 16 |  5 10  2 20 14 | 25 17 23  7 13 | 18  8 21  4 24
# 25 20  8 13 18 |  7 21 19 10  9 | 23 24 11  4  6 | 16  5  1 12 14 |  2 15 22  3 17
# 14  4  6 21 15 |  5 24 22 17 20 | 25  1 18  8 19 |  2 11  9  3 10 | 13  7 16 23 12
# -  -  -  -  -  + -  -  -  -  -  + -  -  -  -  -  + -  -  -  -  -  + -  -  -  -  -
# 12  9 25 11  8 |  2 20 16 24  3 | 10  4 23  6 13 | 17  7 21  5 18 | 22 19 14  1 15
#  4 14 18 24 17 | 15 10  1 21 23 | 16 12 22 11  3 | 13  6  2 19  9 | 25  5  8 20  7
# 16 19 22  5  7 |  9  8 11 18  6 | 20 14 15 24 21 |  4 10 25  1 12 | 17 23 13  2  3
# 15 21 23 10  1 | 12  5 13  4 17 | 18 19 25  7  2 | 14 20  3 22  8 |  6 16 24  9 11
# 20  2  3  6 13 | 25 14  7 22 19 |  1  8  5 17  9 | 23 16 15 11 24 | 21 10 18 12  4
# -  -  -  -  -  + -  -  -  -  -  + -  -  -  -  -  + -  -  -  -  -  + -  -  -  -  -
# 19 11 24  3  9 | 10  4 18  8  2 | 17 22 14 12  1 | 20 13  7 23  5 | 16 21 25 15  6
# 21 18  4 22 14 | 16 17  5 12  7 | 11  6 20  9 15 |  8  3 10 24 25 | 23  2 19 13  1
# 17  1 13 15  6 | 20  9 23 25 22 |  3 16  4  5  8 | 19 12 11 21  2 | 24 18  7 10 14
#  8  7 10 16  2 | 21  6 24  3  1 | 13 23 19 25 18 |  9  4 14 15 17 |  5 11 12 22 20
#  5 25 20 23 12 | 11 19 15 13 14 | 24 21 10  2  7 |  1 18 16  6 22 |  3 17  4  8  9
# -  -  -  -  -  + -  -  -  -  -  + -  -  -  -  -  + -  -  -  -  -  + -  -  -  -  -
#  3 24  7  9 16 |  4  1 12 19 21 | 14  2  6 10  5 | 11  8 18 20 23 | 15 22 17 25 13
# 22 15 21 14  4 | 18  3 17 16 11 | 19 13  7 23 20 | 10 25 12  9  1 |  8 24  5  6  2
# 13  6  5 20 25 | 22 23  9 15 10 |  8 18  3 21 17 |  7  2 24 14  4 | 12  1 11 16 19
#  2 23 12 19 10 | 24  7 20  5  8 |  9 25  1 16 11 | 22 15 13 17  6 |  4 14  3 18 21
# 18 17  1  8 11 |  6 25  2 14 13 | 12 15 24 22  4 | 21 19  5 16  3 | 20  9 23  7 10
# -  -  -  -  -  + -  -  -  -  -  + -  -  -  -  -  + -  -  -  -  -  + -  -  -  -  -
# 23 13 11  1  5 |  8 18 10  6 25 |  4 20 21 14 22 |  3  9 17  2  7 | 19 12 15 24 16
#  6 16 14 25 21 | 19 11  4  7 24 |  2 17  8 18 10 | 12 23 20 13 15 |  1  3  9  5 22
#  7  8 17  2 20 |  1 16  3  9 12 | 15  5 13 19 24 | 18 14 22 25 11 | 10  4  6 21 23
#  9 12 19 18  3 | 23 22 14  2 15 |  6 11 16  1 25 |  5 24  4 10 21 |  7 13 20 17  8
# 24 10 15  4 22 | 17 13 21 20  5 |  7  9 12  3 23 |  6  1 19  8 16 | 11 25  2 14 18
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////


measure_performance(1, "sudoku_problem", sudoku_problem,
                    "heuristic_backtracking_search", with_history=True, inference=None,
                    read_only_variables=read_only_variables)
measure_performance(1, "sudoku_problem", sudoku_problem,
                    "heuristic_backtracking_search", with_history=True, read_only_variables=read_only_variables)
measure_performance(1, "sudoku_problem", sudoku_problem,
                    "naive_cycle_cutset", with_history=True, read_only_variables=read_only_variables)
measure_performance(2, "sudoku_problem", sudoku_problem,
                    "min_conflicts", 100, tabu_size, with_history=True, read_only_variables=read_only_variables)
measure_performance(2, "sudoku_problem", sudoku_problem,
                    "constraints_weighting", 100, with_history=True, read_only_variables=read_only_variables)
measure_performance(2, "sudoku_problem", sudoku_problem,
                    "simulated_annealing", 100000, 0.5, 0.99999, sudoku_start_state_generator,
                    sudoku_successor_generator, sudoku_score_calculator, read_only_variables=read_only_variables)
measure_performance(2, "sudoku_problem", sudoku_problem,
                    "random_restart_first_choice_hill_climbing", 100, 10, 10, sudoku_start_state_generator,
                    sudoku_successor_generator, sudoku_score_calculator, read_only_variables=read_only_variables)
general_genetic_sudoku_problem = GeneticSudokuConstraintProblem(sudoku_problem, read_only_names, 0.1)
measure_performance(2, "general_genetic_sudoku_problem", general_genetic_sudoku_problem,
                    "genetic_local_search", 100, 100, 0.1, read_only_variables=read_only_variables)
genetic_sudoku_problem = GeneticSudokuConstraintProblem(sudoku_problem, read_only_names, 0.1)
measure_performance(2, "sudoku_genetic_sudoku_problem", genetic_sudoku_problem,
                    "genetic_local_search", 100, 100, 0.1, read_only_variables=read_only_variables)


ac3_start_time = time.process_time()
ac3_is_arc_consistent = csp.ac3(ac3_sudoku_problem)
ac3_end_time = time.process_time()
if ac3_is_arc_consistent:
    print()
    print()
    print("-" * 145)
    print("using ac3 as a preprocessing stage which took", ac3_end_time - ac3_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "ac3_sudoku_problem", ac3_sudoku_problem,
                        "backtracking_search", with_history=True, read_only_variables=read_only_variables)
    measure_performance(1, "ac3_sudoku_problem", ac3_sudoku_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True,
                        read_only_variables=read_only_variables)
    measure_performance(1, "ac3_sudoku_problem", ac3_sudoku_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True,
                        read_only_variables=read_only_variables)
    measure_performance(1, "ac3_sudoku_problem", ac3_sudoku_problem,
                        "heuristic_backtracking_search", with_history=True, read_only_variables=read_only_variables)
    measure_performance(1, "ac3_sudoku_problem", ac3_sudoku_problem,
                        "naive_cycle_cutset", with_history=True, read_only_variables=read_only_variables)
    measure_performance(2, "ac3_sudoku_problem", ac3_sudoku_problem,
                        "min_conflicts", 100000, with_history=True, read_only_variables=read_only_variables)
    measure_performance(2, "ac3_sudoku_problem", ac3_sudoku_problem,
                        "constraints_weighting", 10000, with_history=True, read_only_variables=read_only_variables)
    general_genetic_ac3_sudoku_problem = csp.GeneralGeneticConstraintProblem(ac3_sudoku_problem, 0.1)
    measure_performance(2, "general_genetic_ac3_magic_square_problem", general_genetic_ac3_sudoku_problem,
                        "genetic_local_search", 1000, 100, 0.1, read_only_variables=read_only_variables)


ac4_start_time = time.process_time()
ac4_is_arc_consistent = csp.ac4(ac4_sudoku_problem)
ac4_end_time = time.process_time()
if ac4_is_arc_consistent:
    print()
    print()
    print("-" * 145)
    print("using ac4 as a preprocessing stage which took", ac4_end_time - ac4_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "ac4_sudoku_problem", ac4_sudoku_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True,
                        read_only_variables=read_only_variables)
    measure_performance(1, "ac4_sudoku_problem", ac4_sudoku_problem,
                        "heuristic_backtracking_search", with_history=True, read_only_variables=read_only_variables)
    measure_performance(1, "ac4_sudoku_problem", ac4_sudoku_problem,
                        "naive_cycle_cutset", with_history=True, read_only_variables=read_only_variables)
    measure_performance(2, "ac4_sudoku_problem", ac4_sudoku_problem,
                        "min_conflicts", 100000, with_history=True, read_only_variables=read_only_variables)
    measure_performance(2, "ac4_sudoku_problem", ac4_sudoku_problem,
                        "constraints_weighting", 10000, with_history=True, read_only_variables=read_only_variables)
    general_genetic_ac4_sudoku_problem = csp.GeneralGeneticConstraintProblem(ac4_sudoku_problem, 0.1)
    measure_performance(2, "general_genetic_ac4_sudoku_problem", general_genetic_ac4_sudoku_problem,
                        "genetic_local_search", 10, 10, 0.1, read_only_variables=read_only_variables)


pc2_start_time = time.process_time()
pc2_is_path_consistent = csp.pc2(pc2_sudoku_problem)
pc2_end_time = time.process_time()
if pc2_is_path_consistent:
    print()
    print()
    print("-" * 145)
    print("using pc2 as a preprocessing stage which took", pc2_end_time - pc2_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "pc2_sudoku_problem", pc2_sudoku_problem,
                        "backtracking_search", with_history=True, read_only_variables=read_only_variables)
    measure_performance(1, "pc2_sudoku_problem", pc2_sudoku_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True,
                        read_only_variables=read_only_variables)
    measure_performance(1, "pc2_sudoku_problem", pc2_sudoku_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True,
                        read_only_variables=read_only_variables)
    measure_performance(1, "pc2_sudoku_problem", pc2_sudoku_problem,
                        "heuristic_backtracking_search", with_history=True, read_only_variables=read_only_variables)
    measure_performance(1, "pc2_sudoku_problem", pc2_sudoku_problem,
                        "naive_cycle_cutset", with_history=True, read_only_variables=read_only_variables)
    measure_performance(2, "pc2_sudoku_problem", pc2_sudoku_problem,
                        "min_conflicts", 100000, with_history=True, read_only_variables=read_only_variables)
    measure_performance(2, "pc2_sudoku_problem", pc2_sudoku_problem,
                        "constraints_weighting", 10000, with_history=True, read_only_variables=read_only_variables)
    general_genetic_pc2_sudoku_problem = csp.GeneralGeneticConstraintProblem(pc2_sudoku_problem, 0.1)
    measure_performance(2, "general_genetic_pc2_sudoku_problem", general_genetic_pc2_sudoku_problem,
                        "genetic_local_search", 10, 10, 0.1, read_only_variables=read_only_variables)



# /////////////////////////////////////////////////////// PERFORMANCE RESULTS /////////////////////////////////////////////////////////////////////
###################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search' with problem: 'sudoku_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [47]
# time results (seconds): [1.140625]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search_with_forward_checking' with problem: 'sudoku_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [47]
# time results (seconds): [1.25]
# #################################################################################################################################################
# displaying performance results of solver: 'naive_cycle_cutset' with problem: 'sudoku_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [27]
# solution lengths (number of assignment and unassignment actions): [0]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'min_conflicts' with problem: 'sudoku_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [27, 25]
# solution lengths (number of assignment and unassignment actions): [294, 294]
# time results (seconds): [0.484375, 0.46875]
# #################################################################################################################################################
# displaying performance results of solver: 'constraints_weighting' with problem: 'sudoku_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [27, 27]
# solution lengths (number of assignment and unassignment actions): [200, 200]
# time results (seconds): [10.046875, 10.234375]
# #################################################################################################################################################
# displaying performance results of solver: 'simulated_annealing' with problem: 'sudoku_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0, 0]
# time results (seconds): [16.1875, 42.203125]
# #################################################################################################################################################
# displaying performance results of solver: 'random_restart_first_choice_hill_climbing' with problem: 'sudoku_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [18, 17]
# time results (seconds): [9.21875, 9.171875]
# #################################################################################################################################################
# displaying performance results of solver: 'genetic_local_search' with problem: 'general_genetic_sudoku_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [18, 18]
# time results (seconds): [10.125, 10.140625]
# #################################################################################################################################################
# displaying performance results of solver: 'genetic_local_search' with problem: 'sudoku_genetic_sudoku_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [18, 18]
# time results (seconds): [10.140625, 10.140625]
#
#
# -------------------------------------------------------------------------------------------------------------------------------------------------
# using ac3 as a preprocessing stage which took 0.234375 seconds
# -------------------------------------------------------------------------------------------------------------------------------------------------
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search' with problem: 'ac3_sudoku_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [81]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search_with_forward_checking' with problem: 'ac3_sudoku_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [81]
# time results (seconds): [0.0625]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search' with problem: 'ac3_sudoku_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [81]
# time results (seconds): [0.515625]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search_with_forward_checking' with problem: 'ac3_sudoku_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [81]
# time results (seconds): [0.546875]
# #################################################################################################################################################
# displaying performance results of solver: 'naive_cycle_cutset' with problem: 'ac3_sudoku_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [81]
# time results (seconds): [0.015625]
# #################################################################################################################################################
# displaying performance results of solver: 'min_conflicts' with problem: 'ac3_sudoku_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0, 0]
# solution lengths (number of assignment and unassignment actions): [162, 162]
# time results (seconds): [0.0, 0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'constraints_weighting' with problem: 'ac3_sudoku_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0, 0]
# solution lengths (number of assignment and unassignment actions): [0, 0]
# time results (seconds): [0.0, 0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'genetic_local_search' with problem: 'general_genetic_ac3_magic_square_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0, 0]
# time results (seconds): [0.53125, 0.53125]
#
#
# -------------------------------------------------------------------------------------------------------------------------------------------------
# using ac4 as a preprocessing stage which took 0.03125 seconds
# -------------------------------------------------------------------------------------------------------------------------------------------------
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search' with problem: 'ac4_sudoku_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [81]
# time results (seconds): [2.375]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search_with_forward_checking' with problem: 'ac4_sudoku_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [81]
# time results (seconds): [2.625]
####################################################################################################################################################
# displaying performance results of solver: 'min_conflicts' with problem: 'ac4_sudoku_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [10, 12]
# solution lengths (number of assignment and unassignment actions): [200162, 200162]
# time results (seconds): [353.875, 323.203125]
# #################################################################################################################################################
# displaying performance results of solver: 'constraints_weighting' with problem: 'ac4_sudoku_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [27, 27]
# solution lengths (number of assignment and unassignment actions): [20000, 20000]
# time results (seconds): [940.84375, 951.34375]
# #################################################################################################################################################
# displaying performance results of solver: 'genetic_local_search' with problem: 'general_genetic_ac4_sudoku_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [25, 26]
# time results (seconds): [0.109375, 0.09375]
#
# Process finished with exit code 0

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////