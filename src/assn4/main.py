import pathlib2 as path

neanderthal = 'neanderthal.txt'
prototypical_human = 'prototypical_human.txt'


def read_dna(filename: str)->str:
	with open(path.Path.joinpath(path.Path.cwd(), 'data', filename)) as data:
		dna = data.read()

	return dna.strip('\n')


print(read_dna(prototypical_human))
