import unittest
import csp


class TestConstraintProblem(unittest.TestCase):

    def setUp(self):
        colors = ["red", "green", "blue"]
        names = {"wa", "nt", "q", "nsw", "v", "sa", "t"}
        variables = csp.Variable.from_names_to_equal_domain(names, colors)
        self.variables = variables
        const1 = csp.Constraint([variables["sa"], variables["wa"]], csp.all_diff_constraint_evaluator)
        const2 = csp.Constraint([variables["sa"], variables["nt"]], csp.all_diff_constraint_evaluator)
        const3 = csp.Constraint([variables["sa"], variables["q"]], csp.all_diff_constraint_evaluator)
        const4 = csp.Constraint([variables["sa"], variables["nsw"]], csp.all_diff_constraint_evaluator)
        const5 = csp.Constraint([variables["sa"], variables["v"]], csp.all_diff_constraint_evaluator)
        const6 = csp.Constraint([variables["wa"], variables["nt"]], csp.all_diff_constraint_evaluator)
        const7 = csp.Constraint([variables["nt"], variables["q"]], csp.all_diff_constraint_evaluator)
        const8 = csp.Constraint([variables["q"], variables["nsw"]], csp.all_diff_constraint_evaluator)
        const9 = csp.Constraint([variables["nsw"], variables["v"]], csp.all_diff_constraint_evaluator)
        const10 = csp.Constraint([variables["t"]], csp.always_satisfied)
        self.constraints = [const1, const2, const3, const4, const5, const6, const7, const8, const9, const10]
        self.const_problem = csp.ConstraintProblem(frozenset(self.constraints), variables)

    def test_is_completely_unassigned(self):
        self.assertTrue(self.const_problem.is_completely_unassigned())
        for var in self.const_problem.get_variables():
            var.assign("green")
        self.assertFalse(self.const_problem.is_completely_unassigned())

    def test_is_consistently_assigned(self):
        self.assertTrue(self.const_problem.is_consistently_assigned())
        self.assertTrue(self.const_problem.is_completely_unassigned())
        name_to_var_map = self.const_problem.get_name_to_variable_map()
        name_to_var_map["t"].assign("red")
        self.assertTrue(self.const_problem.is_consistently_assigned())
        self.assertFalse(self.const_problem.is_completely_unassigned())

    def test_is_completely_assigned(self):
        self.assertFalse(self.const_problem.is_completely_assigned())
        for var in self.const_problem.get_variables():
            var.assign("green")
        self.assertTrue(self.const_problem.is_completely_assigned())
        self.const_problem.unassign_all_variables()

    def test_is_completely_consistently_assigned(self):
        self.assertFalse(self.const_problem.is_completely_consistently_assigned())
        variables = self.const_problem.get_variables()
        for var in variables:
            var.assign("green")
        self.assertTrue(self.const_problem.is_completely_assigned())
        self.const_problem.unassign_all_variables()
        self.assertTrue(self.const_problem.is_completely_unassigned())
        name_to_var_map = self.const_problem.get_name_to_variable_map()
        name_to_var_map["wa"].assign("red")
        name_to_var_map["nt"].assign("green")
        name_to_var_map["sa"].assign("blue")
        name_to_var_map["q"].assign("red")
        name_to_var_map["nsw"].assign("green")
        name_to_var_map["v"].assign("red")
        name_to_var_map["t"].assign("blue")
        self.assertEqual(frozenset(name_to_var_map.values()), variables)
        self.assertTrue(self.const_problem.is_completely_assigned())
        self.assertTrue(self.const_problem.is_completely_consistently_assigned())

    def test_get_variables(self):
        self.assertEqual(frozenset(self.variables.values()), self.const_problem.get_variables())

    def test_get_constraints(self):
        self.assertEqual(frozenset(self.constraints), self.const_problem.get_constraints())

    def test_get_assigned_variables(self):
        self.const_problem.unassign_all_variables()
        name_to_var_map = self.const_problem.get_name_to_variable_map()
        name_to_var_map["q"].assign("red")
        self.assertEqual(frozenset({name_to_var_map["q"]}), self.const_problem.get_assigned_variables())

    def test_get_unassigned_variables(self):
        self.assertEqual(frozenset(self.variables.values()), self.const_problem.get_unassigned_variables())

    def test_get_neighbors(self):
        first1 = set(self.variables.values()) - {self.variables["sa"], self.variables["t"]}
        second1 = self.const_problem.get_neighbors(self.variables["sa"])
        self.assertEqual(frozenset(first1), second1)
        first2 = {self.variables["sa"], self.variables["nsw"]}
        second2 = self.const_problem.get_neighbors(self.variables["v"])
        self.assertEqual(first2, second2)

    def test_get_assigned_neighbors(self):
        self.variables["wa"].assign("red")
        self.variables["q"].assign("blue")
        first1 = set(self.variables.values()) - {self.variables["sa"], self.variables["t"], self.variables["nt"],
                                                 self.variables["nsw"], self.variables["v"]}
        second1 = self.const_problem.get_assigned_neighbors(self.variables["sa"])
        self.assertEqual(frozenset(first1), second1)

    def test_get_unassigned_neighbors(self):
        self.variables["wa"].assign("red")
        self.variables["q"].assign("blue")
        first1 = set(self.variables.values()) - {self.variables["sa"], self.variables["t"], self.variables["wa"],
                                                 self.variables["q"]}
        second1 = self.const_problem.get_unassigned_neighbors(self.variables["sa"])
        self.assertEqual(frozenset(first1), second1)

    def test_get_consistent_constraints(self):
        self.variables["sa"].assign("red")
        self.variables["wa"].assign("blue")
        self.variables["nt"].assign("red")
        self.variables["q"].assign("red")
        self.variables["nsw"].assign("red")
        self.variables["v"].assign("red")
        const1 = frozenset({self.constraints[0], self.constraints[5], self.constraints[9]})
        const2 = self.const_problem.get_consistent_constraints()
        self.assertEqual(const1, const2)

    def test_get_inconsistent_constraints(self):
        self.variables["sa"].assign("green")
        self.variables["wa"].assign("green")
        self.variables["nt"].assign("green")
        inconst1 = frozenset({self.constraints[0], self.constraints[1], self.constraints[5]})
        inconst2 = self.const_problem.get_inconsistent_constraints()
        self.assertEqual(inconst1, inconst2)

    def test_get_satisfied_constraints(self):
        self.variables["wa"].assign("red")
        self.variables["nt"].assign("green")
        self.variables["sa"].assign("blue")
        self.variables["q"].assign("red")
        self.variables["nsw"].assign("green")
        self.variables["v"].assign("red")
        self.variables["t"].assign("blue")
        self.assertEqual(frozenset(self.constraints), self.const_problem.get_satisfied_constraints())

    def test_get_unsatisfied_constraints(self):
        self.assertEqual(frozenset(self.constraints), self.const_problem.get_unsatisfied_constraints())
        for name in self.variables:
            self.variables[name].assign("green")
        unsat = frozenset(self.constraints) - {self.constraints[9]}
        self.assertEqual(unsat, self.const_problem.get_unsatisfied_constraints())

    def test_get_constraints_containing_variable(self):
        wanted1 = frozenset({self.constraints[0], self.constraints[1], self.constraints[2], self.constraints[3],
                            self.constraints[4]})
        gotten1 = self.const_problem.get_constraints_containing_variable(self.variables["sa"])
        self.assertEqual(wanted1, gotten1)
        wanted2 = frozenset({self.constraints[9]})
        gotten2 = self.const_problem.get_constraints_containing_variable(self.variables["t"])
        self.assertEqual(wanted2, gotten2)
        wanted3 = frozenset({self.constraints[4], self.constraints[8]})
        gotten3 = self.const_problem.get_constraints_containing_variable(self.variables["v"])
        self.assertEqual(wanted3, gotten3)

    def test_get_consistent_domain(self):
        self.variables["wa"].assign("red")
        wanted_const_domain1 = frozenset({"green", "blue"})
        gotten_const_domain11 = self.const_problem.get_consistent_domain(self.variables["sa"])
        gotten_const_domain12 = self.const_problem.get_consistent_domain(self.variables["nt"])
        self.assertEqual(wanted_const_domain1, gotten_const_domain11)
        self.assertEqual(wanted_const_domain1, gotten_const_domain12)
        self.const_problem.unassign_all_variables()
        self.variables["wa"].assign("red")
        self.variables["nt"].assign("green")
        wanted_const_domain2 = frozenset({"blue"})
        gotten_const_domain2 = self.const_problem.get_consistent_domain(self.variables["sa"])
        self.assertEqual(wanted_const_domain2, gotten_const_domain2)

    def test_get_current_assignment(self):
        self.variables["wa"].assign("red")
        self.variables["nt"].assign("green")
        self.variables["sa"].assign("blue")
        self.variables["q"].assign("red")
        self.variables["nsw"].assign("green")
        self.variables["v"].assign("red")
        self.variables["t"].assign("blue")
        my_assignment = dict()
        for name, var in self.variables.items():
            if name == "wa":
                my_assignment[var] = "red"
            if name == "nt":
                my_assignment[var] = "green"
            if name == "sa":
                my_assignment[var] = "blue"
            if name == "q":
                my_assignment[var] = "red"
            if name == "nsw":
                my_assignment[var] = "green"
            if name == "v":
                my_assignment[var] = "red"
            if name == "t":
                my_assignment[var] = "blue"
        assignment = self.const_problem.get_current_assignment()
        self.assertEqual(my_assignment, assignment)

    def test_unassign_all_variables(self):
        self.assertTrue(self.const_problem.is_completely_unassigned())
        self.variables["wa"].assign("red")
        self.variables["nt"].assign("green")
        self.variables["sa"].assign("blue")
        self.variables["q"].assign("red")
        self.variables["nsw"].assign("green")
        self.variables["v"].assign("red")
        self.variables["t"].assign("blue")
        self.assertFalse(self.const_problem.is_completely_unassigned())
        self.const_problem.unassign_all_variables()
        self.assertTrue(self.const_problem.is_completely_unassigned())

    def test_assign_variables(self):
        my_assignment = dict()
        for name, var in self.variables.items():
            if name == "wa":
                my_assignment[var] = "red"
            if name == "nt":
                my_assignment[var] = "green"
            if name == "sa":
                my_assignment[var] = "blue"
            if name == "q":
                my_assignment[var] = "red"
            if name == "nsw":
                my_assignment[var] = "green"
            if name == "v":
                my_assignment[var] = "red"
            if name == "t":
                my_assignment[var] = "blue"
        self.assertTrue(self.const_problem.is_completely_unassigned())
        self.assertTrue(self.const_problem.is_consistently_assigned())
        self.assertFalse(self.const_problem.is_completely_assigned())
        self.assertFalse(self.const_problem.is_completely_consistently_assigned())
        self.const_problem.assign_variables_from_assignment(my_assignment)
        self.assertTrue(self.const_problem.is_completely_assigned())
        self.assertTrue(self.const_problem.is_consistently_assigned())
        self.assertTrue(self.const_problem.is_completely_consistently_assigned())
        self.assertFalse(self.const_problem.is_completely_unassigned())


if __name__ == '__main__':
    unittest.main()
