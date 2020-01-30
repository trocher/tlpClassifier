#!/usr/bin/python3
import itertools
from Problem import Problem

labels = [1,2,3]
whiteDegree = 3
blackDegree = 2
def edgeLabellings(degree):
    return set(itertools.combinations_with_replacement(labels, 3))

def powerset(that):
    return set(itertools.chain.from_iterable(itertools.combinations(that, r) for r in range(len(that)+1)))

whiteConfigurations = edgeLabellings(whiteDegree)
blackConfigurations = edgeLabellings(blackDegree)
whiteConstraints = powerset(whiteConfigurations)
blackConstraints = powerset(blackConfigurations)
print("Constructing the set of all the problems")
programsList = set([(a,b) for a in whiteConstraints for b in blackConstraints])
programsList2 = set([Problem(a,b) for (a,b) in programsList])




MyFile=open('output2.txt','w')
for element in whiteConstraints:
     MyFile.write(''.join(str(element)))
     MyFile.write('\n')
MyFile.close()
