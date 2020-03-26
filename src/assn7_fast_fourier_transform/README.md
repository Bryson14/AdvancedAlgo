# Fast Fourier Transform

## How to Run
From the working directory `assn7_fast_fourier_transform`, run the command `python FFT.py`

## Intro
I had a lot of trial and error in this algorithm. I know this is a valuable algorithm that is used in many different applications. However, it took an eternity and a half to wrap my head aorund what it was actually doing. So in additioin to my professor's notes and videos, here are some of the resources I used to better understand the good work of Mr. Cooley and Mr. Tukey
https://jakevdp.github.io/blog/2013/08/28/understanding-the-fft/

## Implementation
The Fast Fourier Transform gets the name fast by improving the original transform time from O(n^2) to O(n logn) runtime.
This greater improves the usefulness of this common algorithm.

## Results
This algorithm is compared against NumPy's version. NumPy's version is order of magnitudes faster because it runs a vectorized version of fft with base sub-routines in FORTRAN.
This  algorithm does well compared to using python list because of the C code written for NumPy arrays and multiplication.
The algorithm I made is a n log n time but is about a magnitude (10x) slower than the numpy built-in function.



 

 