import unittest
import csp


class TestConstraint(unittest.TestCase):

    def test_get_variables(self):
        var1 = csp.Variable([i for i in range(10)])
        var2 = csp.Variable([i for i in range(10, 20)])
        variables = (var1, var2)
        const = csp.Constraint(variables, csp.ExactSum(28))
        self.assertEqual(const.variables, variables)

    def test_unary_constraint(self):
        var = csp.Variable([i for i in range(10)])
        const = csp.Constraint({var}, csp.MinSum(5))
        var_from_const, *_ = const.variables
        self.assertEqual(frozenset(var_from_const.domain), frozenset(i for i in range(6, 10)))

    def test_bool_operator(self):
        var1 = csp.Variable([i for i in range(10)])
        var2 = csp.Variable([i for i in range(10, 20)])
        variables = {var1, var2}
        const = csp.Constraint(variables, csp.ExactSum(28))
        self.assertFalse(const)
        var1.assign(7)
        var2.assign(13)
        self.assertFalse(const)
        var1.unassign()
        var1.assign(9)
        var2.unassign()
        var2.assign(19)
        self.assertTrue(const)

    def test_is_consistent(self):
        var1 = csp.Variable([i for i in range(5)], 4)
        var2 = csp.Variable([i for i in range(5, 10)], 6)
        var3 = csp.Variable([i for i in range(11, 20)])
        variables = [var1, var2, var3]
        const = csp.Constraint(variables, csp.MaxSum(28))
        self.assertTrue(const.is_consistent())
        self.assertFalse(const)
        var3.assign(17)
        self.assertTrue(const)

    def test_UncontainedVariableError(self):
        var1 = csp.Variable([i for i in range(5)], 4)
        var2 = csp.Variable([i for i in range(5, 10)], 6)
        var3 = csp.Variable([i for i in range(11, 20)])
        variables = [var1, var2]
        const = csp.Constraint(variables, csp.MaxSum(28))
        self.assertRaises(csp.UncontainedVariableError, const.get_consistent_domain_values, var3)

    def test_get_consistent_domain(self):
        var1 = csp.Variable([i for i in range(5)], 4)
        var2 = csp.Variable([i for i in range(5, 10)], 6)
        var3 = csp.Variable([i for i in range(15, 26)])
        variables = [var1, var2, var3]
        const = csp.Constraint(variables, csp.MaxSum(28))
        consistent_domain = const.get_consistent_domain_values(var3)
        const_domain = frozenset({15, 16, 17})
        self.assertTrue(consistent_domain, const_domain)

    def test_from_domains(self):
        const1 = csp.Constraint.from_domains(lambda x: False, [i for i in range(3)], (i for i in range(3, 6)),
                                             {i for i in range(6, 9)})
        domain1 = [i for i in range(3)]
        domain2 = [i for i in range(3, 6)]
        domain3 = [i for i in range(6, 9)]
        domains = [domain1, domain2, domain3]
        for var in const1.variables:
            self.assertIn(sorted(var.domain), domains)

        const2 = csp.Constraint.from_domains(lambda x: False, [i for i in range(3)], 1, (i for i in range(3, 6)),
                                             {i for i in range(6, 9)}, 6)
        for var in const2.variables:
            self.assertIn(var.value, [None, 1, 6])

        const3 = csp.Constraint.from_domains(lambda x: False, [i for i in range(3)], (i for i in range(3, 6)), 3,
                                             (1, 1.5, "1", "one"), 1)
        for var in const3.variables:
            self.assertIn(var.value, [None, 3, 1])

        const4 = csp.Constraint.from_domains(lambda x: False, [i for i in range(3)], (i for i in range(3, 6)), 3,
                                             (1.0, 1.5, "1", 1), 1.0)
        for var in const4.variables:
            self.assertIn(var.value, [None, 3, 1.0])

        const5 = csp.Constraint.from_domains(lambda x: False, [i for i in range(3)],
                                             (i for i in range(3, 6)), 3,
                                             (1.0, 1.5, "1", 1, "one", 1.0, "1", 1, "one"), "1")
        for var in const5.variables:
            self.assertIn(var.value, [None, 3, "1"])


if __name__ == '__main__':
    unittest.main()
