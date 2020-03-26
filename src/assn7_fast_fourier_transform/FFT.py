from numpy import exp, pi, random, array, fft, zeros, concatenate, arange, allclose, conjugate
import matplotlib.pyplot as plt
import time
import pathlib2 as path


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


if __name__ == "__main__":
    # run time trails from n = 128 to n = ...
    n = 23
    from_n = 7
    numpy_runtimes = []
    algo_runtimes = []

    for i in range(from_n, n):
        arr = random.randint(0, 2**i, 2**i)

        start = time.time()
        fft_helper(arr, my_fft)
        mid = time.time()
        fft.fft(arr)
        end = time.time()

        numpy_runtimes.append(end-mid)
        algo_runtimes.append(mid-start)

    print('Numpy: \n', numpy_runtimes)
    print('mine: \n', algo_runtimes)
    plt.plot(arange(from_n, n), numpy_runtimes, label="Built-in Numpy FFT")
    plt.plot(arange(from_n, n), algo_runtimes, label="FFT Implementation")
    plt.xlabel("Size of N (log 2)")
    plt.ylabel("Run time in log 2 Seconds")
    plt.legend()
    plt.yscale('log', basey=2)
    plt.title("Log-Log Graph of Runtime vs N for various FFT algorithms")
    plt.savefig(path.Path.joinpath(path.Path.cwd(), f'Graph(n={n}).png'))
    plt.show()



