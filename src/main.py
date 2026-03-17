from team import get_members_count, load_team_members, print_team_members
from utils import greet, print_json


MEMBERS_FILE = "data/members.txt"


def main() -> None:
    """Run the application."""
    team_members = load_team_members(MEMBERS_FILE)

    print("=== DREAM TEAM ===")
    print_team_members(team_members)

    members_count = get_members_count(team_members)
    print(f"\nTotal members: {members_count}")

    greet("Team")

    team_data = {
        "team_name": "Dream Team",
        "members": team_members,
        "count": members_count,
    }
    print_json(team_data)


if __name__ == "__main__":
    main()