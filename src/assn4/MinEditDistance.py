import numpy as np

# dynamic program is fast
def med_dp(i, j):
	# initialize cache with base case along axis
	c = np.zeros([i+1, j+1], dtype=int)
	for x in range(i+1):
		c[x, 0] = x
	for y in range(j+1):
		c[0, y] = y

	# fill in cache
	for x in range(1, i+1):
		for y in range(1, j+1):
			c[x, y] = min(c[x-1, y] + 1, c[x, y-1] + 1, c[x-1, y-1] + (A[x] != B[y]))

	# return answer
	return c[i, j]


def med(str_a, str_b):
	global A
	global B
	A = str_a
	B = str_b

	# the algorithm stops at index 0, so adding a space at the beginning of each string
	if not A.startswith(" "):
		A = " " + A
	if not B.startswith(" "):
		B = " " + B
	return med_dp(len(A) - 1, len(B) - 1)


A = ''
B = ''
