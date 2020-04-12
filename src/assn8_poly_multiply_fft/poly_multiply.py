import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import pathlib2 as path

'''
Creates a numpy array of int32 of size 2**n.
This represents a very large integer of base 2**32
4294967295 is the largest number representable by unsigned 32-bit int, so the maximum generated
random number has to be the square root of this to avoid overflow errors at runtime during the 
multiplication
'''
def create_int(n: int):

    if n > 20:  # to avoid very large numbers
        return np.random.randint(0, 2147483647//2, np.power(2, n), np.int64)
    else:
        return np.random.randint(0, 2147483647//2, np.power(2, n), np.int64)


# high school math
def foil_multiply(num1: np.array, num2: np.array) -> np.array:
    assert len(num1) == len(num2)
    multiplied = np.zeros(2 * len(num1), dtype=np.int64)

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
            num = str(int(num))
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

# pads any list with zeros so that its len(arr) == 2^something
def pad_power_2(arr):
    i = 0
    n = 0
    while n != len(arr):
        n = 2 ** i
        # requires a buffer to have len of power of 2
        if n > len(arr):
            return np.concatenate((arr, np.zeros([n - len(arr), ])))

        # N is still smaller than arr length
        else:
            i += 1

    return arr

# faster version of the four sub with some tricky algebra
def three_sub_other(p: np.array, q: np.array) -> np.array:
    n = len(p)
    arr = np.zeros(2*n, dtype=float)

    # recursion base case
    if n == 1:
        arr[0] = p[0]*q[0]
        return arr

    # breaking the problem into sub problems. The big difference
    # from four_sub is that there are only three sub problem to
    # computes. Reduces time complexity from O(n^2) to O(n^1.5)
    pq_ll = three_sub_other(p[:n//2], q[:n//2])
    pq_hh = three_sub_other(p[n//2:], q[n//2:])

    # difference mid step
    p_mid = p[:n//2] + p[n//2:]
    q_mid = q[:n//2] + q[n//2:]
    pq_mid = three_sub_other(p_mid, q_mid)

    # solution construction step
    arr[:n] = pq_ll
    arr[-n:] = pq_hh
    arr[n // 2: n // 2 + n] += pq_mid - pq_hh - pq_ll

    return arr

# generates the omegas for the fft algo
def gen_omegas(n, sign=-1):
    return np.array([complex(np.cos(2*np.pi*i/n), sign * np.sin(2*np.pi*i/n)) for i in range(0, n)])

# starts the fft function with only a given array
def fft_helper(arr):
    l = len(arr)
    return fft(arr, gen_omegas(l), l)

# fast fourier transform. Assumes that arr is already of len 2^integer
def fft(arr, w, n):
    if n == 1:
        return arr
    # splits into even and odds
    even = arr[0::2]
    odd = arr[1::2]
    # square omega terms.
    # assumes it is type ndarray
    w2 = w*w
    sol_even = fft(even, w2, n // 2)
    sol_odd = fft(odd, w2, n // 2)
    pos = [sol_even[i] + w[i]*sol_odd[i] for i in range(n//2)]
    neg = [sol_even[i] - w[i]*sol_odd[i] for i in range(n//2)]
    solution = pos + neg
    return solution

# inverse fast fourier transform
def ifft(p):
    length = len(p)
    return np.array(fft(p, gen_omegas(length, 1), length)) / length

# utilizes the fft algorithm above to quickly multiply two large integers.
# output should match high school algorithm and three_sub algorithm
def fft_multiply(arr1, arr2):
    # pad the arrays to a len of a power of 2
    arr1 = pad_power_2(arr1)
    arr2 = pad_power_2(arr2)
    assert len(arr1) == len(arr2)

    # turn both arrays into phase space
    phase_space_arr_1 = np.array(fft(arr1, gen_omegas(len(arr1)), len(arr1)))
    phase_space_arr_2 = np.array(fft(arr2, gen_omegas(len(arr2)), len(arr2)))

    # element wise multiplication in phase space
    total_phase_space_arr = phase_space_arr_1*phase_space_arr_2

    # turn back into real space
    total_real_space_arr = ifft(total_phase_space_arr)

    # takes the integer real part of the complex numbers
    multiplied_coefficients = list(map(lambda x: x.real, total_real_space_arr))

    return multiplied_coefficients

# runs a multiplication problem on larger and larger problem sets until it reaches 20 minutes of CPU time.
# returns a list of size n vs time
def run_for_twenty_minutes(function):
    size = 6
    sizes = []
    cpu_times = []
    start = 0
    runtime = 0.0
    TIME_CUTOFF = 20*60
    while runtime < TIME_CUTOFF:
        sizes.append(size)
        start = time.time()
        arr = create_int(size)
        arr2 = create_int(size)
        function(arr, arr2)
        runtime = time.time() - start
        cpu_times.append(runtime)
        size += 1

    return sizes, cpu_times

# during the multiplication process, the size of ints could have exceeded
# 4294967295. In this case, that int should have 2^32 subtracted from it
# and one can be added to the next cell. Highest orders are first
def carry_over_overflow(arr):
    MAX = 4294967296

    # adding on buffer of 1 in case the highest cell overflows
    if isinstance(arr, np.ndarray) and arr[0] != 0:
        arr = np.concatenate([np.zeros((1,)), arr])
    elif isinstance(arr, list) and arr[0] != 0:
        arr = [0] + arr
    for i in range(len(arr) - 1, 0, -1):
        if arr[i] >= MAX:
            arr[i-1] += arr[i] % MAX
            arr[i] = arr[i] // MAX
    return arr

# takes care of the overflow of int 2^32 and string padding
def correct_printf(arr):
    return pad_printout(carry_over_overflow(arr))


if __name__ == "__main__":
    arr = [0,1,2,3,4,5,6,7]
    print(fft_helper(arr))
    print(np.fft.fft(arr))
    size = 2
    arr = create_int(size)
    print(f"arr : {arr}")
    arr2 = create_int(size)
    print(f"arr 2: {arr2}")
    print('results of high school: ', correct_printf(foil_multiply(arr, arr2)))
    print('results of three sub:   ', correct_printf(three_sub_other(arr, arr2)))
    print('results of fft multiply:', correct_printf(fft_multiply(arr, arr2)))

    if len(sys.argv) > 1 and sys.argv[1] == "-r":
        print("running time out function...")
        if sys.argv[2] == "three":
            print(f"results for three sub max runtime\n {run_for_twenty_minutes(three_sub_other)}")
        elif sys.argv[2] == "fft":
            print(f"results for fft multiply max runtime\n {run_for_twenty_minutes(fft_multiply)}")
        elif sys.argv[2] == "hs":
            print(f"results for high school max runtime\n {run_for_twenty_minutes(foil_multiply)}")
        else:
            pass

    fft_results = ([6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
                   [0.001993417739868164, 0.00498652458190918, 0.007978677749633789, 0.018457412719726562,
                    0.04091620445251465, 0.09674215316772461, 0.25830793380737305, 0.991936445236206,
                    4.190894365310669, 21.34105157852173, 104.79319977760315, 413.393187046051, 1749.1212944984436])
    hs_results = ([6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
                  [0.0029914379119873047, 0.012471437454223633, 0.0468747615814209, 0.19447946548461914,
                   0.772932767868042, 3.2929346561431885, 13.544007301330566, 49.57841515541077, 202.50718665122986,
                   839.6248352527618, 3248.8114218711853])
    three_sub_results = ([6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
                          [0.003988981246948242, 0.010964393615722656, 0.034920454025268555, 0.10271143913269043,
                           0.304180383682251, 0.9285223484039307, 2.7829794883728027, 9.199534177780151,
                           28.146015644073486, 83.44644165039062, 242.09331274032593, 777.3618574142456, 2276.2384588718414])

    # display graph for
    plt.plot(fft_results[0], fft_results[1], label="FFT")
    plt.plot(three_sub_results[0], three_sub_results[1], label="3-Sub")
    plt.plot(hs_results[0], hs_results[1], label="High School")
    plt.title("N reached after 20 Minutes of CPU Time\n Problem size 2^n vs Time")
    plt.xlabel("n")
    plt.ylabel("Seconds (log 2)")
    plt.yscale('log', basey=2)
    plt.legend()
    # plt.savefig(path.Path.joinpath(path.Path.cwd(), 'Graph_20_min_runtime.png'))
    # plt.show()
