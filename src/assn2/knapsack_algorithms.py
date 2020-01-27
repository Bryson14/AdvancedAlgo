import numpy as np
import time
from random import randint


def knapsack_hybrid(sizes: list, k: int) -> bool:
	if k == 0:
		return True

	filled = False

	for i in range(len(sizes)):
		if sizes[i] > k:
			continue
		if knapsack_hybrid(sizes[:i] + sizes[i + 1:], k - sizes[i]):
			filled = True
			break

	return filled


def problem_generator(n: int, ave_size: int):
	# sizes is how much space an objects takes up in the knapsack
	sizes = np.random.randint(1, ave_size * 2, n + 1, dtype=int)
	# values shows how much each objects is worth in $$ google-bucks $$
	values = np.random.randint(1, ave_size * 10, n + 1)*np.random.random(n+1)
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
	if i < 0:
		return 0.0

	return max(optimize_knaps(i - 1, k1 - S[i], k2) + V[i], optimize_knaps(i - 1, k1, k2 - S[i]) + V[i],
	           optimize_knaps(i - 1, k1, k2))


def optimize_memo_knaps(i, k1, k2)->float:
	if k1 < 0 or k2 < 0:
		return -1000000000000.0
	if i < 0:
		return 0.0

	into1 = optimize_knaps(i - 1, k1 - S[i], k2) + V[i]
	into2 = optimize_knaps(i - 1, k1, k2 - S[i]) + V[i]
	intoNone = optimize_knaps(i - 1, k1, k2)


def optimize_dp_knaps(i, k1, k2)->float:
	for n in range(1, i+1):
		for m in range(k1):
			for l in range(k2):
				C[n, m, n] = max(optimize_knaps(i - 1, k1 - S[i], k2) + V[i],
				                 optimize_knaps(i - 1, k1, k2 - S[i]) + V[i],
				                 optimize_knaps(i - 1, k1, k2))


def knapsack_dp(self, i, size):
	c = self.knapsack_cache(i, size)
	return c[i, size]


def knapsack_cache(i, size):
	cache = np.full([size+1, i], False, dtype=bool)
	for k in range(size + 1):
		cache[k, 0] = False
	for j in range(i):
		cache[0, j] = True

	for stone in range(1, i):
		for sub_size in range(1, size + 1):
			cache[sub_size, stone] = cache[sub_size - 1, stone] or cache[sub_size - 1, stone - S[stone]]

	return cache


def optimize_knapsacks_cache( n, k1, k2):
	C = np.zeros([N + 1, K1, K2], dtype=float)
	return C


def run_simple():
	global N
	global K
	global S
	global V
	N = valid_input('How many objects are there to choose from?')
	K = valid_input('How big is the knapsack? I suggest between 10 and 200.')
	ave_size = valid_input(f"Average size of the stones? I suggest around {int(K1/5)}")
	S, V = problem_generator(N, ave_size)
	return knapsack_bool(N, K1)


def run_double(func):
	global N
	global K1
	global K2
	global S
	global V
	N = valid_input('How many objects are there to choose from?')
	K1 = valid_input('How big is knapsack 1? I suggest between 10 and 200.')
	K2 = valid_input('How big is knapsack 2? I suggest between 10 and 200.')
	ave_size = valid_input(f"Average size of the stones? I suggest between {K1/2} and {K2/2}")
	S, V = problem_generator(N, ave_size)
	return func(N, K1, K2)


def run_memo_dp_comparision():
	global N
	global K1
	global K2
	N = valid_input('How many objects are there to choose from?')
	K1 = valid_input('How big is knapsack 1? I suggest between 10 and 200.')
	K2 = valid_input('How big is knapsack 2? I suggest between 10 and 200.')
	average_sizes = np.random.randint(10, 100, 10)
	with open('trials.txt', 'a') as file:
		file.write(f"N={N},K1={K1},K2={K2}\naverage Sizes={average_sizes}\n\n\n")

	for ave_size in average_sizes:
		with open('trials.txt', 'a') as file:
			file.write(f"starting new average size of {ave_size}\n\nTrial\t | memoizing time\t | dynamic program time")

		for trial in range(20):
			global S
			global V
			S, V = problem_generator(N, ave_size)

			start = time.time()
			optimize_memo_knaps(N+1, K1, K2)
			mid = time.time()
			optimize_dp_knaps(N+1, K1, K2)
			end = time.time()

			with open('trials.txt', 'a') as file:
				file.write(f"{trial+1}:\t  {mid - start}\t | {end-mid}\n")


def valid_input(message):
	print(message)
	try:
		response = int(input('-->\t'))
	except ValueError:
		print("Enter a valid integer.")
		return valid_input(message)
	return response


# i didn't want to deal with setting up a class, so i broke the golden CS rule!
# declaring global variables to random stuff
N = 5
K1 = 100
K2 = 100
K = 100
S = [1,2,3,4]
V = [1.2,5.2,2.3,5.8]
C = [[1.2,.2],[1.2,1.2]]

for _ in range(0, 100):
	S = [randint(1, K / 2) for _ in range(0, N + 1)]
	print(f"Set S if {S}. Size of sack is {K}")
	if knapsack_bool(N, K):
		print("Solution exists")
	else:
		print("Solution does not exist")

