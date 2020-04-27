import numpy
from FileHelp import import_data_set
from Problem import Problem
from Complexity import Complexity
from timeit import default_timer as timer
from Tools import alpha_to_problem
WHITE_DEGREE = 2
BLACK_DEGREE = 3

def search(alpha_problem, problems, relaxations, restrictions):
    problem = alpha_to_problem(alpha_problem)
    for elem in problems:
        if problem == elem:
            for x in restrictions[elem]:
                if x.get_complexity()==Complexity.Constant:
                    print (x)
            return elem
    print("error")

def search_border_problems(problems, relaxations, restrictions):
    for elem in problems:
        if elem.get_complexity() == Complexity.Unclassified and all([x.get_complexity() == Complexity.Constant for x in relaxations[elem]]):
            print(elem)
    print("================================")
    for elem in problems:
        if elem.get_complexity() == Complexity.Unclassified and all([x.get_complexity() == Complexity.Unsolvable for x in restrictions[elem]]):
            print(elem)

def search_border_problems_2(problems, relaxations, restrictions):
    for elem in problems:
        if elem.get_complexity() == Complexity.Unclassified and all([x.get_complexity() != Complexity.Unclassified for x in relaxations[elem]]):
            print(elem)

def search_unclassified_problems_with_unclassified_relaxations(problems, relaxations, restrictions, complexity, val):
    for elem in problems:
        if elem.get_complexity() == Complexity.Unclassified and elem.lower_bound == Complexity.Logarithmic and numpy.count_nonzero([x.get_complexity() == Complexity.Unclassified and x.lower_bound == Complexity.Logarithmic for x in relaxations[elem]]) > val:
            print(elem)

problems,relaxations,restrictions = import_data_set(WHITE_DEGREE, BLACK_DEGREE,"C")

white_constraint = {'BC', 'AA'}
black_constraint = {'ABB', 'BBC','BCC','AAB','AAC','ABC'}
alpha_problem = (white_constraint,black_constraint,WHITE_DEGREE,BLACK_DEGREE)

print(search(alpha_problem,problems, relaxations, restrictions))
#for problem in problems:
#    if problem.get_complexity()==Complexity.Constant and problem.constant_upper_bound == 1000:
#        print(problem)
#search_border_problems(problems,relaxations,restrictions)
#search_border_problems_2(problems,relaxations,restrictions)
#search_unclassified_problems_with_unclassified_relaxations(problems, relaxations, restrictions, Complexity.Logarithmic, 5)