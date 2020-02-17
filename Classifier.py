#!/usr/bin/python3
import itertools
from Problem import Problem
from Problem import Configurations
from Complexity import Complexity
from timeit import default_timer as timer

whiteDegree = 3
blackDegree = 3

DEBUG = True
#DEBUG = False
STORE = False
#STORE = False

labels = set([1,2,3])

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

# Delete the symetry between the black and white node in case they have the same degree
if whiteDegree == blackDegree:
    problemsTuple = set(itertools.combinations_with_replacement(whiteConstraints, 2))
else :
    problemsTuple = set([(frozenset(a),frozenset(b)) for a in whiteConstraints for b in blackConstraints])
problems = set([Problem(a,b,whiteDegree,blackDegree) for (a,b) in problemsTuple])
if DEBUG:
    print("Number of problems :", len(problems))

def oneColoring():
    return Problem({(3,0,0)}, {(3,0,0)}, whiteDegree, blackDegree).labelsSymetry()

def problemsToFile(name, that):
    f= open(name,"w+")
    for elem in that:
        elem.writeInFile(f)
    f.close()

# Classify the problems of the given set such that the complexity of the ones on which the given predicate return true is set to the given complexity
def classify(problems, predicate, complexity):
    for problem in problems:
        if predicate(problem):
            problem.setComplexity(complexity)

# A predicate similar to II
# Check if the problem is insolvable : if the black and white constraints does not share any labels
def unsolvableTest(problem):
    return not problem.hasCommonLabels()

# A predicate similar to III
# Check if the black (resp. white) constraint does accept any edge labelling while the black (resp. black) constraint accept at least one configuration
def constantTest(problem):
    return problem.configurationSize(Configurations.White) == len(whiteConfigurations) and problem.configurationSize(Configurations.Black) != 0 or \
           problem.configurationSize(Configurations.Black) == len(blackConfigurations) and problem.configurationSize(Configurations.White) != 0

# A predicate similar to IV
# Check if both the black and white constraints does both contain a configuration that label all edge in the same label
def constantTest2(problem):
    oneColoringProblems = oneColoring()
    for initialProblem in oneColoringProblems:
        if (problem.isRelaxation(initialProblem)):
            return True
    return False

classify(problems, unsolvableTest, Complexity.Unsolvable)
classify(problems, constantTest, Complexity.Constant)
classify(problems, constantTest2, Complexity.Constant)

for complexity in Complexity:
    classifiedSubset = {x for x in problems if x.getComplexity() == complexity}
    if DEBUG:
        print(complexity.value+ " problems classified :",len(classifiedSubset))
    if STORE:
        problemsToFile("output/"+complexity.value + ".txt", classifiedSubset)
