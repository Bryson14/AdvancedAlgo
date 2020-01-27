from knapsack_algorithms import *
import sys


VALID_INPUT = {
	'R': ['run the knapsack algo', run_simple],
	'D': ['run the double knapsack algo', run_double, optimize_knaps],
	'DD': ['run the double knapsack dynamic algo', run_double, optimize_dp_knaps],
	'DM': ['run the double knapsack memoizing algo', run_double, optimize_memo_knaps],
	'C': ['compare the time complexity of the different algos', run_memo_dp_comparision],
	'Q': ['quit the program', sys.exit]
}


def valid_input():
	user = '?'
	while user not in VALID_INPUT:
		print('Enter a command for the program')
		for algo in VALID_INPUT:
			print(f"| {algo} : {VALID_INPUT[algo][0]} |")
		user = input('-->').upper()

	return VALID_INPUT[user]


if __name__ == '__main__':
	print('hello world')
	user = valid_input()

	if len(user) == 3:
		# runs the different double knapsack algorithms
		print(user[1](user[2]))

	else:
		print(user[1]())
