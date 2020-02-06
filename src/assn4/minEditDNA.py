import numpy as np


A = ''
B = ''


# dynamic program is fast
def med_dp(i, j, return_cache=False):
	try:
		# initialize cache with base case along axis
		c = np.zeros([i+1, j+1], dtype=int)
		for x in range(1, i+1):
			offset = DNA_SCORING_DICT[''][A[x]]
			c[x, 0] = c[x - 1, 0] + offset
		for y in range(1, j+1):
			offset = DNA_SCORING_DICT[''][B[y]]
			c[0, y] = c[0, y - 1] + offset

		# fill in cache

		for x in range(1, i+1):

			# to track progress on large files
			if x % 100 == 0:
				print(f"{x} of {i} done")

			for y in range(1, j+1):
				# deletion from A, insertion into A, substitution
				c[x, y] = max(
					c[x-1, y] + DNA_SCORING_DICT[''][A[x]],
					c[x, y-1] + DNA_SCORING_DICT[B[y]][''],
					c[x-1, y-1] + DNA_SCORING_DICT[A[x]][B[y]]
				)

	except KeyError as e:
		print('Sequence contains character other than a, g, c, t')
		print(e.__str__())

	# return answer
	if not return_cache:
		return c[i, j]
	else:
		return c


# helper function for med_dp
def med(str_a, str_b, show_diagram=False):
	global A
	global B
	A = str_a
	B = str_b

	# the algorithm stops at index 0, so adding a space at the beginning of each string
	if not A.startswith(" "):
		A = " " + A
	if not B.startswith(" "):
		B = " " + B

	# returns a diagram of the best alignment of the two strings
	if show_diagram:
		c = med_dp(len(A) - 1, len(B) - 1, show_diagram)
		s = ''
		s += str(c[len(A) - 1, len(B) - 1]) + '\n'
		s += show_alignment(len(A) - 1, len(B) - 1, c)
		return s

	else:
		return med_dp(len(A) - 1, len(B) - 1)


# back-solves from the cache to show an alignment diagram
def show_alignment(i, j, c, filename=None):
	x = 0
	y = 0
	print(f"->{A}<-")
	print(f"->{B}<-")
	x_temp = -10
	y_temp = -10
	s = ''
	while x != i or y != j:
		# comparision and follow greatest path

		# substitution
		try:
			sub = c[x+1][y+1]
		except IndexError:
			sub = -10000000

		# deletion
		try:
			delete = c[x + 1][y]
		except IndexError:
			delete = -10000000

		# insertion
		try:
			insert = c[x][y + 1]
		except IndexError:
			insert = -10000000

		# find the correct x,y step
		m = max(sub, insert, delete)
		if sub == m:
			x_temp = x + 1
			y_temp = y + 1
		elif insert == m:
			y_temp = y + 1
		else:
			x_temp = x + 1

		if x_temp - 1 == x and y_temp - 1 == y:  # substitution
			x += 1
			y += 1
			if A[x] == B[y]:
				s += f"{A[x]} = {B[y]}\n"
			else:
				s += f"{A[x]} -> {B[y]}\n"
		elif x_temp - 1 == x:  # deletion from A
			x += 1
			s += f"{A[x]} -> _\n"
		else:  # insertion from A
			y += 1
			s += f"_ -> {B[y]}\n"

	if filename is not None:
		with open(filename, 'a') as file:
			file.write("\n")
			file.write(s)
	else:
		return s


def save_traceback(str_a, str_b, filename):
	global A
	global B
	A = str_a
	B = str_b

	# the algorithm stops at index 0, so adding a space at the beginning of each string
	if not A.startswith(" "):
		A = " " + A
	if not B.startswith(" "):
		B = " " + B

	# returns a diagram of the best alignment of the two strings
	c = med_dp(len(A) - 1, len(B) - 1, True)
	s = '\n Score = '
	s += str(c[len(A) - 1, len(B) - 1]) + '\n' + 30 * '+'

	# writing score
	with open(filename, 'w+') as file:
		file.write(s)

	show_alignment(len(A) - 1, len(B) - 1, c, filename)


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
DNA_SCORING_DICT = {
	'a': {'a': 5, 'c': -1, 'g': -2, 't': -1, '': -3},
	'c': {'a': -1, 'c': 5, 'g': -3, 't': -2, '': -4},
	'g': {'a': -2, 'c': -3, 'g': 5, 't': -2, '': -2},
	't': {'a': -1, 'c': -2, 'g': -2, 't': 5, '': -1},
	'': {'a': -3, 'c': -4, 'g': -2, 't': -1, '': 0}
}