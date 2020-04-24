# Iterative v Recursion Fast Fourier Transform
## What's faster?

Iteration. 


## Results
Running from n = 2^6 to 2^20
Run times were:

Iterative times

[0.0009131431579589844, 0.002070188522338867, 0.003986358642578125, 0.010169506072998047, 0.023855209350585938, 0.046866655349731445, 0.09477925300598145, 0.19467926025390625, 0.4128904342651367, 2.1313314
43786621, 5.011539697647095, 9.66740345954895, 22.614554405212402, 42.44984817504883]
 
 Recursion Times
 
[0.0, 0.001922607421875, 0.003989219665527344, 0.007865428924560547, 0.016953468322753906, 0.033998727798461914, 0.08676767349243164, 0.2591116428375244, 1.6850368976593018, 14.877243041992188, 79.05675601
959229, 302.4288399219513, 1213.8275513648987, 3220.7977101802826]
 
The iterative algorithm was around O(n*logn * 0.000005)
the Recursive algorithm was around O(n*logn * 0.00032) when n > 2^13

This means the iterative algorithm, especially at greater values of n was about 64 times faster than the recursive algorithm