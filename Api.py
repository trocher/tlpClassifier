import numpy
from FileHelp import import_data_set
from Problem import Problem
from Complexity import Complexity
from timeit import default_timer as timer
from Tools import alpha_to_problem
from Algorithms import local_neighborhood

def get_problem(alpha_problem, problems):
    problem = alpha_to_problem(alpha_problem)
    for elem in problems:
        if problem == elem:
            return elem
    print("error")

def get_relaxations_of(alpha_problem,problems,relaxations,restrictions):
    return relaxations[get_problem(alpha_problem,problems)]

def get_unclassified_relaxations_of(alpha_problem,problems,relaxations,restrictions):
    return {x for x in relaxations[get_problem(alpha_problem,problems)] if x.get_complexity() == Complexity.Unclassified}

def get_unclassified_restrictions_of(alpha_problem,problems,relaxations,restrictions):
    return {x for x in restrictions[get_problem(alpha_problem,problems)] if x.get_complexity() == Complexity.Unclassified}

def get_restrictions_of(alpha_problem,problems,relaxations,restrictions):
    return restrictions[get_problem(alpha_problem,problems)]

def get_problems_of_complexity(complexity,problems,relaxations,restrictions):
    return {problem for problem in problems if problem.get_complexity()==complexity}

def get_constant_problems_with_x_rounds_UB(x,problems):
    return {problem for problem in problems if problem.get_complexity()==Complexity.Constant and problem.constant_upper_bound == x}


def get_UC_problems_with_C_relaxations(problems, relaxations, restrictions):
    return {problem for problem in problems if problem.get_complexity() == Complexity.Unclassified and all([x.get_complexity() != Complexity.Unclassified for x in relaxations[problem]])}

def get_UC_with_C_restrictions(problems, relaxations, restrictions):
    return {problem for problem in problems if problem.get_complexity() == Complexity.Unclassified and all([x.get_complexity() != Complexity.Unclassified for x in restrictions[problem]])}

def get_UC_with_x_UC_relaxations(complexity, val, problems, relaxations, restrictions):
    for elem in problems:
        if elem.get_complexity() == Complexity.Unclassified and elem.lower_bound == Complexity.Logarithmic and numpy.count_nonzero([x.get_complexity() == Complexity.Unclassified and x.lower_bound == Complexity.Logarithmic for x in relaxations[elem]]) > val:
            print(elem)
def get_constant_not_RE(problems):
    return {problem for problem in problems if problem.get_complexity() == Complexity.Constant and problem.constant_upper_bound == 1000}

def get_upper_bounds_constant_problems(problems):
    res = dict()
    for problem in problems:
        if problem.get_complexity()==Complexity.Constant:
            ub = problem.constant_upper_bound
            if ub == 5:
                print(problem)
            res[ub] = res.get(ub,0) + 1
    return res

def get_problems_RCP_eligible(problems):
    return {problem for problem in problems if problem.get_complexity()== Complexity.Unclassified and (problem.upper_bound == Complexity.Global) and (0,0,2) in problem.white_constraint and  (0,2,0) in problem.white_constraint} #and any([x[2] == 2 for x in problem.black_constraint])}


def test_const(problems):
    return {problem for problem in problems if problem.get_complexity( )== Complexity.Constant and not local_neighborhood(problem.white_constraint,problem.black_constraint)} 


problems,relaxations,restrictions = import_data_set(2, 3,"C")
white_constraint = {'AC','BC'}
black_constraint = {'ABB','ACC'}
alpha_problem = (white_constraint,black_constraint,2,3)

print(get_problem(alpha_problem,problems))
#for problem in get_unclassified_relaxations_of(alpha_problem,problems,relaxations,restrictions):
#    print(problem)
#for x in get_UC_problems_with_C_relaxations(problems,relaxations,restrictions):
#    print(x)
#print(get_upper_bounds_constant_problems(problems))
#for x in get_constant_not_RE(problems):
#    print(x)
#for x in get_constant_problems_with_x_rounds_UB(4,problems):
#    print(x)