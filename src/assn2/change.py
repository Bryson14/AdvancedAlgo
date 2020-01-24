def change_recursive(coins, n):
	if n == 0:
		return 0
	if n < 0:
		return 123456789987654321
	# infinity
	return min([change_recursive(coins, n - coins[i]) for i in range(len(coins))]) + 1


def largest_coin(n):
	if n >= 26:
		return 26
	elif n >= 13:
		return 13
	elif n >= 7:
		return 7
	else:
		return 1


# counts the number of calls that change_recursive will make
def recursive_calls(n: int):
	if n <= 0:
		return 1
	return 4 * recursive_calls(n - 1)


coins = [1, 7, 13, 26]
print(change_recursive(coins, 21))
