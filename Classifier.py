#!/usr/bin/python3
from Problem import Problem
from Problem import Constraints
from Complexity import Complexity,complexity_name
from timeit import default_timer as timer
import pickle
import Tools
from Algorithms import constraint_reduction, looping_labels
from FileHelp import import_data_set, problems_to_file,add_degree_suffix,store
from bitarray import bitarray, util
from TwoLabelsClassifier import getComplexityOf
WHITE_DEGREE = 2
BLACK_DEGREE = 3
LABELS = frozenset([1,2,3])

DEBUG = True
#DEBUG = False
STORE = True
#STORE = False


# Classify the problems of the given set according to the given complexity
def compute_restriction_relaxations(problems, that, complexity):
    start = timer()
    relaxations = 0
    restrictions = 0
    for problem in that:
        problem.set_complexity(complexity)
    for problem in problems.difference(that):
        if problem.is_relaxation_of_at_least_1(that):
            relaxations +=1
            problem.set_upper_bound(complexity)
        if problem.is_restriction_of_at_least_1(that):
            restrictions +=1
            problem.set_lower_bound(complexity)
    end = timer()

    print("Computing relaxations and restrictions of the problems of complexity :",complexity_name[complexity])
    print (len(that), "problems")
    print (relaxations, "relaxations founds")
    print (restrictions, "restrictions founds")
    print("Finished in time ", end-start, "\n")


# Return the subset of unsolvable problems
def unsolvable_test(problems):
    unsolvable_set = set()
    for elem in problems:
        white_constraint, black_constraint = constraint_reduction(elem.white_constraint,elem.black_constraint)
        if(len(white_constraint)==0 or len(black_constraint)==0):
            elem.set_complexity(Complexity.Unsolvable)
    
# Return the subset of constant problems
def constant_test(problems):
    for i in [1,2,3]:
        alphabet_i_subsets = Tools.subsets_of_size_n(LABELS,i)
        constraint_white_max = Tools.edge_n_labelling_len(WHITE_DEGREE,i)
        constraint_black_max = Tools.edge_n_labelling_len(BLACK_DEGREE,i)
        for elem in problems:
            for alphabet_subset in alphabet_i_subsets:
                if(elem.constraint_alphabet(Constraints.White) == alphabet_subset and\
                elem.constraint_size(Constraints.White) == constraint_white_max and \
                elem.constraint_alphabet(Constraints.Black)==alphabet_subset or\
                elem.constraint_alphabet(Constraints.Black) == alphabet_subset and\
                elem.constraint_size(Constraints.Black) == constraint_black_max and \
                elem.constraint_alphabet(Constraints.White)==alphabet_subset):
                    elem.set_complexity(Complexity.Constant)

def two_labels_test(problems):
    res = set()
    for elem in problems:
        if len(elem.alphabet()) == 2 and len(elem.white_constraint)>0 and len(elem.black_constraint)>0:
            white = util.zeros(WHITE_DEGREE+1)
            black = util.zeros(BLACK_DEGREE+1)
            label = list(elem.alphabet())[0]-1
            for configuration in elem.white_constraint:
                white[configuration[label]] = 1
            for configuration in elem.black_constraint:
                black[configuration[label]] = 1
            elem.set_complexity(getComplexityOf(white,black))

# Classify the given set of problems
def classify(problems):
    print(len(problems), "problems in the dataset")
    print("degrees : (",WHITE_DEGREE,BLACK_DEGREE,")\n")
    two_labels_test(problems)
    unsolvable_test(problems)
    constant_test(problems)
    total = 0
    for complexity in Complexity:
        classifiedSubset = {x for x in problems if x.get_complexity() == complexity}
        if complexity != Complexity.Unclassified:
            compute_restriction_relaxations(problems, classifiedSubset,complexity)
    for problem in problems:
        if len(problem.white_constraint) != 0 and len(problem.black_constraint) != 0 and len(problem.alphabet()) == 3 and len(looping_labels(problem.white_constraint,problem.black_constraint)) == 2:
            problem.show()
            print(problem.get_complexity())
    store(WHITE_DEGREE,BLACK_DEGREE,problems,"C")
    for complexity in Complexity:
        classifiedSubset = {x for x in problems if x.get_complexity() == complexity}
        total += len(classifiedSubset)
        if DEBUG:
            print(complexity_name.get(complexity)+ " problems :",len(classifiedSubset))
        if STORE:
            problems_to_file("output/" + str(WHITE_DEGREE) + "_" + str(BLACK_DEGREE) + "/" + complexity_name.get(complexity) + ".txt", classifiedSubset)

    if total != len(problems):
        print("Error, the sum of classified problems is not equal to the total number of problems")

problems = import_data_set(WHITE_DEGREE,BLACK_DEGREE,"UC")
classify(problems)