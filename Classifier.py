#!/usr/bin/python3
from Problem import Problem,Constraints
from Complexity import Complexity,complexity_name
from timeit import default_timer as timer
import time
from tqdm import tqdm
import pickle
import Tools
from Algorithms import constraint_reduction, looping_labels,redundancy_algorithm, greedy4Coloring,round_eliminator,cover_map_1,log_test
from FileHelp import import_data_set, problems_to_file,add_degree_suffix,store
from bitarray import bitarray, util
from TwoLabelsClassifier import getComplexityOf,constraints_to_bitvector_tuple
from Input import CONSTANTS, GLOBALS, LOGARITHMIC,ITERATED_LOGARITHMIC, LOGARITHMIC2
from joblib import Parallel, delayed
import multiprocessing

WHITE_DEGREE = 2
BLACK_DEGREE = 3
LABELS = frozenset([0,1,2])

DEBUG = True
#DEBUG = False
STORE = True
#STORE = False

# Classify the problems of the given set according to the given complexity
def compute_restriction_relaxations(problems, that, complexity,restrictions,relaxations):
    for problem in that:
        for relax in relaxations[problem]:
            relax.set_upper_bound(complexity)
            if complexity == Complexity.Constant:
                relax.constant_upper_bound = min(relax.constant_upper_bound,problem.constant_upper_bound)
        for restr in restrictions[problem]:
            restr.set_lower_bound(complexity)

def compute_relaxations(problems, that, complexity,relaxations):
    for problem in that:
        for relax in relaxations[problem]:
            relax.set_upper_bound(complexity)
            if complexity == Complexity.Constant:
                relax.constant_upper_bound = min(relax.constant_upper_bound,problem.constant_upper_bound)

# Return the subset of unsolvable problems
def unsolvable_test(problem):
    if(len(problem.white_constraint)==0 or len(problem.black_constraint)==0):
        problem.set_complexity(Complexity.Unsolvable)
    else:
        problem.set_upper_bound(Complexity.Global)

def two_labels_test(problem):
    if len(problem.alphabet()) < 3 and len(problem.white_constraint)>0 and len(problem.black_constraint)>0:
        problem.set_complexity(getComplexityOf(*constraints_to_bitvector_tuple(problem.white_constraint,problem.black_constraint,problem.alphabet(),WHITE_DEGREE,BLACK_DEGREE)))

def global_test(problem):
    if len(problem.white_constraint) != 0 and len(problem.black_constraint) != 0 and len(problem.alphabet()) == len(LABELS) and len(looping_labels(problem.white_constraint,problem.black_constraint)) == 2:
        problem.set_complexity(Complexity.Global)
        #print(problem)

def redundant_label_test(problem):
    if problem.alphabet_size() == 3:
        tmp = redundancy_algorithm(problem.white_constraint,problem.black_constraint)
        if tmp != None:
            problem.set_complexity(getComplexityOf(*constraints_to_bitvector_tuple(tmp[0],tmp[1],tmp[2],WHITE_DEGREE,BLACK_DEGREE)))

def round_eliminator_test(problem):
    upper_bound = round_eliminator(problem, 9)
    if upper_bound >= 0:
        problem.set_complexity(Complexity.Constant)
        problem.constant_upper_bound = min(problem.constant_upper_bound,upper_bound)
# Classify the given set of problems

def greedy_4_coloring_test(problem):
    if greedy4Coloring(problem):
        problem.set_upper_bound(Complexity.Iterated_Logarithmic)

def cover_map_test(problem):
    if cover_map_1(problem.white_constraint,problem.black_constraint):
        problem.set_lower_bound(Complexity.Iterated_Logarithmic)

def log_test_test(problem):
    if log_test(problem.white_constraint,problem.black_constraint):
        problem.set_upper_bound(Complexity.Logarithmic)

def unclassified_problems(problems):
    return {problem for problem in problems if problem.get_complexity() == Complexity.Unclassified}

def solvable_problems(problems):
    return {problem for problem in problems if problem.get_complexity() != Complexity.Unsolvable}


def classify(problems,relaxations,restrictions):
    print("Starting classification (" + str(len(problems)) + " problems)...")

    def partially_classify(function):
        for problem in tqdm(unclassified_problems(problems)):
            function(problem)

    def partially_classify_debug(function):
        for problem in tqdm(solvable_problems(problems)):
            function(problem)

    partially_classify(unsolvable_test)
    #partially_classify(round_eliminator_test)
    partially_classify(two_labels_test)
    partially_classify(global_test)
    partially_classify(redundant_label_test)
    partially_classify_debug(greedy_4_coloring_test) #done
    partially_classify_debug(cover_map_test)
    partially_classify_debug(log_test_test)
    
    for problem in problems:
        #if any([problem == Tools.alpha_to_problem(elem) for elem in CONSTANTS]):
        #    problem.set_complexity(Complexity.Constant)
        if any([problem == Tools.alpha_to_problem(elem) for elem in GLOBALS]):
            problem.set_complexity(Complexity.Global)
        if any([problem == Tools.alpha_to_problem(elem) for elem in LOGARITHMIC]):
            problem.set_upper_bound(Complexity.Logarithmic)
        if any([problem == Tools.alpha_to_problem(elem) for elem in LOGARITHMIC2]):
            problem.set_complexity(Complexity.Logarithmic)
        if any([problem == Tools.alpha_to_problem(elem) for elem in ITERATED_LOGARITHMIC]):
            problem.set_complexity(Complexity.Iterated_Logarithmic)


    print("Computing restrictions and relaxations ...")
    for complexity in tqdm(Complexity):
        if complexity != Complexity.Unclassified:
            classifiedSubset = {x for x in problems if x.get_complexity() == complexity}
            compute_restriction_relaxations(problems, classifiedSubset,complexity,restrictions,relaxations)
            if complexity == Complexity.Logarithmic or complexity == Complexity.Iterated_Logarithmic:
                UBSubset = {x for x in problems if x.upper_bound == complexity}
                compute_relaxations(problems, UBSubset,complexity,relaxations)


    classifiedSubset = {x for x in problems if x.get_complexity() == Complexity.Unclassified and x.lower_bound == Complexity.Constant}
    
    
    for complexity in Complexity:
        classifiedSubset = {x for x in problems if x.get_complexity() == complexity}
        if DEBUG:
            print(complexity_name.get(complexity)+ " problems :",len(classifiedSubset))
        if STORE:
            problems_to_file("output/" + str(WHITE_DEGREE) + "_" + str(BLACK_DEGREE) + "/" + complexity_name.get(complexity) + ".txt", classifiedSubset)
            if complexity == Complexity.Unclassified:
                classifiedSubset_global = {x for x in classifiedSubset if x.upper_bound == Complexity.Global}
                problems_to_file("output/" + str(WHITE_DEGREE) + "_" + str(BLACK_DEGREE) + "/" + complexity_name.get(complexity) + "global_temp.txt", classifiedSubset_global)

    store(WHITE_DEGREE,BLACK_DEGREE,(problems,relaxations,restrictions),"C")



problems,relaxations,restrictions = import_data_set(WHITE_DEGREE,BLACK_DEGREE,"C")
start = timer()
classify(problems,relaxations,restrictions)
print(timer()-start)