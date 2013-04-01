# CMU Phoneme Dictionary:
# http://www.speech.cs.cmu.edu/cgi-bin/cmudict

import random
import string
import math
import Phoneme

def createPhonemeObjects(phonemeObjects, newPhonemes, phonemeType):
    debugMode = False
    # Create Phoneme objects from the incoming list
    print("Creating (" + str(len(newPhonemes)) + ") phoneme (" + phonemeType + ") objects...")
    # Loop through phonemes, creating objects
    for phoneme in newPhonemes:
        # Create a phoneme object
        baseProbability = determinePhonemeProbability(phoneme)
        positionalRand = random.random()
        # Positional probabilities apply modifiers that incline certain phonemes towards certain positional occurrences
        positionalProbabilities = []
        usePosProbs = True
        if usePosProbs:
            if positionalRand > 0.7:
                # Phoneme will be an 'late' one, appearing more frequently at the end of a word
                print("Phoneme '" + phoneme + "' is late")
                positionalProbabilities = [0, 0.1, 0.2, 0.4, 1.0]
            elif positionalRand < 0.3:
                # Phoneme will be an 'early' one, appearing more frequently at the beginning of a word
                positionalProbabilities = [1.0, 0.5, 0.1, 0, 0]
                print("Phoneme '" + phoneme + "' is early")
            else:
                # Phoneme will be given an even likelihood to occur throughout a word
                positionalProbabilities = []
            
        graphemes = [phoneme]
        nextPhoneme = Phoneme.Phoneme(phoneme, phonemeType, 'example '+phoneme, baseProbability, positionalProbabilities, graphemes)
        if debugMode: print("nextPhoneme: " + nextPhoneme.phonemeSymbol)
        phonemeObjects[nextPhoneme.phonemeSymbol] = nextPhoneme

# Generate a list of words
def generateWords(generatedWords, totalWords, phonemeObjects):
    debugMode = False
    print("Generating (" + str(totalWords) + ") words...")
    for nextWordIndex in range(totalWords):
        if debugMode: print("Generating word " + str(nextWordIndex))
        wordLength = int(sampleTruncatedNormalDist(3, 10, 4.5, 2))
        # Indicate if word length will be calculted in characters or phonemes
        measureLengthInPhonemes = False
        # Call generator function
        finishedWord, symbolString = generateWord(wordLength, measureLengthInPhonemes, phonemeObjects)
        # Add generated word to list
        generatedWords.append(finishedWord)

# Generates a single word, with wordlength measured in characters or phonemes
#  Measuring length in characters gives tighter control over string length, but may prevent the last
#  phoneme generated from knowing it is the terminating phoneme which may affect positional probabilities)
def generateWord(desiredWordLength, measureLengthInPhonemes, phonemeObjects):
    word = ""
    currentLength = 0
    symbolString = ""
    # The empty-string phoneme is used to initiate process
    latestPhoneme = phonemeObjects[""]
    while currentLength < desiredWordLength:       
        if latestPhoneme.successors:
            if debugMode: print("Successors: " + ", ".join(latestPhoneme.successors))
            chosenPhoneme = latestPhoneme.chooseSuccessor(currentLength+1, desiredWordLength)
            word += chosenPhoneme.getRandomGrapheme()
            symbolString += chosenPhoneme.phonemeType
            latestPhoneme = chosenPhoneme
            # Increase length counter, so word knows when to stop selecting successors
            if measureLengthInPhonemes:
                # If length is counter in phonemes, increase length counter by 1, regardless of number of characters in grapheme
                currentLength += 1
            else:
                # If length is counted in characters, set it equal to current length of string
                currentLength = len(word)
        else:
            print("Error: '" + latestPhoneme.phonemeSymbol + "' has no successors (failed on phoneme " + str(nextPhonemeIndex + 1) + " of " + str(wordLength) + ")")
    if word == "":
        print("Error: Empty word was generated. (Symbol string: '" + symbolString + "')")
    return word, symbolString

def printGeneratedWords(generatedWords):    
    print("\nGenerated words:")
    for nextWord in generatedWords:
        print("\t" + str.capitalize(nextWord))

# Generates and prints words to fill multiple lines of given character length, placing spaces between words and occassional full stops
def generateAndPrintParagraph(totalLines, lineWidth, phonemeObjects):
    paragraph = ""
    capitalizeNext = True
    # Indicate if word length will be calculted in characters or phonemes
    measureWordLengthInPhonemes = False
    # Sentence length counters aid decision of punctuation placement
    currentSentenceLength = 0
    minimumSentenceLength = 20
    # Iterate over required lines
    for lineNumber in range(totalLines):
        currentLine = ""
        while len(currentLine) < lineWidth:
            # Generate another word for this line
            wordLength = int(sampleTruncatedNormalDist(0, 7, 3, 2)) + 1
            # Generate word
            word, symbolString = generateWord(wordLength, measureWordLengthInPhonemes, phonemeObjects)
            # Words at beginning of sentences will be capitalized, based on flag
            if capitalizeNext:
                capitalizeNext = False
                word = str.capitalize(word)
            # Chance of sentence ending increases the more the sentence exceeds the minimum length
            currentSentenceLength += len(word)
            if currentSentenceLength > minimumSentenceLength:
                # Sentence overflow is number of characters in sentence past minimum sentence length
                sentenceOverflow = currentSentenceLength - minimumSentenceLength
                # Sentence termination probability increases with sentenceOverflow
                terminationProb = 0.02
                if random.random() < (terminationProb * sentenceOverflow):
                    # If sentence ends here, add a full stop
                    word += "."
                    currentSentenceLength = 0
                    capitalizeNext = True
            # Add a space before the next word
            word += " "
            currentLine += word
        # Add a newline symbol
        currentLine += "\n"
        # Add line to paragraph
        paragraph += currentLine
    # Print the paragraph
    print("\nGenerated paragraph:")
    print(paragraph)

def printPhonemes(phonemeObjects, verbose):
    print("Total phonemeObjects: " + str(len(phonemeObjects)))
    # For testing, print out contents of phoneme objects
    print("Testing phoneme objs:")
    for phonemeKey in phonemeObjects:
        phonemeObjects[phonemeKey].reportPhonemeInfo(verbose)

def printSuccessorUsages(phonemeObjects):
    print("\nPhoneme usage information:\n")
    for phonemeKey, phoneme in phonemeObjects.items():
        phoneme.reportPhonemeSuccessorUsage()
        
# Adds all phonemes as successors to all other phonemes with a probability of 1
def fullyConnectNetwork(phonemeObjects):
    debugMode = False
    print("Fully connecting set of (" + str(len(phonemeObjects)) + ") phoneme objects...")
    for key in phonemeObjects.keys():
        phonemeObj = phonemeObjects[key]
        # Give phonemeObj every other phonemeObject as a successor
        for successorKey in phonemeObjects.keys():
            nextSuccessor = phonemeObjects[successorKey]
            # Add this object as successor
            if debugMode: print(phonemeObj.phonemeSymbol + " adding phoneme " + nextSuccessor.phonemeSymbol + " as successor.")
            successorProbability = determinePhonemeProbability(successorKey)
            phonemeObj.addSuccessor(nextSuccessor, successorProbability)

# Randomly determines popularity of phoneme, allowing approx percentages of high and low probability successors to be controlled
def determinePhonemeProbability(phonemeKey):
    successorProbability = 0
    popularThreshold = 0.6
    regularThreshold = 0.3
    rand = random.random()
    # Determine whether successor will be popular or regular
    if rand > popularThreshold:
        # successor is popular, high probability
        successorProbability = sampleTruncatedNormalDist(0.5, 1, 0.8, 0.08)
    elif rand > regularThreshold:
        # successor is regular, low probability
        successorProbability = sampleTruncatedNormalDist(0, 0.1, 0.01, 0.05)
    else:
        # designated non-successor, almost zero-probability (to avoid some phonemes having no successors)
        successorProbability = 0.00001
    return successorProbability

# Recursive sampling of normal distribution until a sample falls within interval
def sampleTruncatedNormalDist(minSample, maxSample, mean, standardDev):
    # Sample normal distribution
    sample = random.normalvariate(mean, standardDev)
    if sample < minSample or sample > maxSample:
        # If sample is outside of interval, recurse
        sample = sampleTruncatedNormalDist(minSample, maxSample, mean, standardDev)
    # Returned sample guaranteed to be within interval
    return sample

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
            intervalCounter[i] = round(float(intervalCounter[i]) / iterations, 2)
    print("\nDistribution (mu=" + str(mean) + ", sd=" + str(standardDev) + ", interval=[" + str(minSample) + "," + str(maxSample) + "]):")
    print(intervalCounter)

# Removes from each node's listed successors 
def removeSameTypeConnections(phonemeObjects):
    print("Removing same-typed successions...")
    debugMode = False
    for key in phonemeObjects.keys():
        phonemeObj = phonemeObjects[key]
        if debugMode: print("'" + phonemeObj.phonemeSymbol + "(" + phonemeObj.phonemeType + ") being checked for like-typed successors.")
        # retain only differently typed objects
        keysForRemoval = []
        # accumulate probabilities of retained objects
        cumulativeProb = 0
        for key in phonemeObj.successors.keys():
            if phonemeObj.successors[key].phonemeType == phonemeObj.phonemeType:
                # remove phoneme item from dict
                keysForRemoval.append(key)
            else:
                # add retained keys probability to cumulative
                cumulativeProb += phonemeObj.successorProbabilities[key]
        if debugMode: print("...deleting keys: " + ",".join(keysForDeletion))
        # Prompt node to eject keys from successor dicts
        phonemeObj.removeSuccessors(keysForRemoval)
        if debugMode: print("...keys after deletion: " + ",".join(phonemeObj.successors.keys()))

# Remove zero-probability successors
def pruneNetwork(phonemeObjects):
    debugMode = False
    print("Pruning network of zero-probability successions...")
    for phonemeKey in phonemeObjects:
        keysForRemoval = []
        for successorKey in phonemeObjects[phonemeKey].successors:
            # Check probability of successor
            if phonemeObjects[phonemeKey].successorProbabilities[successorKey] == 0:
                # Add to removal list
                keysForRemoval.append(successorKey)
        if debugMode: print("Phoneme '" + phonemeKey + "' is losing " + str(len(keysForRemoval)) + " of " + str(len(phonemeObjects[phonemeKey].successors.keys())) + " successors.")
        phonemeObjects[phonemeKey].removeSuccessors(keysForRemoval)

# Initiator phoneme is the starting state for word generation, with all possible first-phonemes as its successors
def addEmptyInitiator(successorObjects):
    print("Adding empty initiator phoneme...")
    # Create empty-phoneme object
    emptySymbol = ""
    emptyType = "initiator"
    emptyExample = "not applicable"
    baseProbability = 0
    positionalProbability = 1
    emptyGraphemes = [""]
    emptyInitiator = Phoneme.Phoneme(emptySymbol, emptyType, emptyExample, baseProbability, positionalProbability, emptyGraphemes)
    # Provide all phonemes as successors of the initiator with equal probability
    baseProbability = 1.0
    # Probability that for each successor stored in dict, keyed on successor phonemeSymbol
    successorProbabilities = dict()
    for successorKey in successorObjects:
        successorProbabilities[successorKey] = successorObjects[successorKey].baseProbability
    # Place empty initiator as single phoneme in list,
    # Corresponding list with recently created dict of successor probabilities also placed in list
    addSequenceOfSuccessors([emptyInitiator], [successorProbabilities], successorObjects)
    # Add the empty initiator to dictionary
    phonemeObjects[""] = emptyInitiator

# Given list of phoneme takes all in given dict as successors
# For use in cases such as the emptyInitiator, which should have all phoneme objects as successors
# - predecessorPhonemeObjects: list of phoneme objects
# - successorProbabilities: list (corresponding with predecessor list) of dicts, containing probabilities keyed on successor phonemeSymbols
# - successorPhonemeObjects: dict of phonemes using symbol as key
def addSequenceOfSuccessors(predecessorPhonemeObjects, successorProbabilities, successorPhonemeObjects):
    for predecessorIndex in range(len(predecessorPhonemeObjects)):
        phoneme = predecessorPhonemeObjects[predecessorIndex]
        # Collect dict of successor probabilities
        nextSuccessorProbabilities = successorProbabilities[predecessorIndex]
        # Iterate through successors, attaching each to the current phoneme
        for successorKey, successorPhoneme in successorPhonemeObjects.items():
            if successorKey in nextSuccessorProbabilities.keys():
                probability = nextSuccessorProbabilities[successorKey]
                predecessorPhonemeObjects[predecessorIndex].addSuccessor(successorPhoneme, probability)
            else:
                print("Error: Phoneme '" + phoneme.phonemeSymbol + "' successor '" + successorKey + "' not added; no probability provided.")

def normaliseSuccessorProbabilities(phonemeObjects):
    debugMode = False
    # Perform function for each node...    
    for phonemeKey in phonemeObjects:
        # Calculate sum of phoneme's successorProbabilities
        summedProbabilities = 0
        for successorProbability in phonemeObjects[phonemeKey].successorProbabilities.values():
            summedProbabilities += successorProbability
        if debugMode: print("Unnormalised probability for '" + phonemeObjects[phonemeKey].phonemeSymbol + "': " + str(summedProbabilities))
        # Divide each probability by this total
        if summedProbabilities != 0:
            for successorKey in phonemeObjects[phonemeKey].successorProbabilities:
                phonemeObjects[phonemeKey].successorProbabilities[successorKey] /= summedProbabilities
        if debugMode:
            summedProbabilities = 0
            for successorProbability in phonemeObjects[phonemeKey].successorProbabilities.values():
                summedProbabilities += successorProbability
            print("Normalised probability for '" + phonemeObjects[phonemeKey].phonemeSymbol + "': " + str(summedProbabilities))

def testSuccessorNormalisation(phoneme):
    debugMode = False
    cumulativeProb = 0
    keyCounter = 0
    for key in phoneme.successorProbabilities:
        cumulativeProb += phoneme.successorProbabilities[key]
        keyCounter += 1
    if debugMode: print("Phoneme '" + phoneme.phonemeSymbol + "' cumulativeProb: " + str(cumulativeProb) + " (from " + str(keyCounter) + " successors)")

## START OF PROGRAM ROUTINE ##
print("Markov Phonemes!\n")

# Phoneme Lists
vowelPhonemes = ['a', 'e', 'i', 'o', 'u', 'ae', 'ee', 'ie', 'oe', 'ue', 'oo', 'ar', 'ur', 'or', 'au', 'er', 'ow', 'oi', 'air', 'ear']
# Note: This contains graphemes which are not distinct phonemes, such as "c" which shares the phoneme "k"
consonantPhonemes = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z', 'wh', 'th', 'ch', 'sh', 'zh', 'ng']

debugMode = False

# Test variables
#vowelPhonemes = ['a', 'e', 'i']
#consonantPhonemes = ['b', 'd', 'k']

# All phoneme objects must be held together in a list
phonemeObjects = dict()

# Create vowel phoneme objects
createPhonemeObjects(phonemeObjects, vowelPhonemes, "v")

# Create consonant phoneme objects
createPhonemeObjects(phonemeObjects, consonantPhonemes, "c")

# Test the contents of the phoneme objects
if debugMode: printPhonemes(phonemeObjects, False)

# Create fully connected network
fullyConnectNetwork(phonemeObjects)

# Test the contents of the phoneme objects
if debugMode: printPhonemes(phonemeObjects, True)

# Remove connections between like-typed nodes
removeSameTypeConnections(phonemeObjects)

# Add empty-string phoneme as initiation point
addEmptyInitiator(phonemeObjects)

# Remove successor connections from network if they are zero-probability
pruneNetwork(phonemeObjects)

# Normalise successor probabilities for all nodes
normaliseSuccessorProbabilities(phonemeObjects)

# Print information on each phoneme in the network, including 
#printPhonemes(phonemeObjects, True)

# Generate words from network
totalWords = 20
generatedWords = []
generateWords(generatedWords, totalWords, phonemeObjects)

# Print successor-usage information for each phoneme
#printSuccessorUsages(phonemeObjects)

# Print generated list
printGeneratedWords(generatedWords)

# Generate a paragraph of given line length and character width
paragraphTotalLines = 5
paragraphWidth = 65
generateAndPrintParagraph(paragraphTotalLines, paragraphWidth, phonemeObjects)

# Test a distribution (iterations, min, max, mean, sd, normalisation)
#testNormalDist(5000, 0, 1, 0.5, 0.1, True)
#testNormalDist(5000, 0.5, 1, 0.8, 0.08, True)
#testNormalDist(5000, 0, 0.1, 0.01, 0.05, True)
#testNormalDist(5000, 0.5, 1.5, 1, 0.1, True)
#testNormalDist(5000, 0, 7, 2, 2, True)
#testNormalDist(5000, 3, 10, 4.5, 2, True)

