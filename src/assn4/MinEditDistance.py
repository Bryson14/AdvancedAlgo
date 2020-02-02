import numpy as np


A = ''
B = ''


# dynamic program is fast
def med_dp(i, j):
	# initialize cache with base case along axis
	c = np.zeros([i+1, j+1], dtype=int)
	for x in range(i+1):
		c[x, 0] = x
	for y in range(j+1):
		c[0, y] = y

	# fill in cache
	try:
		for x in range(1, i+1):

			if x % 100 == 0:
				print(f"{x} of {i} done")
			for y in range(1, j+1):
				# deletion from A, insertion into A, substitution
				c[x, y] = max(c[x-1, y] + dna_scoring_dict[A[x]][''],
								c[x, y-1] + dna_scoring_dict[''][B[y]],
								c[x-1, y-1] + dna_scoring_dict[A[x]][B[y]])

	except KeyError as e:
		print('Sequence contains character other than a, g, c, t')
		print(e.__str__())

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


'''
Point system when substituting one nucleotide for another nucleotide. 
d represents a deletion from the sequence
	A  C  G  T  d
A   5 -1 -2 -1 -3
C  -1  5 -3 -2 -4
G  -2 -3  5 -2 -2
T  -1 -2 -2  5 -1
d  -3 -4 -2 -1  *
'''
dna_scoring_table = np.array([
	[5, -1, -2, -1, -3],
	[-1, 5, -3, -2, -4],
	[-2, -3, 5, -2, -2],
	[-1, -2, -2, 5, -1],
	[-3, -4, -2, -1, 0]
])
dna_scoring_dict = {'a': {'a': 5, 'c': -1, 'g': -2, 't': -1, '': -3},
					'c': {'a': -1, 'c': 5, 'g': -3, 't': -2, '': -4},
					'g': {'a': -2, 'c': -3, 'g': 5, 't': -2, '': -2},
					't': {'a': -1, 'c': -2, 'g': -2, 't': 5, '': -1},
					'': {'a': -3, 'c': -4, 'g': -2, 't': -1, '': 0}}

