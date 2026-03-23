import argparse
import io
import unittest
from unittest.mock import patch

from main import parse_arguments
from utils import greet


class TestMainFunctions(unittest.TestCase):
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_greet(self, mock_stdout: io.StringIO) -> None:
        greet("Piotr")
        actual_output = mock_stdout.getvalue().strip()
        self.assertEqual(actual_output, "Hello, Piotr!")

    @patch("argparse.ArgumentParser.parse_args")
    def test_parse_arguments_count_flag(
        self,
        mock_parse_args,
    ) -> None:
        mock_parse_args.return_value = argparse.Namespace(
            count=True,
            greet=None,
            add_member=False,
            search_member=None,
            display_list=False,
        )

        args = parse_arguments()
        self.assertTrue(args.count)


if __name__ == "__main__":
    unittest.main()
