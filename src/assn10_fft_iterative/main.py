import pathlib
import sys

try:
    if str(pathlib.Path.cwd()).split('\\')[-1] != 'src':
        raise ImportError
except ImportError:
    print((f"current path -> {pathlib.Path.cwd()}"))
    print("File has to be run from cs5100.project_code.src")
    sys.exit(-1)

import matplotlib.pyplot as plt
import time
import numpy as np


def timer(p, function, print_line=False):
    start = time.time()
    if print_line:
        print(function(p))
    else:
        function(p)
    return time.time() - start


def fft_recur(arr, w, n):
    if n == 1:
        return arr
    # splits into even and odds
    even = arr[0::2]
    odd = arr[1::2]
    # square omega terms.
    # assumes it is type ndarray
    w2 = w*w
    sol_even = fft_recur(even, w2, n // 2)
    sol_odd = fft_recur(odd, w2, n // 2)
    pos = [sol_even[i] + w[i]*sol_odd[i] for i in range(n//2)]
    neg = [sol_even[i] - w[i]*sol_odd[i] for i in range(n//2)]
    solution = pos + neg
    return solution


def fft_helper(arr):
    l = len(arr)
    return fft_recur(arr, gen_omegas(l), l)


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


# generates the omegas for the fft algorithm
def gen_omegas(n, sign=-1):
    return np.array([complex(np.cos(2*np.pi*i/n), sign * np.sin(2*np.pi*i/n)) for i in range(0, n)])


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

# adds buffer so that length of arr is a factor of 2. i.e. len(arr) % 2 == 0
def add_buffer(arr):
    i = 0
    n = 0
    while n != len(arr):
        n = 2**i
        # requires a buffer to have len of power of 2
        if n > len(arr):
            return np.concatenate((arr, np.zeros([n - len(arr), ])))

        # N is still smaller than arr length
        else:
            i += 1

    return arr

# helper function
# p -> polynomial
def fft(p):
    l = len(p)
    return fft_inter(add_buffer(p), gen_omegas(l), l)


if __name__ == "__main__":
    if sys.argv[1] == '-r':
        sizes = []
        iter_time = []
        recur_time = []
        for i in range(6, int(sys.argv[2])):
            arr = np.random.randint(0, 1000000, 2**i)
            sizes.append(i)
            iter_time.append(timer(arr, fft))
            recur_time.append(timer(arr, fft_helper))

        plt.plot(sizes, iter_time, label="Iterative FFT")
        plt.plot(sizes, recur_time, label="Recursive FFT")
        print(iter_time)
        print(np.polyfit(sizes, iter_time, 1))
        plt.yscale('log', basey=2)
        plt.title("FFT (Recursion & Iterative) Runtime v Problem Size")
        plt.xlabel("n (log 2)")
        plt.ylabel("Time (log 2)")
        plt.legend()
        plt.savefig(f"Recur_Iter_FFT_n={sys.argv[2]}.png")
        plt.show()
        print(f"Iterative times\n{iter_time}\nRecursion Times\n{recur_time}")

    else:
        print("USAGE: python main.py -r RANGE")
        print("RANGE is the upper limit that the comparision between fft recursive and fft iterative will run to.")