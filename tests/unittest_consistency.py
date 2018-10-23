import random
import unittest
import csp


class TestConsistency(unittest.TestCase):

    def setUp(self):
        colors = {"red", "green"}
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
        constraints = [const1, const2, const3, const4, const5, const6, const7, const8, const9, const10]
        self.const_problem1 = csp.ConstraintProblem(constraints)

        x = csp.Variable((2, 5))
        y = csp.Variable((2, 4))
        z = csp.Variable((2, 5))

        def is_divisor(values: tuple) -> bool:
            if len(values) < 2:
                return True
            result = values[0] / values[1]
            return result == int(result)

        const1 = csp.Constraint((x, z), is_divisor)
        const2 = csp.Constraint((y, z), is_divisor)
        self.const_problem2 = csp.ConstraintProblem((const1, const2))

        x = csp.Variable((1, 2, 3))
        y = csp.Variable((1, 2, 3))

        def less_than(values: tuple) -> bool:
            if len(values) < 2:
                return True
            return values[0] < values[1]

        const = csp.Constraint((x, y), less_than)
        self.const_problem3 = csp.ConstraintProblem((const,))

    def test_ac3_one(self):
        self.const_problem1.unassign_all_variables()
        res1 = csp.ac3(self.const_problem1)
        self.assertTrue(res1)

    def test_ac3_two(self):
        all_values = set()
        for var in self.const_problem2.get_variables():
            for val in var.domain:
                all_values.add(val)
        self.assertEqual(all_values, {2, 4, 5})
        res2 = csp.ac3(self.const_problem2)
        self.assertTrue(res2)
        reduced_all_values = set()
        for var in self.const_problem2.get_variables():
            for val in var.domain:
                reduced_all_values.add(val)
        self.assertEqual(reduced_all_values, {2, 4})

    def tes_ac3_three(self):
        res = csp.ac3(self.const_problem3)
        self.assertTrue(res)
        wanted_reduced_domains = [[1, 2], [2, 3]]
        for var in self.const_problem3.get_variables():
            self.assertIn(var.domain, wanted_reduced_domains)

    def test_ac4_one(self):
        self.const_problem1.unassign_all_variables()
        res = csp.ac4(self.const_problem1)
        self.assertTrue(res)

    def test_ac4_two(self):
        all_values = set()
        for var in self.const_problem2.get_variables():
            for val in var.domain:
                all_values.add(val)
        self.assertEqual(all_values, {2, 4, 5})
        res2 = csp.ac3(self.const_problem2)
        self.assertTrue(res2)
        reduced_all_values = set()
        for var in self.const_problem2.get_variables():
            for val in var.domain:
                reduced_all_values.add(val)
        self.assertEqual(reduced_all_values, {2, 4})

    def test_ac4_three(self):
        res = csp.ac4(self.const_problem3)
        self.assertTrue(res)
        wanted_reduced_domains = [[1, 2], [2, 3]]
        for var in self.const_problem3.get_variables():
            self.assertIn(var.domain, wanted_reduced_domains)

    def test_pc2(self):
        self.const_problem1.unassign_all_variables()
        res = csp.pc2(self.const_problem1)
        self.assertFalse(res)

    def test_i_consistency_one(self):
        rand_var = random.choice(tuple(self.const_problem1.get_variables()))
        rand_var.assign(random.choice(rand_var.domain))
        self.assertRaises(AssertionError, csp.i_consistency, self.const_problem1, 17)
        self.const_problem1.unassign_all_variables()
        res = csp.i_consistency(self.const_problem1, 1)
        self.assertTrue(res)

    def test_i_consistency_two(self):
        res = csp.i_consistency(self.const_problem1, 2)
        self.assertFalse(res)

    def test_i_consistency_three(self):
        res = csp.i_consistency(self.const_problem1, 3)
        self.assertFalse(res)

    def test_i_consistency_four(self):
        res = csp.i_consistency(self.const_problem2, 1)
        self.assertTrue(res)

    def test_i_consistency_five(self):
        res = csp.i_consistency(self.const_problem2, 2)
        self.assertFalse(res)

    def test_i_consistency_six(self):
        res = csp.i_consistency(self.const_problem3, 1)
        self.assertTrue(res)

    def test_i_consistency_seven(self):
        res = csp.i_consistency(self.const_problem3, 2)
        self.assertTrue(res)

    def test_i_consistency_eight(self):
        self.assertRaises(AssertionError, csp.i_consistency, self.const_problem1, 17)


if __name__ == '__main__':
    unittest.main()
