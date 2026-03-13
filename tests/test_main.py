import unittest

from src.main import get_members_count, greet

class TestMainFunctions(unittest.TestCase):

    def test_get_members_count(self):
        count = get_members_count()
        self.assertEqual(count, 4)

    def test_greet(self):
        result = greet("Piotr")
        self.assertEqual(result, "Hello, Piotr!")

if __name__ == '__main__':
    unittest.main()