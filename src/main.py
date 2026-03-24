"""
Application entry point.

This module parses command-line arguments and executes the requested
actions based on the provided options.
"""

import argparse

from team import (
    TeamDataError,
    add_team_member,
    get_team_members_list,
    search_team_member,
    export_team_data,
)
from utils import greet


TEAM_DATA_FILE = "data/team_data.json"


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    :return: Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Dream Team command-line application."
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
    parser.add_argument(
        "--add-member",
        action="store_true",
        help="Add a new member to the team JSON.",
    )
    parser.add_argument(
        "--search-member",
        metavar="QUERY",
        help="Search member in team JSON by forename or surname.",
    )
    parser.add_argument(
        "--display-list",
        action="store_true",
        help="Display the member list from team JSON.",
    )
    parser.add_argument(
        "--export-data",
        metavar="FILE_PATH",
        help="Export team data to a specified file.",
    )
    return parser.parse_args()


def main() -> None:
    """
    Run the application based on command-line arguments.
    """
    args = parse_arguments()

    if args.count:
        try:
            members = get_team_members_list(TEAM_DATA_FILE)
            print(f"Total members: {len(members)}")
        except TeamDataError as error:
            print(f"Could not count members: {error}")

    if args.greet:
        greet(args.greet)

    if args.add_member:
        try:
            forename = input("Forename: ").strip()
            surname = input("Surname: ").strip()
            new_member = add_team_member(TEAM_DATA_FILE, forename, surname)
            print(
                "Added member: "
                f"{new_member['forename']} {new_member['surname']} "
                f"(id={new_member['id']})"
            )
        except EOFError:
            print("Input was interrupted. Member was not added.")
        except KeyboardInterrupt:
            print("Operation cancelled by user.")
        except ValueError as error:
            print(f"Could not add member: {error}")
        except TeamDataError as error:
            print(f"Could not add member: {error}")

    if args.search_member:
        try:
            matches = search_team_member(TEAM_DATA_FILE, args.search_member)
            if not matches:
                print("No matching members found.")
            else:
                print(f"Found {len(matches)} member(s):")
                for member in matches:
                    print(
                        f"- [{member.get('id', '?')}] "
                        f"{member.get('forename', '')} "
                        f"{member.get('surname', '')}"
                    )
        except ValueError as error:
            print(f"Could not search members: {error}")
        except TeamDataError as error:
            print(f"Could not search members: {error}")

    if args.display_list:
        try:
            members = get_team_members_list(TEAM_DATA_FILE)
            if not members:
                print("No members found.")
            else:
                print("=== TEAM MEMBERS (JSON) ===")
                for member in members:
                    founder_tag = ""
                    if member.get("team_founder"):
                        founder_tag = " (founder)"
                    print(
                        f"- [{member.get('id', '?')}] "
                        f"{member.get('forename', '')} "
                        f"{member.get('surname', '')}{founder_tag}"
                    )
        except TeamDataError as error:
            print(f"Could not display members: {error}")

    if args.export_data:
        try:
            export_team_data(args.export_data, TEAM_DATA_FILE)
            print(f"Team data exported to: {args.export_data}")
        except TeamDataError as error:
            print(error)

    if not any(
        [
            args.count,
            args.greet,
            args.add_member,
            args.search_member,
            args.display_list,
            args.export_data,
        ]
    ):
        print("No arguments provided. Use --help to see available options.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Operation cancelled by user.")
