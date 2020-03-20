from numpy import exp, pi, random


# used for removing computationally unstable numbers
lim = 1e-16


# Recursive fast fourier transform
def fft(x: list) -> list:
    N = x.size
    if N <= 1:
        return x
    even = fft(x[0::2])
    odd = fft(x[1::2])
    T = [exp(-2j*pi*k/N)*odd[k] for k in range(N//2)]
    a = [even[k] + T[k] for k in range(N//2)] + [even[k] - T[k] for k in range(N//2)]
    return a

print(fft(random.random(1000000)))