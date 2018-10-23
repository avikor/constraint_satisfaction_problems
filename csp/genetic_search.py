from abc import ABCMeta, abstractmethod
from typing import Dict, Any, List, Optional
from csp.variable import Variable
from csp.constraint_problem import ConstraintProblem


Assignment = Dict[Variable, Any]


class GeneticConstraintProblem(metaclass=ABCMeta):
    """ Whoever wants to use genetic_local_search must inherit this class.
        See general_genetic_constraint_problem for an example. """

    def __init__(self, constraint_problem: ConstraintProblem) -> None:
        self._constraint_problem = constraint_problem

    def get_constraint_problem(self) -> ConstraintProblem:
        return self._constraint_problem

    @abstractmethod
    def generate_population(self, population_size: int) -> List[Assignment]:
        pass

    @abstractmethod
    def calculate_fitness(self, assignment: Assignment) -> int:
        """ High fitness is good fitness. """
        pass

    @abstractmethod
    def perform_natural_selection(self, population: List[Assignment]) -> List[Assignment]:
        pass

    @abstractmethod
    def reproduce_next_generation(self, old_generation: List[Assignment]) -> List[Assignment]:
        pass

    @abstractmethod
    def mutate_population(self, population: List[Assignment], mutation_probability: float) -> None:
        pass

    def get_solution(self, population: List[Assignment]) -> Optional[ConstraintProblem]:
        for assignment in population:
            self._constraint_problem.unassign_all_variables()
            self._constraint_problem.assign_variables_from_assignment(assignment)
            if self._constraint_problem.is_completely_consistently_assigned():
                return self._constraint_problem
        return None


def genetic_local_search(genetic_constraint_problem: GeneticConstraintProblem,
                         population_size: int, max_generations: int, mutation_probability: float) -> ConstraintProblem:
    constraint_problem = genetic_constraint_problem.get_constraint_problem()

    population = genetic_constraint_problem.generate_population(population_size)
    best_fitness = float("-inf")
    most_fit_individual = population[-1]
    for i in range(max_generations):
        possible_solution = genetic_constraint_problem.get_solution(population)
        if possible_solution is not None:
            return possible_solution
        selected_population = genetic_constraint_problem.perform_natural_selection(population)
        new_generation = genetic_constraint_problem.reproduce_next_generation(selected_population)
        genetic_constraint_problem.mutate_population(new_generation, mutation_probability)
        population = new_generation

        curr_most_fit_individual = max(population, key=genetic_constraint_problem.calculate_fitness)
        curr_best_fitness = genetic_constraint_problem.calculate_fitness(curr_most_fit_individual)
        if best_fitness < curr_best_fitness:
            best_fitness = curr_best_fitness
            most_fit_individual = curr_most_fit_individual

    constraint_problem.unassign_all_variables()
    constraint_problem.assign_variables_from_assignment(most_fit_individual)
    return constraint_problem
