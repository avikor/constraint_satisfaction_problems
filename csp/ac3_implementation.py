from csp.variable import Variable
from csp.constraint_problem import ConstraintProblem


def ac3(constraint_problem: ConstraintProblem, assigned_variable: Variable = None) -> bool:
    if assigned_variable is not None:  # usage of ac3 as part of Maintaining Arc Consistency (MAC) algorithm
        unassigned_neighbors = constraint_problem.get_unassigned_neighbors(assigned_variable)
        arcs = {(unassigned_neighbor, assigned_variable) for unassigned_neighbor in unassigned_neighbors}
    else:
        arcs = {(variable, neighbor) for variable in constraint_problem.get_unassigned_variables()
                for neighbor in constraint_problem.get_neighbors(variable)}

    while arcs:
        variable, neighbor = arcs.pop()
        if __revise(constraint_problem, variable, neighbor):
            if not constraint_problem.get_consistent_domain(variable):
                return False
            rest_of_neighbors = constraint_problem.get_neighbors(variable) - {neighbor}
            if rest_of_neighbors:
                for other_neighbor in rest_of_neighbors:
                    arcs.add((other_neighbor, variable))

    for var in constraint_problem.get_variables():
        if not var.domain or not constraint_problem.get_consistent_domain(var):
            return False
    return True


def __revise(constraints_problem: ConstraintProblem, variable: Variable, neighbor: Variable) -> bool:
    if variable.value is not None:
        return False
    variable_constraints = constraints_problem.get_constraints_containing_variable(variable)
    neighbor_constraints = constraints_problem.get_constraints_containing_variable(neighbor)
    shared_constraint, *_ = (variable_constraints & neighbor_constraints)
    revised = False
    for value in variable.domain:
        variable.assign(value)
        if not shared_constraint.get_consistent_domain_values(neighbor):
            variable.remove_from_domain(value)
            revised = True
        variable.unassign()
    return revised
