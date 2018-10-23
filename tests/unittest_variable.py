import array
import unittest
import csp


class TestVariable(unittest.TestCase):

    def setUp(self):
        self.var = csp.Variable([i for i in range(10)])

    def test_iterable_constructor(self):
        gen_domain = (i for i in range(10))
        var1 = csp.Variable(gen_domain)
        self.assertEqual(list(i for i in range(10)).sort(), var1.domain.sort())
        set_domain = {i for i in range(17)}
        var2 = csp.Variable(set_domain)
        self.assertEqual(list(set_domain).sort(), var2.domain.sort())
        dict_domain = {i: i+1 for i in range(5)}
        var3 = csp.Variable(dict_domain)
        self.assertEqual(list(dict_domain).sort(), var3.domain.sort())
        arr_domain = array.array('h', (i for i in range(3)))
        var4 = csp.Variable(arr_domain)
        self.assertEqual(list(arr_domain).sort(), var4.domain.sort())

    def test_get_domain(self):
        domain = list(i for i in range(10))
        self.assertEqual(domain.sort(), self.var.domain.sort())

    def test_set_domain(self):
        domain = list(i for i in range(10))
        new_domain = list(i for i in range(5))
        self.var.domain = new_domain
        self.assertNotEqual(domain, self.var.domain)

    def test_unique_domain_elements(self):
        var1 = csp.Variable((1, 1, "1", "1", 1.0, 1.0, "1.0", "1.0", "one", "one"))
        self.assertEqual(set(var1.domain), {1, 1.0, "1", "1.0", "one"})
        var2 = csp.Variable("abcd")
        self.assertEqual(var2.domain.sort(), list("abcd").sort())
        var3 = csp.Variable("abcd blah xyz")
        self.assertEqual(var3.domain.sort(), list("abcd").sort())

    def test_string_domain(self):
        var1 = csp.Variable("abcd efg")
        var1.assign("a")
        self.assertTrue(var1)
        var1.unassign()
        self.assertNotIn(" ", var1.domain)
        self.assertNotIn("e", var1.domain)
        self.assertNotIn("f", var1.domain)
        self.assertNotIn("g", var1.domain)
        var1.assign("b")
        self.assertTrue(var1)
        self.assertEqual(set(var1.domain), {"a", "b", "c", "d"})

    def test_assign(self):
        value = 5
        self.var.assign(value)
        self.assertEqual(self.var.value, value)

    def test_unassign(self):
        value = 5
        self.var.assign(value)
        self.var.unassign()
        self.assertNotEqual(self.var.value, value)
        self.assertIsNone(self.var.value)

    def test_bool_operator(self):
        val = 0
        self.var.assign(val)
        self.assertTrue(self.var)
        self.var.unassign()
        self.assertFalse(self.var)

    def test_UncontainedValueError(self):
        value = 17
        self.assertRaises(csp.UncontainedValueError, self.var.assign, value)

    def test_OverAssignmentError(self):
        value = 5
        self.var.assign(value)
        different_value = 3
        self.assertRaises(csp.OverAssignmentError, self.var.assign, different_value)

    def test_remove_from_domain(self):
        removed_value = 5
        self.var.remove_from_domain(5)
        self.assertNotIn(removed_value, self.var.domain)

    def test_assigned_variable_construction(self):
        var1 = csp.Variable((i for i in range(10)), 7)
        self.assertEqual(7, var1.value)
        self.assertRaises(csp.UncontainedValueError, csp.Variable, (i for i in range(10)), 12)

    def test_instantiate_variables_with_equal_domain(self):
        domain = [i for i in range(10)]
        varis1 = csp.Variable.from_domain(10, domain)
        for var in varis1:
            self.assertEqual(var.domain.sort(), domain.sort())

        varis2 = csp.Variable.from_domain(10, domain, 3)
        for var in varis2:
            self.assertEqual(var.domain.sort(), domain.sort())
            self.assertEqual(var.value, 3)

    def test_from_names_and_domains(self):
        name_to_domain = dict()
        domain = [i for i in range(1, 10)]
        for i in range(80):
            name_to_domain[i] = domain
        name_to_var = csp.Variable.from_names_to_domains(name_to_domain)
        for name in name_to_var:
            self.assertEqual(name_to_var[name].domain.sort(), domain.sort())

    def test_from_names_with_equal_domain(self):
        colors = ["red", "green", "blue"]
        names = {"wa", "nt", "q", "nsw", "v", "sa", "t"}
        name_to_var_map = csp.Variable.from_names_to_equal_domain(names, colors)
        for name, var in name_to_var_map.items():
            self.assertEqual(var.domain.sort(), colors.sort())
        res = sorted(names)
        other_res = list(name_to_var_map.keys())
        other_res.sort()
        self.assertEqual(other_res, res)


if __name__ == '__main__':
    unittest.main()
