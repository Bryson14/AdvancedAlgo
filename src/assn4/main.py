import pathlib2 as path
from minEditDNA import med
import sys


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
		for j in range(i+1, len(DNA_SAMPLES)):

			print(f"Starting comparision between {DNA_SAMPLES[i].split('.')[0].capitalize()} "
					f"and {DNA_SAMPLES[j].split('.')[0].capitalize()}")

			result = med(read_dna(DNA_SAMPLES[i]), read_dna(DNA_SAMPLES[j]))

			with open(results_file, 'a') as file:
				file.write(f"{DNA_SAMPLES[i].split('.')[0].capitalize()} compared "
							f"with {DNA_SAMPLES[j].split('.')[0].capitalize()}\n\t {result}")


def valid_input():
	user_input = '?'
	while user_input not in VALID_INPUT:
		print('Enter a valid command.')
		for option in VALID_INPUT:
			print(f" | {option} -- {VALID_INPUT[option][0]}")
		user_input = input('--> ').upper()
	return user_input


VALID_INPUT = {'C': ['Run a comparision between all the DNA', run_comparisons],
				'MED': ['Manually enter in two DNA sequences to score', med],
				'Q': ['Quit the program', sys.exit]}


if __name__ == "__main__":
	command = valid_input()

	if command == 'MED':
		seq1 = input('Enter DNA sequence 1: ').lower()
		seq2 = input('Enter DNA sequence 2: ').lower()
		print(VALID_INPUT[command][1](seq1, seq2))

	else:
		VALID_INPUT[command][1]()
