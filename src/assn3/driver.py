from MinEditDistance import med
import pathlib

# print(med('abc','abb'))

filename = 'commonly_misspelled_words.txt'
file = pathlib.Path.joinpath(pathlib.Path.cwd(), filename)

print(file)