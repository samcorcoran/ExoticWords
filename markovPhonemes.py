# CMU Phoneme Dictionary:
# http://www.speech.cs.cmu.edu/cgi-bin/cmudict

import random
import string
import Phoneme

def createPhonemeObjects(phonemeObjects, newPhonemes, phonemeType):
    debugMode = False
    # Create Phoneme objects from the incoming list
    print("Creating (" + str(len(newPhonemes)) + ") phoneme (" + phonemeType + ") objects...")
    # Loop through phonemes, creating objects
    for phoneme in newPhonemes:
        # Create a phoneme object
        baseProbability = random.random()
        nextPhoneme = Phoneme.Phoneme(phoneme, phonemeType, 'example '+phoneme, baseProbability, 1, [phoneme])
        if debugMode: print("nextPhoneme: " + nextPhoneme.phonemeSymbol)
        phonemeObjects[nextPhoneme.phonemeSymbol] = nextPhoneme

def generateWords(generatedWords, totalWords, phonemeObjects):
    debugMode = False
    print("Generating (" + str(totalWords) + ") words...")
    for nextWordIndex in range(totalWords):
        if debugMode: print("Generating word " + nextWord)
        wordLength = random.randint(3,6)
        finishedWord = ""
        symbolString = ""
        # The empty-string phoneme is used to initiate process
        latestPhoneme = phonemeObjects[""]
        for nextPhonemeIndex in range(wordLength):
            if latestPhoneme.successors:
                if debugMode: print("Successors: " + ", ".join(latestPhoneme.successors))
                chosenPhoneme = latestPhoneme.chooseSuccessor(len(finishedWord), wordLength)
                finishedWord += chosenPhoneme.getRandomGrapheme()
                #finishedWord += chosenPhoneme.phonemeSymbol
                #finishedWord += chosenPhoneme.phonemeType
                latestPhoneme = chosenPhoneme
            else:
                print("Error: '" + latestPhoneme.phonemeSymbol + "' has no successors (failed on phoneme " + str(nextPhonemeIndex + 1) + " of " + str(wordLength) + ")") 
        generatedWords.append(finishedWord)

def printGeneratedWords(generatedWords):    
    print("\nGenerated words:")
    for nextWord in generatedWords:
        print("\t" + str.capitalize(nextWord))

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
            # Determine whether successor will be popular or regular
            successorProbability = 0
            popularityThreshold = 0.9
            rand = random.random()
            if rand > popularityThreshold:
                # successor is popular, high probability
                successorProbability = random.uniform(0.8, 1)
            elif rand > 0.6:
                # successor is regular, low probability
                successorProbability = random.uniform(0, 0.1)
            else:
                # designated non-successor, zero-probability
                successorProbability = 0
                
            phonemeObj.addSuccessor(nextSuccessor, successorProbability)

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

def addEmptyInitiator(phonemeObjects):
    print("Adding empty initiator phoneme...")
    # Create empty-phoneme object
    emptySymbol = ""
    emptyType = "none"
    emptyExample = "not applicable"
    baseProbability = 0
    positionalProbability = 1
    emptyGraphemes = [""]
    emptyInitiator = Phoneme.Phoneme(emptySymbol, emptyType, emptyExample, baseProbability, positionalProbability, emptyGraphemes)
    # Provide all phonemes as successors of the initiator with equal probability
    baseProbability = 1.0
    for phonemeSymbol in phonemeObjects:
        emptyInitiator.addSuccessor(phonemeObjects[phonemeSymbol], baseProbability)
    # Add the empty initiator to dictionary
    phonemeObjects[""] = emptyInitiator

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

#testVowelPhonemes = ['a', 'e', 'i']
#testConsonantPhonemes = ['b', 'd', 'k']

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
totalWords = 20000
generatedWords = []
generateWords(generatedWords, totalWords, phonemeObjects)

# Print successor-usage information for each phoneme
printSuccessorUsages(phonemeObjects)

# Print generated list
#printGeneratedWords(generatedWords)

