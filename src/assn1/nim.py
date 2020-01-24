import numpy as np
import time
import matplotlib.pyplot as plt


class Nim:
	def __init__(self, n: int=1):
		self.n = n
		# cache that stores the time complexity associated with solving nim recursively
		self.win_time_cache = [0]
		# cache that stores a boolean of chance of winning at n stones
		self.win_cache = [True]
		self.update_n(n)

	def time_complex_dynamic(self, n: int=None):
		if n:
			self.n = n
			self.win_time_cache = [0] * (n + 1)

		self.win_time_cache[1] = 1

		for i in range(2, n+1):
			self.win_time_cache[i] = self.win_time_cache[i - 1] + self.win_time_cache[i - 2]

		return self.win_time_cache[self.n]

	def update_n(self, n: int):
		self.n = n
		self.win_time_cache = [0] * (n + 1)
		self.win_cache = [None] * (n + 1)

		# generates cache for win_dynamic
		self.win_cache[0] = True
		self.win_cache[1] = False

		for i in range(2, n + 1):
			self.win_cache[i] = not(self.win_cache[i - 1] and self.win_cache[i - 2])

	def time_complex_recur(self, n: int):
		if n <= 1:
			return n
		return self.time_complex_recur(n - 1) + self.time_complex_recur(n - 2)

	def win_recur(self, n: int):
		if n == 0:
			return True
		if n == 1:
			return False
		return not (self.win_recur(n - 1) and self.win_recur(n - 2))

	def win_dynamic(self, n: int):

		return self.win_cache[n]

	def nim_recur(self, n: int):
		if n == 0:
			return -1  # you win
		# if opponent can't win having one less stone, then take one
		if not(self.win_recur(n - 1)):
			return 1
		return 2

	def nim_dynamic(self, n: int):
		if n == 0:
			return -1  # you win
		# if opponent can't win having one less stone, then take one
		if not(self.win_dynamic(n - 1)):
			return 1
		return 2

	def is_winner(self):
		if self.n <= 0:
			return True
		else:
			return False

	def play(self, n: int, recur: bool=True):
		self.update_n(n)
		end = False
		print(f"There are {self.n} stones on the table. Computer goes first.")

		if recur:
			while not end:
				c = self.nim_recur(self.n)
				self.n -= c
				print(f"Computer took {c} stones. There are {self.n} stones left")
				if self.is_winner():
					print("you won")
					end = True
					break
				user = int(input("please enter the stones you want to take: \n"))
				self.n -= user
				print(f"User took {user} stones. There are {self.n} stones left")
				if self.is_winner():
					print("computer won")
					end = True
					break
		else:
			while not end:
				c = self.nim_dynamic(self.n)
				self.n -= c
				print(f"Computer took {c} stones. There are {self.n} stones left")
				if self.is_winner():
					print("you won")
					end = True
					break
				user = int(input("please enter the stones you want to take: \n"))
				self.n -= user
				print(f"User took {user} stones. There are {self.n} stones left")
				if self.is_winner():
					print("computer won")
					end = True
					break


nim = Nim(40)
# nim.play(4, False)

# creates the trendlines
x = np.arange(25, 40)
expected = np.array([np.power(1.618, i) for i in x])*.0000000008
best_fit = np.array([np.power(1.537, i) for i in x])*.0000000015
y = x.copy() * expected
y2 = x.copy() * best_fit
times = []

# runs recursive program and times each run
for i in range(25, 40):
	start = time.time()
	nim.nim_recur(i)
	end_time = time.time()
	times.append(end_time - start)

# creates graph with legend and log base y scale
print(times)
plt.plot(x, np.array(times), label='runtime of nim recursive')
plt.plot(x, y, label='1.618^n: expected')
plt.plot(x, y2, label='1.537^n: best fit')
plt.yscale("log")
plt.xlabel("n")
plt.ylabel("seconds (log)")
plt.title("log time complexity vs n for Nim")
plt.legend()
plt.show()

# shows the same results between recursive and dynamic programs
for i in range(30):
	print(f"i = {i}\t dynamic = {nim.win_cache[i]}\t  recursive = {nim.win_recur(i)}")


