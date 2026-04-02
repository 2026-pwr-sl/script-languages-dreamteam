"""
Team-related operations.
"""

import logging
import json
from typing import Any, List

logger = logging.getLogger()

class TeamDataError(Exception):
    """
    Raised when team JSON data cannot be read, validated, or written.
    """


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
    logger.debug(f"Cleaned forename: '{cleaned_forename}', surname: '{cleaned_surname}'")
    
    if not cleaned_forename or not cleaned_surname:
        raise ValueError("Forename and surname are required.")

    team_data = _read_team_data(json_file_path)
    members = _get_members_list(team_data)
    next_id = max((member.get("id", 0) for member in members), default=0) + 1
    logger.debug(f"Next member ID: {next_id}")

    new_member = {
        "id": next_id,
        "forename": cleaned_forename,
        "surname": cleaned_surname,
        "team_founder": False,
    }

    members.append(new_member)
    team_data["members"] = members
    _write_team_data(json_file_path, team_data)
    logger.debug(f"Team data updated with new member: {new_member}")
    return new_member


def get_team_members_list(json_file_path: str) -> List[dict[str, Any]]:
    """
    Get all members from the team JSON file.

    :param json_file_path: Path to team JSON file.
    :return: Members list.
    """
    team_data = _read_team_data(json_file_path)
    logger.debug(f"Team data read successfully from {json_file_path}")
    return _get_members_list(team_data)


def search_team_member(
    json_file_path: str,
    query: str,
) -> List[dict[str, Any]]:
    """
    Search for team members in the JSON file.

    :param json_file_path: Path to team JSON file.
    :param query: Search text.
    :return: Matching members.
    """
    normalized_query = query.strip().lower()

    if not normalized_query:
        raise ValueError("Search query cannot be empty.")

    members = get_team_members_list(json_file_path)
    matching_members: List[dict[str, Any]] = []

    logger.debug(f"Searching through {len(members)} members for query: '{normalized_query}'")

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

    logger.debug(f"Member search results: {matching_members}")
    
    return matching_members


def export_team_data(export_path: str, json_file_path: str) -> None:
    """
    Export team data to a JSON file.

    :param export_path: Path to which export the JSON file.
    :param json_file_path: Path to the source JSON file.
    """
    try:
        team_data = _read_team_data(json_file_path)
        with open(export_path, "w+", encoding="utf-8") as file:
            json.dump(team_data, file, indent=2, ensure_ascii=False)
            file.write("\n")
    except FileNotFoundError as error:
        raise TeamDataError(f"Can't find path: {export_path}.") from error
    except PermissionError as error:
        raise TeamDataError(
            f"Permission denied for path: {export_path}."
        ) from error
    except OSError as error:
        raise TeamDataError(
            f"Could not write to path: {export_path}."
        ) from error
    
    logger.debug(f"Team data exported successfully to {export_path}")


def _read_team_data(json_file_path: str) -> dict[str, Any]:
    """
    Read and return the full team JSON payload.
    """
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            team_data = json.load(file)
    except FileNotFoundError as error:
        raise TeamDataError(
            f"Team data file not found: {json_file_path}."
        ) from error
    except json.JSONDecodeError as error:
        raise TeamDataError(
            "Team data file is not a valid JSON document."
        ) from error
    except OSError as error:
        raise TeamDataError("Could not read team data file.") from error

    if not isinstance(team_data, dict):
        raise TeamDataError("Team data format is invalid.")

    return team_data


def _write_team_data(json_file_path: str, team_data: dict[str, Any]) -> None:
    """
    Persist team JSON payload to disk.
    """
    try:
        with open(json_file_path, "w", encoding="utf-8") as file:
            json.dump(team_data, file, indent=2, ensure_ascii=False)
            file.write("\n")
    except OSError as error:
        raise TeamDataError("Could not save team data file.") from error
    
    logger.debug(f"Team data written successfully to {json_file_path}")


def _get_members_list(team_data: dict[str, Any]) -> List[dict[str, Any]]:
    """
    Extract members list from team data with a safe default.
    """
    members = team_data.get("members", [])
    if not isinstance(members, list):
        raise TeamDataError("Invalid team data: 'members' must be a list.")

    logger.debug(f"Extracted members list with {len(members)} items.")
    
    return members
