from itertools import chain, filterfalse
from typing import DefaultDict, Set, FrozenSet, Dict, Any, Iterable, Optional, Deque, Tuple
from collections import defaultdict
from operator import methodcaller
from random import choice
from csp.constraint import Constraint
from csp.variable import Variable


class ConstraintProblem:

    __is_consistent_method_caller = methodcaller("is_consistent")

    def __init__(self, constraints: Iterable[Constraint], name_to_variable_map: Optional[Dict[Any, Variable]] = None) \
            -> None:
        self.__variables_to_constraints_map = _build_variables_to_constraints_mapping(constraints)
        self.__constraint_graph = _build_constraint_graph_as_adjacency_list(self.__variables_to_constraints_map)
        self.__name_to_variable_map = name_to_variable_map
        if name_to_variable_map is not None:
            assert frozenset(self.__name_to_variable_map.values()).issubset(self.get_variables()), \
                "name_to_variable_map.values() is not a subset of the variables given in constraints. "

    def get_name_to_variable_map(self) -> Optional[Dict[Any, Variable]]:
        return self.__name_to_variable_map

    def is_completely_unassigned(self) -> bool:
        return not any(self.__variables_to_constraints_map.keys())

    def is_completely_assigned(self) -> bool:
        return all(self.__variables_to_constraints_map.keys())

    def is_consistently_assigned(self) -> bool:
        constraints = tuple(chain.from_iterable(self.__variables_to_constraints_map.values()))
        is_consistent_results = map(ConstraintProblem.__is_consistent_method_caller, constraints)
        return all(is_consistent_results)

    def is_completely_consistently_assigned(self) -> bool:
        constraints = frozenset(chain.from_iterable(self.__variables_to_constraints_map.values()))
        return all(constraints)

    def get_variables(self) -> FrozenSet[Variable]:
        return frozenset(self.__variables_to_constraints_map.keys())

    def get_assigned_variables(self) -> FrozenSet[Variable]:
        assigned_variables = filter(None, self.__variables_to_constraints_map.keys())
        return frozenset(assigned_variables)

    def get_unassigned_variables(self) -> FrozenSet[Variable]:
        unassigned_variables = filterfalse(None, self.__variables_to_constraints_map.keys())
        return frozenset(unassigned_variables)

    def get_neighbors(self, variable: Variable) -> FrozenSet[Variable]:
        return frozenset(self.__constraint_graph[variable])

    def get_assigned_neighbors(self, variable: Variable) -> FrozenSet[Variable]:
        assigned_neighbors = filter(None, self.__constraint_graph[variable])
        return frozenset(assigned_neighbors)

    def get_unassigned_neighbors(self, variable: Variable) -> FrozenSet[Variable]:
        unassigned_neighbors = filterfalse(None, self.__constraint_graph[variable])
        return frozenset(unassigned_neighbors)

    def get_constraints(self) -> FrozenSet[Constraint]:
        return frozenset(chain.from_iterable(self.__variables_to_constraints_map.values()))

    def get_consistent_constraints(self) -> FrozenSet[Constraint]:
        constraints = frozenset(chain.from_iterable(self.__variables_to_constraints_map.values()))
        consistent_constraints = filter(ConstraintProblem.__is_consistent_method_caller, constraints)
        return frozenset(consistent_constraints)

    def get_inconsistent_constraints(self) -> FrozenSet[Constraint]:
        constraints = frozenset(chain.from_iterable(self.__variables_to_constraints_map.values()))
        inconsistent_constraints = filterfalse(ConstraintProblem.__is_consistent_method_caller, constraints)
        return frozenset(inconsistent_constraints)

    def get_satisfied_constraints(self) -> FrozenSet[Constraint]:
        constraints = frozenset(chain.from_iterable(self.__variables_to_constraints_map.values()))
        satisfied_constraints = filter(None, constraints)
        return frozenset(satisfied_constraints)

    def get_unsatisfied_constraints(self) -> FrozenSet[Constraint]:
        constraints = frozenset(chain.from_iterable(self.__variables_to_constraints_map.values()))
        unsatisfied_constraints = filterfalse(None, constraints)
        return frozenset(unsatisfied_constraints)

    def get_constraints_containing_variable(self, variable: Variable) -> FrozenSet[Constraint]:
        return frozenset(self.__variables_to_constraints_map[variable])

    def get_consistent_domain(self, variable: Variable) -> set:
        consistent_domains = map(methodcaller("get_consistent_domain_values", variable),
                                 self.__variables_to_constraints_map[variable])
        return set.intersection(*consistent_domains)

    def get_current_assignment(self) -> Dict[Variable, Any]:
        return {variable: variable.value for variable in self.__variables_to_constraints_map.keys()}

    def unassign_all_variables(self, read_only_variables: Optional[FrozenSet[Variable]] = None) -> None:
        if read_only_variables is None:
            for variable in self.__variables_to_constraints_map.keys():
                variable.unassign()
        else:
            for variable in self.__variables_to_constraints_map.keys():
                if variable not in read_only_variables:
                    variable.unassign()

    def assign_variables_from_assignment(self, assignment: Dict[Variable, Any]) -> None:
        for variable in self.__variables_to_constraints_map.keys():
            if assignment[variable] is not None:
                variable.assign(assignment[variable])
            else:
                variable.unassign()

    def assign_variables_with_random_values(self, read_only_variables: Optional[FrozenSet[Variable]] = None,
                                            action_history: Optional[Deque[Tuple[Variable, Any]]] = None) \
            -> Optional[Deque[Tuple[Variable, Any]]]:
        for variable in self.__variables_to_constraints_map.keys():
            if read_only_variables is None or variable not in read_only_variables:
                value = choice(variable.domain)
                variable.assign(value)
                if action_history is not None:
                    action_history.append((variable, value))
        return action_history

    def get_constraint_graph_as_adjacency_list(self) -> DefaultDict[Variable, Set[Variable]]:
        return self.__constraint_graph

    def add_constraint(self, constraint: Constraint) -> None:
        new_constraints = set(chain.from_iterable(self.__variables_to_constraints_map.values())) | {constraint}
        self.__variables_to_constraints_map = _build_variables_to_constraints_mapping(new_constraints)
        self.__constraint_graph = _build_constraint_graph_as_adjacency_list(self.__variables_to_constraints_map)

    def __str__(self):
        constraints = frozenset(chain.from_iterable(self.__variables_to_constraints_map.values()))
        state = "\n  constraint_problem is completely assigned: " + str(all(self.__variables_to_constraints_map)) + \
                ". constraint_problem is consistent: " + str(self.is_consistently_assigned()) + \
                ". constraint_problem is satisfied: " + str(all(constraints)) + ". }\n"
        return "{ " + "\n  ".join(map(lambda constraint: str(constraint), constraints)) + state


def _build_variables_to_constraints_mapping(constraints: Iterable[Constraint]) \
        -> DefaultDict[Variable, Set[Constraint]]:
    variables_to_constraints_map = defaultdict(set)
    for const in constraints:
        for var in const.variables:
            variables_to_constraints_map[var].add(const)
    return variables_to_constraints_map


def _build_constraint_graph_as_adjacency_list(variables_to_constraints_map: DefaultDict[Variable, Set[Constraint]]) \
        -> DefaultDict[Variable, Set[Variable]]:
    constraints_graph = defaultdict(set)
    for variable in variables_to_constraints_map:
        for constraint in variables_to_constraints_map[variable]:
            constraints_graph[variable].update(constraint.variables)
        constraints_graph[variable].discard(variable)
    return constraints_graph
