#!/usr/bin/python3
from Problem import Problem,Constraints
from Complexity import Complexity,complexity_name
from timeit import default_timer as timer
import pickle
import Tools
from Algorithms import constraint_reduction, looping_labels,redundancy_algorithm
from FileHelp import import_data_set, problems_to_file,add_degree_suffix,store
from bitarray import bitarray, util
from TwoLabelsClassifier import getComplexityOf,constraints_to_bitvector_tuple
from Input import CONSTANTS, GLOBALS
WHITE_DEGREE = 2
BLACK_DEGREE = 3
LABELS = frozenset([0,1,2])

DEBUG = True
#DEBUG = False
STORE = True
#STORE = False

# Classify the problems of the given set according to the given complexity
def compute_restriction_relaxations(problems, that, complexity,restrictions,relaxations):
    start = timer()
    for problem in that:
        for relax in relaxations[problem]:
            relax.set_upper_bound(complexity)
        for restr in restrictions[problem]:
            restr.set_lower_bound(complexity)
    end = timer()
    print("Computing relaxations and restrictions of the problems of complexity :",complexity_name[complexity])
    print (len(that), "problems")
    print("Finished in time ", end-start, "\n")


# Return the subset of unsolvable problems
def unsolvable_test(problem):
    if(len(problem.white_constraint)==0 or len(problem.black_constraint)==0):
        problem.set_complexity(Complexity.Unsolvable)
    else:
        problem.set_upper_bound(Complexity.Global)

    
# Return the subset of constant problems
def constant_test(problem):
    labels_subsets = Tools.powerset(LABELS)
    labels_subsets.remove(())
    for elem in labels_subsets:
        labels_subset_generator_w = Tools.edge_n_labelling_generator(WHITE_DEGREE,elem)
        labels_subset_generator_b = Tools.edge_n_labelling_generator(BLACK_DEGREE,elem)
        if(labels_subset_generator_w.issubset(problem.white_constraint) and any([ set([item]).issubset(labels_subset_generator_b) for item in problem.black_constraint]) or\
            labels_subset_generator_b.issubset(problem.black_constraint) and any([ set([item]).issubset(labels_subset_generator_w) for item in problem.white_constraint])):
            problem.set_complexity(Complexity.Constant)


def two_labels_test(problem):
    if len(problem.alphabet()) == 2 and len(problem.white_constraint)>0 and len(problem.black_constraint)>0:
        problem.set_complexity(getComplexityOf(*constraints_to_bitvector_tuple(problem.white_constraint,problem.black_constraint,problem.alphabet(),WHITE_DEGREE,BLACK_DEGREE)))

def global_test(problem):
    if len(problem.white_constraint) != 0 and len(problem.black_constraint) != 0 and len(problem.alphabet()) == len(LABELS) and len(looping_labels(problem.white_constraint,problem.black_constraint)) == 2:
        problem.set_complexity(Complexity.Global)

def redundant_label_test(problem):
    if problem.alphabet_size() == 3:
        tmp = redundancy_algorithm(problem.white_constraint,problem.black_constraint)
        if tmp != None:
            problem.set_complexity(getComplexityOf(*constraints_to_bitvector_tuple(tmp[0],tmp[1],tmp[2],WHITE_DEGREE,BLACK_DEGREE)))

# Classify the given set of problems
def classify(problems,relaxations,restrictions):
    print(len(problems), "problems in the dataset")
    print("degrees : (",WHITE_DEGREE,BLACK_DEGREE,")\n")
    new_complexity = Complexity.Unclassified
    for problem in problems:
        
        two_labels_test(problem)
        unsolvable_test(problem)
        constant_test(problem)
        global_test(problem)
        redundant_label_test(problem)
    
        if any([problem == Tools.alpha_to_problem(elem) for elem in CONSTANTS]):
            problem.set_complexity(Complexity.Constant)
        if any([problem == Tools.alpha_to_problem(elem) for elem in GLOBALS]):
            problem.set_complexity(Complexity.Global)
    
    for complexity in Complexity:
        if complexity != Complexity.Unclassified:
            classifiedSubset = {x for x in problems if x.get_complexity() == complexity}
            compute_restriction_relaxations(problems, classifiedSubset,complexity,restrictions,relaxations)


    store(WHITE_DEGREE,BLACK_DEGREE,(problems,relaxations,restrictions),"C")
    
    for complexity in Complexity:
        classifiedSubset = {x for x in problems if x.get_complexity() == complexity}
        if DEBUG:
            print(complexity_name.get(complexity)+ " problems :",len(classifiedSubset))
        if STORE:
            problems_to_file("output/" + str(WHITE_DEGREE) + "_" + str(BLACK_DEGREE) + "/" + complexity_name.get(complexity) + ".txt", classifiedSubset)


problems,relaxations,restrictions = import_data_set(WHITE_DEGREE,BLACK_DEGREE,"UC")
start = timer()
classify(problems,relaxations,restrictions)
print(timer()-start)