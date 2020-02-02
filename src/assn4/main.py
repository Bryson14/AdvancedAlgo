import pathlib2 as path
from MinEditDistance import med


neanderthal = 'neanderthal.txt'
prototypical_human = 'prototypical_human.txt'
great_apes = 'Great_Apes.txt'
human_diversity = 'human_diversity.txt'


def read_dna(filename: str)->str:
	with open(path.Path.joinpath(path.Path.cwd(), 'data', filename)) as data:
		dna = data.read()

	return dna.strip('\n')


def clean_data(to_file: str, from_file:str ='new.txt'):
	reciever = open(path.Path.joinpath(path.Path.cwd(), 'data', to_file), 'w+')
	with open(path.Path.joinpath(path.Path.cwd(), 'data', from_file), 'r') as sender:

		lines = sender.readlines()
		s = ''
		for line in lines:
			broken = line.strip().split()
			for chunk in broken[1:]:
				s += chunk

		reciever.write(s)
		reciever.close()


apes = read_dna(great_apes)
hm = read_dna(human_diversity)
print(med(apes, hm))
