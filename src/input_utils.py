def read_members(path):
	file = open(path, 'r')
	members = [line.strip() for line in file.readlines()]
	file.close()
	return members