from input_utils import read_members

members = read_members('data/members.txt')

print("=== DREAM TEAM ===")

print("Members:")
for member in members:
	print("- " + member)


# Return the number of members in the team
def get_members_count():
	return len(read_members('data/members.txt'))

# Greet someone by their name
def greet(name):
    print(f"Hello, {name}!")

def display_as_json(data):
	import json
	print(json.dumps(data, indent=4))