import numpy as np
import time
import sys


class Knapsack:
	def __init__(self):
		self.N = 3
		self.K1 = 2
		self.K2 = 3
		self.S = []
		self.V = []
		self.C = [[]]


	def knapsack_hybrid(self, sizes: list, k: int) -> bool:
		if k == 0:
			return True

		filled = False

		for i in range(len(sizes)):
			if sizes[i] > k:
				continue
			if self.knapsack_hybrid(sizes[:i] + sizes[i + 1:], k - sizes[i]):
				filled = True
				break

		return filled

	def problem_generator(self, n: int, ave_size: int):
		# sizes is how much space an objects takes up in the knapsack
		sizes = np.random.randint(1, ave_size * 2, n + 1, dtype=int)
		# values shows how much each objects is worth in $$ google-bucks $$
		values = np.random.randint(1, ave_size * 10, n + 1)*np.random.random(n+1)
		return sizes, values

	def knapsack_bool(self, i, size):
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
		return self.knapsack_bool(i - 1, size - self.S[i]) or self.knapsack_bool(i - 1, size)

	def optimize_knaps(self, i, k1, k2)->float:
		if k1 < 0 or k2 < 0:
			return -1000000000000.0
		if i < 0:
			return 0.0

		return max(self.optimize_knaps(i - 1, k1 - self.S[i], k2) + self.V[i],
		           self.optimize_knaps(i - 1, k1, k2 - self.S[i]) + self.V[i],
		           self.optimize_knaps(i - 1, k1, k2))

	def optimize_memo_knaps(self, i, k1, k2)->float:
		if k1 < 0 or k2 < 0:
			return -1000000000000.0
		if i < 0:
			return 0.0

		into1 = self.optimize_knaps(i - 1, k1 - self.S[i], k2) + self.V[i]
		into2 = self.optimize_knaps(i - 1, k1, k2 - self.S[i]) + self.V[i]
		intoNone = self.optimize_knaps(i - 1, k1, k2)

	def optimize_dp_knaps(self, i, k1, k2)->float:
		for n in range(1, i+1):
			for m in range(k1):
				for l in range(k2):
					self.C[n, m, n] = max(self.optimize_knaps(i - 1, k1 - self.S[i], k2) + self.V[i],
					                 self.optimize_knaps(i - 1, k1, k2 - self.S[i]) + self.V[i],
					                 self.optimize_knaps(i - 1, k1, k2))

	def knapsack_dp(self, i, size):
		self.C = self.knapsack_cache(i, size)
		return self.C[i, size]

	def knapsack_cache(self, i, size):
		cache = np.full([size+1, i], False, dtype=bool)
		for k in range(size + 1):
			cache[k, 0] = False
		for j in range(i):
			cache[0, j] = True

		for stone in range(1, i):
			for sub_size in range(1, size + 1):
				cache[sub_size, stone] = cache[sub_size - 1, stone] or cache[sub_size - 1, stone - self.S[stone]]

		return cache

	def optimize_knapsacks_cache(self, n, k1, k2):
		self.C = np.zeros([self.N + 1, self.K1, self.K2], dtype=float)

	def run_simple(self):
		pass

	def run_double(self, func):
		N = self.valid_input('How many objects are there to choose from?')
		K1 = self.valid_input('How big is knapsack 1? I suggest between 10 and 200.')
		K2 = self.valid_input('How big is knapsack 2? I suggest between 10 and 200.')
		ave_size = self.valid_input(f"Average size of the stones? I suggest between {K1/2} and {K2/2}")
		self.S, self.V = self.problem_generator(N, ave_size)
		return func(N, K1, K2)

	def run_memo_dp_comparision(self):
		N = self.valid_input('How many objects are there to choose from?')
		K1 = self.valid_input('How big is knapsack 1? I suggest between 10 and 200.')
		K2 = self.valid_input('How big is knapsack 2? I suggest between 10 and 200.')
		average_sizes = np.random.randint(10, 100, 10)
		with open('trials.txt', 'a') as file:
			file.write(f"N={N},K1={K1},K2={K2}\naverage Sizes={average_sizes}\n\n\n")

		for ave_size in average_sizes:
			with open('trials.txt', 'a') as file:
				file.write(f"starting new average size of {ave_size}\n\nTrial\t | memoizing time\t | dynamic program time")

			for trial in range(20):
				self.S, self.V = self.problem_generator(N, ave_size)

				start = time.time()
				self.optimize_memo_knaps(N+1, K1, K2)
				mid = time.time()
				self.optimize_dp_knaps(N+1, K1, K2)
				end = time.time()

				with open('trials.txt', 'a') as file:
					file.write(f"{trial+1}:\t  {mid - start}\t | {end-mid}\n")

	def valid_input(self, message):
		print(message)
		try:
			response = input('-->\t')
			if response == 'q':
				sys.exit()
			response = int(input('-->\t'))
		except ValueError:
			print("Enter a valid integer.")
			return self.valid_input(message)
		return response

#
# ks = Knapsack()
# ks.run_memo_dp_comparision()


# S, V = problem_generator(N, 40)
# # double knapsack cache
# C = optimize_knapsacks_cache(N+1, K1, K2)
# print(C)
# print(f"S = {S}\nV = {V}")
# print(optimize_knaps(N, K1, K2))
# print(optimize_memo_knaps(N, K1, K2))

#
# for _ in range(0, 100):
# 	S = [randint(1, K / 2) for _ in range(0, N + 1)]
# 	print(f"Set S if {S}. Size of sack is {K}")
# 	if knapsack_bool(N, K):
# 		print("Solution exists")
# 	else:
# 		print("Solution does not exist")

