import random
import string
import math
import Phoneme

# Randomly determines popularity of item (e.g. a phoneme), allowing approx percentages of high and low probability items to be controlled
def determinePopularityProbability():
    probability = 0
    popularThreshold = 0.6
    regularThreshold = 0.3
    rand = random.random()
    # Determine whether will be popular or regular
    if rand > popularThreshold:
        # popular, high probability
        probability = sampleTruncatedNormalDist(0.5, 1, 0.8, 0.08)
    elif rand > regularThreshold:
        # regular, low probability
        probability = sampleTruncatedNormalDist(0, 0.1, 0.01, 0.05)
    else:
        # very unlikely, almost zero-probability (to avoid some phonemes having no successors)
        probability = 0.00001
    return probability

# Recursive sampling of normal distribution until a sample falls within interval
def sampleTruncatedNormalDist(minSample, maxSample, mean, standardDev):
    # Sample normal distribution
    sample = random.normalvariate(mean, standardDev)
    if sample < minSample or sample > maxSample:
        # If sample is outside of interval, recurse
        sample = sampleTruncatedNormalDist(minSample, maxSample, mean, standardDev)
    # Returned sample guaranteed to be within interval
    return sample

# Generates a list of given intervals, describing a symmetric distribution of values
def generateHistogramFrequencies(totalIntervals, meanInterval, meanIntervalProb, falloff, isNormalised):
    distribution = []
    if totalIntervals > 0 and (falloff > 0 and falloff < 1):
        # Fill list with correct number of zero-initialised intervals
        distribution = [0] * totalIntervals
        if meanIntervalProb <= 1:
            distribution[meanInterval] = meanIntervalProb
            latestValue = meanIntervalProb
            cumulativeProb = meanIntervalProb
            complete = False
            offsetFromMeanInterval = 1
            while not complete:
                # Apply falloff to latest values
                nextProb = latestValue * falloff
                # If normalisation specified then cumulative prob stops at one and process ends
                if isNormalised:
                    if (nextProb * 2) + cumulativeProb > 1:
                        # Next step will deplete probability
                        nextProb = (1 - cumulativeProb)/2
                        complete = True
                # Keep running total of probability values inserted so far
                cumulativeProb += 2 * nextProb
                latestValue = nextProb
                # Place nextProbs in intervals
                insertedValues = False
                if meanInterval - offsetFromMeanInterval >= 0:
                    distribution[meanInterval - offsetFromMeanInterval] = nextProb
                    insertedValues = True
                if meanInterval + offsetFromMeanInterval < totalIntervals:
                    distribution[meanInterval + offsetFromMeanInterval] = nextProb
                    insertedValues = True
                if not insertedValues:
                    # If offset was outside interval range on both ends of list then flag will be false
                    complete = True
                offsetFromMeanInterval += 1
        else:
            print("Error: Mean interval probability was specified to be greater than 1. Capping at 1.")
            distribution[meanInterval] = 1
    return distribution

# Uses parameters to generate a distribution list, and prints out the rounded values
def testHistogramFrequencyGeneration(totalIntervals, meanInterval, meanIntervalProb, falloff, isNormalised, decimalPlaces):
    distribution = generateHistogramFrequencies(totalIntervals, meanInterval, meanIntervalProb, falloff, isNormalised)
    cumulativeProbability = sum(distribution)
    for i in range(len(distribution)):
        # Convert values to strings to retain their rounded representation
        distribution[i] = str(round(distribution[i], decimalPlaces))
    print("Test distribution (cumProb=" + str(round(cumulativeProbability, decimalPlaces)) + "):")
    print(distribution)

# Generates a number of samples and registers which descrete intervals they fall into
# This function should be used to test interval-mean-sd combinations before use,
#  with large numbers of iterations, to provide a human readable impression of sample distribution
#  e.g.  testNormalDist(500, 0, 1, 0.5, 0.1) resulting in:
#       [0, 0, 16, 64, 169, 176, 65, 9, 1, 0]
#   reveals the concentation of samples around the mean. Params can then be adjusted accordingly.
# Normalisation flag can assist in abstracting away iteration-specifics
def testNormalDist(iterations, minSample, maxSample, mean, standardDev, normaliseResults):
    debugMode = False
    sampleIntervalWidth = maxSample - minSample
    # Interval will be divided into smaller sub-intervals
    totalDiscreteIntervals = 10
    discreteIntervalWidth = float(sampleIntervalWidth) / totalDiscreteIntervals
    # Each sample that falls within a certain interval
    intervalCounter = [0] * totalDiscreteIntervals
    for i in range(iterations):
        sample = sampleTruncatedNormalDist(minSample, maxSample, mean, standardDev)
        # Starting from lowest, determine which interval
        for counterIndex in range(totalDiscreteIntervals):
            if sample <= (minSample + (discreteIntervalWidth * (counterIndex+1))):
                # Sample fell in this interval; increment counter
                if debugMode: print("Sample: " + str(sample) + ", counterIndex: " + str(counterIndex) + " of " + str(totalDiscreteIntervals) + ",  sample upper bound: " + str(minSample + (discreteIntervalWidth * (counterIndex+1))))
                intervalCounter[counterIndex] += 1
                break
    if normaliseResults:
        for i in range(len(intervalCounter)):
            intervalCounter[i] = round(float(intervalCounter[i]) / iterations, 3)
    print("\nDistribution (mu=" + str(mean) + ", sd=" + str(standardDev) + ", interval=[" + str(minSample) + "," + str(maxSample) + "]):")
    print(intervalCounter)

