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
def pad_printout(item):
    if isinstance(item, np.ndarray) or isinstance(item, list):
        output = ""
        for num in item:
            num = str(num)
            num = (10-len(num))*"0" + num
            output += num + ", "

        return output[:-2]

    elif isinstance(item, int):
        num = str(item)
        num = (10 - len(num)) * "0" + num
        return num

    elif isinstance(item, str):
        num = (10 - len(item)) * "0" + item
        return num

    else:
        return

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


def getV(n, sign = 1):
    return [complex(np.cos(2*np.pi*i/n), sign * np.sin(2*np.pi*i/n)) for i in range(0, n)]

# TODO undertand this code and switch the signs to make it into ifft
def fft(p, v, n, depth = 0):
    #print("%s%s" % (" |"*depth+"in =", str(p)))
    if n == 1:
        #print("%s%s" % (" |"*depth+"out=", str(p)))
        return p
    # split into even and odd
    eve = [p[i] for i in range(0, n, 2)]
    odd = [p[i] for i in range(1, n, 2)]
    # square the v values
    v2 = [v[i]*v[i] for i in range(0, n//2)]
    # solve the two sub problems
    eveS = fft(eve, v2, n//2, depth+3)
    oddS = fft(odd, v2, n//2, depth+3)
    # construct the solution
    solution = ([eveS[i] + v[i]*oddS[i] for i in range(0, n//2)] +
                [eveS[i] - v[i]*oddS[i] for i in range(0, n//2)])
    #print("%s%s" % (" |"*depth+"out=", str(solution)))
    return solution

