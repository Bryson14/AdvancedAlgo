import numpy as np


Q = np.array([1,2])
P = np.array([1,2])


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
	return function()

# for future use
def set_globals(p1, p2):
	global Q, P
	Q = p1
	P = p2


'''
Four Subproblem Foiling Algorithm
PQ = Pl*Ql + x^(n/2)*(Pl*Qh+Ph*Ql) + x^n * Ph*Qh
where Ql and Pl are the lower half of the polynomials
and Qh and Ph are the upper half of the polynomials
'''
# other algorithm, with 4 sub problems
def four_sub_other():
	PQ = np.zeros(2*len(P), dtype=float)
	print('PQ', PQ)
	print('P', P)
	print('Q', Q)

	# lows
	PQ[:len(PQ)//4] = P[:len(P)//2] * Q[:len(Q)//2]

	# highs
	PQ[3*len(PQ)//4 - 1: - 1] = P[len(P)//2:] * Q[len(Q)//2:]

	# mids
	PQ[len(PQ)//4:  3*len(PQ)//4 - 1] = P[len(P)//2:] * Q[:len(Q)//2] + P[:len(P)//2] * Q[len(Q)//2:]

	return PQ


# faster version of the four sub with some tricky algebra
def three_sub_other():
	pass
	

