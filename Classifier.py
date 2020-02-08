#!/usr/bin/python3
import itertools
from Problem import Problem
from Problem import Configurations

from Complexity import Complexity
from timeit import default_timer as timer 

DEBUG = True
#DEBUG = False

labels = [1,2,3]
whiteDegree = 3
blackDegree = 3

### Generate the Configurations
def edgeLabellings(degree):
    return set(itertools.combinations_with_replacement(labels, degree))

def powerset(that):
    return set(itertools.chain.from_iterable(itertools.combinations(that, r) for r in range(len(that)+1)))

whiteConfigurations = edgeLabellings(whiteDegree)
whiteConstraints = powerset(whiteConfigurations)
whiteConstraints.remove(())
blackConfigurations = edgeLabellings(blackDegree)
blackConstraints = powerset(blackConfigurations)
blackConstraints.remove(())

if DEBUG:
    print("Number of White Constraints :",len(whiteConstraints))
    print("Number of Black Constraints :",len(blackConstraints))

### Construct the set of all possible problems

problemsTuple = set([(frozenset(a),frozenset(b)) for a in whiteConstraints for b in blackConstraints])
problems = set([Problem(a,b) for (a,b) in problemsTuple])
if DEBUG:
    print("Number of problems :", len(problems))



def oneColoring():
    return {Problem(set([tuple([l] * whiteDegree)]), set([tuple([l] * blackDegree)])) for l in labels}

def classifyConstant(problems):
    oneColoringProblems = oneColoring()
    for problem in problems:
        if problem.configurationSize(Configurations.White) == len(whiteConfigurations) or problem.configurationSize(Configurations.Black) == len(blackConfigurations):
            problem.setComplexity(Complexity.Constant)
        for initialProblem in oneColoringProblems:
            if (problem.isRelaxation(initialProblem)):
                problem.setComplexity(Complexity.Constant)

classifyConstant(problems)
constantProblems = {x for x in problems if x.getComplexity() == Complexity.Constant}
if DEBUG:
    print("Constant problems classified :",len(constantProblems))


def classifyUnsolvable(problems):
    for problem in problems:
        if not problem.hasCommonLabels():
            problem.setComplexity(Complexity.Unsolvable)
classifyUnsolvable(problems)
unsolvableProblems = {x for x in problems if x.getComplexity() == Complexity.Unsolvable}
if DEBUG:
    print("Unsolvable problems classified :",len(unsolvableProblems))
