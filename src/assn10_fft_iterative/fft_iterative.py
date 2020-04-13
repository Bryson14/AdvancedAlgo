import numpy as np

'''
p -> polynomial is array form
w -> primitive root/ omegas
n -> size of p
'''
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

