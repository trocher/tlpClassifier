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


problems,relaxations,restrictions = import_data_set(WHITE_DEGREE, BLACK_DEGREE,"C")

white_constraint = {'AC', 'AB'}
black_constraint = {'ABB', 'BBC', 'BCC', 'CCC', 'AAA', 'BBB', 'ACC', 'ABC'}
#black_constraint = {'ABB', 'ABC', 'ACC', 'BBB'}
alpha_problem = (white_constraint,black_constraint,WHITE_DEGREE,BLACK_DEGREE)

print(search(alpha_problem,problems, relaxations, restrictions))
#search_border_problems(problems,relaxations,restrictions)