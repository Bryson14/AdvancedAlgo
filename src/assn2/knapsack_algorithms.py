import numpy as np


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

	# # optimize putting stone in either knapsack1, knapsack2, no throwing it away
	# if k1 - S[i] < 0:
	# 	if k2 - S[i] < 0:
	# 		# both can't fit stone i
	# 		return optimize_knaps(i-1, k1, k2)
	# 	else:
	# 		# k1 can't fit stone i
	# 		return max(optimize_knaps(i - 1, k1, k2 - S[i]) + V[i], optimize_knaps(i - 1, k1, k2))
	# elif k2 - S[i] < 0:
	# 	# k2 can't fit stone i
	# 	return max(optimize_knaps(i - 1, k1 - S[i], k2) + V[i], optimize_knaps(i - 1, k1, k2))
	# # they both can fit stone i
	#


def knapsack_dp(i, size):
	pass


def make_cache(i, size):
	cache = np.full([size+1, i], None, dtype=bool)
	for k in range(size + 1):
		cache[k, 0] = False
	for j in range(i):
		cache[0, j] = True

	for stone in range(1, i):
		for sub_size in range(1, size + 1):
			cache[sub_size, stone] = cache[sub_size - 1, stone] or cache[sub_size - 1, stone - S[stone]]

	return cache



N = 3
K1 = 40
K2 = 30


S, V = problem_generator(N, 40)
print(f"S = {S}\nV = {V}")
print(optimize_knaps(N, K1, K2))

#
# for _ in range(0, 100):
# 	S = [randint(1, K / 2) for _ in range(0, N + 1)]
# 	print(f"Set S if {S}. Size of sack is {K}")
# 	if knapsack_bool(N, K):
# 		print("Solution exists")
# 	else:
# 		print("Solution does not exist")

