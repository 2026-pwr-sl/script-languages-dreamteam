import json
import pytest

from team import (
    TeamDataError,
    add_team_member,
    search_team_member,
    get_team_members_list,
)

def test_add_team_member_empty_names(tmp_path):
    """Test that adding a member with blank names raises a ValueError."""
    test_file = tmp_path / "team_data.json"
    test_file.write_text('{"members": []}', encoding="utf-8")
    
    
    with pytest.raises(ValueError, match="Forename and surname are required."):
        add_team_member(str(test_file), "   ", "Doe")
        
    
    with pytest.raises(ValueError, match="Forename and surname are required."):
        add_team_member(str(test_file), "John", "")

def test_search_team_member_empty_query(tmp_path):
    """Test that submitting an empty search query raises a ValueError."""
    test_file = tmp_path / "team_data.json"
    test_file.write_text('{"members": []}', encoding="utf-8")
    
    with pytest.raises(ValueError, match="Search query cannot be empty."):
        search_team_member(str(test_file), "   \n ")

def test_read_missing_file():
    """Test that attempting to read a non-existent file raises a TeamDataError."""
    with pytest.raises(TeamDataError, match="Team data file not found"):
        get_team_members_list("this_file_does_not_exist.json")

def test_read_invalid_json(tmp_path):
    """Test that reading a corrupted/malformed JSON file raises a TeamDataError."""
    test_file = tmp_path / "corrupted_data.json"
    
    test_file.write_text("{bad_json: missing_quotes}", encoding="utf-8")
    
    with pytest.raises(TeamDataError, match="Team data file is not a valid JSON document."):
        get_team_members_list(str(test_file))

def test_invalid_members_format(tmp_path):
    """Test that if the JSON payload is missing the list structure, it raises a TeamDataError."""
    test_file = tmp_path / "wrong_format.json"
    
    test_file.write_text('{"members": "This should be a list, not a string"}', encoding="utf-8")
    
    with pytest.raises(TeamDataError, match="Invalid team data: 'members' must be a list."):
        get_team_members_list(str(test_file))