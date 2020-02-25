Everything in this program in run from main.py

If you want to run a comparision on all the different DNA sequences, simply enter the command 'C' when prompted

To manually enter in a DNA sequence, enter the command 'MED' when prompted.

Note, this program scores DNA sequences based on a given table:

 Point system when substituting one nucleotide for another nucleotide. 
d represents a deletion from the sequence

	    A  C  G  T  d
	A   5 -1 -2 -1 -3
	C  -1  5 -3 -2 -4
	G  -2 -3  5 -2 -2
	T  -1 -2 -2  5 -1
	d  -3 -4 -2 -1  *

If a sequence entered contains characters other than ACGT, then the program will fail.


Something I noticed was that using NumPy arrays sped up the processing significantly. Also, the program ran in O(n) time because of the fact it had to access the array three time for each operation. Overall, the average run time for a DNA comparision was around 10 minutes.

The program becomes impractical when the strings approach 100K characters each. This is because the dp algorithm needs a NxM array to create the solutions cache. At this point, there is not enough memory to create the data structure. I.e. when the strings are both 105 K characters long, the array necessary to make the cache would take up 41.1 GiB

The scientific significance of this algorithm cannot be overstated. Thanks to dynamic programming, it took an operation that would have taken an infinite amount of time and reduced it to linear problem. This makes DNA sequences possible and opens up the realm of DNA study, manipulation, and control. As we advance into future, DNA altering will become easier and more reliable thanks to the work of computer scientists like us.

The file human_diversity.txt was deleted because it was the same DNA sequence as prototypical_human.txt 