from typing import FrozenSet, Counter, Tuple, Any, DefaultDict, Deque, Set
import collections
from csp.variable import Variable
from csp.constraint import Constraint
from csp.constraint_problem import ConstraintProblem


def ac4(constraint_problem: ConstraintProblem) -> bool:
    support_counter = collections.Counter()
    variable_value_pairs_supported_by = collections.defaultdict(set)
    unsupported_variable_value_pairs = collections.deque()
    __initialize_ac4(constraint_problem.get_constraints(), support_counter, variable_value_pairs_supported_by,
                     unsupported_variable_value_pairs)

    while unsupported_variable_value_pairs:
        second_variable, second_value = unsupported_variable_value_pairs.popleft()
        for first_variable, first_value in variable_value_pairs_supported_by[(second_variable, second_value)]:
            if first_value in first_variable.domain:
                support_counter[(first_variable, first_value, second_variable)] -= 1
                if support_counter[(first_variable, first_value, second_variable)] == 0:
                    first_variable.remove_from_domain(first_value)
                    unsupported_variable_value_pairs.append((first_variable, first_value))

    for var in constraint_problem.get_variables():
        if not var.domain or not constraint_problem.get_consistent_domain(var):
            return False
    return True


def __initialize_ac4(constraints: FrozenSet[Constraint], support_counter: Counter[Tuple[Variable, Any, Variable]],
                     variable_value_pairs_supported_by: DefaultDict[Tuple[Variable, Any], Set[Tuple[Variable, Any]]],
                     unsupported_variable_value_pairs: Deque[Tuple[Variable, Any]]) -> None:
    for constraint in constraints:
        if len(constraint.variables) == 1:
            continue
        first_variable, second_variable, *_ = constraint.variables
        for i in range(2):
            first_variable_was_assigned = False if first_variable.value is None else True
            for first_value in first_variable.domain:
                if not first_variable_was_assigned:
                    first_variable.assign(first_value)
                second_variable_was_assigned = False if second_variable.value is None else True
                for second_value in second_variable.domain:
                    if not second_variable_was_assigned:
                        second_variable.assign(second_value)
                    if constraint.is_consistent():
                        support_counter[(first_variable, first_value, second_variable)] += 1
                        variable_value_pairs_supported_by[(second_variable, second_value)].add((first_variable,
                                                                                                first_value))
                    if not second_variable_was_assigned:
                        second_variable.unassign()
                if support_counter[(first_variable, first_value, second_variable)] == 0:
                    first_variable.remove_from_domain(first_value)
                    unsupported_variable_value_pairs.append((first_variable, first_value))
                if not first_variable_was_assigned:
                    first_variable.unassign()
            first_variable, second_variable = second_variable, first_variable
