from numpy import exp, pi, random, array, fft, zeros, concatenate, arange, allclose, conjugate


# fast fourier transform
def my_fft(p, n):
    if do_print:
        print(f"in = {p}")
    if n == 1:
        if do_print:
            print(f"out = {p}")
        return p
    even = my_fft(p[0::2], n // 2)
    odd = my_fft(p[1::2], n // 2)
    factor = exp(-2j * pi * arange(n) / n)
    return concatenate([even + factor[:n//2] * odd, even + factor[n//2:] * odd])


# inverse fast fourier transform
def my_ifft(p, n):
    if do_print:
        print(f"in = {p}")
    if n == 1:
        if do_print:
            print(f"out = {p}")
        return p
    even = my_ifft(p[0::2], n // 2)
    odd = my_ifft(p[1::2], n // 2)
    factor = exp(2j * pi * arange(n // 2) / (n//2))
    return concatenate([even + factor * odd, even - factor * odd])*2/n


# adds buffer so that length of arr is a factor of 2. i.e. len(arr) % 2 == 0
def add_buffer(arr):
    i = 0
    n = 0
    while n != len(arr):
        n = 2**i
        # requires a buffer to have len of power of 2
        if n > len(arr):
            return concatenate((arr, zeros([n - len(arr), ])))

        # N is still smaller than arr length
        else:
            i += 1

    return arr


def fft_helper(arr, function):
    arr = add_buffer(arr)
    return function(arr, len(arr))


do_print = False

arr = array([0,1,2,3,4,5,6,7], dtype=complex)
print(fft.fft(arr))
print('mine')
print(fft_helper(arr, my_fft))
print("It's close enough? : ", allclose(fft_helper(arr, my_fft), fft.fft(arr)))
print(fft_helper(fft.fft(arr), my_ifft))

