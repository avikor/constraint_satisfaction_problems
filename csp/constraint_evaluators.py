

def always_satisfied(values: tuple) -> bool:
    return True


def never_satisfied(values: tuple) -> bool:
    return False


def all_equal_constraint_evaluator(values: tuple) -> bool:
    if len(values) == 1:
        return True
    first_val = values[0]
    for val in values:
        if val != first_val:
            return False
    return True


def all_diff_constraint_evaluator(values: tuple) -> bool:
    seen_values = set()
    for val in values:
        if val in seen_values:
            return False
        seen_values.add(val)
    return True


class MaxSum:
    def __init__(self, maximum) -> None:
        self.__maximum = maximum

    def __call__(self, values: tuple) -> bool:
        return sum(values) < self.__maximum


class MinSum:
    def __init__(self, minimum) -> None:
        self.__minimum = minimum

    def __call__(self, values: tuple) -> bool:
        return self.__minimum < sum(values)


class ExactSum:
    def __init__(self, sum_value) -> None:
        self.__sum_value = sum_value

    def __call__(self, values: tuple) -> bool:
        return sum(values) == self.__sum_value


class ExactLengthExactSum:
    def __init__(self, number_of_values: int, sum_value) -> None:
        self.__number_of_values = number_of_values
        self.__sum_value = sum_value

    def __call__(self, values: tuple) -> bool:
        if len(values) < self.__number_of_values:
            return True
        if len(values) == self.__number_of_values:
            return sum(values) == self.__sum_value
        if len(values) > self.__number_of_values:
            return False


class OnlyiConsistentAssignment:
    def __init__(self, i_consistent_assignments: set):
        self.__i_consistent_assignments = i_consistent_assignments

    def __call__(self, values: tuple) -> bool:
        return values in self.__i_consistent_assignments

