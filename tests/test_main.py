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
import json
import pytest

from team import get_members_count, search_team_member, add_team_member
from utils import read_members


def test_get_members_count():
    """Test that the member counting logic returns the correct length."""
    members = ["Alice", "Bob", "Charlie", "David"]
    assert get_members_count(members) == 4
    
    empty_members = []
    assert get_members_count(empty_members) == 0


def test_read_members_ignores_blank_lines(tmp_path):
    """Test that text file reading extracts names and ignores empty lines."""
    test_file = tmp_path / "dummy_members.txt"
    

    test_file.write_text("Alice\n\nBob\n \nCharlie\n", encoding="utf-8")
    
    members = read_members(str(test_file))
    
    assert len(members) == 3
    assert members == ["Alice", "Bob", "Charlie"]


def test_search_team_member(tmp_path):
    """Test that searching finds members by forename, surname, or full name (case-insensitive)."""
    test_json = tmp_path / "team_data.json"
    data = {
        "members": [
            {"id": 1, "forename": "John", "surname": "Doe", "team_founder": True},
            {"id": 2, "forename": "Jane", "surname": "Smith", "team_founder": False}
        ]
    }
    test_json.write_text(json.dumps(data), encoding="utf-8")
    
    results_jane = search_team_member(str(test_json), "Jane")
    assert len(results_jane) == 1
    assert results_jane[0]["surname"] == "Smith"

    results_doe = search_team_member(str(test_json), "oe")
    assert len(results_doe) == 1
    assert results_doe[0]["forename"] == "John"


def test_add_team_member(tmp_path):
    """Test adding a member generates the correct ID and saves to the JSON file."""
    test_json = tmp_path / "team_data.json"
    
    data = {"members": [{"id": 1, "forename": "John", "surname": "Doe", "team_founder": True}]}
    test_json.write_text(json.dumps(data), encoding="utf-8")
    
    new_member = add_team_member(str(test_json), "Alan", "Turing")
    
    assert new_member["id"] == 2 
    assert new_member["forename"] == "Alan"
    assert new_member["surname"] == "Turing"
    assert new_member["team_founder"] is False
    
   
    saved_data = json.loads(test_json.read_text(encoding="utf-8"))
    assert len(saved_data["members"]) == 2
    assert saved_data["members"][1]["forename"] == "Alan"
