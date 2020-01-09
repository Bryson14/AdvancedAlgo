def win(n):
	if n == 0:
		return True
	if n == 1:
		return False
	return not(win(n-1) and win(n-2))

def f(n):
	if n <= 1:
		return n
	return f(n-1) + f(n-2)

