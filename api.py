import numpy
from file_help import import_data_set
from problem import Problem,alpha_to_problem
from complexity import Complexity
from timeit import default_timer as timer
from input import LOGARITHMIC_LOWER_BOUND
from problem_set import Problem_set


# Get the complexity of a problem
def get_problem(alpha_problem, problems):
    problem = alpha_to_problem(alpha_problem)
    for elem in problems:
        if problem == elem:
            return elem
    print("error")

# Get the relaxations of a given problem
def get_relaxations_of(alpha_problem,problems,relaxations,restrictions):
    return relaxations[get_problem(alpha_problem,problems)]

# Get the restrictions of a given problem
def get_restrictions_of(alpha_problem,problems,relaxations,restrictions):
    return restrictions[get_problem(alpha_problem,problems)]

# Get the set of unclassified problems
def get_unclassified_problems(problems,relaxations,restrictions):
    return {x for x in problems if x.get_complexity() == Complexity.Unclassified}

# Get the set of problems with a given complexity
def get_problems_of_complexity(complexity,problems,relaxations,restrictions):
    return {problem for problem in problems if problem.get_complexity()==complexity}

# Return the set of constant problems that have the given upper bound
def get_constant_problems_with_x_rounds_UB(x,problems):
    return {problem for problem in problems if problem.get_complexity()==Complexity.Constant and problem.constant_upper_bound == x}

#Get all the unclassfied problem that does'nt have any unclassified relaxations
def get_UC_problems_with_C_relaxations(problems, relaxations, restrictions):
    return {problem for problem in problems if problem.get_complexity() == Complexity.Unclassified and all([x.get_complexity() != Complexity.Unclassified for x in relaxations[problem]])}

#Get all the unclassfied problem that does'nt have any unclassified restrictions
def get_UC_with_C_restrictions(problems, relaxations, restrictions):
    return {problem for problem in problems if problem.get_complexity() == Complexity.Unclassified and all([x.get_complexity() != Complexity.Unclassified for x in restrictions[problem]])}

#Get the distribution of the upper bounds on constant problems
def get_upper_bounds_constant_problems(problems):
    res = dict()
    for problem in problems:
        if problem.get_complexity()==Complexity.Constant:
            ub = problem.constant_upper_bound
            res[ub] = res.get(ub,0) + 1
    return res

problems,relaxations,restrictions = import_data_set(2, 3,Problem_set.Classified)

white_constraint = {'BC','AA'}
black_constraint = {'AAC', 'BBB'}
alpha_problem = (white_constraint,black_constraint,2,3)

print(get_problem(alpha_problem,problems))

print(get_upper_bounds_constant_problems(problems))
