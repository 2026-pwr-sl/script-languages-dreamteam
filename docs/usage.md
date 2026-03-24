# Tools Usage

```bash
python src/main.py [OPTIONS]
```

### Options

| Option                  | Description                                |
| ----------------------- | ------------------------------------------ |
| `--count`               | Display the total number of team members   |
| `--greet NAME`          | Print a greeting for the given name        |
| `--add-member`          | Interactively add a new member to the team |
| `--search-member QUERY` | Search for a member by forename or surname |
| `--display-list`        | Display all team members                   |

### Examples

```bash
# Count members
python main.py --count

# Greet someone
python main.py --greet Alice

# Add a new member (interactive prompt)
python main.py --add-member

# Search for a member
python main.py --search-member "Smith"

# List all members
python main.py --display-list
```
