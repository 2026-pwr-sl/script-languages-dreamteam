"""
Team-related operations.
"""

from typing import List

from utils import read_members


def load_team_members(file_path: str) -> List[str]:
    """
    Load team members from a file.
    """
    return read_members(file_path)


def print_team_members(members: List[str]) -> None:
    """
    Print all team members.
    """
    print("Members:")
    for member in members:
        print(f"- {member}")


def get_members_count(members: List[str]) -> int:
    """
    Return number of team members.
    """
    return len(members)