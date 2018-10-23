from typing import List, FrozenSet
from random import choice, uniform, sample
from csp.variable import Variable
from csp.constraint_problem import ConstraintProblem
from csp.genetic_search import GeneticConstraintProblem, Assignment


class GeneralGeneticConstraintProblem(GeneticConstraintProblem):

    def __init__(self, constraint_problem: ConstraintProblem, mutation_fraction: float,
                 read_only_variables: FrozenSet[Variable] = frozenset()) -> None:
        super(GeneralGeneticConstraintProblem, self).__init__(constraint_problem)
        self.__mutation_fraction = mutation_fraction
        self.__read_only_variables = read_only_variables

    def __get_mutation_fraction(self) -> float:
        return self.__mutation_fraction

    def __set_mutation_fraction(self, mutation_fraction: float) -> None:
        self.__mutation_fraction = mutation_fraction

    mutation_fraction = property(__get_mutation_fraction, __set_mutation_fraction)

    def generate_population(self, population_size: int) -> List[Assignment]:
        """ generating individuals by random assignments. """
        population = list()
        for i in range(population_size):
            for variable in self._constraint_problem.get_variables() - self.__read_only_variables:
                variable.assign(choice(variable.domain))
            population.append(self._constraint_problem.get_current_assignment())
            self._constraint_problem.unassign_all_variables()
        return population

    def calculate_fitness(self, assignment: Assignment) -> int:
        """ fitness is the number of consistent constraints.  """
        self._constraint_problem.unassign_all_variables()
        self._constraint_problem.assign_variables_from_assignment(assignment)
        return len(self._constraint_problem.get_consistent_constraints())

    def perform_natural_selection(self, population: List[Assignment]) -> List[Assignment]:
        """ half truncation selection. """
        population.sort(key=self.calculate_fitness, reverse=True)
        return population[:len(population)//2]

    def reproduce_next_generation(self, old_generation: List[Assignment]) -> List[Assignment]:
        new_generation = list()
        for i in range(len(old_generation) * 2):
            parent1, parent2 = sample(old_generation, 2)
            new_generation.append(self.__reproduce(parent1, parent2))
        return new_generation

    def __reproduce(self, parent1: Assignment, parent2: Assignment) -> Assignment:
        """ a child has half of each parent's variables and their assigned values.
            choose from which parent to get variable randomly. """
        child = dict()
        for variable in self._constraint_problem.get_variables():
            if uniform(0, 1) < 0.5:
                child[variable] = parent1[variable]
            else:
                child[variable] = parent2[variable]
        return child

    def mutate_population(self, population: List[Assignment], mutation_probability: float) -> None:
        for individual in population:
            if uniform(0, 1) < mutation_probability:
                self.__mutate(individual)

    def __mutate(self, assignment: Assignment) -> None:
        """ for each selected mutation variable assign a new value randomly. """
        variables = assignment.keys()
        number_of_mutations = int(len(variables) * self.__mutation_fraction)
        mutation_variables = sample(variables - self.__read_only_variables, number_of_mutations)
        for variable in mutation_variables:
            old_value = variable.value
            variable.unassign()
            possible_values = variable.domain
            if len(possible_values) > 1:
                possible_values.remove(old_value)
            variable.assign(choice(possible_values))

