from numpy import exp, pi, random, array, fft, zeros, concatenate, arange


# used for removing computationally unstable numbers
lim = 1e-16


def some_fft(p, n):
    if do_print:
        print(f"in = {p}")
    if n == 1:
        if do_print:
            print(f"out = {p}")
        return p
    even = some_fft(p[0::2], n//2)
    odd = some_fft(p[1::2], n//2)
    factor = exp(-2j * pi * arange(n) / n)
    return concatenate([even + factor[:n//2] * odd, even - factor[n//2:] * odd])


def add_buffer(arr):
    i = 0
    done = False
    while not done:
        n = 2**i
        # requires a buffer to have len of power of 2
        if n > len(arr):
            add_on = zeros([n - len(arr), ])
            return concatenate((arr, add_on))
        # arr is already a power of 2 length
        elif n == len(arr):
            return arr
        # N is still smaller than arr length
        else:
            i += 1


do_print = False

arr = array([0,1,2,3,4,5,6,7])
print(fft.fft(arr))
print(some_fft(arr,8))