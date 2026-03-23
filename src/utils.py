"""
Utility/helper functions.

Contains reusable functions for:
- file input,
- formatting,
- general-purpose helpers.
"""

import json
from typing import Any


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
