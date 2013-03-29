# CMU Phoneme Dictionary:
# http://www.speech.cs.cmu.edu/cgi-bin/cmudict

import random
import string
import Phoneme

def printPhonemes(phonemeObjects, verbose):
    print("")
    print("Total phonemeObjects: " + str(len(phonemeObjects)))
    # For testing, print out contents of phoneme objects
    print("Testing phone objs:")
    for phonemeObj in phonemeObjects:
        phonemeObj.reportContents(verbose)

# Adds all phonemes as successors to all other phonemes with a probability of 1
def fullyConnectNetwork(phonemeObjects):
    print("")
    print("Fully connecting set of phoneme objects...")
    for phonemeObj in phonemeObjects:
        # Give phonemeObj every other phonemeObject as a successor
        for nextSuccessor in phonemeObjects:
            if phonemeObj == nextSuccessor:
                # Object should not have itself as successor
                print(phonemeObj.phonemeSymbol + " ...not adding self as successor.")
            else:
                # Add this object as successor
                print(phonemeObj.phonemeSymbol + " adding phoneme " + nextSuccessor.phonemeSymbol + " as successor.")
                # Add 
                phonemeObj.addSuccessor(nextSuccessor, 1.0)

## Phoneme Lists
vowelPhonemes = ['a', 'e', 'i', 'o', 'u', 'ae', 'ee', 'ie', 'oe', 'ue', 'oo', 'ar', 'ur', 'or', 'au', 'er', 'ow', 'oi', 'air', 'ear']
# Note: This contains graphemes which are not distinct phonemes, such as "c" which shares the phoneme "k"
consonantPhonemes = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z', 'wh', 'th', 'ch', 'sh', 'zh', 'ng']

print("Markov Phonemes!")


testVowelPhonemes = ['a', 'e', 'i']
testConsonantPhonemes = ['b', 'd', 'k']
# Add vowelPhonemes as objects
vowelPhonemeObjects = []
# Loop through phonemes, creating objects
for phoneme in testVowelPhonemes:
    # Create a phoneme object
    nextPhoneme = Phoneme.Phoneme(phoneme, 'v', 'example '+phoneme, 1, phoneme)
    vowelPhonemeObjects.append(nextPhoneme)

# Test the contents of the phoneme objects
printPhonemes(vowelPhonemeObjects, False)

# Create fully connected network
fullyConnectNetwork(vowelPhonemeObjects)

# Test the contents of the phoneme objects
printPhonemes(vowelPhonemeObjects, True)


