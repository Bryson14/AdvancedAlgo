import pathlib2 as path
from minEditDNA import med


neanderthal = 'neanderthal.txt'
prototypical_human = 'prototypical_human.txt'
great_apes = 'Great_Apes.txt'
human_diversity = 'human_diversity.txt'

DNA_SAMPLES = [neanderthal, prototypical_human, great_apes, human_diversity]


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


def run_comparisons():
	results_file = path.Path.joinpath(path.Path.cwd(), 'data', 'results.txt')

	for i in range(len(DNA_SAMPLES)):
		for j in range(i, len(DNA_SAMPLES)):

			result = med(read_dna(DNA_SAMPLES[i]), read_dna(DNA_SAMPLES[j]))

			with open(results_file, 'a') as file:
				file.write(f"{DNA_SAMPLES[i].split('.')[0].capitalize()} compared "
							f"with {DNA_SAMPLES[j].split('.')[0].capitalize()}\n\t {result}")



print(med('aaagcttttt','cgtacg'))
