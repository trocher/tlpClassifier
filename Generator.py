import itertools
from Tools import edge_3_labelling,powerset
from Problem import Problem
from FileHelp import data_name, store
from timeit import default_timer as timer

WHITE_DEGREE = 3
BLACK_DEGREE = 3

DEBUG = True
#DEBUG = False

# Return the set of all characteristics problems with the given degrees
def generate(white_degree, black_degree):
    white_configurations, black_configurations = edge_3_labelling(white_degree),edge_3_labelling(black_degree)
    white_constraints, black_constraints = powerset(white_configurations),powerset(black_configurations)
    problems_tuple = set([(frozenset(a),frozenset(b)) for a in white_constraints for b in black_constraints])
    problems = set([Problem(a,b,white_degree,black_degree) for (a,b) in problems_tuple if Problem(a,b,white_degree,black_degree).is_characteristic_problem()])
    number_of_problems = len(problems)

    if DEBUG:
        print("Number of White Configurations :",len(white_configurations))
        print("Number of Black Configurations :",len(black_configurations))
        print("Number of White Constraints :",len(white_constraints))
        print("Number of Black Constraints :",len(black_constraints))
        print("Number of problems :", number_of_problems)
    relaxations_dict, restrictions_dict = dict(),dict()
    i = 0
    for elem in problems:
        i+=1
        print('{:.1%}'.format(i/number_of_problems))
        relaxations,restrictions = set(),set()
        equivalent_set = elem.equivalent_problems_instance()
        for other in problems:
            for x in equivalent_set:
                if elem != other :
                    if x.is_restriction(other):
                        relaxations.add(other)
                    if x.is_relaxation(other):
                        restrictions.add(other)
        relaxations_dict[elem] = relaxations
        restrictions_dict[elem] = restrictions

    return (problems,relaxations_dict,restrictions_dict)

p = generate(WHITE_DEGREE,BLACK_DEGREE)
store(WHITE_DEGREE,BLACK_DEGREE,p,"UC")
