import time
import copy
import csp
from examples.performance_testing import measure_performance


# SOLVING:                      (where each letter uniquely represent a digit)
#               TWO
#              +TWO
#              ----
#              FOUR


name_to_domain_map = dict()
name_to_domain_map["o"] = range(10)
name_to_domain_map["w"] = range(10)
name_to_domain_map["r"] = range(10)
name_to_domain_map["u"] = range(10)

name_to_domain_map["t"] = range(1, 10)
name_to_domain_map["f"] = range(1, 10)

# carry digits
name_to_domain_map["c_10"] = (0, 1)
name_to_domain_map["c_100"] = (0, 1)
name_to_domain_map["c_1000"] = (0, 1)

name_to_variable_map = csp.Variable.from_names_to_domains(name_to_domain_map)

all_diff_const = csp.Constraint((name_to_variable_map[name] for name in name_to_variable_map if name not in
                                 ["c_10", "c_100", "c_1000"]), csp.all_different)


def units_digit(values: tuple) -> bool:
    if len(values) < 3:
        return True
    o, r, c_10 = values
    return o + o == r + 10 * c_10


units_digit_const = csp.Constraint((name_to_variable_map["o"], name_to_variable_map["r"],
                                    name_to_variable_map["c_10"]), units_digit)


def tens_digit(values: tuple) -> bool:
    if len(values) < 4:
        return True
    c_10, w, u, c_100, = values
    return c_10 + w + w == u + 10 * c_100


tens_digit_const = csp.Constraint((name_to_variable_map["c_10"], name_to_variable_map["w"],
                                   name_to_variable_map["u"], name_to_variable_map["c_100"]), tens_digit)


def hundreds_digit(values: tuple) -> bool:
    if len(values) < 4:
        return True
    c_100, t, o, c_1000 = values
    return c_100 + t + t == o + 10 * c_1000


hundreds_digits_const = csp.Constraint((name_to_variable_map["c_100"], name_to_variable_map["t"],
                                        name_to_variable_map["o"], name_to_variable_map["c_1000"]),
                                       hundreds_digit)


def thousands_digit(values: tuple) -> bool:
    if len(values) < 2:
        return True
    c_1000, f = values
    return c_1000 == f


thousands_digit_const = csp.Constraint((name_to_variable_map["c_1000"], name_to_variable_map["f"]),
                                       thousands_digit)

verbal_arithmetic_problem = csp.ConstraintProblem((all_diff_const, units_digit_const, tens_digit_const,
                                                   hundreds_digits_const, thousands_digit_const))


# /////////////////////////////////////////////// USAGE EXAMPLE ///////////////////////////////////////////////
# csp.heuristic_backtracking_search(verbal_arithmetic_problem)
# for name in name_to_variable_map:
#    print(name, ":", name_to_variable_map[name].value)
#
# o : 4
# u : 6
# r : 8
# c_100 : 0
# w : 3
# t : 7
# c_10 : 0
# c_1000 : 1
# f : 1
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////


measure_performance(1, "verbal_arithmetic_problem", verbal_arithmetic_problem,
                    "backtracking_search", with_history=True)
measure_performance(1, "verbal_arithmetic_problem", verbal_arithmetic_problem,
                    "backtracking_search", inference=csp.forward_check, with_history=True)
measure_performance(1, "verbal_arithmetic_problem", verbal_arithmetic_problem,
                    "heuristic_backtracking_search", inference=None, with_history=True)
measure_performance(1, "verbal_arithmetic_problem", verbal_arithmetic_problem,
                    "heuristic_backtracking_search", with_history=True)
measure_performance(1, "verbal_arithmetic_problem", verbal_arithmetic_problem,
                    "naive_cycle_cutset", with_history=True)
measure_performance(2, "verbal_arithmetic_problem", verbal_arithmetic_problem,
                    "min_conflicts", 100000, with_history=True)
measure_performance(2, "verbal_arithmetic_problem", verbal_arithmetic_problem,
                    "constraints_weighting", 10000, with_history=True)
measure_performance(2, "verbal_arithmetic_problem", verbal_arithmetic_problem,
                    "simulated_annealing", 100000, 0.5, 0.99999)
measure_performance(2, "verbal_arithmetic_problem", verbal_arithmetic_problem,
                    "random_restart_first_choice_hill_climbing", 100, 100, 10)
general_genetic_verbal_arithmetic_problem = csp.GeneralGeneticConstraintProblem(verbal_arithmetic_problem, 0.1)
measure_performance(2, "verbal_arithmetic_problem", general_genetic_verbal_arithmetic_problem,
                    "genetic_local_search", 100, 100, 0.1)

ac3_verbal_arithmetic_problem = copy.deepcopy(verbal_arithmetic_problem)
ac3_verbal_arithmetic_problem.unassign_all_variables()
ac3_start_time = time.process_time()
ac3_is_arc_consistent = csp.ac3(ac3_verbal_arithmetic_problem)
ac3_end_time = time.process_time()
if ac3_is_arc_consistent:
    print()
    print()
    print("-" * 145)
    print("using ac3 as a preprocessing stage which took", ac3_end_time - ac3_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "ac3_verbal_arithmetic_problem", ac3_verbal_arithmetic_problem,
                        "backtracking_search", with_history=True)
    measure_performance(1, "ac3_verbal_arithmetic_problem", ac3_verbal_arithmetic_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "ac3_verbal_arithmetic_problem", ac3_verbal_arithmetic_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True)
    measure_performance(1, "ac3_verbal_arithmetic_problem", ac3_verbal_arithmetic_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "ac3_verbal_arithmetic_problem", ac3_verbal_arithmetic_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "ac3_verbal_arithmetic_problem", ac3_verbal_arithmetic_problem,
                        "min_conflicts", 100000, with_history=True)
    measure_performance(2, "ac3_verbal_arithmetic_problem", ac3_verbal_arithmetic_problem,
                        "constraints_weighting", 10000, with_history=True)
    measure_performance(2, "ac3_verbal_arithmetic_problem", ac3_verbal_arithmetic_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "ac3_verbal_arithmetic_problem", ac3_verbal_arithmetic_problem,
                        "random_restart_first_choice_hill_climbing", 100, 100, 10)
    general_genetic_verbal_arithmetic_problem = csp.GeneralGeneticConstraintProblem(ac3_verbal_arithmetic_problem, 0.1)
    measure_performance(2, "ac3_verbal_arithmetic_problem", general_genetic_verbal_arithmetic_problem,
                        "genetic_local_search", 100, 100, 0.1)

ac4_verbal_arithmetic_problem = copy.deepcopy(verbal_arithmetic_problem)
ac4_verbal_arithmetic_problem.unassign_all_variables()
ac4_start_time = time.process_time()
ac4_is_arc_consistent = csp.ac4(ac4_verbal_arithmetic_problem)
ac4_end_time = time.process_time()
if ac4_is_arc_consistent:
    print()
    print()
    print("-" * 145)
    print("using ac4 as a preprocessing stage which took", ac4_end_time - ac4_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "ac4_verbal_arithmetic_problem", ac4_verbal_arithmetic_problem,
                        "backtracking_search", with_history=True)
    measure_performance(1, "ac4_verbal_arithmetic_problem", ac4_verbal_arithmetic_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "ac4_verbal_arithmetic_problem", ac4_verbal_arithmetic_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True)
    measure_performance(1, "ac4_verbal_arithmetic_problem", ac4_verbal_arithmetic_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "ac4_verbal_arithmetic_problem", ac4_verbal_arithmetic_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "ac4_verbal_arithmetic_problem", ac4_verbal_arithmetic_problem,
                        "min_conflicts", 100000, with_history=True)
    measure_performance(2, "ac4_verbal_arithmetic_problem", ac4_verbal_arithmetic_problem,
                        "constraints_weighting", 10000, with_history=True)
    measure_performance(2, "ac4_verbal_arithmetic_problem", ac4_verbal_arithmetic_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "ac4_verbal_arithmetic_problem", ac4_verbal_arithmetic_problem,
                        "random_restart_first_choice_hill_climbing", 100, 100, 10)
    general_genetic_verbal_arithmetic_problem = csp.GeneralGeneticConstraintProblem(ac4_verbal_arithmetic_problem, 0.1)
    measure_performance(2, "ac4_verbal_arithmetic_problem", general_genetic_verbal_arithmetic_problem,
                        "genetic_local_search", 100, 100, 0.1)

pc2_verbal_arithmetic_problem = copy.deepcopy(verbal_arithmetic_problem)
pc2_verbal_arithmetic_problem.unassign_all_variables()
pc2_start_time = time.process_time()
pc2_is_path_consistent = csp.pc2(pc2_verbal_arithmetic_problem)
pc2_end_time = time.process_time()
if pc2_is_path_consistent:
    print()
    print()
    print("-" * 145)
    print("using pc2 as a preprocessing stage which took", pc2_end_time - pc2_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "pc2_verbal_arithmetic_problem", pc2_verbal_arithmetic_problem,
                        "backtracking_search", with_history=True)
    measure_performance(1, "pc2_verbal_arithmetic_problem", pc2_verbal_arithmetic_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "pc2_verbal_arithmetic_problem", pc2_verbal_arithmetic_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True)
    measure_performance(1, "pc2_verbal_arithmetic_problem", pc2_verbal_arithmetic_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "pc2_verbal_arithmetic_problem", pc2_verbal_arithmetic_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "pc2_verbal_arithmetic_problem", pc2_verbal_arithmetic_problem,
                        "min_conflicts", 100000, with_history=True)
    measure_performance(2, "pc2_verbal_arithmetic_problem", pc2_verbal_arithmetic_problem,
                        "constraints_weighting", 10000, with_history=True)
    measure_performance(2, "pc2_verbal_arithmetic_problem", pc2_verbal_arithmetic_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "pc2_verbal_arithmetic_problem", pc2_verbal_arithmetic_problem,
                        "random_restart_first_choice_hill_climbing", 100, 100, 10)
    general_genetic_verbal_arithmetic_problem = csp.GeneralGeneticConstraintProblem(pc2_verbal_arithmetic_problem, 0.1)
    measure_performance(2, "pc2_verbal_arithmetic_problem", general_genetic_verbal_arithmetic_problem,
                        "genetic_local_search", 100, 100, 0.1)

two_consistency_verbal_arithmetic_problem = copy.deepcopy(verbal_arithmetic_problem)
two_consistency_verbal_arithmetic_problem.unassign_all_variables()
two_consistency_start_time = time.process_time()
is_two_consistent = csp.i_consistency(two_consistency_verbal_arithmetic_problem, 2)
two_consistency_end_time = time.process_time()
if is_two_consistent:
    print()
    print()
    print("-" * 145)
    print("using 2-consistency as a preprocessing stage which took",
          two_consistency_end_time - two_consistency_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "two_consistency_verbal_arithmetic_problem", two_consistency_verbal_arithmetic_problem,
                        "backtracking_search", with_history=True)
    measure_performance(1, "two_consistency_verbal_arithmetic_problem", two_consistency_verbal_arithmetic_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "two_consistency_verbal_arithmetic_problem", two_consistency_verbal_arithmetic_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True)
    measure_performance(1, "two_consistency_verbal_arithmetic_problem", two_consistency_verbal_arithmetic_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "two_consistency_verbal_arithmetic_problem", two_consistency_verbal_arithmetic_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "two_consistency_verbal_arithmetic_problem", two_consistency_verbal_arithmetic_problem,
                        "min_conflicts", 100000, with_history=True)
    measure_performance(2, "two_consistency_verbal_arithmetic_problem", two_consistency_verbal_arithmetic_problem,
                        "constraints_weighting", 10000, with_history=True)
    measure_performance(2, "two_consistency_verbal_arithmetic_problem", two_consistency_verbal_arithmetic_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "two_consistency_verbal_arithmetic_problem", two_consistency_verbal_arithmetic_problem,
                        "random_restart_first_choice_hill_climbing", 100, 100, 10)
    general_genetic_verbal_arithmetic_problem = \
        csp.GeneralGeneticConstraintProblem(two_consistency_verbal_arithmetic_problem, 0.1)
    measure_performance(2, "two_consistency_verbal_arithmetic_problem", general_genetic_verbal_arithmetic_problem,
                        "genetic_local_search", 100, 100, 0.1)
