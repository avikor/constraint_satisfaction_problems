import random
import unittest
import csp


class TestGraphColoring(unittest.TestCase):

    def setUp(self):
        colors = ["red", "green", "blue"]
        names = {"wa", "nt", "q", "nsw", "v", "sa", "t"}
        self.name_to_variable_map = csp.Variable.from_names_to_equal_domain(names, colors)
        const1 = csp.Constraint([self.name_to_variable_map["sa"], self.name_to_variable_map["wa"]],
                                csp.all_different)
        const2 = csp.Constraint([self.name_to_variable_map["sa"], self.name_to_variable_map["nt"]],
                                csp.all_different)
        const3 = csp.Constraint([self.name_to_variable_map["sa"], self.name_to_variable_map["q"]],
                                csp.all_different)
        const4 = csp.Constraint([self.name_to_variable_map["sa"], self.name_to_variable_map["nsw"]],
                                csp.all_different)
        const5 = csp.Constraint([self.name_to_variable_map["sa"], self.name_to_variable_map["v"]],
                                csp.all_different)
        const6 = csp.Constraint([self.name_to_variable_map["wa"], self.name_to_variable_map["nt"]],
                                csp.all_different)
        const7 = csp.Constraint([self.name_to_variable_map["nt"], self.name_to_variable_map["q"]],
                                csp.all_different)
        const8 = csp.Constraint([self.name_to_variable_map["q"], self.name_to_variable_map["nsw"]],
                                csp.all_different)
        const9 = csp.Constraint([self.name_to_variable_map["nsw"], self.name_to_variable_map["v"]],
                                csp.all_different)
        const10 = csp.Constraint([self.name_to_variable_map["t"]], csp.always_satisfied)
        constraints1 = [const1, const2, const3, const4, const5, const6, const7, const8, const9, const10]
        self.const_problem1 = csp.ConstraintProblem(constraints1)

        const11 = csp.Constraint([self.name_to_variable_map["sa"], self.name_to_variable_map["wa"]],
                                 csp.all_different)
        const12 = csp.Constraint([self.name_to_variable_map["sa"], self.name_to_variable_map["nt"]],
                                 csp.all_different)
        const13 = csp.Constraint([self.name_to_variable_map["sa"], self.name_to_variable_map["nsw"]],
                                 csp.all_different)
        const14 = csp.Constraint([self.name_to_variable_map["nsw"], self.name_to_variable_map["q"]],
                                 csp.all_different)
        const15 = csp.Constraint([self.name_to_variable_map["nsw"], self.name_to_variable_map["v"]],
                                 csp.all_different)
        constraints2 = [const11, const12, const13, const14, const15]
        self.const_problem2 = csp.ConstraintProblem(constraints2)

        const21 = csp.Constraint([self.name_to_variable_map["sa"], self.name_to_variable_map["wa"]],
                                 csp.all_different)
        const22 = csp.Constraint([self.name_to_variable_map["sa"], self.name_to_variable_map["q"]],
                                 csp.all_different)
        const23 = csp.Constraint([self.name_to_variable_map["wa"], self.name_to_variable_map["nt"]],
                                 csp.all_different)
        const24 = csp.Constraint([self.name_to_variable_map["nt"], self.name_to_variable_map["q"]],
                                 csp.all_different)
        const25 = csp.Constraint([self.name_to_variable_map["q"], self.name_to_variable_map["v"]],
                                 csp.all_different)
        constraints3 = [const21, const22, const23, const24, const25]
        self.const_problem3 = csp.ConstraintProblem(constraints3)

    def test_backtracking(self):
        csp.backtracking_search(self.const_problem1)
        self.assertTrue(self.const_problem1.is_completely_consistently_assigned())

    def test_forward_checking_backtracking(self):
        csp.backtracking_search(self.const_problem1, csp.forward_check)
        self.assertTrue(self.const_problem1.is_completely_consistently_assigned())

    def test_heuristic_backtracking(self):
        csp.heuristic_backtracking_search(self.const_problem1)
        self.assertTrue(self.const_problem1.is_completely_consistently_assigned())

    def test_min_conflicts(self):
        csp.min_conflicts(self.const_problem1, 100)
        self.assertTrue(self.const_problem1.is_completely_consistently_assigned())

    def test_constraint_weighting(self):
        self.const_problem1.unassign_all_variables()
        csp.constraints_weighting(self.const_problem1, 1000)
        self.assertTrue(self.const_problem1.is_completely_consistently_assigned())

    def test_hill_climber(self):
        const_prob = csp.random_restart_first_choice_hill_climbing(self.const_problem1, 100, 100, 100)
        self.assertTrue(const_prob.is_completely_consistently_assigned())

    def test_simulated_annealer(self):
        const_prob = csp.simulated_annealing(self.const_problem1, 1000, 0.5, 0.99999)
        self.assertTrue(const_prob.is_completely_consistently_assigned())

    def test_genetic_local_search(self):
        common_genetic_constraint_problem = csp.GeneralGeneticConstraintProblem(self.const_problem1, 0.1)
        rand_var = random.choice(list(common_genetic_constraint_problem.get_constraint_problem().get_variables()))
        rand_var.assign(random.choice(rand_var.domain))
        common_genetic_constraint_problem.get_constraint_problem().unassign_all_variables()
        solution = csp.genetic_local_search(common_genetic_constraint_problem, 100, 10, 0.1)
        self.assertTrue(solution.is_completely_consistently_assigned())

    def test_tree_csp_solver(self):
        csp.tree_csp_solver(self.const_problem2)
        self.assertTrue(self.const_problem2.is_completely_consistently_assigned())

    def test_cycle_cutset(self):
        csp.naive_cycle_cutset(self.const_problem3)
        self.assertTrue(self.const_problem3.is_completely_consistently_assigned())


if __name__ == '__main__':
    unittest.main()
