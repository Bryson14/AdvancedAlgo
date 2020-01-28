import numpy as np
import time


# recursion is slow
def med(i, j):
	if i == 0:
		return j
	if j == 0:
		return i

	return min(med(i-1, j) + 1,
	           med(i, j-1) + 1,
	           med(i-1, j-1) + (A[i] != B[j]))


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


A = ' bbadsek813dsafadsfsafdsfbkdsfbdsfabcdefeghi159481'
B = ' bbcddlfhlaiufasdfasdfldsifelifesfsefue1fabcdefghi159159'


mid = time.time()
print(med_dp(len(A)-1, len(B)-1))
end = time.time()

print(f"string lengths {len(A) + len(B)} |  dp time = {end - mid}")
