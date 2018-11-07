from csp.variable import Variable
from csp.constraint_problem import ConstraintProblem


def forward_check(constraint_problem: ConstraintProblem, assigned_variable: Variable) -> bool:
    unassigned_neighbors_frozenset = constraint_problem.get_unassigned_neighbors(assigned_variable)
    unsatisfiable_neighbors = filter(lambda unassigned_neighbor:
                                     not constraint_problem.get_consistent_domain(unassigned_neighbor),
                                     unassigned_neighbors_frozenset)
    return False if any(unsatisfiable_neighbors) else True
