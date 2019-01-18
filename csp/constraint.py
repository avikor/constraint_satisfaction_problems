from typing import Callable, Iterable, Tuple, Any
from operator import attrgetter
from csp.variable import Variable


ConstraintEvaluator = Callable[[tuple], bool]


class Constraint:

    def __init__(self, variables: Iterable[Variable], evaluate_constraint: ConstraintEvaluator) -> None:
        self.__variables = tuple(variables)

        if len(self.__variables) != len(frozenset(self.__variables)):
            self.__variables = list()
            seen_variables = set()
            for var in variables:
                if var not in seen_variables:
                    self.__variables.append(var)
                    seen_variables.add(var)
            self.__variables = tuple(self.__variables)

        self.__evaluate_constraint = evaluate_constraint
        self.__i_consistent_assignments = set()
        if len(self.__variables) == 1:
            self.__enforce_unary_constraint()

    def __enforce_unary_constraint(self) -> None:
        variable, *_ = self.__variables
        variable.domain = list(self.get_consistent_domain_values(variable))

    def __get_variables(self) -> Tuple[Variable, ...]:
        return self.__variables

    variables = property(__get_variables)

    @classmethod
    def from_domains(cls, evaluate_constraint: ConstraintEvaluator, *domains) -> Any:
        variables = list()
        for elem in domains:
            try:
                if type(elem) is str:
                    raise TypeError
                elem_iterator = iter(elem)
                variables.append(Variable(elem))
            except TypeError:
                last_variable = variables[-1]
                if elem in last_variable.domain:
                    last_variable.assign(elem)
        return cls(variables, evaluate_constraint)

    def __bool__(self) -> bool:
        if self.__i_consistent_assignments:
            return all(self.__variables) and self.is_consistent() and self.__is_i_consistent_assignment()
        return all(self.__variables) and self.is_consistent()

    __value_getter = attrgetter("value")

    def is_consistent(self) -> bool:
        all_values = map(Constraint.__value_getter, self.__variables)
        values_of_assigned_variables = tuple(filter(None.__ne__, all_values))
        if self.__i_consistent_assignments:
            return self.__evaluate_constraint(values_of_assigned_variables) and self.__is_i_consistent_assignment()
        return self.__evaluate_constraint(values_of_assigned_variables)

    def get_consistent_domain_values(self, variable: Variable) -> set:
        if variable not in self.__variables:
            raise UncontainedVariableError(self, variable)

        original_value = variable.value
        variable.unassign()
        consistent_domain = set()
        for value in variable.domain:
            variable.assign(value)
            if self.is_consistent():
                consistent_domain.add(value)
            variable.unassign()

        if original_value is not None and variable.domain:
            variable.assign(original_value)
        return consistent_domain

    def update_i_consistent_assignments(self, i_consistent_assignments: set) -> None:
        if not i_consistent_assignments:
            self.__i_consistent_assignments.add(frozenset())
        for assignment in i_consistent_assignments:
            self.__i_consistent_assignments.add(frozenset(assignment))

    def __is_i_consistent_assignment(self) -> bool:
        all_values = map(Constraint.__value_getter, self.__variables)
        current_assignment = set(filter(None.__ne__, all_values))
        for assignment in self.__i_consistent_assignments:
            if assignment.issubset(current_assignment):
                return True
        return False

    def __str__(self) -> str:
        state = "\n  constraint is completely assigned: " + str(all(self.__variables)) + \
                ". constraint is consistent: " + str(self.is_consistent()) + ". constraint is satisfied: " + \
              str(bool(self)) + ". ]\n"
        return "[ " + "\n  ".join(map(str, self.variables)) + state


class ConstraintError(Exception):
    """ Base class for various Constraint Errors. """


class UncontainedVariableError(ConstraintError):
    def __init__(self, constraint: Constraint, variable: Variable) -> None:
        msg = "Cannot return consistent domain of " + str(variable) + " since variable is not contained in\n" \
              + str(constraint) + "variables."
        super(UncontainedVariableError, self).__init__(msg)
