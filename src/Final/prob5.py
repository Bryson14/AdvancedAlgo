import numpy as np
import matplotlib.pyplot as plt
import time

# reverse bit shuffle
def rbs(i: int, logn: int):
    N = 1 << logn
    iter = i
    for j in range(1, logn):
        i >>= 1
        iter <<= 1
        iter |= (i & 1)
    iter &= N-1
    return iter

# generates the omegas for the fft algorithm
def gen_omegas(n, sign=-1):
    return np.array([complex(np.cos(2*np.pi*i/n), sign * np.sin(2*np.pi*i/n)) for i in range(0, n)])


def fft_inter(p, w, n):
    logn = np.int(np.log2(n))
    cache = np.full((logn + 1, n), np.complex)

    # reverse bit shuffle
    for i in range(n):
        cache[0, i] = np.complex(p[rbs(i, logn)])

    # fill in cache from base case row up
    for i in range(1, logn + 1):

        # squares the imaginary roots enough to mimic recursion
        omegas = w
        for s in range(logn - i):
            omegas = np.power(omegas, 2)

        # fills in cache side to side
        size = 1 << i
        for j in range(0, n, size):
            idx = 0
            for k in range(size // 2):
                cache[i][j + k] =             cache[i - 1][j + k] + omegas[idx] * cache[i - 1][j + k + size // 2]
                cache[i][j + size // 2 + k] = cache[i - 1][j + k] - omegas[idx] * cache[i - 1][j + k + size // 2]
                idx += 1

    return cache[logn]

def fft_multiply(arr1, arr2):
    # pad the arrays to a len of a power of 2
    assert len(arr1) == len(arr2)

    # turn both arrays into phase space
    phase_space_arr_1 = np.array(fft_inter(arr1, gen_omegas(len(arr1)), len(arr1)))
    phase_space_arr_2 = np.array(fft_inter(arr2, gen_omegas(len(arr2)), len(arr2)))

    # element wise multiplication in phase space
    total_phase_space_arr = phase_space_arr_1*phase_space_arr_2

    # turn back into real space
    total_real_space_arr = np.fft.ifft(total_phase_space_arr)

    # takes the integer real part of the complex numbers
    multiplied_coefficients = list(map(lambda x: x.real, total_real_space_arr))

    return multiplied_coefficients


def foil_multiply(num1: np.array, num2: np.array) -> np.array:
    assert len(num1) == len(num2)
    multiplied = np.zeros(2 * len(num1), dtype=np.int64)

    for i in range(len(num1)):
        for j in range(len(num2)):
            multiplied[i + j] += num1[i] * num2[j]

    return multiplied

def smart_multiply(arr1, arr2):
    if len(arr1) < 2**6:
        return foil_multiply(arr1, arr2)
    else:
        fft_multiply(arr1, arr2)


# sizes = []
# smart_time = []
# fft_time = []
# foil_time = []
# for i in range(2, 5):
#     A = np.random.randint(-1000,1000,2**i)
#     B = np.random.randint(-1000,1000,2**i)
#
#     start = time.time()
#     foil_multiply(A,B)
#     mid = time.time()
#     fft_multiply(A,B)
#     end = time.time()
#     smart_multiply(A,B)
#     another_end = time.time()
#
#     fft_time.append(end-mid)
#     foil_time.append(mid - start)
#     smart_time.append(another_end - end)
#     sizes.append(i)
#
# plt.plot(sizes, fft_time, label="FFT")
# plt.plot(sizes, foil_time, label="FOIL")
# plt.plot(sizes, smart_time, label="ADAPTIVE")
# plt.legend()
# plt.yscale('log', basey=2)
# plt.show()

"""
An algorithm that would be faster using the “3 sub” algorithm and the high school algorithm would be to initially 
use the 3 sub algorithm, which recursively breaks down the problem. In the recursion stack, if the size of the sub 
problem is less than 2^6 (where foiling is faster), the it hands off that sub problem to foil to finish it off. Then 
is reconstructs the answer on the way up the recursion stack.
"""

