"""
Team-related operations.
"""

import json
from typing import Any, List

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


def add_team_member(json_file_path: str, forename: str, surname: str) -> dict:
    """
    Add a new member to the team JSON file.

    :param json_file_path: Path to team JSON file.
    :param forename: Member forename.
    :param surname: Member surname.
    :return: Created member object.
    """
    cleaned_forename = forename.strip()
    cleaned_surname = surname.strip()
    if not cleaned_forename or not cleaned_surname:
        raise ValueError("Forename and surname are required.")

    team_data = _read_team_data(json_file_path)
    members = _get_members_list(team_data)
    next_id = max((member.get("id", 0) for member in members), default=0) + 1

    new_member = {
        "id": next_id,
        "forename": cleaned_forename,
        "surname": cleaned_surname,
        "team_founder": False,
    }

    members.append(new_member)
    team_data["members"] = members
    _write_team_data(json_file_path, team_data)
    return new_member


def get_team_members_list(json_file_path: str) -> List[dict[str, Any]]:
    """
    Get all members from the team JSON file.

    :param json_file_path: Path to team JSON file.
    :return: Members list.
    """
    team_data = _read_team_data(json_file_path)
    return _get_members_list(team_data)


def search_team_member(json_file_path: str, query: str) -> List[dict[str, Any]]:
    """
    Search for team members in the JSON file.

    :param json_file_path: Path to team JSON file.
    :param query: Search text.
    :return: Matching members.
    """
    normalized_query = query.strip().lower()
    if not normalized_query:
        return []

    members = get_team_members_list(json_file_path)
    matching_members: List[dict[str, Any]] = []

    for member in members:
        forename = str(member.get("forename", "")).strip()
        surname = str(member.get("surname", "")).strip()
        full_name = f"{forename} {surname}".strip().lower()

        if (
            normalized_query in full_name
            or normalized_query in forename.lower()
            or normalized_query in surname.lower()
        ):
            matching_members.append(member)

    return matching_members


def _read_team_data(json_file_path: str) -> dict[str, Any]:
    """
    Read and return the full team JSON payload.
    """
    with open(json_file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def _write_team_data(json_file_path: str, team_data: dict[str, Any]) -> None:
    """
    Persist team JSON payload to disk.
    """
    with open(json_file_path, "w", encoding="utf-8") as file:
        json.dump(team_data, file, indent=2, ensure_ascii=False)
        file.write("\n")


def _get_members_list(team_data: dict[str, Any]) -> List[dict[str, Any]]:
    """
    Extract members list from team data with a safe default.
    """
    members = team_data.get("members", [])
    return members if isinstance(members, list) else []