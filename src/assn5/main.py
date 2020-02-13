from PolyM import *
import sys
import pathlib2 as path
import time
import matplotlib.pyplot as plt


# for smoother command line interface
def valid_input():
	user = '?'
	while user not in VALID_INPUT:
		for key in VALID_INPUT:
			print(f" | {key} : {VALID_INPUT[key][0]} |")
		user = input("-->").upper()
	return user


# gets n for the size of the polynomial
def get_n():
	try:
		n = '?'
		while not isinstance(n, int):
			n = int(input('Enter a n value between 1 and 30:  '))
		if 0 > n > 30:
			return get_n()

		return n

	except ValueError as e:
		return get_n()


# gets the coefficient for the manually made polynomials
def get_coefficient(poly_str: str ,x: int):
	try:
		n = '?'
		while not isinstance(n, float):
			n = float(input(f'Enter a coefficient value for {poly_str}{x}: '))
		return n

	except ValueError as e:
		return get_coefficient(poly_str ,x)


# creates a polynomial from the input of the user
def get_user_polynomial(poly_str: str, n: int):
	s = ''
	for i in range(2**n - 1, -1, -1):
		s += f"{poly_str}{i}x^{i} +"

	# removing the last + sign
	s = s[:-2]

	print(f'Following the model {s}, enter the coefficients...')
	arr = np.zeros(2**n, dtype=float)

	for i in range(2**n):
		arr[i] = get_coefficient(poly_str, i)
	return arr


# runs a comparision between the two algorithms' runtimes
def run_comparison():
	filename = path.Path.joinpath(path.Path.cwd(), 'results.txt')
	trial_sizes = []
	high_school_runtimes = []
	four_sub_algorithm_runtimes = []
	
	limit = 16
	# from assignment description, start at N=32 to as large as possible
	for n in range(3, limit):
		print(f"Starting run {n} of {limit - 1}")
		trial_sizes.append(2**n)
		create_problem_arrays(n)
	
		start = time.time()
		highschool = classic_foil()
		mid = time.time()
		better = four_sub_other()
		end = time.time()

		highschool_runtime = mid - start
		other_runtime = end - mid

		s = ''
		s += f"\n+++++Trial {n}+++++\n Time for High school Algorithm --> {highschool_runtime}\n"
		s += f"Time for the other Algorithm --> {other_runtime}\n"
		s += f"Do their outputs match? --> {highschool == better}\n"
		
		# changes very small run times for the sake of logarithmic plotting
		if highschool_runtime == 0.0:
			highschool_runtime += 0.0000001
		high_school_runtimes.append(highschool_runtime)
		if other_runtime == 0.0:
			other_runtime += 0.0000001
		four_sub_algorithm_runtimes.append(other_runtime)

		file = open(filename, 'a')
		file.write(s)
		file.close()
			
	plt.plot(np.array(trial_sizes), np.array(high_school_runtimes), label='High School')
	plt.plot(np.array(trial_sizes), np.array(four_sub_algorithm_runtimes), label='Other Algo')
	plt.title('Run times of High school FOILing with Other Algorithm vs Time \n(Base 2 Log Scale)')
	plt.xscale('log', basex=2)
	plt.yscale('log', basey=2)
	plt.xlabel('Size of Polynomials (Log Base 2)')
	plt.ylabel('Runtime in Log Time (Log Base 2)')
	plt.legend()
	plt.savefig(path.Path.joinpath(path.Path.cwd(), f'Graph(n={limit}).png'))
	plt.show()
		
		
VALID_INPUT = {
	'S': ['Study the time between high school algorithm and the other algorithm', run_comparison],
	'H': ['Foil two polynomials with the High School algorithm', classic_foil],
	'O': ['Foil two poynomials with the other algorithm', four_sub_other],
	'3': ['Foil two polynomials with the three sub algorithm', three_sub_other],
	'Q': ['Quit the program', sys.exit]
}


if __name__ == "__main__":
	key = valid_input()
	if key == 'Q':
		VALID_INPUT[key][1]()

	if key == 'S':
		VALID_INPUT[key][1]()
	else:	
		n = get_n()
		p1 = get_user_polynomial('P', n)
		p2 = get_user_polynomial('Q', n)

		print(run_manually(p1, p2, VALID_INPUT[key][1]))
