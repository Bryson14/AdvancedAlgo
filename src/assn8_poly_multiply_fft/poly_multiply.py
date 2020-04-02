import numpy as np


'''
Creates a numpy array of int32 of size 2**n.
This represents a very large integer of base 2**32
4294967295 is the largest number representable by unsigned 32-bit int, so the maximum generated
random number has to be the square root of this to avoid overflow errors at runtime during the 
multiplication
'''
def create_int(n: int):

    if n > 20:  # to avoid very large numbers
        return np.random.randint(0, 65534, np.power(2, n), np.uint32)
    else:
        return np.random.randint(0, 65534, np.power(2, n), np.uint32)


# high school math
def foil_multiply(num1: np.array, num2: np.array) -> np.array:
    assert len(num1) == len(num2)
    multiplied = np.zeros(2 * len(num1), dtype=float)

    for i in range(len(num1)):
        for j in range(len(num2)):
            multiplied[i + j] += num1[i] * num2[j]

    return multiplied


# pad the printout of numbers so that 3373494 is turned into 0003373494
# len of max string length is 10 characters
# can take a list of strings, a list of ints, or a single int
def pad_printout(input):
    if isinstance(input, np.ndarray) or isinstance(input, list):
        output = ""
        for num in input:
            num = str(num)
            num = (10-len(num))*"0" + num
            output += num + ", "

        return output[:-2]

    elif isinstance(input, int):
        num = str(input)
        num = (10 - len(num)) * "0" + num
        return num

    elif isinstance(input, str):
        num = (10 - len(input)) * "0" + input
        return num

    else:
        return

