from input_utils import read_members

members = read_members('data/members.txt')

print("=== DREAM TEAM ===")

print("Members:")
for member in members:
	print("- " + member)