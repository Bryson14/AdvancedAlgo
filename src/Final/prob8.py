import sys
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


def setup(p, n):
    logn = np.int(np.log2(n))
    cache = np.full((logn + 1, n), np.complex)

    # reverse bit shuffle
    for i in range(n):
        cache[0, i] = np.complex(p[rbs(i, logn)])
    return cache


def fft_no_setup(p,w,n, cache):
    logn = np.int(np.log2(n))
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
                cache[i][j + k] = cache[i - 1][j + k] + omegas[idx] * cache[i - 1][j + k + size // 2]
                cache[i][j + size // 2 + k] = cache[i - 1][j + k] - omegas[idx] * cache[i - 1][j + k + size // 2]
                idx += 1

    return cache[logn]

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
    sizes = []
    iter_time = []
    without_setup_time = []
    end = 18
    for i in range(6, end):
        arr = np.random.randint(0, 1000000, 2 ** i)
        sizes.append(i)
        iter_time.append(timer(arr, fft))
        cache = setup(arr, len(arr))
        omegas = gen_omegas(len(arr))
        start = time.time()
        fft_no_setup(arr, omegas, len(arr), cache)
        without_setup_time.append(time.time() - start)

    plt.plot(sizes, iter_time, label="Iterative FFT")
    plt.plot(sizes, without_setup_time, label="Without Setup FFT")
    plt.yscale('log', basey=2)
    plt.title("FFT (Recursion & Iterative) Runtime v Problem Size")
    plt.xlabel("n (log 2)")
    plt.ylabel("Time (log 2)")
    plt.legend()
    plt.savefig(f"Recur_Iter_FFT_n={end}.png")
    plt.show()

