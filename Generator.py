import itertools
import Tools
from Problem import Problem
import pickle
from FileHelp import data_name, store
from ProblemEquivalence import is_characteristic_problem
from timeit import default_timer as timer

WHITE_DEGREE = 2
BLACK_DEGREE = 3
LABELS = set([1,2,3])

DEBUG = True
#DEBUG = False

# Return the set of all characteristics problems with the given degrees
def generate(white_degree, black_degree):
    white_configurations = Tools.edge_3_labelling(white_degree)
    black_configurations = Tools.edge_3_labelling(black_degree)
    start = timer()
    white_constraints = Tools.powerset(white_configurations)
    black_constraints = Tools.powerset(black_configurations)
    problemsTuple = set([(frozenset(a),frozenset(b)) for a in white_constraints for b in black_constraints])
    problems = set([Problem(a,b,white_degree,black_degree) for (a,b) in problemsTuple if Problem(a,b,white_degree,black_degree).is_characteristic_problem()])
    end = timer()
    print(end-start)
    numberOfProblems = len(problems)

    if DEBUG:
        print("Number of White Configurations :",len(white_configurations))
        print("Number of Black Configurations :",len(black_configurations))
        print("Number of White Constraints :",len(white_constraints))
        print("Number of Black Constraints :",len(black_constraints))
        print("Number of problems :", numberOfProblems)
    return problems



problems = generate(WHITE_DEGREE,BLACK_DEGREE)
store(WHITE_DEGREE,BLACK_DEGREE,problems,"UC")
