from copy import deepcopy
from collections import Iterable, Set
from typing import Any, Dict


class Variable:

    def __init__(self, domain: Iterable, value=None) -> None:
        if type(domain) is not str:
            my_domain = frozenset(domain)
        else:
            my_domain = frozenset(str(domain).split()[0])
        self.__domain = deepcopy(list(my_domain))
        self.__value = None
        if value is not None:
            self.assign(value)

    @classmethod
    def from_domain(cls, amount: int, domain: Iterable, value=None) -> set:
        variables = set()
        for i in range(amount):
            if value is not None:
                variables.add(cls(domain, value))
            else:
                variables.add(cls(domain))
        return variables

    @classmethod
    def from_names_to_domains(cls, name_to_domain_map: Dict[Any, Iterable]) -> dict:
        name_to_variable_map = dict()
        for name, domain in name_to_domain_map.items():
            name_to_variable_map[name] = cls(domain)
        return name_to_variable_map

    @classmethod
    def from_names_to_equal_domain(cls, names: Set, domain: Iterable, value=None) -> dict:
        name_to_variable_map = dict()
        for name in names:
            if value is not None:
                name_to_variable_map[name] = cls(domain, value)
            else:
                name_to_variable_map[name] = cls(domain)
        return name_to_variable_map

    def __bool__(self) -> bool:
        return self.__value is not None

    def __get_domain(self) -> list:
        return deepcopy(self.__domain)

    def __set_domain(self, domain: set) -> None:
        self.__domain = deepcopy(domain)

    domain = property(__get_domain, __set_domain)

    def __get_value(self) -> Any:
        return deepcopy(self.__value)

    value = property(__get_value)

    def assign(self, value: Any) -> None:
        if self.__value is not None:
            raise OverAssignmentError(self)
        if value not in self.__domain:
            raise UncontainedValueError(self, value)
        self.__value = value

    def unassign(self) -> None:
        self.__value = None

    def remove_from_domain(self, value: Any) -> None:
        self.__domain.remove(value)

    def __str__(self) -> str:
        return "(variable's value: " + str(self.value) + ". variable's domain: " + str(self.__domain) + ")"


class VariableError(Exception):
    """ Base class for various Variable Errors. """


class UncontainedValueError(VariableError):
    def __init__(self, variable: Variable, value: Any) -> None:
        msg = "Cannot assign variable: " + str(variable) + " with value: " + str(value) + \
              " since it is not contained in variable's domain."
        super(UncontainedValueError, self).__init__(msg)


class OverAssignmentError(VariableError):
    def __init__(self, variable: Variable) -> None:
        msg = "Over-assignment of an assigned variable: " + str(variable) + \
              ". variable must be unassigned before assignment."
        super(OverAssignmentError, self).__init__(msg)

