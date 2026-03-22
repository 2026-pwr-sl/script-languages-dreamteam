"""
Utility/helper functions.

Contains reusable functions for:
- file input,
- formatting,
- general-purpose helpers.
"""

import json
from typing import Any, List


def read_members(file_path: str) -> List[str]:
    """
    Read team members from a text file.

    Each non-empty line represents one member.

    :param file_path: Path to the input file.
    :return: List of member names.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def greet(name: str) -> None:
    """
    Print a greeting message.

    :param name: Name of the person to greet.
    """
    print(f"Hello, {name}!")


def print_json(data: Any) -> None:
    """
    Pretty-print data as JSON.

    :param data: Data to be printed in JSON format.
    """
    print(json.dumps(data, indent=4))