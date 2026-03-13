import unittest
import io
from unittest.mock import patch  
from main import greet, get_members_count

class TestMainFunctions(unittest.TestCase):

    def test_get_members_count(self):
        self.assertEqual(get_members_count(), 4)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_greet(self, mock_stdout):
        greet("Piotr")
        actual_output = mock_stdout.getvalue().strip()
        self.assertEqual(actual_output, "Hello, Piotr!")

if __name__ == '__main__':
    unittest.main()