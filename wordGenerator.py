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


vowels = ['a', 'e', 'i', 'o', 'u']
consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']

vowelPhonemes = ['a', 'e', 'i', 'o', 'u', 'ae', 'ee', 'ie', 'oe', 'ue', 'oo', 'ar', 'ur', 'or', 'au', 'er', 'ow', 'oi', 'air', 'ear']
# Note: This contains graphemes which are not distinct phonemes, such as "c" which shares the phoneme "k"
consonantPhonemes = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z', 'wh', 'th', 'ch', 'sh', 'zh', 'ng']

# How many words should be generated in this batch?
totalWords = 10

# How should the process be configured?
print "Config:"
minWordLength = 3
print "Minimum word length: " + str(minWordLength)
maxWordLength = minWordLength + random.randint(0, 5)
print "Maximum word length: " + str(maxWordLength)
vowelProbability = round(random.uniform(0.4, 0.6), 2)
print "Vowel probability: " + str(vowelProbability) + " (0.4 to 0.6)"
streakModifier = round(random.uniform(0.35, 0.5), 2)
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
            vowelsIndex = random.randint(0, len(vowelPhonemes)-1)
            ##print "Vowel chosen (" + str(vowelsIndex) + ": " + vowelPhonemes[vowelsIndex] + ")"
            finishedWord += vowelPhonemes[vowelsIndex]
            # Continue vowel streak/break consonant streak
            wasVowel = True

            vowelStreak += 1
            consonantStreak = 0
        else:
            #print "Chose consonant"

            # Choose a consonant
            symbolString += "c"
            consonantsIndex = random.randint(0, len(consonantPhonemes)-1)
            ##print "Consonant chosen (" + str(consonantsIndex) + ": " + consonantPhonemes[consonantsIndex] + ")"
            finishedWord += consonantPhonemes[consonantsIndex]
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
