#!/usr/bin/python3
import itertools
from Problem import Problem
from Problem import Configurations
from Complexity import Complexity
from timeit import default_timer as timer

whiteDegree = 2
blackDegree = 3

DEBUG = True
#DEBUG = False
STORE = True
#STORE = False

labels = set([1,2,3])

complexityName = {
    Complexity.Unsolvable : "unsolvable",
    Complexity.Constant : "constant",
    Complexity.Iterated_Logarithmic : "iterated_logarithmic",
    Complexity.Logarithmic : "logarithmic",
    Complexity.Global : "global",
    Complexity.Unclassified : "unclassified"
    }

def edgeLabelling(degree):
    return [(a,b,degree-a-b) for a in range(0,degree+1) for b in range(0,degree+1-a)]

def powerset(that):
    return set(itertools.chain.from_iterable(itertools.combinations(that, r) for r in range(len(that)+1)))

whiteConfigurations = edgeLabelling(whiteDegree)
blackConfigurations = edgeLabelling(blackDegree)
whiteConstraints = powerset(whiteConfigurations)
blackConstraints = powerset(blackConfigurations)

if STORE:
    with open('output/informations.txt', mode='w+', encoding='utf-8') as f:
        f.write("White Configurations :\n")
        f.write('\n'.join(str(elem) for elem in whiteConfigurations))
        f.write("\nBlack Configurations :\n")
        f.write('\n'.join(str(elem) for elem in blackConfigurations))

if DEBUG:
    print("Number of White Constraints :",len(whiteConstraints))
    print("Number of Black Constraints :",len(blackConstraints))

### Construct the set of all possible problems

problemsTuple = set([(frozenset(a),frozenset(b)) for a in whiteConstraints for b in blackConstraints])
problems = set([Problem(a,b,whiteDegree,blackDegree) for (a,b) in problemsTuple])
numberOfProblems = len(problems)
if DEBUG:
    print("Number of problems :", numberOfProblems)



# Return the set of problem such that the white and black nodes have only edges labeled with a given color
def oneColoring():
    return Problem({(whiteDegree,0,0)}, {(blackDegree,0,0)}, whiteDegree, blackDegree).equivalentProblems()

# Return the set of problems that define a maximal matching
def maximalMatchings():
    return Problem({(0,0,whiteDegree),(1, whiteDegree-1, 0)},\
                    {(0,blackDegree,0)}.union({(1,a,blackDegree-1-a) for a in range(0,blackDegree)}),\
                    whiteDegree, blackDegree).equivalentProblems()

# Store a given set of problems in a file
# name, a string, the name of the file
# that, the set of problems
def problemsToFile(name, that):
    f= open(name,"w+")
    for elem in that:
        elem.writeInFile(f)
    f.close()

# Classify the problems of the given set according to the given complexity
def evaluate(problems, that, complexity):
    print (len(that))
    start = timer()
    for problem in problems:
        if problem.isRelaxationOfAtLeast1(that):
            problem.setUpperBound(complexity)
        if problem.isRestrictionOfAtLeast1(that):
            problem.setLowerBound(complexity)
    end = timer()
    print(end-start)


# Similar to II
# Return the set of unsolvabe problems for which the black and white constraints does not share any labels
def unsolvableTest():
    return {elem for elem in problems if not elem.hasCommonLabels()}

# Similar to III
# Return the set of problems for which the black (resp. white) constraint does accept any edge labelling while the black (resp. black) constraint accept at least one configuration
def constantTest3():
    return {elem for elem in problems if elem.configurationAlphabetSize(Configurations.White) == len(whiteConfigurations) and elem.configurationAlphabetSize(Configurations.Black) != 0 or \
           elem.configurationAlphabetSize(Configurations.Black) == len(blackConfigurations) and elem.configurationAlphabetSize(Configurations.White) != 0}

# Similar to IV
# Return the set of problems for which the black and white constraints does both contain a configuration that label all edge in the same label
def constantTest4():
    return oneColoring()

# Return the set of problems for which the white and black constraints contains a subset of configuration defining a maximal matching
#def iteratedLogarithmicTest():
#    maximalMatchingProblems = maximalMatchings()
#    for initialProblem in maximalMatchingProblems:
#        if (problem.isRelaxation(initialProblem)):
#            return True
#    return False
#


# Classify the given set of problems
def classify(problems):
    evaluate(problems, constantTest4(), Complexity.Constant)
    evaluate(problems, constantTest3(), Complexity.Constant)
    evaluate(problems, unsolvableTest(), Complexity.Unsolvable)
    #evaluate(problems, iteratedLogarithmicTest(), Complexity.Iterated_Logarithmic)
    total = 0
    for complexity in Complexity:
        classifiedSubset = {x for x in problems if x.getComplexity() == complexity}
        total += len(classifiedSubset)
        if DEBUG:
            print(complexityName.get(complexity)+ " problems :",len(classifiedSubset))
        if STORE:
            problemsToFile("output/"+complexityName.get(complexity) + ".txt", classifiedSubset)

    if total != numberOfProblems:
        print("Error, the sum of classified problems is not equal to the total number of problems")

classify(problems)