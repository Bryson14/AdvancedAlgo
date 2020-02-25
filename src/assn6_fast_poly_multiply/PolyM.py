import numpy as np


Q = np.array([1, 2])
P = np.array([1, 2])


# returns an array of size 2**n which contains the coefficient for polynomials P and Q
def create_problem_arrays(n):
	if n > 28:
		print(f"Cannot create an array of size 2^n or length {2**n}")
	else:
		global Q, P
		size = np.power(2,n)
		Q = (np.random.random(size) - 0.5) * 2
		P = (np.random.random(size) - 0.5) * 2


# the classic high school foiling technique
def classic_foil():
	assert len(P) == len(Q)
	PQ = np.zeros(2*len(P), dtype=float)

	for i in range(len(P)):
		for j in range(len(Q)):
			PQ[i+j] += P[i] * Q[j]

	return PQ


# sets the global variables then runs the passed in function
def run_manually(p1, p2, function):
	global Q, P
	Q = p1
	P = p2

	if function == classic_foil:
		return function()
	return function(p1, p2, len(p1))


# for future use
def set_globals(p1, p2):
	global Q, P
	Q = p1
	P = p2


'''
Four Sub problem Foiling Algorithm
PQ = Pl*Ql + x^(n/2)*(Pl*Qh+Ph*Ql) + x^n * Ph*Qh
where Ql and Pl are the lower half of the polynomials
and Qh and Ph are the upper half of the polynomials
'''


# other algorithm, with 4 sub problems
def four_sub_other(p: np.array, q: np.array, n: int) -> np.array:
	PQ = np.zeros(2*n, dtype=float)

	if n == 1:
		PQ[0] = p[0]*q[0]
		return PQ

	PQ_ll = four_sub_other(p[:n//2], q[:n//2], n//2)
	PQ_hh = four_sub_other(p[n//2:], q[n//2:], n//2)
	PQ_lh = four_sub_other(p[:n//2], q[n//2:], n//2)
	PQ_hl = four_sub_other(p[n//2:], q[:n//2], n//2)

	PQ[:n] = PQ_ll
	PQ[-n:] = PQ_hh
	PQ[n // 2: n // 2 + n] += PQ_hl + PQ_lh

	return PQ


# faster version of the four sub with some tricky algebra
def three_sub_other(p: np.array, q: np.array, n: int) -> np.array:
	arr = np.zeros(2*n, dtype=float)

	# recursion base case
	if n == 1:
		arr[0] = p[0]*q[0]
		return arr

	# breaking the problem into sub problems. The big difference
	# from four_sub is that there are only three sub problem to
	# computes. Reduces time complexity from O(n^2) to O(n^1.5)
	pq_ll = three_sub_other(p[:n//2], q[:n//2], n//2)
	pq_hh = three_sub_other(p[n//2:], q[n//2:], n//2)

	# difference mid step
	p_mid = p[:n//2] + p[n//2:]
	q_mid = q[:n//2] + q[n//2:]
	pq_mid = three_sub_other(p_mid, q_mid, n//2)

	# solution construction step
	arr[:n] = pq_ll
	arr[-n:] = pq_hh
	arr[n // 2: n // 2 + n] += pq_mid - pq_hh - pq_ll

	return arr


# multiplies two arrays at polynomials
def poly_m(arr1, arr2):
	l1 = len(arr1)
	l2 = len(arr2)

	if l1 == 1 and l2 == 1:
		sol = np.zeros(1, dtype=float)
	elif l1 == 2 and l2 == 2:
		sol = np.zeros(3, dtype=float)
	else:
		sol = np.zeros(l1 - 1 + l2, dtype=float)

	for i in range(len(arr1)):
		for j in range(len(arr2)):
			sol[i+j] += arr1[i] * arr2[j]

	return sol


def run(func):
	return func(P, Q, P.size)
