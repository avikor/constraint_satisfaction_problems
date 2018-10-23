from typing import List, Tuple, Dict, Set
from math import sqrt
from random import shuffle, choice, sample, randint, uniform
from copy import deepcopy
from itertools import product
import csp


def construct_sudoku_problem(file_name: str) -> csp.ConstraintProblem:
    grid = _parse_sudoku(file_name)
    name_to_var_map = dict()
    grid_len = len(grid)
    for i in range(grid_len):
        for j in range(grid_len):
            if grid[i][j] != 0:
                name_to_var_map[(i, j)] = csp.Variable((grid[i][j],), grid[i][j])
            else:
                name_to_var_map[(i, j)] = csp.Variable(range(1, grid_len + 1))

    return _constraint_sudoku_problem_from_name_to_var_map(name_to_var_map)


def _constraint_sudoku_problem_from_name_to_var_map(name_to_var_map: Dict[Tuple[int, int], csp.Variable]) \
        -> csp.ConstraintProblem:
    grid_len = int(sqrt(len(name_to_var_map.keys())))
    constraints = set()
    rows_indices = _get_rows_indices(grid_len)
    for row in rows_indices:
        row_vars = (name_to_var_map[(i, j)] for i, j in name_to_var_map.keys() if (i, j) in row)
        constraints.add(csp.Constraint(row_vars, csp.all_different))

    column_indices = _get_columns_indices(grid_len)
    for column in column_indices:
        column_vars = (name_to_var_map[(i, j)] for i, j in name_to_var_map.keys() if (i, j) in column)
        constraints.add(csp.Constraint(column_vars, csp.all_different))

    block_indices = _get_block_indices(grid_len)
    for block in block_indices:
        block_vars = (name_to_var_map[(i, j)] for i, j in name_to_var_map.keys() if (i, j) in block)
        constraints.add(csp.Constraint(block_vars, csp.all_different))

    return csp.ConstraintProblem(constraints, name_to_var_map)


def _parse_sudoku(file_name: str) -> List[List[int]]:
    grid = list()
    with open(file_name) as sudoku_board:
        while True:
            curr_line = sudoku_board.readline()
            if not curr_line:
                break
            row_string = curr_line.split(" ")
            if "\n" in row_string[-1][-1]:
                row_string[-1] = row_string[-1][:-1]
            grid.append(list(map(int, row_string)))
    return grid


def print_solution(name_to_var_map: Dict[Tuple[int, int], csp.Variable]) -> None:
    grid_len = int(sqrt(len(name_to_var_map.keys())))
    grid = [[0] * grid_len for i in range(grid_len)]
    for i, j in name_to_var_map.keys():
        grid[i][j] = name_to_var_map[(i, j)].value

    block_len = int(sqrt(grid_len))
    mid_indices = range(block_len, grid_len, block_len)
    grid_strings = list()
    for i in range(grid_len):
        if i in mid_indices:
            for k in range(block_len):
                grid_strings.append("-  " * block_len)
                if k != block_len - 1:
                    grid_strings.append("+ ")
            grid_strings.append("\n")

        for j in range(grid_len):
            if j in mid_indices:
                grid_strings.append("| ")
            if grid[i][j] < 10:
                grid_strings.append(" " + str(grid[i][j]) + " ")
            else:
                grid_strings.append(str(grid[i][j]) + " ")

        grid_strings.append("\n")

    print("".join(grid_strings))


def _get_rows_indices(grid_len: int) -> List[List[Tuple[int, int]]]:
    rows_indices = list()
    for i in range(grid_len):
        row_idxs = list()
        for j in range(grid_len):
            row_idxs.append((i, j))
        rows_indices.append(row_idxs)
    return rows_indices


def _get_columns_indices(grid_len: int) -> List[List[Tuple[int, int]]]:
    columns_indices = list()
    for i in range(grid_len):
        column_idxs = list()
        for j in range(grid_len):
            column_idxs.append((j, i))
        columns_indices.append(column_idxs)
    return columns_indices


def _get_block_indices(grid_len: int) -> List[List[Tuple[int, int]]]:
    block_len = int(sqrt(grid_len))
    blocks_starting_indices = product(range(0, grid_len, block_len), repeat=2)
    blocks_indices = list()
    for start_s, start_t in blocks_starting_indices:
        block_idxs = list()
        for i in range(start_s, start_s + block_len):
            for j in range(start_t, start_t + block_len):
                block_idxs.append((i, j))
        blocks_indices.append(block_idxs)
    return blocks_indices


def _get_block_values(constraint_problem: csp.ConstraintProblem, s: int, t: int) -> Set[int]:
    name_to_var_map = constraint_problem.get_name_to_variable_map()
    block_len = int(sqrt(sqrt(len(constraint_problem.get_variables()))))
    block_values = set()
    for row in range(s, s + block_len):
        for column in range(t, t + block_len):
            if name_to_var_map[(row, column)].value is not None:
                block_values.add(name_to_var_map[(row, column)].value)
    return block_values


class SudokuStartStateGenerator:
    def __init__(self, read_only_names: Set[Tuple[int, int]]) -> None:
        self.__read_only_names = read_only_names

    def __call__(self, constraint_problem: csp.ConstraintProblem) -> None:
        """ Generate a random complete assignment which doesn't violate any block constraints. """
        name_to_variable_map = constraint_problem.get_name_to_variable_map()
        for i, j in name_to_variable_map.keys():
            if (i, j) not in self.__read_only_names:
                name_to_variable_map[(i, j)].unassign()

        grid_len = int(sqrt(len(constraint_problem.get_variables())))
        block_len = int(sqrt(grid_len))
        name_to_var_map = constraint_problem.get_name_to_variable_map()
        for s, t in product(range(0, grid_len, block_len), repeat=2):
            block_values = _get_block_values(constraint_problem, s, t)
            consistent_block_values = set((i for i in range(1, grid_len + 1) if i not in block_values))
            # shuffle(consistent_block_values)
            for i in range(s, s + block_len):
                for j in range(t, t + block_len):
                    if (i, j) not in self.__read_only_names:
                        possible_values = set(name_to_variable_map[(i, j)].domain) & consistent_block_values
                        try:
                            value = possible_values.pop()
                        except KeyError:
                            raise UnsuccessfulSudokuCompleteAssignment()
                        name_to_var_map[(i, j)].assign(value)
                        consistent_block_values.discard(value)


def sudoku_score_calculator(constraint_problem: csp.ConstraintProblem) -> int:
    """ calculate state score by the number of unique values in each row and column. """
    grid_len = int(sqrt(len(constraint_problem.get_variables())))
    name_to_var_map = constraint_problem.get_name_to_variable_map()
    score = 0
    for row in _get_rows_indices(grid_len):
        score += len(set((name_to_var_map[(i, j)].value for i, j in row)))
    for column in _get_columns_indices(grid_len):
        score += len(set((name_to_var_map[(i, j)].value for i, j in column)))
    return score


class SudokuSuccessorGenerator:
    def __init__(self, read_only_names: Set[Tuple[int, int]]) -> None:
        self.__read_only_names = read_only_names

    def __call__(self, constraint_problem: csp.ConstraintProblem) -> csp.ConstraintProblem:
        """ choose a block randomly, swap two squares (which aren't read-only) inside the block. """
        grid_len = int(sqrt(len(constraint_problem.get_variables())))
        block_len = int(sqrt(grid_len))
        name_to_var_map = constraint_problem.get_name_to_variable_map()
        successor_name_to_var_map = dict()
        for i, j in name_to_var_map.keys():
            successor_name_to_var_map[(i, j)] = deepcopy(name_to_var_map[(i, j)])
        successor_sudoku_problem = _constraint_sudoku_problem_from_name_to_var_map(successor_name_to_var_map)

        blocks_starting_indices = tuple(product(range(0, grid_len, block_len), repeat=2))
        (s, t) = choice(blocks_starting_indices)
        block_variables = list()
        for i in range(s, s + block_len):
            for j in range(t, t + block_len):
                if (i, j) not in self.__read_only_names:
                    block_variables.append((i, j))

        shuffle(block_variables)
        for a, b in block_variables:
            for u, v in block_variables:
                if (a, b) == (u, v):
                    continue
                if self.__have_been_swapped(successor_name_to_var_map, a, b, u, v):
                    return successor_sudoku_problem
        raise UnsuccessfulSudokuCompleteAssignment()

    @staticmethod
    def __have_been_swapped(successor_name_to_var_map, a, b, u, v) -> bool:
        if successor_name_to_var_map[(a, b)].value in successor_name_to_var_map[(u, v)].domain and \
                successor_name_to_var_map[(u, v)].value in successor_name_to_var_map[(a, b)].domain:
            a_b_value = successor_name_to_var_map[(a, b)].value
            u_v_value = successor_name_to_var_map[(u, v)].value
            successor_name_to_var_map[(a, b)].unassign()
            successor_name_to_var_map[(u, v)].unassign()
            successor_name_to_var_map[(a, b)].assign(u_v_value)
            successor_name_to_var_map[(u, v)].assign(a_b_value)
            return True
        return False


class GeneticSudokuConstraintProblem(csp.GeneticConstraintProblem):
    def __init__(self, constraint_problem: csp.ConstraintProblem, read_only_names: Set[Tuple[int, int]],
                 mutation_fraction: float) -> None:
        super(GeneticSudokuConstraintProblem, self).__init__(constraint_problem)
        self.__mutation_fraction = mutation_fraction
        self.__read_only_names = read_only_names
        self.__grid_len = int(sqrt(len(constraint_problem.get_variables())))
        self.__block_len = int(sqrt(self.__grid_len))

    def __get_mutation_fraction(self) -> float:
        return self.__mutation_fraction

    def __set_mutation_fraction(self, mutation_fraction: float) -> None:
        self.__mutation_fraction = mutation_fraction

    mutation_fraction = property(__get_mutation_fraction, __set_mutation_fraction)

    def generate_population(self, population_size: int) -> List[csp.Assignment]:
        """ Generate a random complete assignment which doesn't violate any block constraints. """
        blocks_starting_indices = tuple(product(range(0, self.__grid_len, self.__block_len), repeat=2))
        name_to_variable_map = self._constraint_problem.get_name_to_variable_map()
        population = list()
        for k in range(population_size):
            for s, t in blocks_starting_indices:
                block_values = _get_block_values(self._constraint_problem, s, t)
                consistent_block_values = set((i for i in range(1, self.__grid_len + 1) if i not in block_values))
                for i in range(s, s + self.__block_len):
                    for j in range(t, t + self.__block_len):
                        if (i, j) not in self.__read_only_names:
                            possible_values = set(name_to_variable_map[(i, j)].domain) & consistent_block_values
                            try:
                                value = possible_values.pop()
                            except KeyError:
                                raise UnsuccessfulSudokuCompleteAssignment()
                            name_to_variable_map[(i, j)].assign(value)
                            consistent_block_values.discard(value)

            new_individual = dict()
            for m, n in name_to_variable_map.keys():
                new_individual[name_to_variable_map[(m, n)]] = name_to_variable_map[(m, n)].value
            population.append(new_individual)

            for u, v in name_to_variable_map.keys():
                if (u, v) not in self.__read_only_names:
                    name_to_variable_map[(u, v)].unassign()

        return population

    def calculate_fitness(self, assignment: csp.Assignment) -> int:
        """ calculate state score by the number of unique values in each row and column. """
        self._constraint_problem.unassign_all_variables()
        self._constraint_problem.assign_variables_from_assignment(assignment)
        name_to_var_map = self._constraint_problem.get_name_to_variable_map()
        score = 0
        for row in _get_rows_indices(self.__grid_len):
            score += len(set((name_to_var_map[(i, j)].value for i, j in row)))
        for column in _get_columns_indices(self.__grid_len):
            score += len(set((name_to_var_map[(i, j)].value for i, j in column)))
        return score

    def perform_natural_selection(self, population: List[csp.Assignment]) -> List[csp.Assignment]:
        """ half truncation selection. """
        population.sort(key=self.calculate_fitness, reverse=True)
        return population[:len(population)//2]

    def reproduce_next_generation(self, old_generation: List[csp.Assignment]) -> List[csp.Assignment]:
        new_generation = list()
        for i in range(len(old_generation) * 2):
            parent1, parent2 = sample(old_generation, 2)
            new_generation.append(self.__reproduce(parent1, parent2))
        return new_generation

    def __reproduce(self, parent1: csp.Assignment, parent2: csp.Assignment) -> csp.Assignment:
        """ one-point crossover reproduction. since we don't want to violate any block constraints, randomly recombine
            half of one parent's blocks with the other half of the other parent's blocks. """
        crossover_point = randint(0, self.__grid_len - 1)
        block_indices = _get_block_indices(self.__grid_len)
        parent1_block_indices = block_indices[:crossover_point]
        parent2_block_indices = block_indices[crossover_point:]

        child = dict()
        self._constraint_problem.unassign_all_variables()
        self._constraint_problem.assign_variables_from_assignment(parent1)
        parent1_name_to_var_map = self._constraint_problem.get_name_to_variable_map()
        for block in parent1_block_indices:
            for s, t in block:
                child[parent1_name_to_var_map[(s, t)]] = parent1_name_to_var_map[(s, t)].value

        self._constraint_problem.unassign_all_variables()
        self._constraint_problem.assign_variables_from_assignment(parent2)
        parent2_name_to_var_map = self._constraint_problem.get_name_to_variable_map()
        for block in parent2_block_indices:
            for s, t in block:
                child[parent2_name_to_var_map[(s, t)]] = parent2_name_to_var_map[(s, t)].value

        return child

    def mutate_population(self, population: List[csp.Assignment], mutation_probability: float) -> None:
        for individual in population:
            if uniform(0, 1) < mutation_probability:
                self.__mutate(individual)

    def __mutate(self, individual: csp.Assignment) -> None:
        """ choose a block randomly, swap two squares (which aren't read-only) inside the block. """
        blocks_starting_indices = tuple(product(range(0, self.__grid_len, self.__block_len), repeat=2))
        (s, t) = choice(blocks_starting_indices)
        block_variables = list()
        for i in range(s, s + self.__block_len):
            for j in range(t, t + self.__block_len):
                if (i, j) not in self.__read_only_names:
                    block_variables.append((i, j))

        self._constraint_problem.unassign_all_variables()
        self._constraint_problem.assign_variables_from_assignment(individual)

        shuffle(block_variables)
        for a, b in block_variables:
            for u, v in block_variables:
                if (a, b) == (u, v):
                    continue
                if self.__have_been_swapped(a, b, u, v):
                    return

    def __have_been_swapped(self, a, b, u, v) -> bool:
        name_to_var_map = self._constraint_problem.get_name_to_variable_map()
        if name_to_var_map[(a, b)].value in name_to_var_map[(u, v)].domain and \
                name_to_var_map[(u, v)].value in name_to_var_map[(a, b)].domain:
            a_b_value = name_to_var_map[(a, b)].value
            u_v_value = name_to_var_map[(u, v)].value
            name_to_var_map[(a, b)].unassign()
            name_to_var_map[(u, v)].unassign()
            name_to_var_map[(a, b)].assign(u_v_value)
            name_to_var_map[(u, v)].assign(a_b_value)
            return True
        return False


class SudokuError(Exception):
    """ Base class for various Sudoku Errors. """


class UnsuccessfulSudokuCompleteAssignment(SudokuError):
    def __init__(self):
        super(UnsuccessfulSudokuCompleteAssignment, self).__init__("unable to generate a complete Sudoku assignment.")
