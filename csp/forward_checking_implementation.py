from csp.variable import Variable
from csp.constraint_problem import ConstraintProblem


def forward_check(constraints_problem: ConstraintProblem, assigned_variable: Variable) -> bool:
    unassigned_neighbors_frozenset = constraints_problem.get_unassigned_neighbors(assigned_variable)
    unsatisfiable_neighbors = filter(lambda unassigned_neighbor:
                                     not constraints_problem.get_consistent_domain(unassigned_neighbor),
                                     unassigned_neighbors_frozenset)
    return False if any(unsatisfiable_neighbors) else True
