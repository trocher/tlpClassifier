import itertools
import Tools
from Problem import Problem
import pickle
from FileHelp import data_name


WHITE_DEGREE = 2
BLACK_DEGREE = 3
LABELS = set([1,2,3])

DEBUG = True
#DEBUG = False

# Return a list of equivalents problem to the given problem
def equivalent_problems(problem):
    problemList = [[[ (t[a],t[b],t[c]) for t in x] for x in problem] for a,b,c in itertools.permutations([0,1,2])]
    if BLACK_DEGREE == WHITE_DEGREE:
        problemList+=([[b,w] for w,b in problemList])
    return problemList

# Return true if and only if the given problem is the unique characteristic problem of all of its equivalents problems
def is_characteristic_problem(problem):
    equivalent_problems_list = equivalent_problems(problem)
    for white,black in equivalent_problems_list:
        white.sort()
        black.sort() 
    equivalent_problems_list.sort()
    problem[0].sort()
    problem[1].sort()
    return equivalent_problems_list[0] == problem

# Return the set of all characteristics problems with the given degrees
def generate(white_degree, black_degree):
    white_configurations = Tools.edge_3_labelling(white_degree)
    black_configurations = Tools.edge_3_labelling(black_degree)

    white_constraints = Tools.powerset(white_configurations)
    black_constraints = Tools.powerset(black_configurations)
    problemsTuple = set([(frozenset(a),frozenset(b)) for a in white_constraints for b in black_constraints if is_characteristic_problem([list(a),list(b)])])
    problems = set([Problem(a,b,white_degree,black_degree) for (a,b) in problemsTuple])
    numberOfProblems = len(problemsTuple)

    if DEBUG:
        print("Number of White Configurations :",len(white_configurations))
        print("Number of Black Configurations :",len(black_configurations))
        print("Number of White Constraints :",len(white_constraints))
        print("Number of Black Constraints :",len(black_constraints))
        print("Number of problems :", numberOfProblems)
    return problems

# Store the given problem set in the file with the given name
def store(name,probems):
    with open(name, 'wb') as problem_file:
        pickle.dump(probems, problem_file)

problems = generate(WHITE_DEGREE,BLACK_DEGREE)
store(data_name(WHITE_DEGREE,BLACK_DEGREE),problems)
