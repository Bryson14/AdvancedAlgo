# Poly Multiplication w/ Fast Fourier Transform
## To Run:
python poly_multiply.py --> runs the analysis

TODO add some other stuff here

## Intro
This algorithm builds on past assignments and tests the speed of three algorithms when multiplying very large integers.
The three algorithms are:

* High School Algorithm (FOIL)
* Three-sub problem Algorithm
* FFT

## Results
1) The high school algorithm, three-sub algorithm, and fft multiply all give the same results. 
2) When there are very large numbers, they are put into the denominator in the gen_omegas function. Dividing by a very large number is that same as multiplying by a very small number. when any small and large number are multiplied, they lose numerical significance. This is due to the numerical instability in how numbers are stored in base 2 registers in the computer. This problem can be mitigated with larger floating point types, but is never fully avoided.
As n increases, the numerical instability increases. for example, if n is larger than 2^16, it can't be accurately represented with a 16 bit float. Python might be able to identify this and switch to a arbitrarily large float, but this still will lead to inaccuracies. This numerical error can result in an error in the integer solution
3) The FFT multiply algorithm was by far the fastest. The results are shown in the graph "Graph_20_min_runtime.png". Note the different slopes of the various lines representing the big_O time complexity. For the FFT, it did n=2^18 in 30 minutes. For highschool, it did 2^16 in 54 minutes. For the three-sub algo, it did it n=2^18 in 38 minutes.
4) The correct padding and correct handing of excessively large integers (larger than 2^32) are all handled by passing the list/array into the function "correct_printf"
5) The code is well documented and explained

