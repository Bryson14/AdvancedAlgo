"""
Write the simple minimum edit distance algorithm where a deletion, insertion or substitution is scored as 1 and the
 goal is to find the minimum number of edit steps. Answer the following questions:
Many kinds of typing errors (and mutations in DNA) involve switching the order of two adjacent letters. For instance,
a classic when typing is to produce “hte” rather than “the”
Modify your recursive algorithm to include this kind of edit step and count it as 1.
"""

import numpy as np


# recursion is slow
def med_recur(i, j):
    if i <= 0:
        return j
    if j <= 0:
        return i
    # del from i, del from j, substitution, swap
    deli = med_recur(i - 1, j) + 1
    delj = med_recur(i, j - 1) + 1
    sub = med_recur(i - 1, j - 1) + (A[i] != B[j])
    swap = 1000000
    if i > 1 and j > 1:
        swap = med_recur(i - 2, j - 2) + 2 - (A[i-1] == B[i] and A[i] == B[i-1])

    return min(deli, delj, sub, swap)


# dynamic program is fast
def med_dp(i, j):
    # initialize cache with base case along axis
    c = np.zeros([i + 1, j + 1], dtype=int)
    for x in range(i + 1):
        c[x, 0] = x
    for y in range(j + 1):
        c[0, y] = y

    swap = 10000000
    # fill in cache
    for x in range(1, i + 1):
        for y in range(1, j + 1):
            insert = c[x - 1, y] + 1
            deletion = c[x, y - 1] + 1
            substitution = c[x - 1, y - 1] + (A[x] != B[y])
            if x > 1 and y > 1:
                swap = c[x - 2, y - 2] + 2 - (A[x-1] == B[y] and A[x] == B[y-1])
            c[x, y] = min(insert, deletion, substitution, swap)

    # return answer
    return c[i, j]


# helper function
def med(str_a, str_b):
    global A, B
    A = str_a
    B = str_b

    # the algorithm stops at index 0, so adding a space at the beginning of each string
    if not A.startswith(" "):
        A = " " + A
    if not B.startswith(" "):
        B = " " + B

    print("recursive", med_recur(len(A) - 1, len(B) - 1))
    return med_dp(len(A) - 1, len(B) - 1)


A = ''
B = ''

print("dp", med('the', 'hte'))