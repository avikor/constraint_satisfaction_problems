import time
import copy
import csp
from examples.performance_testing import measure_performance


# ////////////////////////////////////////// einstein's five house riddle //////////////////////////////////////////
# ///// The situation: /////
# 1. There are 5 houses in five different colors.
# 2. In each house lives a person with a different nationality.
# 3. These five owners drink a certain type of beverage, smoke a certain brand of cigar and keep a certain pet.
# 4. No owners have the same pet, smoke the same brand of cigar or drink the same beverage.
#
# - THE QUESTION IS: WHO OWNS THE FISH?
#
# /// Hints: ///
# 1. the brit lives in the red house
# 2. the swede keeps dogs as pets
# 3. the dane drinks tea
# 4. the green house is on the left of the white house
# 5. the green house's owner drinks coffee
# 6. the person who smokes pallmall rears birds
# 7. the owner of the yellow house smokes dunhill
# 8. the man living in the center house drinks milk
# 9. the norwegian lives in the first house
# 10. the man who smokes blends lives next to the one who keeps cats
# 11. the man who keeps horses lives next to the man who smokes dunhill
# 12. the owner who smokes bluemaster drinks beer
# 13. the german smokes prince
# 14. the norwegian lives next to the blue house
# 15. the man who smokes blend has a neighbor who drinks water
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////


colors = ("red", "white", "green", "yellow", "blue")
nationalities = ("brit", "swede", "dane", "norwegian", "german")
drinks = ("tea", "coffee", "milk", "beer", "water")
smokes = ("pallmall", "dunhill", "blends", "bluemaster", "prince")
pets = ("dogs", "birds", "cats", "horses", "fish")

color_vars = dict()
nationality_vars = dict()
drink_vars = dict()
smoke_vars = dict()
pets_vars = dict()

for i in range(1, 6):
    color_vars[i] = csp.Variable(colors)
    nationality_vars[i] = csp.Variable(nationalities)
    drink_vars[i] = csp.Variable(drinks)
    smoke_vars[i] = csp.Variable(smokes)
    pets_vars[i] = csp.Variable(pets)

constraints = set()
constraints.add(csp.Constraint(color_vars.values(), csp.all_different))
constraints.add(csp.Constraint(nationality_vars.values(), csp.all_different))
constraints.add(csp.Constraint(drink_vars.values(), csp.all_different))
constraints.add(csp.Constraint(smoke_vars.values(), csp.all_different))
constraints.add(csp.Constraint(pets_vars.values(), csp.all_different))


def hint_one(values: tuple) -> bool:
    if len(values) < 2:
        return True
    nationality, color = values
    return nationality != "brit" or color == "red"


def hint_two(values: tuple) -> bool:
    if len(values) < 2:
        return True
    nationality, pet = values
    return nationality != "swede" or pet == "dogs"


def hint_three(values: tuple) -> bool:
    if len(values) < 2:
        return True
    nationality, drink = values
    return nationality != "dane" or drink == "tea"


def hint_four_a(values: tuple) -> bool:
    if len(values) < 2:
        return True
    color1, color2 = values
    return color1 != "green" or color2 == "white"


def hint_four_b(values: tuple) -> bool:
    if len(values) < 1:
        return True
    color, *_ = values
    return color != "green"


def hint_five(values: tuple) -> bool:
    if len(values) < 2:
        return True
    color, drink = values
    return color != "green" or drink == "coffee"


def hint_six(values: tuple) -> bool:
    if len(values) < 2:
        return True
    smoke, pet = values
    return smoke != "pallmall" or pet == "birds"


def hint_seven(values: tuple) -> bool:
    if len(values) < 2:
        return True
    color, smoke = values
    return color != "yellow" or smoke == "dunhill"


def hint_eight(values: tuple) -> bool:
    if len(values) < 1:
        return True
    drink, *_ = values
    return drink == "milk"


def hint_nine(values: tuple) -> bool:
    if len(values) < 1:
        return True
    nationality, *_ = values
    return nationality == "norwegian"


def hint_ten_a(values: tuple) -> bool:
    if len(values) < 3:
        return True
    smoke, pet1, pet2 = values
    return smoke != "blends" or pet1 == "cats" or pet2 == "cats"


def hint_ten_b(values: tuple) -> bool:
    if len(values) < 2:
        return True
    smoke, pet = values
    return smoke != "blends" or pet == "cats"


def hint_elven_a(values: tuple) -> bool:
    if len(values) < 3:
        return True
    pet, smoke1, smoke2 = values
    return pet != "horses" or smoke1 == "dunhill" or smoke2 == "dunhill"


def hint_elven_b(values: tuple) -> bool:
    if len(values) < 2:
        return True
    pet,  smoke = values
    return pet != "horses" or smoke == "dunhill"


def hint_twelve(values: tuple) -> bool:
    if len(values) < 2:
        return True
    smoke, drink = values
    return smoke != "bluemaster" or drink == "beer"


def hint_thirteen(values: tuple) -> bool:
    if len(values) < 2:
        return True
    nationality, smoke = values
    return nationality != "german" or smoke == "prince"


def hint_fourteen_a(values: tuple) -> bool:
    if len(values) < 3:
        return True
    nationality, color1, color2 = values
    return nationality != "norwegian" or color1 == "blue" or color2 == "blue"


def hint_fourteen_b(values: tuple) -> bool:
    if len(values) < 2:
        return True
    nationality, color = values
    return nationality != "norwegian" or color == "blue"


def hint_fifteen_a(values: tuple) -> bool:
    if len(values) < 3:
        return True
    smoke, drink1, drink2 = values
    return smoke != "blends" or drink1 == "water" or drink2 == "water"


def hint_fifteen_b(values: tuple) -> bool:
    if len(values) < 2:
        return True
    smoke, drink = values
    return smoke != "blends" or drink == "water"


for i in range(1, 6):
    constraints.add(csp.Constraint((nationality_vars[i], color_vars[i]), hint_one))
    constraints.add(csp.Constraint((nationality_vars[i], pets_vars[i]), hint_two))
    constraints.add(csp.Constraint((nationality_vars[i], drink_vars[i]), hint_three))

    if i < 5:
        constraints.add(csp.Constraint((color_vars[i], color_vars[i + 1]), hint_four_a))
    else:
        constraints.add(csp.Constraint((color_vars[i],), hint_four_b))

    constraints.add(csp.Constraint((color_vars[i], drink_vars[i]), hint_five))
    constraints.add(csp.Constraint((smoke_vars[i], pets_vars[i]), hint_six))
    constraints.add(csp.Constraint((color_vars[i], smoke_vars[i]), hint_seven))

    if i == 3:
        constraints.add(csp.Constraint((drink_vars[i],), hint_eight))
    if i == 1:
        constraints.add(csp.Constraint((nationality_vars[i],), hint_nine))

    if 1 < i < 5:
        constraints.add(csp.Constraint((smoke_vars[i], pets_vars[i - 1], pets_vars[i + 1]), hint_ten_a))
    elif i == 1:
        constraints.add(csp.Constraint((smoke_vars[i], pets_vars[2]), hint_ten_b))
        constraints.add(csp.Constraint((smoke_vars[2], pets_vars[i]), hint_ten_b))
    else:
        constraints.add(csp.Constraint((smoke_vars[i], pets_vars[4]), hint_ten_b))
        constraints.add(csp.Constraint((smoke_vars[4], pets_vars[i]), hint_ten_b))

    if 1 < i < 5:
        constraints.add(csp.Constraint((pets_vars[i], smoke_vars[i - 1], smoke_vars[i + 1]), hint_elven_a))
    elif i == 1:
        constraints.add(csp.Constraint((pets_vars[i], smoke_vars[2]), hint_elven_a))
        constraints.add(csp.Constraint((pets_vars[2], smoke_vars[i]), hint_elven_a))
    else:
        constraints.add(csp.Constraint((pets_vars[i], smoke_vars[4]), hint_elven_a))
        constraints.add(csp.Constraint((pets_vars[4], smoke_vars[i]), hint_elven_a))

    constraints.add(csp.Constraint((smoke_vars[i], drink_vars[i]), hint_twelve))
    constraints.add(csp.Constraint((nationality_vars[i], smoke_vars[i]), hint_thirteen))

    if 1 < i < 5:
        constraints.add(csp.Constraint((nationality_vars[i], color_vars[i - 1], color_vars[i + 1]),
                                       hint_fourteen_a))
    elif i == 1:
        constraints.add(csp.Constraint((nationality_vars[i], color_vars[2]), hint_fourteen_b))
        constraints.add(csp.Constraint((nationality_vars[2], color_vars[i]), hint_fourteen_b))
    else:
        constraints.add(csp.Constraint((nationality_vars[i], color_vars[4]), hint_fourteen_b))
        constraints.add(csp.Constraint((nationality_vars[4], color_vars[i]), hint_fourteen_b))

    if 1 < i < 5:
        constraints.add(csp.Constraint((smoke_vars[i], drink_vars[i - 1], drink_vars[i + 1]), hint_fifteen_a))
    elif i == 1:
        constraints.add(csp.Constraint((smoke_vars[i], drink_vars[2]), hint_fifteen_b))
        constraints.add(csp.Constraint((smoke_vars[2], drink_vars[i]), hint_fifteen_b))
    else:
        constraints.add(csp.Constraint((smoke_vars[i], drink_vars[4]), hint_fifteen_b))
        constraints.add(csp.Constraint((smoke_vars[4], drink_vars[i]), hint_fifteen_b))


einstein_problem = csp.ConstraintProblem(constraints)


# /////////////////////////////////////////////// USAGE EXAMPLE ///////////////////////////////////////////////
# csp.heuristic_backtracking_search(einstein_problem)
# for i in range(1, 6):
#    print(i, ":", color_vars[i].value, nationality_vars[i].value, drink_vars[i].value, smoke_vars[i].value,
#          pets_vars[i].value)
#
# 1 : yellow norwegian water dunhill cats
# 2 : blue dane tea blends horses
# 3 : red brit milk pallmall birds
# 4 : green german coffee prince fish
# 5 : white swede beer bluemaster dogs
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////


measure_performance(1, "einstein_problem", einstein_problem,
                    "heuristic_backtracking_search", inference=None, with_history=True)
measure_performance(1, "einstein_problem", einstein_problem,
                    "heuristic_backtracking_search", with_history=True)
measure_performance(1, "einstein_problem", einstein_problem,
                    "naive_cycle_cutset", with_history=True)
measure_performance(2, "einstein_problem", einstein_problem,
                    "min_conflicts", 100000, with_history=True)
measure_performance(2, "einstein_problem", einstein_problem,
                    "constraints_weighting", 10000, with_history=True)
measure_performance(2, "einstein_problem", einstein_problem,
                    "simulated_annealing", 100000, 0.5, 0.99999)
measure_performance(2, "einstein_problem", einstein_problem,
                    "random_restart_first_choice_hill_climbing", 100, 100, 10)
general_genetic_einstein_problem = csp.GeneralGeneticConstraintProblem(einstein_problem, 0.1)
measure_performance(2, "einstein_problem", general_genetic_einstein_problem,
                    "genetic_local_search", 100, 100, 0.1)


ac3_einstein_problem = copy.deepcopy(einstein_problem)
ac3_einstein_problem.unassign_all_variables()
ac3_start_time = time.process_time()
ac3_is_arc_consistent = csp.ac3(ac3_einstein_problem)
ac3_end_time = time.process_time()
if ac3_is_arc_consistent:
    print()
    print()
    print("-" * 145)
    print("using ac3 as a preprocessing stage which took", ac3_end_time - ac3_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "ac3_einstein_problem", ac3_einstein_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True)
    measure_performance(1, "ac3_einstein_problem", ac3_einstein_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "ac3_einstein_problem", ac3_einstein_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "ac3_einstein_problem", ac3_einstein_problem,
                        "min_conflicts", 100000, with_history=True)
    measure_performance(2, "ac3_einstein_problem", ac3_einstein_problem,
                        "constraints_weighting", 10000, with_history=True)
    measure_performance(2, "ac3_einstein_problem", ac3_einstein_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "ac3_einstein_problem", ac3_einstein_problem,
                        "random_restart_first_choice_hill_climbing", 100, 100, 10)
    general_genetic_ac3_einstein_problem = csp.GeneralGeneticConstraintProblem(ac3_einstein_problem, 0.1)
    measure_performance(2, "ac3_einstein_problem", general_genetic_ac3_einstein_problem,
                        "genetic_local_search", 100, 100, 0.1)


ac4_einstein_problem = copy.deepcopy(einstein_problem)
ac4_einstein_problem.unassign_all_variables()
ac4_start_time = time.process_time()
ac4_is_arc_consistent = csp.ac4(ac4_einstein_problem)
ac4_end_time = time.process_time()
if ac4_is_arc_consistent:
    print()
    print()
    print("-" * 145)
    print("using ac4 as a preprocessing stage which took", ac4_end_time - ac4_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "ac4_einstein_problem", ac4_einstein_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True)
    measure_performance(1, "ac4_einstein_problem", ac4_einstein_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "ac4_einstein_problem", ac4_einstein_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "ac4_einstein_problem", ac4_einstein_problem,
                        "min_conflicts", 100000, with_history=True)
    measure_performance(2, "ac4_einstein_problem", ac4_einstein_problem,
                        "constraints_weighting", 10000, with_history=True)
    measure_performance(2, "ac4_einstein_problem", ac4_einstein_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "ac4_einstein_problem", ac4_einstein_problem,
                        "random_restart_first_choice_hill_climbing", 100, 100, 10)
    general_genetic_ac4_einstein_problem = csp.GeneralGeneticConstraintProblem(ac4_einstein_problem, 0.1)
    measure_performance(2, "ac4_einstein_problem", general_genetic_ac4_einstein_problem,
                        "genetic_local_search", 100, 100, 0.1)


pc2_einstein_problem = copy.deepcopy(einstein_problem)
pc2_einstein_problem.unassign_all_variables()
pc2_start_time = time.process_time()
pc2_is_path_consistent = csp.pc2(pc2_einstein_problem)
pc2_end_time = time.process_time()
if pc2_is_path_consistent:
    print()
    print()
    print("-" * 145)
    print("using pc2 as a preprocessing stage which took", pc2_end_time - pc2_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "pc2_einstein_problem", pc2_einstein_problem,
                        "backtracking_search", with_history=True)
    measure_performance(1, "pc2_einstein_problem", pc2_einstein_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "pc2_einstein_problem", pc2_einstein_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True)
    measure_performance(1, "pc2_einstein_problem", pc2_einstein_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "pc2_einstein_problem", pc2_einstein_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "pc2_einstein_problem", pc2_einstein_problem,
                        "min_conflicts", 100000, with_history=True)
    measure_performance(2, "pc2_einstein_problem", pc2_einstein_problem,
                        "constraints_weighting", 10000, with_history=True)
    measure_performance(2, "pc2_einstein_problem", pc2_einstein_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "pc2_einstein_problem", pc2_einstein_problem,
                        "random_restart_first_choice_hill_climbing", 100, 100, 10)
    general_genetic_pc2_einstein_problem = csp.GeneralGeneticConstraintProblem(pc2_einstein_problem, 0.1)
    measure_performance(2, "pc2_einstein_problem", general_genetic_pc2_einstein_problem,
                        "genetic_local_search", 100, 100, 0.1)


two_consistency_einstein_problem = copy.deepcopy(einstein_problem)
two_consistency_einstein_problem.unassign_all_variables()
two_consistency_start_time = time.process_time()
is_two_consistent = csp.i_consistency(two_consistency_einstein_problem, 2)
two_consistency_end_time = time.process_time()
if is_two_consistent:
    print()
    print()
    print("-" * 145)
    print("using 2-consistency as a preprocessing stage which took",
          two_consistency_end_time - two_consistency_start_time, "seconds")
    print("-" * 145)
    measure_performance(1, "two_consistency_einstein_problem", two_consistency_einstein_problem,
                        "backtracking_search", with_history=True)
    measure_performance(1, "two_consistency_einstein_problem", two_consistency_einstein_problem,
                        "backtracking_search", inference=csp.forward_check, with_history=True)
    measure_performance(1, "two_consistency_einstein_problem", two_consistency_einstein_problem,
                        "heuristic_backtracking_search", inference=None, with_history=True)
    measure_performance(1, "two_consistency_einstein_problem", two_consistency_einstein_problem,
                        "heuristic_backtracking_search", with_history=True)
    measure_performance(1, "two_consistency_einstein_problem", two_consistency_einstein_problem,
                        "naive_cycle_cutset", with_history=True)
    measure_performance(2, "two_consistency_einstein_problem", two_consistency_einstein_problem,
                        "min_conflicts", 100000, with_history=True)
    measure_performance(2, "two_consistency_einstein_problem", two_consistency_einstein_problem,
                        "constraints_weighting", 10000, with_history=True)
    measure_performance(2, "two_consistency_einstein_problem", two_consistency_einstein_problem,
                        "simulated_annealing", 100000, 0.5, 0.99999)
    measure_performance(2, "two_consistency_einstein_problem", two_consistency_einstein_problem,
                        "random_restart_first_choice_hill_climbing", 100, 100, 10)
    general_genetic_two_consistency_einstein_problem = \
        csp.GeneralGeneticConstraintProblem(two_consistency_einstein_problem, 0.1)
    measure_performance(2, "two_consistency_verbal_arithmetic_problem",
                        general_genetic_two_consistency_einstein_problem, "genetic_local_search", 100, 100, 0.1)



# /////////////////////////////////////////////////////// PERFORMANCE RESULTS /////////////////////////////////////////////////////////////////////
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search' with problem: 'einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [317]
# time results (seconds): [1.734375]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search_with_forward_checking' with problem: 'einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [317]
# time results (seconds): [2.015625]
# #################################################################################################################################################
# displaying performance results of solver: 'naive_cycle_cutset' with problem: 'einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [80]
# solution lengths (number of assignment and unassignment actions): [0]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'min_conflicts' with problem: 'einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [2, 1]
# solution lengths (number of assignment and unassignment actions): [200050, 200050]
# time results (seconds): [333.546875, 332.453125]
# #################################################################################################################################################
# displaying performance results of solver: 'constraints_weighting' with problem: 'einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [14, 16]
# solution lengths (number of assignment and unassignment actions): [20000, 20000]
# time results (seconds): [195.65625, 197.671875]
# #################################################################################################################################################
# displaying performance results of solver: 'simulated_annealing' with problem: 'einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [1, 1]
# time results (seconds): [527.453125, 523.734375]
# #################################################################################################################################################
# displaying performance results of solver: 'random_restart_first_choice_hill_climbing' with problem: 'einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [2, 2]
# time results (seconds): [473.453125, 474.375]
# #################################################################################################################################################
# displaying performance results of solver: 'genetic_local_search' with problem: 'einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [3, 3]
# time results (seconds): [10.75, 10.578125]
#
#
# -------------------------------------------------------------------------------------------------------------------------------------------------
# using ac3 as a preprocessing stage which took 0.078125 seconds
# -------------------------------------------------------------------------------------------------------------------------------------------------
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search' with problem: 'ac3_einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [247]
# time results (seconds): [1.265625]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search_with_forward_checking' with problem: 'ac3_einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [247]
# time results (seconds): [1.46875]
# #################################################################################################################################################
# displaying performance results of solver: 'naive_cycle_cutset' with problem: 'ac3_einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [80]
# solution lengths (number of assignment and unassignment actions): [0]
# time results (seconds): [0.0]
# #################################################################################################################################################
# displaying performance results of solver: 'min_conflicts' with problem: 'ac3_einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [2, 2]
# solution lengths (number of assignment and unassignment actions): [200050, 200050]
# time results (seconds): [294.84375, 293.53125]
# #################################################################################################################################################
# displaying performance results of solver: 'constraints_weighting' with problem: 'ac3_einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [11, 12]
# solution lengths (number of assignment and unassignment actions): [20000, 20000]
# time results (seconds): [172.859375, 172.46875]
# #################################################################################################################################################
# displaying performance results of solver: 'simulated_annealing' with problem: 'ac3_einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [0, 1]
# time results (seconds): [413.96875, 518.515625]
# #################################################################################################################################################
# displaying performance results of solver: 'random_restart_first_choice_hill_climbing' with problem: 'ac3_einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [2, 2]
# time results (seconds): [442.84375, 441.34375]
# #################################################################################################################################################
# displaying performance results of solver: 'genetic_local_search' with problem: 'ac3_einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [2, 2]
# time results (seconds): [10.53125, 10.546875]
#
#
# -------------------------------------------------------------------------------------------------------------------------------------------------
# using ac4 as a preprocessing stage which took 0.046875 seconds
# -------------------------------------------------------------------------------------------------------------------------------------------------
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search' with problem: 'ac4_einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [245]
# time results (seconds): [1.34375]
# #################################################################################################################################################
# displaying performance results of solver: 'heuristic_backtracking_search_with_forward_checking' with problem: 'ac4_einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [0]
# solution lengths (number of assignment and unassignment actions): [245]
# time results (seconds): [1.53125]
# #################################################################################################################################################
# displaying performance results of solver: 'naive_cycle_cutset' with problem: 'ac4_einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [80]
# solution lengths (number of assignment and unassignment actions): [0]
# time results (seconds): [0.015625]
# #################################################################################################################################################
# displaying performance results of solver: 'min_conflicts' with problem: 'ac4_einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [1, 2]
# solution lengths (number of assignment and unassignment actions): [200050, 200050]
# time results (seconds): [281.71875, 304.828125]
# #################################################################################################################################################
# displaying performance results of solver: 'constraints_weighting' with problem: 'ac4_einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [12, 13]
# solution lengths (number of assignment and unassignment actions): [20000, 20000]
# time results (seconds): [190.71875, 190.609375]
#################################################################################################################################################
# displaying performance results of solver: 'simulated_annealing' with problem: 'ac4_einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [1, 1]
# time results (seconds): [518.59375, 523.484375]
# #################################################################################################################################################
# displaying performance results of solver: 'random_restart_first_choice_hill_climbing' with problem: 'ac4_einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [2, 2]
# time results (seconds): [442.65625, 444.84375]
# #################################################################################################################################################
# displaying performance results of solver: 'genetic_local_search' with problem: 'ac4_einstein_problem'
# unsatisfied_constraints_amounts out of 80 overall constraints: [3, 3]
# time results (seconds): [10.15625, 10.1875]
#
# Process finished with exit code 0

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////