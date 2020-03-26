import unittest
from FileHelp import import_data_set

WHITE_DEGREE = 2
BLACK_DEGREE = 3

class TestClassification(unittest.TestCase):
    def test1(self):
        problems, restrictions, relaxations = import_data_set(WHITE_DEGREE,BLACK_DEGREE,"UC")
        for x in list(relaxations.keys()):
            for elem in relaxations[x]:
                self.assertIn(x,restrictions[elem])
if __name__ == '__main__':
    unittest.main()