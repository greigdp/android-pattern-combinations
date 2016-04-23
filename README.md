# Android Pattern Combinations

This is a quick script, designed to compute all possible Android lock pattern combinations.

Note that this is not a particularly elegant or neat solution. For example, getAdjacent, getLinear and getEndLinear
could be considered as sets, since getLinear is the union of getAdjacent and getEndLinear, and getAdjacent and
getEndLinear are mutually exclusive.

Running this script will do a self-test, then make a file called "allPatterns.txt" in the current directory, containing
a new-line separated list of patterns.

Future work could look at optimising the ordering in a more clever way than right now - the arrays here are tweaked
to be in an order that tries to prioritise the more "likely" transitions. For example, 0 -> 5 is a valid transition, but
it's a very hard one to enter, and very unlikely to see used.

The results are validated against "Quantifying the Security of Graphical Passwords: The Case of Android Unlock Patterns"
(Uellenbeck et al.) which stated that 389,112 total pattern combinations are found. This is confirmed as follows:

	$ wc -l allPatterns.txt
	389112 allPatterns.txt
