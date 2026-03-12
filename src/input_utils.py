def read_members(path):
	file = open(path, 'r', encoding='utf-8')
	members = [line.strip() for line in file.readlines()]
	file.close()
	return members