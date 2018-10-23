from itertools import combinations, product, chain
from typing import Tuple, FrozenSet, Dict, Iterable
from csp.constraint import Constraint
from csp.variable import Variable
from csp.constraint_problem import ConstraintProblem
from csp.constraint_evaluators import OnlyiConsistentAssignment


def i_consistency(constraint_problem: ConstraintProblem, i: int) -> bool:
    variables = constraint_problem.get_variables()

    assert 0 < i <= len(variables), "for i = {0}: i <= 0 or (number of variables in constraint_problem) < i.".format(i)

    i_minus_one_sized_subsets = combinations(variables, i - 1)
    i_subsets_consistent_assignments = __initialize_i_consistency(variables, i_minus_one_sized_subsets)

    reducing_domains = True
    while reducing_domains:
        reducing_domains = False
        for subset, ith_variable in i_subsets_consistent_assignments:
            if __revise_i(constraint_problem, subset, ith_variable, i_subsets_consistent_assignments):
                reducing_domains = True

    for var in constraint_problem.get_variables():
        if not var.domain or not constraint_problem.get_consistent_domain(var):
            return False
    return True


def __initialize_i_consistency(variables: FrozenSet[Variable],
                               i_minus_one_sized_subsets: Iterable[Tuple[Variable, ...]]) \
        -> Dict[Tuple[Tuple[Variable, ...], Variable], set]:
    i_subsets_consistent_assignments = dict()
    for subset in i_minus_one_sized_subsets:
        for ith_variable in variables - frozenset(subset):
            domains = [variable.domain for variable in subset]
            domains.append(ith_variable.domain)
            i_subsets_consistent_assignments[(subset, ith_variable)] = set(product(*domains))
    return i_subsets_consistent_assignments


def __revise_i(constraint_problem: ConstraintProblem, subset: Tuple[Variable, ...], ith_variable: Variable,
               i_subsets_consistent_assignments:  Dict[Tuple[Tuple[Variable, ...], Variable], set]) -> bool:
    revised = False
    i_subsets_constraints = map(constraint_problem.get_constraints_containing_variable, subset)
    i_subsets_constraints = set(chain.from_iterable(i_subsets_constraints))
    i_subsets_constraints.update(constraint_problem.get_constraints_containing_variable(ith_variable))
    subset_domain = [variable.domain for variable in subset]
    for assignment in product(*subset_domain):
        var_were_assigned = dict()
        for variable, value in zip(subset, assignment):
            variable_was_assigned = False if variable.value is None else True
            var_were_assigned[variable] = variable_was_assigned
            if not variable_was_assigned:
                variable.assign(value)
        ith_variable_was_assigned = False if ith_variable.value is None else True
        for value in ith_variable.domain:
            if not ith_variable_was_assigned:
                ith_variable.assign(value)
            for constraint in i_subsets_constraints:
                i_assignment = assignment + (value,)
                if not constraint.is_consistent() and i_assignment in i_subsets_consistent_assignments[(subset,
                                                                                                        ith_variable)]:
                    revised = True
                    i_subsets_consistent_assignments[(subset, ith_variable)].remove(i_assignment)
            if not ith_variable_was_assigned:
                ith_variable.unassign()
        for variable in subset:
            if not var_were_assigned[variable]:
                variable.unassign()

    __reduce_assignment_constraints_domains(constraint_problem, i_subsets_consistent_assignments)
    return revised


def __reduce_assignment_constraints_domains(constraint_problem: ConstraintProblem,
                                            i_subsets_consistent_assignments:
                                            Dict[Tuple[Tuple[Variable, ...], Variable], set]) -> None:
    constraints = constraint_problem.get_constraints()
    for subset, ith_variable in i_subsets_consistent_assignments:
        i_variables = frozenset(subset + (ith_variable,))
        found = False
        for constraint in constraints:
            if i_variables.issubset(constraint.variables):
                found = True
                constraint.update_i_consistent_assignments(i_subsets_consistent_assignments[(subset, ith_variable)])
        if not found:
            i_constraint = OnlyiConsistentAssignment((i_subsets_consistent_assignments[(subset, ith_variable)]))
            new_constraint = Constraint(i_variables, i_constraint)
            constraint_problem.add_constraint(new_constraint)
