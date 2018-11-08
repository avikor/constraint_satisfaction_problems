import time
import copy
import csp
from examples.performance_testing import measure_performance


# SOLVING JOB-SCHEDULING PROBLEM:
# car assembly broken down to 15 tasks, which we'll model as variables:
# [1-2] install axles (front and back),
# [3-6] affix all four wheels (right and left, front and back),
# [7-10] tighten nuts for each wheel,
# [11-14] affix hubcaps,
# [15] inspect the final assembly.
#
# we'll model the following requirement as a domain:
# 1. the whole assembly must be done in 30 minutes.
#
# we'll model the following requirements as constraints:
# 1. the axles have to be in place before the wheels are put on, and it takes 10 minutes to install an axle.
# 2. for each wheel we must affix the wheel (which takes 1 minute), then tighten the nuts (2 minutes), and only then
#    attach the hubcap (which also takes 1 minute).
# 3. we have four workers to install wheels, but they have to share one tool that helps put the axle in place.
#    therefore installing the front axel and the back axel cannot be simultaneous.
# 4. before shipping the car we must inspect it, and the inspection takes 3 minutes.


names = {"axel_f", "axel_b", "wheel_rf", "wheel_lf", "wheel_rb", "wheel_lb", "nuts_rf", "nuts_lf", "nuts_rb", "nuts_lb",
         "cap_rf", "cap_lf", "cap_rb", "cap_lb", "inspect"}

name_to_variable_map = csp.Variable.from_names_to_equal_domain(names, range(1, 28))


class TimeDelayer:
    def __init__(self, delay_time: int):
        self.__delay_time = delay_time

    def __call__(self, values: tuple) -> bool:
        if len(values) < 2:
            return True
        first_task, second_task = values
        return first_task + self.__delay_time <= second_task


ten_delayer = TimeDelayer(10)
one_delayer = TimeDelayer(1)
two_delayer = TimeDelayer(2)
three_delayer = TimeDelayer(3)

const1 = csp.Constraint((name_to_variable_map["axel_f"], name_to_variable_map["wheel_rf"]), ten_delayer)
const2 = csp.Constraint((name_to_variable_map["axel_b"], name_to_variable_map["wheel_rb"]), ten_delayer)
const3 = csp.Constraint((name_to_variable_map["axel_f"], name_to_variable_map["wheel_lf"]), ten_delayer)
const4 = csp.Constraint((name_to_variable_map["axel_b"], name_to_variable_map["wheel_lb"]), ten_delayer)

const5 = csp.Constraint((name_to_variable_map["wheel_rf"], name_to_variable_map["nuts_rf"]), one_delayer)
const6 = csp.Constraint((name_to_variable_map["wheel_lf"], name_to_variable_map["nuts_lf"]), one_delayer)
const7 = csp.Constraint((name_to_variable_map["wheel_rb"], name_to_variable_map["nuts_rb"]), one_delayer)
const8 = csp.Constraint((name_to_variable_map["wheel_lb"], name_to_variable_map["nuts_lb"]), one_delayer)

const9 = csp.Constraint((name_to_variable_map["nuts_rf"], name_to_variable_map["cap_rf"]), two_delayer)
const10 = csp.Constraint((name_to_variable_map["nuts_lf"], name_to_variable_map["cap_lf"]), two_delayer)
const11 = csp.Constraint((name_to_variable_map["nuts_rb"], name_to_variable_map["cap_rb"]), two_delayer)
const12 = csp.Constraint((name_to_variable_map["nuts_lb"], name_to_variable_map["cap_lb"]), two_delayer)

const13 = csp.Constraint((name_to_variable_map["axel_f"], name_to_variable_map["axel_b"]), ten_delayer)

constraints = set()
for name in names - {"inspect"}:
    constraints.add(csp.Constraint((name_to_variable_map[name], name_to_variable_map["inspect"]), three_delayer))

constraints.update((const1, const2, const3, const4, const5, const6, const7, const8, const9, const10, const11, const12,
                    const13))

car_assembly_problem = csp.ConstraintProblem(constraints)


# /////////////////////////////////////////////// USAGE EXAMPLE ///////////////////////////////////////////////
# csp.heuristic_backtracking_search(car_assembly_problem)
# sorted_by_value = sorted((var.value, name) for name, var in name_to_variable_map.items())
# for value, name in sorted_by_value:
#    print(name, ":", value)
#
# axel_f : 1
# axel_b : 11
# wheel_lf : 11
# wheel_rf : 11
# nuts_lf : 12
# nuts_rf : 12
# cap_lf : 14
# cap_rf : 14
# wheel_lb : 21
# wheel_rb : 21
# nuts_lb : 22
# nuts_rb : 22
# cap_lb : 24
# cap_rb : 24
# inspect : 27
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////


measure_performance(1, "car_assembly_problem", car_assembly_problem,
                    "heuristic_backtracking_search", with_history=True)
measure_performance(1, "car_assembly_problem", car_assembly_problem,
                    "heuristic_backtracking_search", inference=csp.forward_check, with_history=True)
measure_performance(2, "car_assembly_problem", car_assembly_problem,
                    "min_conflicts", 100000, with_history=True)
measure_performance(2, "car_assembly_problem", car_assembly_problem,
                    "constraints_weighting", 100000, with_history=True)
measure_performance(2, "car_assembly_problem", car_assembly_problem,
                    "simulated_annealing", 100000, 0.5, 0.99999)
measure_performance(2, "car_assembly_problem", car_assembly_problem,
                    "random_restart_first_choice_hill_climbing", 10, 10, 10)
general_genetic_car_assembly_problem = csp.GeneralGeneticConstraintProblem(car_assembly_problem, 0.1)
measure_performance(2, "car_assembly_problem", general_genetic_car_assembly_problem,
                    "genetic_local_search", 100, 100, 0.1)


ac3_car_assembly_problem = copy.deepcopy(car_assembly_problem)
ac3_car_assembly_problem.unassign_all_variables()
ac3_start_time = time.process_time()
ac3_is_arc_consistent = csp.ac3(ac3_car_assembly_problem)
ac3_end_time = time.process_time()
if ac3_is_arc_consistent:
    print()
    print()
    print("-" * 145)
    print("using ac3 as a preprocessing stage which took", ac3_end_time - ac3_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "ac3_car_assembly_problem", ac3_car_assembly_problem,
                        "backtracking_search", with_history=True)
    measure_performance(1, "ac3_car_assembly_problem", ac3_car_assembly_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "ac3_car_assembly_problem", ac3_car_assembly_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "ac3_car_assembly_problem", ac3_car_assembly_problem,
                        "heuristic_backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "ac3_car_assembly_problem", ac3_car_assembly_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "ac3_car_assembly_problem", ac3_car_assembly_problem,
                        "min_conflicts", 100, with_history=True)
    measure_performance(2, "ac3_car_assembly_problem", ac3_car_assembly_problem,
                        "constraints_weighting", 1000, with_history=True)
    measure_performance(2, "ac3_car_assembly_problem", ac3_car_assembly_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "ac3_car_assembly_problem", ac3_car_assembly_problem,
                        "random_restart_first_choice_hill_climbing", 10, 10, 10)
    general_genetic_car_assembly_problem = csp.GeneralGeneticConstraintProblem(ac3_car_assembly_problem, 0.1)
    measure_performance(2, "ac3_car_assembly_problem", general_genetic_car_assembly_problem,
                        "genetic_local_search", 100, 100, 0.1)


ac4_car_assembly_problem = copy.deepcopy(car_assembly_problem)
ac4_car_assembly_problem.unassign_all_variables()
ac4_start_time = time.process_time()
ac4_is_arc_consistent = csp.ac4(ac4_car_assembly_problem)
ac4_end_time = time.process_time()
if ac4_is_arc_consistent:
    print()
    print()
    print("-" * 145)
    print("using ac4 as a preprocessing stage which took", ac4_end_time - ac4_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "ac4_car_assembly_problem", ac4_car_assembly_problem,
                        "backtracking_search", with_history=True)
    measure_performance(1, "ac4_car_assembly_problem", ac4_car_assembly_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "ac4_car_assembly_problem", ac4_car_assembly_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "ac4_car_assembly_problem", ac4_car_assembly_problem,
                        "heuristic_backtracking_search", inference=csp.forward_check,  with_history=True)
    measure_performance(1, "ac4_car_assembly_problem", ac4_car_assembly_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "ac4_car_assembly_problem", ac4_car_assembly_problem,
                        "min_conflicts", 100, with_history=True)
    measure_performance(2, "ac4_car_assembly_problem", ac4_car_assembly_problem,
                        "constraints_weighting", 100, with_history=True)
    measure_performance(2, "ac4_car_assembly_problem", ac4_car_assembly_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "ac4_car_assembly_problem", ac4_car_assembly_problem,
                        "random_restart_first_choice_hill_climbing", 10, 10, 10)
    general_genetic_car_assembly_problem = csp.GeneralGeneticConstraintProblem(ac4_car_assembly_problem, 0.1)
    measure_performance(2, "ac4_car_assembly_problem", general_genetic_car_assembly_problem,
                        "genetic_local_search", 100, 100, 0.1)


pc2_car_assembly_problem = copy.deepcopy(car_assembly_problem)
pc2_car_assembly_problem.unassign_all_variables()
pc2_start_time = time.process_time()
pc2_is_path_consistent = csp.pc2(pc2_car_assembly_problem)
pc2_end_time = time.process_time()
if pc2_is_path_consistent:
    print()
    print()
    print("-" * 145)
    print("using pc2 as a preprocessing stage which took", pc2_end_time - pc2_start_time, "seconds")
    print("-" * 145)

    measure_performance(1, "pc2_car_assembly_problem", pc2_car_assembly_problem,
                        "backtracking_search", with_history=True)
    measure_performance(1, "pc2_car_assembly_problem", pc2_car_assembly_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "pc2_car_assembly_problem", pc2_car_assembly_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "pc2_car_assembly_problem", pc2_car_assembly_problem,
                        "heuristic_backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "pc2_car_assembly_problem", pc2_car_assembly_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "pc2_car_assembly_problem", pc2_car_assembly_problem,
                        "min_conflicts", 100000, with_history=True)
    measure_performance(2, "pc2_car_assembly_problem", pc2_car_assembly_problem,
                        "constraints_weighting", 100, with_history=True)
    measure_performance(2, "pc2_car_assembly_problem", pc2_car_assembly_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "pc2_car_assembly_problem", pc2_car_assembly_problem,
                        "random_restart_first_choice_hill_climbing", 10, 10, 10)
    general_genetic_car_assembly_problem = csp.GeneralGeneticConstraintProblem(pc2_car_assembly_problem, 0.1)
    measure_performance(2, "pc2_car_assembly_problem", general_genetic_car_assembly_problem,
                        "genetic_local_search", 100, 100, 0.1)


two_consistency_car_assembly_problem = copy.deepcopy(car_assembly_problem)
two_consistency_car_assembly_problem.unassign_all_variables()
two_consistency_start_time = time.process_time()
is_two_consistent = csp.i_consistency(two_consistency_car_assembly_problem, 2)
two_consistency_end_time = time.process_time()
if is_two_consistent:
    print()
    print()
    print("-" * 145)
    print("using 2-consistency as a preprocessing stage which took",
          two_consistency_end_time - two_consistency_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "two_consistency_car_assembly_problem", two_consistency_car_assembly_problem,
                        "backtracking_search", with_history=True)
    measure_performance(1, "two_consistency_car_assembly_problem", two_consistency_car_assembly_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True)
    
    measure_performance(1, "two_consistency_car_assembly_problem", two_consistency_car_assembly_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "two_consistency_car_assembly_problem", two_consistency_car_assembly_problem,
                        "heuristic_backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "two_consistency_car_assembly_problem", two_consistency_car_assembly_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "two_consistency_car_assembly_problem", two_consistency_car_assembly_problem,
                        "min_conflicts", 100, with_history=True)
    measure_performance(2, "two_consistency_car_assembly_problem", two_consistency_car_assembly_problem,
                        "constraints_weighting", 100, with_history=True)
    measure_performance(2, "two_consistency_car_assembly_problem", two_consistency_car_assembly_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "two_consistency_car_assembly_problem", two_consistency_car_assembly_problem,
                        "random_restart_first_choice_hill_climbing", 10, 10, 10)
    general_genetic_car_assembly_problem = \
        csp.GeneralGeneticConstraintProblem(two_consistency_car_assembly_problem, 0.1)
    measure_performance(2, "two_consistency_car_assembly_problem", general_genetic_car_assembly_problem,
                        "genetic_local_search", 100, 100, 0.1)



# /////////////////////////////////////////////////////// PERFORMANCE RESULTS /////////////////////////////////////////////////////////////////////
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search' with problem: 'car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [1579]
# time results (seconds): [13.0625]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search_with_forward_checking' with problem: 'car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [1579]
# time results (seconds): [14.53125]
# #################################################################################################################################################
# displaying performance results of solver: 'min_conflicts' with problem: 'car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [1, 0]
# solution lengths (number of assignment and unassignment actions): [200030, 858]
# time results (seconds): [629.140625, 2.578125]
# #################################################################################################################################################
# displaying performance results of solver: 'constraints_weighting' with problem: 'car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [9, 13]
# solution lengths (number of assignment and unassignment actions): [200000, 200000]
# time results (seconds): [2121.328125, 2127.15625]
# #################################################################################################################################################
# displaying performance results of solver: 'simulated_annealing' with problem: 'car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [1, 1]
# time results (seconds): [244.34375, 243.328125]
# #################################################################################################################################################
# displaying performance results of solver: 'random_restart_first_choice_hill_climbing' with problem: 'car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [4, 5]
# time results (seconds): [1.296875, 1.078125]
# #################################################################################################################################################
# displaying performance results of solver: 'genetic_local_search' with problem: 'car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [3, 3]
# time results (seconds): [3.515625, 3.71875]
#
#
# -------------------------------------------------------------------------------------------------------------------------------------------------
# using ac3 as a preprocessing stage which took 0.25 seconds
# -------------------------------------------------------------------------------------------------------------------------------------------------
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search' with problem: 'ac3_car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [15]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search_with_forward_checking' with problem: 'ac3_car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [15]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search' with problem: 'ac3_car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [15]
# time results (seconds): [0.046875]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search_with_forward_checking' with problem: 'ac3_car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [15]
# time results (seconds): [0.046875]
# #################################################################################################################################################
# displaying performance results of solver: 'naive_cycle_cutset' with problem: 'ac3_car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [15]
# time results (seconds): [0.015625]
# #################################################################################################################################################
# displaying performance results of solver: 'min_conflicts' with problem: 'ac3_car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0, 0]
# solution lengths (number of assignment and unassignment actions): [34, 32]
# time results (seconds): [0.0, 0.015625]
# #################################################################################################################################################
# displaying performance results of solver: 'constraints_weighting' with problem: 'ac3_car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0, 0]
# solution lengths (number of assignment and unassignment actions): [26, 74]
# time results (seconds): [0.046875, 0.171875]
# #################################################################################################################################################
# displaying performance results of solver: 'simulated_annealing' with problem: 'ac3_car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0, 0]
# time results (seconds): [0.15625, 0.078125]
# #################################################################################################################################################
# displaying performance results of solver: 'random_restart_first_choice_hill_climbing' with problem: 'ac3_car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0, 0]
# time results (seconds): [0.796875, 0.09375]
# #################################################################################################################################################
# displaying performance results of solver: 'genetic_local_search' with problem: 'ac3_car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0, 0]
# time results (seconds): [0.015625, 0.03125]
#
#
# -------------------------------------------------------------------------------------------------------------------------------------------------
# using ac4 as a preprocessing stage which took 0.296875 seconds
# -------------------------------------------------------------------------------------------------------------------------------------------------
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search' with problem: 'ac4_car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [15]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'backtracking_search_with_forward_checking' with problem: 'ac4_car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [15]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search' with problem: 'ac4_car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [15]
# time results (seconds): [0.0625]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search_with_forward_checking' with problem: 'ac4_car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [15]
# time results (seconds): [0.046875]
# #################################################################################################################################################
# displaying performance results of solver: 'naive_cycle_cutset' with problem: 'ac4_car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [15]
# time results (seconds): [103.90625]
# #################################################################################################################################################
# displaying performance results of solver: 'min_conflicts' with problem: 'ac4_car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0, 0]
# solution lengths (number of assignment and unassignment actions): [34, 36]
# time results (seconds): [0.0, 0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'constraints_weighting' with problem: 'ac4_car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0, 0]
# solution lengths (number of assignment and unassignment actions): [34, 14]
# time results (seconds): [0.078125, 0.03125]
# #################################################################################################################################################
# displaying performance results of solver: 'simulated_annealing' with problem: 'ac4_car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0, 0]
# time results (seconds): [0.015625, 0.203125]
# #################################################################################################################################################
# displaying performance results of solver: 'random_restart_first_choice_hill_climbing' with problem: 'ac4_car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0, 0]
# time results (seconds): [0.0, 0.234375]
# #################################################################################################################################################
# displaying performance results of solver: 'genetic_local_search' with problem: 'ac4_car_assembly_problem'
# unsatisfied_constraints_amounts out of 27 overall constraints: [0, 0]
# time results (seconds): [0.015625, 0.015625]
#
# Process finished with exit code 0

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////