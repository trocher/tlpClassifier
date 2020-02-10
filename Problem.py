from Complexity import Complexity
from enum import Enum

class Configurations(Enum):
    White = 0
    Black = 1 

class Problem:

    # Creating a Problem
    # whiteConfigurations is a set of all the configurations (tuples) allowed for the white nodes
    # blackConfigurations is a set of all the configurations (tuples) allowed for the black nodes
    def __init__(self, whiteConfigurations, blackConfigurations, whiteDegree, blackDegree):
        self.whiteConfigurations = frozenset(whiteConfigurations)
        self.blackConfigurations = frozenset(blackConfigurations)
        self.whiteDegree = whiteDegree
        self.blackDegree = blackDegree
        self.lowerbound = Complexity.Constant
        self.upperbound = Complexity.Unsolvable
    # The hash function for problems
    def __hash__(self):
        return hash((self.whiteConfigurations,self.blackConfigurations))
        ### TODO implement hashing function

    # Equality of problem.
    def __eq__(self,other):
        return (self.whiteConfigurations == other.whiteConfigurations and self.blackConfigurations == other.blackConfigurations)

    # Print the main characteristics of the problem in the console
    def show(self):
        print("W degree =", self.whiteDegree, "| B degree =", self.blackDegree, "| Alphabet :", self.alphabet())
        print("White Config : ", self.whiteConfigurations)
        print("Black Config : ", self.blackConfigurations)
        print(" ")

    # Write the main characteristics of the problem in a file
    # io is the stream where the problem should be written
    def writeInFile(self, io):
        io.write("W degree = "+ str(self.whiteDegree) + " | B degree = " + str(self.blackDegree) + " | Alphabet : " + str(self.alphabet()) +"\n")
        io.write("White Config : " + str(self.whiteConfigurations)+"\n")
        io.write("Black Config : " + str(self.blackConfigurations)+"\n\n")

    # Return the alphabet of the given configuration
    # configuration is either Configurations.Black or Configurations.Black
    def configurationAlphabet(self, configuration):
        alphabet = set()
        config = self.blackConfigurations if configuration == Configurations.Black else self.whiteConfigurations
        for elem in config:
            alphabet.update(elem)
        return alphabet

    # Return the size of the alphabet of the given configuration
    # configuration is either Configurations.Black or Configurations.Black
    def configurationSize(self, configuration):
        return len(self.blackConfigurations if configuration == Configurations.Black else self.whiteConfigurations)

    # Return the the alphabet of the problem
    def alphabet(self):
        return self.configurationAlphabet(Configurations.White).union(self.configurationAlphabet(Configurations.Black))

    # Return the the alphabet size of the problem
    def alphabetSize(self):
        return len(self.alphabet())

    def hasCommonLabels(self):
        return len(self.configurationAlphabet(Configurations.White).intersection(self.configurationAlphabet(Configurations.Black))) != 0

    # Check if the current problem is a restriction of the given problem
    def isRestriction(self, other):
        return self.whiteConfigurations.issubset(other.whiteConfigurations) and self.blackConfigurations.issubset(other.blackConfigurations)
   
    # Check if the current problem is a relaxation of the given problem
    def isRelaxation(self, other):
        return other.isRestriction(self)

    def setLowerBound(self,complexity):
        self.lowerbound = complexity

    def setUpperBound(self,complexity):
        self.upperbound = complexity

    def setComplexity(self,complexity):
        self.setLowerBound(complexity)
        self.setUpperBound(complexity)

    def getComplexity(self):
        if self.lowerbound == self.upperbound:
            return self.lowerbound
        else :
            return Complexity.Unclassified