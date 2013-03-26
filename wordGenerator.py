# This version makes it uncommon to have double-vowel (or double-consonant) phonemes. Likelihood varies with streakModifier.

# Needed:
#  Some letters need to be considered less common

# Control by phoneme:
#  How rounded the phoneme is? How sharp? Short? Upwards inflexion, downwards inflexion?
#  http://www.lancsngfl.ac.uk/curriculum/literacy/lit_site/lit_sites/phonemes_001/
#  phoneme freq: http://myweb.tiscali.co.uk/wordscape/wordlist/phonfreq.html

import random
import string

print 'Word Generator!\n'


vowelsList = ['a', 'e', 'i', 'o', 'u']
consonantsList = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']




vowelPhonemes = ['a', 'e', 'i', 'o', 'u', 'ae', 'ee', 'ie', 'oe', 'ue', 'oo', 'ar', 'ur', 'or', 'au', 'er', 'ow', 'oi', 'air', 'ear']
# Note: This contains graphemes which are not distinct phonemes, such as "c" which shares the phoneme "k"
consonantPhonemes = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z', 'wh', 'th', 'ch', 'sh', 'zh', 'ng']

## Vowel Probabilities
vowelProbs = dict()
# Assign a probability to each vowelPhoneme
totalVowelProbs = 0
for nextPhoneme in vowelPhonemes:
    vowelProbs[nextPhoneme] = random.uniform(0.5, 1)
    totalVowelProbs += vowelProbs[nextPhoneme]
# Normalise vowel probabilities
for vowel in vowelProbs:
    vowelProbs[vowel] /= totalVowelProbs
#print vowelProbs

## Consonant Probabilities
consonantProbs = dict()
# Assign a probability to each vowelPhoneme
totalConsonantProbs = 0
for nextPhoneme in consonantPhonemes:
    consonantProbs[nextPhoneme] = random.random()
    totalConsonantProbs += consonantProbs[nextPhoneme]
# Normalise consonant probabilities
for cons in consonantProbs:
    consonantProbs[cons] /= totalVowelProbs
#print consonantProbs



# How many words should be generated in this batch?
totalWords = 20

# How should the process be configured?
print "Config:"
minWordLength = 3
print "Minimum word length: " + str(minWordLength)
maxWordLength = minWordLength + random.randint(0, 5)
print "Maximum word length: " + str(maxWordLength)
vowelProbability = round(random.uniform(0.4, 0.6), 2)
print "Vowel probability: " + str(vowelProbability) + " (0.4 to 0.6)"
streakModifier = round(random.uniform(0.2, 0.5), 2)

print "Streak modifier: " + str(streakModifier) + " (larger modifiers decrease the likelihood of double-selections)"

print "\nGenerated words: "
for i in range(totalWords):
    wordLength = random.randint(minWordLength, maxWordLength)

    consonantCounter = 0
    consonantStreak = 0
    vowelCounter = 0
    vowelStreak = 0

    probabilityString = ""
    symbolString = ""
    finishedWord = ""

    #wasVowel = False
    
    for x in range(wordLength):
        vowelChoiceRand = random.random()
        # Tip choice based on streaks (very unlikely to get same choice repeated)
        vowelChoiceRand -= consonantStreak * streakModifier
        vowelChoiceRand += vowelStreak * streakModifier
        #print "letter: " + str(x) + ": " + str(vowelStreak) + " " + str(consonantStreak)
        probabilityString += str(vowelChoiceRand)[:4] + ", "
        
        # Alternate between vowel phonemes and consonant phonemes
        if vowelChoiceRand < vowelProbability:
            #print "Chose vowel"
            # Choose a vowel
            symbolString += "v"
            
            chosenVowel = ""
            # Generate a random to sample from vowel pdf
            vSample = random.random()
            cumVowelProbs = 0
            # Move through vowel probs, checking if sample is within interval
            for vowel in vowelProbs:
                cumVowelProbs += vowelProbs[vowel]
                if vSample < cumVowelProbs:
                    # sample is within interval
                    chosenVowel = vowel
                    break
                        
            ##vowelsIndex = random.randint(0, len(vowelPhonemes)-1)

            ##print "Vowel chosen (" + str(vowelsIndex) + ": " + vowelPhonemes[vowelsIndex] + ")"
            
            finishedWord += chosenVowel

            # Continue vowel streak/break consonant streak
            wasVowel = True
            vowelStreak += 1
            consonantStreak = 0
        else:
            #print "Chose consonant"
            # Choose a consonant
            symbolString += "c"

            chosenConsonant = ""
            # Generate a random to sample from consonant pdf
            cSample = random.random()
            cumConsProbs = 0
            # Move through vowel probs, checking if sample is within interval
            for cons in consonantProbs:
                cumConsProbs += consonantProbs[cons]
                if cSample < cumConsProbs:
                    # sample is within interval
                    chosenConsonant = cons
                    break
            finishedWord += chosenConsonant
            # Continue vowel streak/break consonant streak
            wasVowel = False
            consonantStreak += 1
            vowelStreak = 0

    finishedWord = string.capitalize(finishedWord)
    # Print finished word
    print finishedWord 
    #print " (" + symbolString + ": " + probabilityString + ")"


# A phoneme exists as a unit 
class Phoneme:
    #Phonemes can be vowel phonemes or consonant phonemes
    __phonemeType = ""
    def __init__(self, newPhonemeType):
        self.phonemeType = newPhonemeType
        
    def getPhonemeType(self):
        return __self.phonemeType
