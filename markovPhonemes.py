# CMU Phoneme Dictionary:
# http://www.speech.cs.cmu.edu/cgi-bin/cmudict

import random
import string
import Phoneme

def createPhonemeObjects(phonemeObjects, newPhonemes, phonemeType):
    debugMode = False
    # Create Phoneme objects from the incoming list
    print("\nCreating vowel phoneme objects...")
    # Loop through phonemes, creating objects
    for phoneme in newPhonemes:
        # Create a phoneme object
        nextPhoneme = Phoneme.Phoneme(phoneme, phonemeType, 'example '+phoneme, 1, phoneme)
        if debugMode: print("nextPhoneme: " + nextPhoneme.phonemeSymbol)
        phonemeObjects.append(nextPhoneme)

def generateWords(generatedWords, totalWords, phonemeObjects):
    debugMode = False
    print("\nGenerating words...")
    for nextWord in range(totalWords):
        if debugMode: print("Generating word " + nextWord)
        wordLength = random.randint(3,6)
        finishedWord = ""
        symbolString = ""
        for nextPhoneme in range(wordLength):
            nextGrapheme = ""
            # First phoneme is selected from entire set
            if finishedWord == "":
                chosenPhoneme = random.choice(phonemeObjects)
                finishedWord = chosenPhoneme.getRandomGrapheme()
            else:
                chosenPhoneme = random.choice(phonemeObjects)
                finishedWord += chosenPhoneme.getRandomGrapheme()
        generatedWords.append(finishedWord)

def printGeneratedWords(generatedWords):    
    print("\nGenerated words (" + str(len(generatedWords)) + "):")
    for nextWord in generatedWords:
        print("\t" + nextWord)

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

## Generate words from network
totalWords = 10
generatedWords = []
generateWords(generatedWords, totalWords, phonemeObjects)

# Print generated list
printGeneratedWords(generatedWords)
