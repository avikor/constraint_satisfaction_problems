from csp.variable import Variable
from csp.constraint_problem import ConstraintProblem


def do_not_sort(constraint_problem: ConstraintProblem, variable: Variable) -> list:
    return list(constraint_problem.get_consistent_domain(variable))


def least_constraining_value(constraint_problem: ConstraintProblem, variable: Variable) -> list:
    unassigned_neighbors = constraint_problem.get_unassigned_neighbors(variable)

    def neighbors_consistent_domain_lengths(value) -> int:
        variable.assign(value)
        consistent_domain_lengths = map(lambda neighbor: len((constraint_problem.get_consistent_domain(neighbor))),
                                        unassigned_neighbors)
        variable.unassign()
        return sum(consistent_domain_lengths)

    return sorted(constraint_problem.get_consistent_domain(variable), key=neighbors_consistent_domain_lengths,
                  reverse=True)
