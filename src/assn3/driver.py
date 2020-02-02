from MinEditDistance import med
import pathlib
import matplotlib.pyplot as plt


filename = 'commonly_misspelled_words.txt'
file = pathlib.Path.joinpath(pathlib.Path.cwd(), filename)

with open(file, 'r') as data:
	lines = data.readlines()

n = 0
words_per_edits = {}

for line in lines:
	line = line.strip()
	s = line.split('->')
	a = s[1].split(',')

	for i in range(len(a)):
		m = med(s[0], a[i])
		n += 1

		if m in words_per_edits:
			words_per_edits[m] += 1
		else:
			words_per_edits[m] = 1


values = []
bins = []
for i in words_per_edits:
	values.append(words_per_edits[i])
	bins.append(i)

big = max(bins)
n_bigs = words_per_edits[big]
print(f"Execution over the database of {n} words")
print(f"largest edit distance is {big} with {n_bigs} occurances")
print(words_per_edits)

plt.bar(bins, values)
plt.show()