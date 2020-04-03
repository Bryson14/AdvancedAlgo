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
        return np.random.randint(0, 65534, np.power(2, n), np.uint64)
    else:
        return np.random.randint(0, 65534, np.power(2, n), np.uint64)


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

def getV(n, sign=1):
    return np.array([complex(np.cos(2*np.pi*i/n), sign * np.sin(2*np.pi*i/n)) for i in range(0, n)])

# TODO understand this code and switch the signs to make it into ifft
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


def fft_helper(arr):
    l = len(arr)
    return new_fft(arr, getV(l), l)

def new_fft(arr, w, n):
    if n == 1:
        return arr
    even = arr[0::2]
    odd = arr[1::2]
    # square omega terms.
    # assumes it is type ndarray
    w2 = w*w
    sol_even = new_fft(even, w2, n//2)
    sol_odd = new_fft(odd, w2, n//2)
    pos = [sol_even[i] + w[i]*sol_odd[i] for i in range(n//2)]
    neg = [sol_even[i] - w[i]*sol_odd[i] for i in range(n//2)]
    solution = pos + neg
    return solution

def ifft(p):
    length = len(p)
    return np.array(fft(p, getV(length, -1), length))/length


def fft_multiply(arr1, arr2):
    arr1 = pad_power_2(arr1)
    arr2 = pad_power_2(arr2)
    assert len(arr1) == len(arr2)

    phase_space_arr_1 = fft(arr1, getV(len(arr1)), len(arr1))
    phase_space_arr_2 = fft(arr2, getV(len(arr2)), len(arr2))

    whole_phase_space_arr = [phase_space_arr_1[i]*phase_space_arr_2[i] for i in range(len(arr1))]

    whole_real_space_arr = ifft(whole_phase_space_arr)

    multiplied_coefficients = [round(num.real) for num in whole_real_space_arr]

    return multiplied_coefficients


if __name__ == "__main__":
    size = 2
    arr = create_int(size)
    arr2 = create_int(size)
    print('results of three sub:   ', pad_printout(three_sub_other(arr, arr2, 2 ** size)))
    print('results of high school: ', pad_printout(foil_multiply(arr, arr2)))
    print('results of fft multiply:', pad_printout(fft_multiply(arr, arr2)))

    print("my fft: ", fft(arr, getV(2**size), 2**size))
    print("np fft: ", np.fft.fft(arr))
    print("my new fft: ", fft_helper(arr))
