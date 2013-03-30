# CMU Phoneme Dictionary:
# http://www.speech.cs.cmu.edu/cgi-bin/cmudict

import random
import string
import Phoneme

def createPhonemeObjects(phonemeObjects, newPhonemes, phonemeType):
    debugMode = False
    # Create Phoneme objects from the incoming list
    print("\nCreating (" + str(len(newPhonemes)) + ") phoneme (" + phonemeType + ") objects...")
    # Loop through phonemes, creating objects
    for phoneme in newPhonemes:
        # Create a phoneme object
        nextPhoneme = Phoneme.Phoneme(phoneme, phonemeType, 'example '+phoneme, 1, [phoneme])
        if debugMode: print("nextPhoneme: " + nextPhoneme.phonemeSymbol)
        phonemeObjects.append(nextPhoneme)

def generateWords(generatedWords, totalWords, phonemeObjects):
    debugMode = False
    print("\nGenerating (" + str(totalWords) + ") words...")
    for nextWord in range(totalWords):
        if debugMode: print("Generating word " + nextWord)
        wordLength = random.randint(3,6)
        finishedWord = ""
        symbolString = ""
        latestPhoneme = phonemeObjects[0]
        for nextPhoneme in range(wordLength):
            # First phoneme is selected from entire set
            if finishedWord == "":
                chosenPhoneme = random.choice(phonemeObjects)
                finishedWord = chosenPhoneme.getRandomGrapheme()
                #finishedWord = chosenPhoneme.phonemeSymbol
                #finishedWord = chosenPhoneme.phonemeType
                latestPhoneme = chosenPhoneme
            else:
                if latestPhoneme.successors:
                    if debugMode: print("Successors: " + ", ".join(latestPhoneme.successors))
                    chosenPhoneme = latestPhoneme.successors[random.choice(list(latestPhoneme.successors.keys()))]
                    finishedWord += chosenPhoneme.getRandomGrapheme()
                    #finishedWord += chosenPhoneme.phonemeSymbol
                    #finishedWord += chosenPhoneme.phonemeType
                    latestPhoneme = chosenPhoneme
        generatedWords.append(finishedWord)

def printGeneratedWords(generatedWords):    
    print("\nGenerated (" + str(len(generatedWords)) + ") words:")
    for nextWord in generatedWords:
        print("\t" + str.capitalize(nextWord))

def printPhonemes(phonemeObjects, verbose):
    print("")
    print("Total phonemeObjects: " + str(len(phonemeObjects)))
    # For testing, print out contents of phoneme objects
    print("Testing phoneme objs:")
    for phonemeObj in phonemeObjects:
        phonemeObj.reportPhonemeInfo(verbose)

# Adds all phonemes as successors to all other phonemes with a probability of 1
def fullyConnectNetwork(phonemeObjects):
    debugMode = False
    print("\nFully connecting set of phoneme objects... (" + str(len(phonemeObjects)) + ")")
    for phonemeObj in phonemeObjects:
        # Give phonemeObj every other phonemeObject as a successor
        for nextSuccessor in phonemeObjects:
            # Add this object as successor
            if debugMode: print(phonemeObj.phonemeSymbol + " adding phoneme " + nextSuccessor.phonemeSymbol + " as successor.")
            phonemeObj.addSuccessor(nextSuccessor, 1.0)

# Removes from each node's listed successors 
def removeSameTypeConnections(phonemeObjects):
    debugMode = False
    for phonemeObj in phonemeObjects:
        if debugMode: print("'" + phonemeObj.phonemeSymbol + "(" + phonemeObj.phonemeType + ") being checked for like-typed successors.")
        # retain only differently typed objects
        keysForDeletion = []
        for key in phonemeObj.successors.keys():
            if phonemeObj.successors[key].phonemeType == phonemeObj.phonemeType:
                # remove phoneme item from dict
                keysForDeletion.append(key)
        if debugMode: print("...deleting keys: " + ",".join(keysForDeletion))
        for key in keysForDeletion:
            del phonemeObj.successors[key]
            del phonemeObj.successorProbabilities[key]
        if debugMode: print("...keys after deletion: " + ",".join(phonemeObj.successors.keys()))


print("Markov Phonemes!")

## Phoneme Lists
vowelPhonemes = ['a', 'e', 'i', 'o', 'u', 'ae', 'ee', 'ie', 'oe', 'ue', 'oo', 'ar', 'ur', 'or', 'au', 'er', 'ow', 'oi', 'air', 'ear']
# Note: This contains graphemes which are not distinct phonemes, such as "c" which shares the phoneme "k"
consonantPhonemes = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z', 'wh', 'th', 'ch', 'sh', 'zh', 'ng']

debugMode = False

#testVowelPhonemes = ['a', 'e', 'i']
#testConsonantPhonemes = ['b', 'd', 'k']

# All phoneme objects must be held together in a list
phonemeObjects = []

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

## Generate words from network
totalWords = 10
generatedWords = []
generateWords(generatedWords, totalWords, phonemeObjects)

# Print generated list
printGeneratedWords(generatedWords)
