#!/usr/bin/python3
from Problem import Problem
from Problem import Constraints
from Complexity import Complexity,complexity_name
from timeit import default_timer as timer
import pickle
import Tools
from ConstraintReductionAlgorithm import constraint_reduction
from FileHelp import data_name, problems_to_file,add_degree_suffix

WHITE_DEGREE = 2
BLACK_DEGREE = 3
LABELS = frozenset([1,2,3])

DEBUG = True
#DEBUG = False
STORE = True
#STORE = False

def import_data_set(white_degree, black_degree):
    with open(data_name(WHITE_DEGREE,BLACK_DEGREE), 'rb') as problem_file:
        problems = pickle.load(problem_file)
    return problems

# Classify the problems of the given set according to the given complexity
def evaluate(problems, that, complexity):
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

    print("Classifying problems of complexity :",complexity_name[complexity])
    print (len(that), "problems founds")
    print (relaxations, "relaxations founds")
    print (restrictions, "restrictions founds")
    print("Finished in time ", end-start, "\n")

# Return the subset of unsolvable problems
def unsolvable_test(problems):
    unsolvable_set = set()
    for elem in problems:
        white_constraint, black_constraint = constraint_reduction(elem)
        if(len(white_constraint)==0 or len(black_constraint)==0):
            unsolvable_set.add(elem)
    return unsolvable_set
    
# Return the subset of constant problems
def constant_test(problems):
    res = set()
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
                    res.add(elem)
    return res

# Classify the given set of problems
def classify(problems):
    print(len(problems), "problems in the dataset")
    print("degrees : (",WHITE_DEGREE,BLACK_DEGREE,")\n")

    evaluate(problems, unsolvable_test(problems), Complexity.Unsolvable)
    evaluate(problems, constant_test(problems), Complexity.Constant)
    total = 0
    for complexity in Complexity:
        classifiedSubset = {x for x in problems if x.get_complexity() == complexity}
        total += len(classifiedSubset)
        if DEBUG:
            print(complexity_name.get(complexity)+ " problems :",len(classifiedSubset))
            if complexity == Complexity.Unclassified:
                subset_3_labels = {x for x in classifiedSubset if len(x.reduced_alphabet()) == 3}
                subset_2_labels = {x for x in classifiedSubset if len(x.reduced_alphabet()) == 2}
                print("including",len(subset_2_labels), "2_labelling problems")
        if STORE:
            problems_to_file("output/" + str(WHITE_DEGREE) + "_" + str(BLACK_DEGREE) + "/" + complexity_name.get(complexity) + ".txt", classifiedSubset)
            if complexity == Complexity.Unclassified:
                subset_3_labels = {x for x in classifiedSubset if len(x.reduced_alphabet()) == 3}
                problems_to_file("output/" + str(WHITE_DEGREE) + "_" + str(BLACK_DEGREE) + "/" + complexity_name.get(complexity) + "3_labels.txt", subset_3_labels)

    if total != len(problems):
        print("Error, the sum of classified problems is not equal to the total number of problems")
problems = import_data_set(WHITE_DEGREE,BLACK_DEGREE)
classify(problems)