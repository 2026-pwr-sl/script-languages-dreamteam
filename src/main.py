"""
Application entry point.

This module parses command-line arguments and executes the requested
actions based on the provided options.
"""

import argparse

from team import get_members_count, load_team_members, print_team_members
from utils import greet


MEMBERS_FILE = "data/members.txt"


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    :return: Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Dream Team command-line application."
    )
    parser.add_argument(
        "--show-team",
        action="store_true",
        help="Display all team members.",
    )
    parser.add_argument(
        "--count",
        action="store_true",
        help="Display the number of team members.",
    )
    parser.add_argument(
        "--greet",
        metavar="NAME",
        help="Print a greeting for the given name.",
    )

    return parser.parse_args()


def main() -> None:
    """
    Run the application based on command-line arguments.
    """
    args = parse_arguments()

    needs_members = args.show_team or args.count
    team_members = load_team_members(MEMBERS_FILE) if needs_members else []

    if args.show_team:
        print("=== DREAM TEAM ===")
        print_team_members(team_members)

    if args.count:
        members_count = get_members_count(team_members)
        print(f"Total members: {members_count}")

    if args.greet:
        greet(args.greet)

    if not any([args.show_team, args.count, args.greet]):
        print("No arguments provided. Use --help to see available options.")


if __name__ == "__main__":
    main()