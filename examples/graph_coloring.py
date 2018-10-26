import copy
import time
import csp
from examples.performance_testing import measure_performance

# Solving the States and Territories of Australia map-coloring problem:   (see problem construction for edges)
#                                   |Northern Territory|
#                                                           |Queensland|
#           |Western Australia|
#                                     |South Australia|
#                                                           |New South Wales|
#                                                   |Victoria|
#
#
#                                                   |Tasmania|

colors = ["red", "green", "blue"]
names = {"wa", "nt", "q", "nsw", "v", "sa", "t"}
name_to_variable_map = csp.Variable.from_names_to_equal_domain(names, colors)
const1 = csp.Constraint([name_to_variable_map["sa"], name_to_variable_map["wa"]], csp.all_different)
const2 = csp.Constraint([name_to_variable_map["sa"], name_to_variable_map["nt"]], csp.all_different)
const3 = csp.Constraint([name_to_variable_map["sa"], name_to_variable_map["q"]], csp.all_different)
const4 = csp.Constraint([name_to_variable_map["sa"], name_to_variable_map["nsw"]], csp.all_different)
const5 = csp.Constraint([name_to_variable_map["sa"], name_to_variable_map["v"]], csp.all_different)
const6 = csp.Constraint([name_to_variable_map["wa"], name_to_variable_map["nt"]], csp.all_different)
const7 = csp.Constraint([name_to_variable_map["nt"], name_to_variable_map["q"]], csp.all_different)
const8 = csp.Constraint([name_to_variable_map["q"], name_to_variable_map["nsw"]], csp.all_different)
const9 = csp.Constraint([name_to_variable_map["nsw"], name_to_variable_map["v"]], csp.all_different)
const10 = csp.Constraint([name_to_variable_map["t"]], csp.always_satisfied)
constraints = (const1, const2, const3, const4, const5, const6, const7, const8, const9, const10)
map_coloring_problem = csp.ConstraintProblem(constraints)


# /////////////////////////////////////////////// USAGE EXAMPLE ///////////////////////////////////////////////
# csp.heuristic_backtracking_search(map_coloring_problem)
# for name in name_to_variable_map:
#    print(name, ":", name_to_variable_map[name].value)
#
# t : blue
# q : red
# nsw : green
# wa : red
# nt : green
# sa : blue
# v : red
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////


measure_performance(1, "map_coloring_problem", map_coloring_problem,
                    "backtracking_search", with_history=True)
measure_performance(1, "map_coloring_problem", map_coloring_problem,
                    "backtracking_search", inference=csp.forward_check, with_history=True)
measure_performance(1, "map_coloring_problem", map_coloring_problem,
                    "heuristic_backtracking_search", inference=None, with_history=True)
measure_performance(1, "map_coloring_problem", map_coloring_problem,
                    "heuristic_backtracking_search", with_history=True)
measure_performance(1, "map_coloring_problem", map_coloring_problem,
                    "naive_cycle_cutset", with_history=True)
measure_performance(2, "map_coloring_problem", map_coloring_problem,
                    "min_conflicts", 100000, with_history=True)
measure_performance(2, "map_coloring_problem", map_coloring_problem,
                    "constraints_weighting", 10000, with_history=True)
measure_performance(2, "map_coloring_problem", map_coloring_problem,
                    "simulated_annealing", 100000, 0.5, 0.99999)
measure_performance(2, "map_coloring_problem", map_coloring_problem,
                    "random_restart_first_choice_hill_climbing", 100, 100, 10)
general_genetic_map_coloring_problem = csp.GeneralGeneticConstraintProblem(map_coloring_problem, 0.1)
measure_performance(2, "map_coloring_problem", general_genetic_map_coloring_problem,
                    "genetic_local_search", 100, 100, 0.1)


ac3_map_coloring_problem = copy.deepcopy(map_coloring_problem)
ac3_map_coloring_problem.unassign_all_variables()
ac3_start_time = time.process_time()
ac3_is_arc_consistent = csp.ac3(ac3_map_coloring_problem)
ac3_end_time = time.process_time()
if ac3_is_arc_consistent:
    print()
    print()
    print("-" * 145)
    print("using ac3 as a preprocessing stage which took", ac3_end_time - ac3_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "ac3_map_coloring_problem", ac3_map_coloring_problem,
                        "backtracking_search", with_history=True)
    measure_performance(1, "ac3_map_coloring_problem", ac3_map_coloring_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "ac3_map_coloring_problem", ac3_map_coloring_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True)
    measure_performance(1, "ac3_map_coloring_problem", ac3_map_coloring_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "ac3_map_coloring_problem", ac3_map_coloring_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "ac3_map_coloring_problem", ac3_map_coloring_problem,
                        "min_conflicts", 100000, with_history=True)
    measure_performance(2, "ac3_map_coloring_problem", ac3_map_coloring_problem,
                        "constraints_weighting", 10000, with_history=True)
    measure_performance(2, "ac3_map_coloring_problem", ac3_map_coloring_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "ac3_map_coloring_problem", ac3_map_coloring_problem,
                        "random_restart_first_choice_hill_climbing", 100, 100, 10)
    general_genetic_map_coloring_problem = csp.GeneralGeneticConstraintProblem(ac3_map_coloring_problem, 0.1)
    measure_performance(2, "ac3_map_coloring_problem", general_genetic_map_coloring_problem,
                        "genetic_local_search", 100, 100, 0.1)


ac4_map_coloring_problem = copy.deepcopy(map_coloring_problem)
ac4_map_coloring_problem.unassign_all_variables()
ac4_start_time = time.process_time()
ac4_is_arc_consistent = csp.ac4(ac4_map_coloring_problem)
ac4_end_time = time.process_time()
if ac4_is_arc_consistent:
    print()
    print()
    print("-" * 145)
    print("using ac4 as a preprocessing stage which took", ac4_end_time - ac4_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "ac4_map_coloring_problem", ac4_map_coloring_problem,
                        "backtracking_search", with_history=True)
    measure_performance(1, "ac4_map_coloring_problem", ac4_map_coloring_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "ac4_map_coloring_problem", ac4_map_coloring_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True)
    measure_performance(1, "ac4_map_coloring_problem", ac4_map_coloring_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "ac4_map_coloring_problem", ac4_map_coloring_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "ac4_map_coloring_problem", ac4_map_coloring_problem,
                        "min_conflicts", 100000, with_history=True)
    measure_performance(2, "ac4_map_coloring_problem", ac4_map_coloring_problem,
                        "constraints_weighting", 10000, with_history=True)
    measure_performance(2, "ac4_map_coloring_problem", ac4_map_coloring_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "ac4_map_coloring_problem", ac4_map_coloring_problem,
                        "random_restart_first_choice_hill_climbing", 100, 100, 10)
    general_genetic_map_coloring_problem = csp.GeneralGeneticConstraintProblem(ac4_map_coloring_problem, 0.1)
    measure_performance(2, "ac4_map_coloring_problem", general_genetic_map_coloring_problem,
                        "genetic_local_search", 100, 100, 0.1)


pc2_map_coloring_problem = copy.deepcopy(map_coloring_problem)
pc2_map_coloring_problem.unassign_all_variables()
pc2_start_time = time.process_time()
pc2_is_path_consistent = csp.pc2(pc2_map_coloring_problem)
pc2_end_time = time.process_time()
if pc2_is_path_consistent:
    print()
    print()
    print("-" * 145)
    print("using pc2 as a preprocessing stage which took", pc2_end_time - pc2_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "pc2_map_coloring_problem", pc2_map_coloring_problem,
                        "backtracking_search", with_history=True)
    measure_performance(1, "pc2_map_coloring_problem", pc2_map_coloring_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "pc2_map_coloring_problem", pc2_map_coloring_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True)
    measure_performance(1, "pc2_map_coloring_problem", pc2_map_coloring_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "pc2_map_coloring_problem", pc2_map_coloring_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "pc2_map_coloring_problem", pc2_map_coloring_problem,
                        "min_conflicts", 100000, with_history=True)
    measure_performance(2, "pc2_map_coloring_problem", pc2_map_coloring_problem,
                        "constraints_weighting", 10000, with_history=True)
    measure_performance(2, "pc2_map_coloring_problem", pc2_map_coloring_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "pc2_map_coloring_problem", pc2_map_coloring_problem,
                        "random_restart_first_choice_hill_climbing", 100, 100, 10)
    general_genetic_map_coloring_problem = csp.GeneralGeneticConstraintProblem(pc2_map_coloring_problem, 0.1)
    measure_performance(2, "pc2_map_coloring_problem", general_genetic_map_coloring_problem,
                        "genetic_local_search", 100, 100, 0.1)


two_consistency_map_coloring_problem = copy.deepcopy(map_coloring_problem)
two_consistency_map_coloring_problem.unassign_all_variables()
two_consistency_start_time = time.process_time()
is_two_consistent = csp.i_consistency(two_consistency_map_coloring_problem, 2)
two_consistency_end_time = time.process_time()
if is_two_consistent:
    print()
    print()
    print("-" * 145)
    print("using 2-consistency as a preprocessing stage which took",
          two_consistency_end_time - two_consistency_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "two_consistency_map_coloring_problem", two_consistency_map_coloring_problem,
                        "backtracking_search", with_history=True)
    measure_performance(1, "two_consistency_map_coloring_problem", two_consistency_map_coloring_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "two_consistency_map_coloring_problem", two_consistency_map_coloring_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True)
    measure_performance(1, "two_consistency_map_coloring_problem", two_consistency_map_coloring_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "two_consistency_map_coloring_problem", two_consistency_map_coloring_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "two_consistency_map_coloring_problem", two_consistency_map_coloring_problem,
                        "min_conflicts", 100000, with_history=True)
    measure_performance(2, "two_consistency_map_coloring_problem", two_consistency_map_coloring_problem,
                        "constraints_weighting", 10000, with_history=True)
    measure_performance(2, "two_consistency_map_coloring_problem", two_consistency_map_coloring_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "two_consistency_map_coloring_problem", two_consistency_map_coloring_problem,
                        "random_restart_first_choice_hill_climbing", 100, 100, 10)
    general_genetic_map_coloring_problem = \
        csp.GeneralGeneticConstraintProblem(two_consistency_map_coloring_problem, 0.1)
    measure_performance(2, "two_consistency_map_coloring_problem", general_genetic_map_coloring_problem,
                        "genetic_local_search", 100, 100, 0.1)



# /////////////////////////////////////////////////////// PERFORMANCE RESULTS /////////////////////////////////////////////////////////////////////
###################################################################################################################################################
# displaying performance results of solver: 'backtracking_search' with problem: 'map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [411]
# time results (seconds): [0.015625]
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search_with_forward_checking' with problem: 'map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [411]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search' with problem: 'map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [7]
# time results (seconds): [0.015625]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search_with_forward_checking' with problem: 'map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [7]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'naive_cycle_cutset' with problem: 'map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [21]
# time results (seconds): [0.015625]
# #################################################################################################################################################
# displaying performance results of solver: 'min_conflicts' with problem: 'map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0, 0]
# solution lengths (number of assignment and unassignment actions): [20, 64]
# time results (seconds): [0.0, 0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'constraints_weighting' with problem: 'map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0, 0]
# solution lengths (number of assignment and unassignment actions): [22, 96]
# time results (seconds): [0.015625, 0.03125]
# #################################################################################################################################################
# displaying performance results of solver: 'simulated_annealing' with problem: 'map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0, 0]
# time results (seconds): [0.015625, 0.015625]
# #################################################################################################################################################
# displaying performance results of solver: 'random_restart_first_choice_hill_climbing' with problem: 'map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0, 0]
# time results (seconds): [0.84375, 0.046875]
# #################################################################################################################################################
# displaying performance results of solver: 'genetic_local_search' with problem: 'map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0, 0]
# time results (seconds): [0.0, 0.015625]
#
#
# -------------------------------------------------------------------------------------------------------------------------------------------------
# using ac3 as a preprocessing stage which took 0.0 seconds
# -------------------------------------------------------------------------------------------------------------------------------------------------
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search' with problem: 'ac3_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [993]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search_with_forward_checking' with problem: 'ac3_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [993]
# time results (seconds): [0.03125]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search' with problem: 'ac3_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [7]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search_with_forward_checking' with problem: 'ac3_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [7]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'naive_cycle_cutset' with problem: 'ac3_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [63]
# time results (seconds): [0.015625]
# #################################################################################################################################################
# displaying performance results of solver: 'min_conflicts' with problem: 'ac3_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0, 0]
# solution lengths (number of assignment and unassignment actions): [52, 30]
# time results (seconds): [0.015625, 0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'constraints_weighting' with problem: 'ac3_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0, 0]
# solution lengths (number of assignment and unassignment actions): [110, 868]
# time results (seconds): [0.046875, 0.375]
# #################################################################################################################################################
# displaying performance results of solver: 'simulated_annealing' with problem: 'ac3_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0, 0]
# time results (seconds): [0.0625, 0.0625]
# #################################################################################################################################################
# displaying performance results of solver: 'random_restart_first_choice_hill_climbing' with problem: 'ac3_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0, 0]
# time results (seconds): [0.0, 2.578125]
# #################################################################################################################################################
# displaying performance results of solver: 'genetic_local_search' with problem: 'ac3_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0, 0]
# time results (seconds): [0.015625, 0.015625]
#
#
# -------------------------------------------------------------------------------------------------------------------------------------------------
# using ac4 as a preprocessing stage which took 0.0 seconds
# -------------------------------------------------------------------------------------------------------------------------------------------------
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search' with problem: 'ac4_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [371]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search_with_forward_checking' with problem: 'ac4_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [371]
# time results (seconds): [0.015625]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search' with problem: 'ac4_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [7]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search_with_forward_checking' with problem: 'ac4_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [7]
# time results (seconds): [0.015625]
# #################################################################################################################################################
# displaying performance results of solver: 'naive_cycle_cutset' with problem: 'ac4_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [189]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'min_conflicts' with problem: 'ac4_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0, 0]
# solution lengths (number of assignment and unassignment actions): [76, 20]
# time results (seconds): [0.015625, 0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'constraints_weighting' with problem: 'ac4_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0, 0]
# solution lengths (number of assignment and unassignment actions): [102, 280]
# time results (seconds): [0.046875, 0.109375]
# #################################################################################################################################################
# displaying performance results of solver: 'simulated_annealing' with problem: 'ac4_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0, 0]
# time results (seconds): [0.015625, 0.015625]
# #################################################################################################################################################
# displaying performance results of solver: 'random_restart_first_choice_hill_climbing' with problem: 'ac4_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0, 0]
# time results (seconds): [4.140625, 4.1875]
# #################################################################################################################################################
# displaying performance results of solver: 'genetic_local_search' with problem: 'ac4_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0, 0]
# time results (seconds): [0.015625, 0.015625]
#
#
# -------------------------------------------------------------------------------------------------------------------------------------------------
# using pc2 as a preprocessing stage which took 0.03125 seconds
# -------------------------------------------------------------------------------------------------------------------------------------------------
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search' with problem: 'pc2_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [269]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search_with_forward_checking' with problem: 'pc2_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [269]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search' with problem: 'pc2_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [7]
# time results (seconds): [0.015625]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search_with_forward_checking' with problem: 'pc2_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [7]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'naive_cycle_cutset' with problem: 'pc2_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [63]
# time results (seconds): [0.015625]
# #################################################################################################################################################
# displaying performance results of solver: 'min_conflicts' with problem: 'pc2_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0, 0]
# solution lengths (number of assignment and unassignment actions): [34, 32]
# time results (seconds): [0.0, 0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'constraints_weighting' with problem: 'pc2_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0, 0]
# solution lengths (number of assignment and unassignment actions): [452, 638]
# time results (seconds): [0.21875, 0.25]
# #################################################################################################################################################
# displaying performance results of solver: 'simulated_annealing' with problem: 'pc2_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0, 0]
# time results (seconds): [0.015625, 0.03125]
# #################################################################################################################################################
# displaying performance results of solver: 'random_restart_first_choice_hill_climbing' with problem: 'pc2_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0, 0]
# time results (seconds): [0.03125, 0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'genetic_local_search' with problem: 'pc2_map_coloring_problem'
# unsatisfied_constraints_amounts out of 10 overall constraints: [0, 0]
# time results (seconds): [0.015625, 0.015625]
#
# Process finished with exit code 0

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////