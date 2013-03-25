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


totalWords = 10

print "Config:"
minWordLength = 3
print "Minimum word length: " + str(minWordLength)
maxWordLength = minWordLength + random.randint(0, 5)
print "Maximum word length: " + str(maxWordLength)
vowelProbability = 0.5
print "Starting vowel probability: " + str(vowelProbability)

print "\nGenerated words: " 
for i in range(totalWords):
    wordLength = random.randint(minWordLength, maxWordLength)

    consonantCounter = 0
    consonantStreak = 0
    vowelCounter = 0
    vowelStreak = 0

    symbolString = ""
    finishedWord = ""

    wasVowel = False
    randomNum = random.random()
    if randomNum <= 0.5:
        wasVowel = True

    for x in range(wordLength):
        # Alternate between vowel phonemes and consonant phonemes
        if wasVowel == False:
            #print "Chose vowel"
            # Choose a vowel
            symbolString += "v"
            vowelsIndex = random.randint(0, len(vowelPhonemes)-1)
            ##print "Vowel chosen (" + str(vowelsIndex) + ": " + vowelPhonemes[vowelsIndex] + ")" 
            finishedWord += vowelPhonemes[vowelsIndex]
            # Continue vowel streak/break consonant streak
            wasVowel = True
        else:
            #print "Chose consonant"
            # Choose a consonant
            symbolString += "c"
            consonantsIndex = random.randint(0, len(consonantPhonemes)-1)
            ##print "Consonant chosen (" + str(consonantsIndex) + ": " + consonantPhonemes[consonantsIndex] + ")" 
            finishedWord += consonantPhonemes[consonantsIndex]
            # Continue vowel streak/break consonant streak
            wasVowel = False

    finishedWord = string.capitalize(finishedWord)
    # Print finished word
    print finishedWord
