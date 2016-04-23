#!/usr/bin/env python3

"""
github.com/greigdp, 2016
The Android pattern grid is as follows:


   0    1    2

   3    4    5

   6    7    8


A pattern is just an array which can be appended to, until a pattern is formed.

Also note that this is not a particularly elegant or neat solution. For example, getAdjacent, getLinear and getEndLinear
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

"""


# Find out what points are adjacent to current one
# Again, optimised replies to put more likely patterns first
def getAdjacent(dot):
    if (dot == 0):
        return [1, 3, 4]
    elif (dot == 1):
        return [0, 2, 4, 3, 5]
    elif (dot == 2):
        return [1, 5, 4]
    elif (dot == 3):
        return [0, 6, 4, 1, 7]
    elif (dot == 4):
        return [1, 3, 5, 7, 0, 3, 6, 8]
    elif (dot == 5):
        return [2, 8, 4, 7, 1]
    elif (dot == 6):
        return [3, 7, 4]
    elif (dot == 7):
        return [6, 8, 4, 3, 5]
    elif (dot == 8):
        return [7, 5, 4]

# Remember, linear ALSO includes adjacent! This is only for non-adjacent linear!
# The replies are optimised to return the most likely combinations first.
def getLinear(dot):
    if (dot == 0):
        return [1, 3, 4, 2, 6, 8]
    elif (dot == 1):
        return [4, 7]
    elif (dot == 2):
        return [1, 4, 5, 0, 6, 8]
    elif (dot == 3):
        return [4, 5]
    elif (dot == 4):
        return []
    elif (dot == 5):
        return [4, 3]
    elif (dot == 6):
        return [3, 4, 7, 0, 2, 8]
    elif (dot == 7):
        return [4, 1]
    elif (dot == 8):
        return [7, 5, 4, 6, 2, 0]

# Finds linear dots which are at extremities of the grid
# Remember, linear ALSO includes adjacent! This is only for non-adjacent linear!
#
# i.e.   for dot 0, the endlinear dots are 2 to the right, 2 below, and 2 below-left diagonally
def getEndLinear(dot):
    if (dot == 0):
        return [2, 6, 8]
    elif (dot == 1):
        return [7]
    elif (dot == 2):
        return [0, 8, 6]
    elif (dot == 3):
        return [5]
    elif (dot == 4):
        return []
    elif (dot == 5):
        return [3]
    elif (dot == 6):
        return [0, 8, 2]
    elif (dot == 7):
        return [1]
    elif (dot == 8):
        return [6, 2, 0]

# Finds the dot between any given "extremities" of the pattern grid
#
# i.e.   0    _    2
# Invoking this on (0,2) or (2,0) will return 1
def getMiddle(dot1, dot2):
    # Half the combinations to consider by sorting these numerically
    lower = min(dot1, dot2)
    higher = max(dot1, dot2)
    if (lower == 0 and higher == 2):
        return 1
    if (lower == 0 and higher == 6):
        return 3
    if (lower == 0 and higher == 8):
        return 4
    if (lower == 1 and higher == 7):
        return 4
    if (lower == 2 and higher == 6):
        return 4
    if (lower == 2 and higher == 8):
        return 5
    if (lower == 3 and higher == 5):
        return 4
    if (lower == 6 and higher == 8):
        return 7

# one-liner to check a dot hasn't already been visited in the current pattern
def isAlreadyVisited(currentPattern, next):
    return next in currentPattern

# one-liner to fetch the most recent dot from the current pattern
def getLast(currentPattern):
    return currentPattern[len(currentPattern)-1]

# Returns a list of dots which are permitted to feature next, for a given pattern passed in
def getAllowedNextDots(currentPattern):
    # dots already used are not eligible
    # dots not in a line are not eligible
    # dots not adjacent must "skip" a visited dot
    allDots = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    candidateDots = allDots.copy()
    for dot in allDots:
        if isAlreadyVisited(currentPattern, dot):
            # Remove as already visited
            candidateDots.remove(dot)
            continue
        # reaching this point means the dot is NOT already visited

        # now check if the point is adjacent - if it is, it's fine
        if dot in getAdjacent(getLast(currentPattern)):
            # the candidate dot is adjacent to the last dot, AND we know it's not visited before - it's OK
            continue
        # if it isn't adjacent, let's check if it's linear, AND that the adjacent is already visited

        # if the dot is linear (skipping adjacent)
        if dot in getEndLinear(getLast(currentPattern)):
            # we can find the intersecting dot
            intersect = getMiddle(dot, getLast(currentPattern))
            if isAlreadyVisited(currentPattern, intersect):
                # this is allowed
                continue
            else:
                candidateDots.remove(dot)

    # Now we have removed non-allowed dots
    return candidateDots


# Include some automated self-tests to help ensure this works correctly. These do not aim to test every scenario; rather
# they tested conditions needed while writing the code.
def test():
    # The text at the end of an assertion is the "hint" stating what was wrong
    assert 6 in getLinear(0), "0 and 6 are linear"
    assert 5 not in getLinear(0), "0 and 5 are not linear"
    pattern1 = [0, 1, 4]
    assert isAlreadyVisited(pattern1, 1), "Already visited 1"
    assert not isAlreadyVisited(pattern1, 3), "Haven't already visited 3"
    testPattern = [0, 3, 6]
    for i in [1, 4, 7, 5]:
        assert i in getAllowedNextDots(testPattern), "Dot should be allowed but wasn't"
    for i in [0, 2, 3, 6, 8]:
        assert i not in getAllowedNextDots(testPattern), "Dot should not be allowed but was"

    testPattern2 = [2, 1, 5, 4, 3, 0]
    for i in [6, 7, 8]:
        assert i in getAllowedNextDots(testPattern2), "Dot should be allowed but wasn't"
    for i in [2, 1, 5, 4, 3, 0]:
        assert i not in getAllowedNextDots(testPattern2), "Dot should not be allowed but was"

    testPattern3 = [0, 7]
    assert 4 in getAllowedNextDots(testPattern3), "Dot should be allowed but wasn't"
    assert 1 not in getAllowedNextDots(testPattern3), "Dot should not be allowed but was"
    testPattern4 = [0, 4, 7]
    assert 1 in getAllowedNextDots(testPattern4), "Dot should be allowed but wasn't"

########################################

# Returns a list of the possible "next pattern"
def getNextOptions(currentPattern):
    allPatterns = []
    x = getAllowedNextDots(currentPattern)
    #print("Next options are: " + str(x))
    #print(x)
    for i in x:
        candidate = currentPattern.copy()
        candidate.append(i)
        allPatterns.append(candidate)
    #print(allPatterns)
    return allPatterns

# This is the core of the logic - find all patterns of a given length, starting with a given prefix
def recursivelyEvaluate(patternStart, targetLength):
    lstStart = []
    # add the first digit of the pattern into the list
    lstStart.append(patternStart)
    # get the length of the current pattern
    currentLength = len(lstStart)
    if (len(lstStart) == 1):
        # this is first iteration, define currentPattern
        currentPattern = lstStart.copy()
    # work out how many iterations are needed, based on how many more dots are needed
    iterationsToDo = targetLength - currentLength

    # for each iteration
    for i in range(iterationsToDo):
        #print("Iteration " + str(i))
        # get a list of the possible next ones
        if (i == 0):
            # first time round, we get the list of possible patterns
            nextOpts = getNextOptions(currentPattern)
        else:
            # after that, we make a list
            nextOpts = []
            # for each of the branches we've identified
            for branch in currentPattern:
                # add the branched possible options
                nextOpts.extend(getNextOptions(branch))
        # now update currentPattern for the next iteration of the loop
        currentPattern = nextOpts
    # return the array of possible patterns for this length
    return currentPattern


# For a given length, finds the set of all valid patterns
def findAllPatterns(targetLength):
    allPatterns = []
    for i in range(9): # for each starting point
        thisSet = recursivelyEvaluate(i, targetLength)
        allPatterns.extend(thisSet)
    return allPatterns

# The main function - this will find all valid patterns upto a given length
def findAllCombinations(maxLength):
    allPatterns = []
    # Patterns must be a minimum of 4 dots in length
    for i in range(4,maxLength+1):
        # For each pattern length, find all valid patterns for that length
        thisSet = findAllPatterns(i)
        print("Length = " + str(i) + ": " + str(len(thisSet)) + " patterns")
        # Now add these patterns into the overall set of all patterns
        allPatterns.extend(thisSet)
    return allPatterns


############################
# The part to do the actual work
# First run the little self-test
test()
# Now find all combinations of up-to 9 dots in length
x = findAllCombinations(9)
print("Total number: " + str(len(x)))
f = open("allPatterns.txt", "w")
for pattern in x:
    toWrite = ""
    for result in pattern:
        toWrite += str(result)
    f.write(str(toWrite) + "\n")
f.close()
