import time
import csp


def measure_performance(tests_amount: int, problem_name: str, problem, constraint_solver: str, *args, **kwargs) -> None:
    read_only_variables = None
    try:
        read_only_variables = kwargs.pop("read_only_variables")
    except KeyError:
        pass

    if isinstance(problem, csp.GeneticConstraintProblem):
        const_problem = problem.get_constraint_problem()
        const_problem.unassign_all_variables(read_only_variables)
    else:
        problem.unassign_all_variables(read_only_variables)

    start_time = time.process_time()
    solution = getattr(csp, constraint_solver)(problem, *args, **kwargs)
    end_time = time.process_time()

    time_results = [end_time - start_time]
    histories_lengths = list()
    unsatisfied_constraints_amounts = list()
    if hasattr(solution, "__len__"):
        histories_lengths.append(len(solution))
        unsatisfied_constraints_amounts.append(len(problem.get_unsatisfied_constraints()))
    else:
        unsatisfied_constraints_amounts.append(len(solution.get_unsatisfied_constraints()))

    for i in range(tests_amount - 1):
        if isinstance(problem, csp.GeneticConstraintProblem):
            const_problem = problem.get_constraint_problem()
            const_problem.unassign_all_variables(read_only_variables)
        else:
            problem.unassign_all_variables(read_only_variables)

        start_time = time.process_time()
        solution = getattr(csp, constraint_solver)(problem, *args, **kwargs)
        end_time = time.process_time()
        time_results.append(end_time - start_time)
        if hasattr(solution, "__len__"):
            histories_lengths.append(len(solution))
            unsatisfied_constraints_amounts.append(len(problem.get_unsatisfied_constraints()))
        else:
            unsatisfied_constraints_amounts.append(len(solution.get_unsatisfied_constraints()))

    print("#" * 145)
    if constraint_solver in ["backtracking_search", "heuristic_backtracking_search"] and "inference" in kwargs:
        constraint_solver += "_with_forward_checking"
    print("displaying performance results of solver: '", constraint_solver, "' with problem: '", problem_name, "'",
          sep='')
    if isinstance(problem, csp.GeneticConstraintProblem):
        const_problem = problem.get_constraint_problem()
        overall_constraints_amount = len(const_problem.get_constraints())
    else:
        overall_constraints_amount = str(len(problem.get_constraints()))
    print("unsatisfied_constraints_amounts out of", overall_constraints_amount, "overall constraints:",
          unsatisfied_constraints_amounts)
    if hasattr(solution, "__len__"):
        print("solution lengths (number of assignment and unassignment actions):", histories_lengths)
    print("time results (seconds):", time_results)
