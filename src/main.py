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
    get_members_count,
    load_team_members,
    print_team_members,
    search_team_member,
)
from utils import greet


MEMBERS_FILE = "data/members.txt"
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
        "--show-team",
        action="store_true",
        help="Display all team members. (Reads from members.txt file)",
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
    return parser.parse_args()


def main() -> None:
    """
    Run the application based on command-line arguments.
    """
    args = parse_arguments()

    needs_members = args.show_team or args.count
    team_members = []
    if needs_members:
        try:
            team_members = load_team_members(MEMBERS_FILE)
        except FileNotFoundError:
            print(f"Could not open members file: {MEMBERS_FILE}.")
        except OSError:
            print("Could not read members file due to a system error.")

    if args.show_team:
        print("=== DREAM TEAM ===")
        print_team_members(team_members)

    if args.count:
        members_count = get_members_count(team_members)
        print(f"Total members: {members_count}")

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
                        f"{member.get('forename', '')} {member.get('surname', '')}"
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
                    founder_tag = " (founder)" if member.get("team_founder") else ""
                    print(
                        f"- [{member.get('id', '?')}] "
                        f"{member.get('forename', '')} {member.get('surname', '')}{founder_tag}"
                    )
        except TeamDataError as error:
            print(f"Could not display members: {error}")

    if not any(
        [
            args.show_team,
            args.count,
            args.greet,
            args.add_member,
            args.search_member,
            args.display_list,
        ]
    ):
        print("No arguments provided. Use --help to see available options.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Operation cancelled by user.")