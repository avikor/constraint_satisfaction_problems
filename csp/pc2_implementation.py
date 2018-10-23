from collections import deque
from csp.variable import Variable
from csp.constraint_problem import ConstraintProblem


def pc2(constraint_problem: ConstraintProblem) -> bool:
    variable_diffvariable_neighbor_triplets = deque()
    variables = constraint_problem.get_variables()
    for var in variables:
        for neighbor in constraint_problem.get_neighbors(var):
            for different_variable in variables - {var, neighbor}:
                variable_diffvariable_neighbor_triplets.append((var, different_variable, neighbor))

    while variable_diffvariable_neighbor_triplets:
        var, different_variable, neighbor = variable_diffvariable_neighbor_triplets.popleft()
        if __revise3(constraint_problem, var, neighbor, different_variable):
            for different_variable in variables - {var, neighbor}:
                variable_diffvariable_neighbor_triplets.append((different_variable, var, neighbor))
                variable_diffvariable_neighbor_triplets.append((different_variable, neighbor, var))

    for var in variables:
        if not var.domain or not constraint_problem.get_consistent_domain(var):
            return False
    return True


def __revise3(constraints_problem: ConstraintProblem, variable: Variable, neighbor: Variable,
              different_variable: Variable) -> bool:
    any_revised = False
    for variable_value in variable.domain:
        variable_was_assigned = False if variable.value is None else True
        if not variable_was_assigned:
            variable.assign(variable_value)

        curr_revised = False
        inconsistent_neighbor_values = list()
        neighbor_was_assigned = False if neighbor.value is None else True
        for neighbor_value in neighbor.domain:
            if not neighbor_was_assigned:
                neighbor.assign(neighbor_value)
            if not constraints_problem.get_consistent_domain(different_variable):
                inconsistent_neighbor_values.append(neighbor_value)
                curr_revised, any_revised = True, True
            if not neighbor_was_assigned:
                neighbor.unassign()

        if not variable_was_assigned:
            variable.unassign()
        if curr_revised:
            variable.remove_from_domain(variable_value)
            for value in inconsistent_neighbor_values:
                neighbor.remove_from_domain(value)

    return any_revised
