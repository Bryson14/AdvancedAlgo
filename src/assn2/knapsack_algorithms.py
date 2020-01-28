import numpy as np
import time


def problem_generator(n: int, ave_size: int):
	# sizes is how much space an objects takes up in the knapsack
	sizes = np.random.randint(1, ave_size * 2, n + 1, dtype=int)
	# values shows how much each objects is worth in $$ google-bucks $$
	values = np.random.randint(1, ave_size * 2, n + 1)*np.random.random(n+1)
	# making index 0 of both arrays useless
	values[0] = 0.0
	sizes[0] = 0
	return sizes, values


def knapsack_bool(i, size):
	# if the size of the knapsack has been filled
	if size == 0:
		return True
	# if the knapsack cannot be filled exactly
	if size < 0:
		return False
	# if the available stones to use has run out
	if i <= 0:
		return False
	# try skipping/ reducing the size of the knapsack with the next stone
	return knapsack_bool(i - 1, size - S[i]) or knapsack_bool(i - 1, size)


def optimize_knaps(i, k1, k2)->float:
	if k1 < 0 or k2 < 0:
		return -1000000000000.0
	if i <= 0:
		return 0.0

	return max(optimize_knaps(i - 1, k1 - S[i], k2) + V[i], optimize_knaps(i - 1, k1, k2 - S[i]) + V[i],
			   optimize_knaps(i - 1, k1, k2))


def optimize_memo_knaps(i, k1, k2)->float:
	if k1 < 0 or k2 < 0:
		return -1000000000000.0
	if i <= 0:
		return 0.0

	# if answer is already calculated, return that
	if Done[i][k1][k2]:
		return C[i][k1][k2]

	else:

		# solve a unique problem then return it after saving
		C[i][k1][k2] = max(optimize_memo_knaps(i - 1, k1 - S[i], k2) + V[i],
		                   optimize_memo_knaps(i - 1, k1, k2 - S[i]) + V[i],
		                   optimize_memo_knaps(i - 1, k1, k2))
		Done[i][k1][k2] = True
		return C[i][k1][k2]



# TODO don't know what to do for this
def optimize_dp_knaps(i, k1, k2)->float:
	for n in range(1, i+1):
		for m in range(1, k1+1):
			for l in range(1, k2+1):

				# catches indexes less than zero
				if m - S[n] < 0:
					add_one = -1000000000
				else:
					add_one = C[n - 1][m - S[n]][l] + V[n]
				if l - S[n] < 0:
					add_two = -1000000000
				else:
					add_two = C[n - 1][m][l - S[n]] + V[n]

				add_none = C[n - 1][m][l]

				C[n][m][l] = max(add_one, add_two, add_none)

	print(C)

	return np.max(C)


# TODO Write a dp for the simple knapsack problem


def optimize_knapsacks_cache(n, k1, k2):
	return np.zeros([n + 1, k1+1, k2+1], dtype=float)


def run_simple():
	global N
	global K
	global S
	global V
	N = valid_int('How many objects are there to choose from?')
	K = valid_int('How big is the knapsack? I suggest between 10 and 200.')
	ave_size = valid_int(f"Average size of the stones? I suggest around {int(K1/5)}")
	S, V = problem_generator(N, ave_size)
	print(f"Set S if {S}. Size of sack is {K}")
	return knapsack_bool(N, K1)


def run_double(func):
	global N
	global K1
	global K2
	global S
	global V
	global C
	global Done
	N = valid_int('How many objects are there to choose from?')
	K1 = valid_int('How big is knapsack 1? I suggest between 10 and 200.')
	K2 = valid_int('How big is knapsack 2? I suggest between 10 and 200.')
	ave_size = valid_int(f"Average size of the stones? I suggest between {K1/2} and {K2/2}")
	S, V = problem_generator(N, ave_size)
	Done = np.full([N + 1, K1 + 1, K2 + 1], False)
	print(f"Set S if {S}. Values inside the sack is {V}")
	print(f"Best value able to be carried with knapsacks of size {K1} and {K2} is...")
	C = optimize_knapsacks_cache(N, K1, K2)
	return func(N, K1, K2)


def run_memo_dp_comparision():
	global N
	global K1
	global K2
	global Done
	N = valid_int('How many objects are there to choose from?')
	K1 = valid_int('How big is knapsack 1? I suggest between 10 and 200.')
	K2 = valid_int('How big is knapsack 2? I suggest between 10 and 200.')
	average_sizes = np.random.randint(5, 120, 10)
	with open('trials.txt', 'a') as file:
		file.write(f"N={N},K1={K1},K2={K2}\naverage Sizes={average_sizes}\n\n\n")

	for ave_size in average_sizes:
		i = 1
		total_dp_time = 0.0
		total_memo_time = 0.0
		with open('trials.txt', 'a') as file:
			file.write("-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\n")
			file.write(f"starting new average size of {ave_size}\n\n Trial\t | memoizing time\t "
			           f"| dynamic program time\t | answers match\n")

		for trial in range(20):
			global S
			global V
			global C
			S, V = problem_generator(N, ave_size)
			Done = np.full([N + 1, K1 + 1, K2 + 1], False)
			C = optimize_knapsacks_cache(N, K1, K2)

			# test memoizing
			start = time.time()
			memo = optimize_memo_knaps(N, K1, K2)
			mid = time.time()

			# reset cache
			C = optimize_knapsacks_cache(N, K1, K2)

			# test dynamic program
			mid2 = time.time()
			dp = optimize_dp_knaps(N, K1, K2)
			end = time.time()

			# to keep track of average times
			total_dp_time += end - mid2
			total_memo_time += mid - start

			with open('trials.txt', 'a') as file:
				file.write(f"{trial+1}:\t  {mid - start}\t | {end-mid2}\t | {memo==dp} {memo}  {dp}\n")
			i += 1

		with open('trials.txt', 'a') as file:
			file.write(f'\nAverage time for ave_size= {ave_size}. Memo= {total_memo_time/i}. DP = {total_dp_time/i}.\n')


def valid_int(message):
	print(message)
	try:
		response = int(input('-->\t'))
	except ValueError:
		print("Enter a valid integer.")
		return valid_int(message)
	return response


# i didn't want to deal with setting up a class, so i broke the golden CS rule!
# declaring global variables to random stuff
N = 5
K1 = 100
K2 = 100
K = 100
S = [1, 2]
V = [1.1, 1.2]
C = [[1.2], [1.1]]
Done = [True]
