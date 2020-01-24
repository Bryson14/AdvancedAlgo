
def can_fill_recur(sizes: list, k: int) -> bool:
	if k == 0:
		return True

	filled = False

	for i in range(len(sizes)):
		if sizes[i] > k:
			continue
		if can_fill_recur(sizes[:i] + sizes[i + 1:], k - sizes[i]):
			filled = True
			break

	return filled


a = [3, 8, 9, 84, 35, 10, 8, 8, 7]
for i in range(sum(a)):

	print(f' knapsack size : {i} | Can fill?: {can_fill_recur(a, i)} |')
