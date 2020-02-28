import unittest

from Problem import Problem

class TestProblem(unittest.TestCase):

    def test_equality(self):
        problem1 = Problem(set([(1,2,0),(2,1,0)]), set([(1,1,1),(3,0,0)]), 3, 3)
        problem2 = Problem(set([(2,1,0),(1,2,0)]), set([(1,1,1),(3,0,0)]), 3, 3)
        self.assertEqual(problem1, problem2)

    def test_alphabet(self):
        problem1 = Problem(frozenset([(1,2,0),(2,1,0)]), frozenset([(1,2,0),(3,0,0)]), 3, 3)
        self.assertEqual(frozenset([1,2]), problem1.alphabet())
        problem2 = Problem(frozenset([(1,1,1),(2,1,0)]), frozenset([(1,2,0),(3,0,0)]), 3, 3)
        self.assertEqual(frozenset([1,2,3]), problem2.alphabet())
        problem3 = Problem(frozenset([(3,0,0)]), frozenset([(3,0,0)]), 3, 3)
        self.assertEqual(frozenset([1]), problem3.alphabet())

    def test_hasCommonLabels(self):
        problem1 = Problem(frozenset([(1,2,0),(2,1,0)]), frozenset([(1,2,0),(3,0,0)]), 3, 3)
        problem2 = Problem(frozenset([(0,3,0)]), frozenset([(3,0,0)]), 3, 3)
        self.assertTrue(problem1.has_common_labels())
        self.assertFalse(problem2.has_common_labels())

    def test_hash(self):
        problem1 = Problem(frozenset([(1,2,3),(1,1,1)]), frozenset([(1,3,2),(3,2,2)]), 3, 3)
        problem2 = Problem(frozenset([(1,1,1),(1,2,3)]), frozenset([(1,3,2),(3,2,2)]), 3, 3)
        problem3 = Problem(frozenset([(1,1,1),(1,2,2)]), frozenset([(1,3,2),(3,2,2)]), 3, 3)
        self.assertEqual(hash(problem1),hash(problem2))
        self.assertNotEqual(hash(problem1),hash(problem3))

    def test_restriction_relaxation(self):
        problem1 = Problem(set([(1,2,0),(2,1,0)]), set([(1,2,0),(3,0,0)]), 3, 3)
        problem2 = Problem(set([(2,1,0)]), set([(1,2,0),(3,0,0)]), 3, 3)
        problem3 = Problem(set([(1,2,0),(0,3,0)]), set([(1,2,0),(3,0,0)]), 3, 3)
        self.assertTrue(problem2.is_restriction(problem1))
        self.assertTrue(problem1.is_restriction(problem2))
        self.assertFalse(problem2.is_restriction(problem3))

if __name__ == '__main__':
    unittest.main()