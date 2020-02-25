#This is a empirical study between the classic FOIL method that was taught in high school versus the efficiency of a algorithm better suited to computation speed.
======

** To run**

'python main.py'

There will appear options to run:
*a large study comparing FOIL and the other method
*Manually enter two polynomials to multiply and run with FOIL
*Manually enter two polynomials to multiply and run with the three-sub recursive algorithm

## Observations
From the n = 15 test, it took about 6 hours to run and the graph can be seen in the files.

The Coefficients from that run are the following:

These data sets are linear, but graphed on a log v log graph to better illustrate the problem sets they solved.


High School: 
t(x) = 1.27047330e-02 *x  - 1.97367607e+01
the overhead constant is - 5.33 seconds

four sub problem algorithm:
t(x) = 6.28732511e-02 *x - 9.82700823e+01
the overhead constant is - 26.83 seconds

three sub problem algorithm:
t(x) = 1.74827990e-03 *x - 2.17241708e+00
the overhead constant is - 2.17 seconds


From the graph, which was scaled log base 2 on both axis, 
it was found that the slope of the lines for the high school 
and the four sub problem algorithms were approximately 1.5. 
For the three sub problem algorithm, the slope of the line was 
approximately 1. 

Also from the graph, it show that around n=2^7, the three sub problem 
faster than the other two algorithms. This means that for anything
under the size 2^7, the high school algorithm is preferable; after this
the three sub problem is the best 