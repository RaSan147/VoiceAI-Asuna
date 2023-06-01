D = set()

with open("./Asuna_data/server/unknown query.txt", "r") as f:
	for line in f.readlines():
		D.add(line)

with open("./Asuna_data/server/unknown query.txt", "w") as f:
	D = sorted(list(D))
	for line in D:
		f.write(line)