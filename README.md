## Basic Definitions
A _Constraint Satisfaction Problem (CSP)_ is a triplet _(X, D, C)_ where _X_ is a set of variables X<sub>1</sub>, ...,X<sub>n</sub>.  
_D_ is a set of domains D<sub>1</sub>, ...,D<sub>n</sub>, where each variable X<sub>i</sub> is assigned by values from domain D<sub>i</sub>.  
And _C_ is a set of constraints C<sub>1</sub>(S<sub>1</sub>), ..., C<sub>m</sub>(S<sub>m</sub>), where each S<sub>i</sub> is a set of variables on which C<sub>i</sub> defines a constraint.  
A state of _Constraint Satisfaction Problem_ instance is defined by an **assignment** of values to some or all of its variables.  
A **complete assignment** is a state in which every variable is assigned with a value from its domain.  
A **partial assignment** is a state in which some variables are assigned and some are not.  
A **consistent assignment** is a state in which the assigned variables do not violate any constraints.  
A **complete consistent assignment** is a solution to a _Constraint Satisfaction Problem_ instance.  
A **constraint graph** (could be a hypergraph) is a graph in which the nodes correspond to varaibles  
and the edges correspond to constraints, i.e. V = X and E = C.
<br>
<br>

## Toy Example: Magic Square
![](https://upload.wikimedia.org/wikipedia/commons/e/e4/Magicsquareexample.svg)  
<br>
Variables: squares on the board.  
Domains: each variable's domain is (1, ..., n x n).   
Constraints:  
-- Define **magic sum** to be n * ((n * n + 1) / 2).  
1. All variables must be have a unique value.
2. The values of all rows sum up to **magic sum**.
3. The values of all columns sum up to **magic sum**.
4. The values of both diagonals sum up to **magic sum**.

Code implementation:

    import csp  
    n = 3  
    order = n**2  
    magic_sum = n * int((order + 1) / 2)  
    name_to_variable_map = {square: csp.Variable(range(1, order + 1)) for square in range(1, order + 1)}  
    
    constraints = set()
    
    # each variable must have a unique value  
    constraints.add(csp.Constraint(name_to_variable_map.values(), csp.all_different))  
    
    exact_length_magic_sum = csp.ExactLengthExactSum(n, magic_sum)  
    
    # row constraints
    for row in range(1, order + 1, n):  
        constraints.add(csp.Constraint((name_to_variable_map[i] for i in range(row, row + n)),  
                                       exact_length_magic_sum))  
    
    # column constraints
    for column in range(1, n + 1):  
        constraints.add(csp.Constraint((name_to_variable_map[i] for i in range(column, order + 1, n)),  
                                       exact_length_magic_sum))  
    
    # diagonals constraints
    constraints.add(csp.Constraint((name_to_variable_map[diag] for diag in range(1, order + 1, n + 1)), 
                                   exact_length_magic_sum))  
    constraints.add(csp.Constraint((name_to_variable_map[diag] for diag in range(n, order, n - 1)), 
                                   exact_length_magic_sum))  
    
    magic_square_problem = csp.ConstraintProblem(constraints)  
    csp.heuristic_backtracking_search(magic_square_problem)  
    for name in name_to_variable_map.keys():  
        print(name, ":", name_to_variable_map[name].value)  
    
    >>> 1 : 8  
    >>> 2 : 1  
    >>> 3 : 6  
    >>> 4 : 3  
    >>> 5 : 5  
    >>> 6 : 7  
    >>> 7 : 4  
    >>> 8 : 9  
    >>> 9 : 2  

Alternatively, one could use any of the other algorithms implemented in the package (min-conflicts, simulated annealing,  
 naive cycle cutset etc. see full list below).

Other examples which can be found under 'examples' directory:
1. Graph coloring.
2. Job scheduling.
3. n-Queens.
4. Verbal arithmetic. 
5. Einstein's five houses riddle.
6. Sudoku.
<br>
<br>

## Implemented Algorithms List
#### Solvers
1. backtracking search (with or without forward checking).
2. heuristic backtracking search: defaults to Minimum Remaining Values for choosing next unassigned variable,  
and Degree heuristic as tie breaker. Defaults to Least Constraining Value for domain sorting of chosen unassigned variable.  
Allows users to define, pick and choose custom heuristics. Can be used with or without forward checking.
3. min conflicts (with or without tabu search).
4. constraints weighting.
5. tree csp solver: an algorithm that can solve tree-structured constraint satisfaction problems.
6. cycle cutset: a naive cutset conditioning solver. See source code for exhaustive description.
7. simulated annealing.
8. random-restart first-choice hill climbing.
9. genetic local search.
<br>

#### preprocessing
1. Arc Consistency 3 (AC3). Could be given to both backtracking algorithms and thus implement  
Maintaining Arc Consistency (MAC).
2. Arc Consistency 4 (AC4).
3. Path Consistency 2 (PC2).
4. i-consistency.
<br>
<br>

## Basic API (unsound and incomplete, made for explanatory purposes ONLY)
![](https://i.imgur.com/GjwBr45.png)