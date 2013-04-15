# Needed:
#  - More interesting way of determining how common phonemes are. 
#  - Create function for handling probability assignment. Break phonemes into smaller groups, grouped by shared factor or by 
#  - Current vowel/consonant choice is made first. Really, permissable phonemes should be considered for each selection, decisions weighted by probabilities 
#    ~ vowel probabilities should be higher if current is consonant and vice versa


# Control by phoneme:
#  How rounded the phoneme is? How sharp? Short? Upwards inflexion, downwards inflexion?
#  http://www.lancsngfl.ac.uk/curriculum/literacy/lit_site/lit_sites/phonemes_001/
#  phoneme freq: http://myweb.tiscali.co.uk/wordscape/wordlist/phonfreq.html
#  Permissable combination of phonemes in a language: http://en.wikipedia.org/wiki/Phonotactics
#  Phonotactic library: http://www.iphod.com/
#  CMUPD is a phoneme list/key system which uses combinations of alphabetic characters to represent phonemes
#  Phonemes coding for multiple graphemes: http://en.wikipedia.org/wiki/Phonemic_orthography
#   Different speech sounds representing the same phoneme are allophones: http://en.wikipedia.org/wiki/Allophone
#  Ranking phones by aplitude: http://en.wikipedia.org/wiki/Sonority_hierarchy (also lists various consonant types)

# (http://en.wikipedia.org/wiki/Manner_of_articulation)
#Manners of articulation: 
# Obstruent (obstructed airflow, air pressure in vocal tract) 
#  Stop (p t k b d g)
#  Affricate
#  Fricative
#   Sibilant        
# Sonorant (continuous, non-turbulant airflow in vocal tract)
#  Nasal
#  Flap/Tap
#  Approximant
#   Liquid
#  Vowel
#   SemiVowel
# Lateral
# Trill



import random
import string

print("Word Generator!\n")


## How many words should be generated in this batch?
totalWords = 15

## How should the process be configured?
print("Config:")

minWordLength = 3
print("Minimum word length: " + str(minWordLength))

upperWordLengthBound = 8
maxWordLength = minWordLength + random.randint(0, upperWordLengthBound-minWordLength)
print("Maximum word length: " + str(maxWordLength))

vowelProbMin = 0.4
vowelProbMax = 0.6
vowelProbability = round(random.uniform(vowelProbMin, vowelProbMax), 2)
print("Vowel probability: " + str(vowelProbability) + " (" + str(vowelProbMin) + " to " + str(vowelProbMax) + ")")

streakModMin = 0.2
streakModMax = 0.5
streakModifier = round(random.uniform(streakModMin, streakModMax), 2)
print("Streak modifier: " + str(streakModifier) + " (" + str(streakModMin) + " to " + str(streakModMax) + ", reduces double selections)")

# likelihood of vowel popularity
vowelPopularityProb = 0.1
# popular vowels
minPopularVowelProb = 0.8
maxPopularVowelProb = 1.0
# regular vowels
minRegularVowelProb = 0
maxRegularVowelProb = 0.2
print("Vowel probability intervals... popular(" + str(vowelPopularityProb) + "): " + str(minPopularVowelProb) + " to " + str(maxPopularVowelProb) + ", regular: " + str(minRegularVowelProb) + " to " + str(maxRegularVowelProb))

# likelihood of consonant popularity
consPopularityProb = 0.1
# popular consonants
minPopularConsProb = 0.8
maxPopularConsProb = 1.0
# regular consonants
minRegularConsProb = 0
maxRegularConsProb = 0.1
print("Consonant probability intervals... popular(" + str(consPopularityProb) + "): " + str(minPopularConsProb) + " to " + str(maxPopularConsProb) + ", regular: " + str(minRegularConsProb) + " to " + str(maxRegularConsProb))

print("")

## Phoneme Lists
vowelPhonemes = ['a', 'e', 'i', 'o', 'u', 'ae', 'ee', 'ie', 'oe', 'ue', 'oo', 'ar', 'ur', 'or', 'au', 'er', 'ow', 'oi', 'air', 'ear']
# Note: This contains graphemes which are not distinct phonemes, such as "c" which shares the phoneme "k"
consonantPhonemes = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z', 'wh', 'th', 'ch', 'sh', 'zh', 'ng']

## Vowel Probabilities
vowelProbs = dict()
# Assign a probability to each vowelPhoneme
totalVowelProbs = 0
# Track high-probability vowel phonemes
popularVowels = ""
for nextPhoneme in vowelPhonemes:
    # Give a small percentage of vowel phonemes high probabilities
    if random.random() < vowelPopularityProb:
        vowelProbs[nextPhoneme] = random.uniform(minPopularVowelProb, maxPopularVowelProb)
        popularVowels += nextPhoneme + ", "
    else:
        vowelProbs[nextPhoneme] = random.uniform(minRegularVowelProb, maxRegularVowelProb)
    totalVowelProbs += vowelProbs[nextPhoneme]
# Normalise vowel probabilities
for vowel in vowelProbs:
    vowelProbs[vowel] /= totalVowelProbs
#print vowelProbs
#print "Total vowel probs: " + str( sum(vowelProbs.values()) )
print("Popular vowels: " + popularVowels)

## Consonant Probabilities
consonantProbs = dict()
# Assign a probability to each vowelPhoneme
totalConsonantProbs = 0
# Track high-probability consonant phonemes
popularConsonants = ""
for nextPhoneme in consonantPhonemes:
    # Give a small percentage of consonant phonemes high probabilities
    if random.random() < consPopularityProb:
        consonantProbs[nextPhoneme] = random.uniform(minPopularConsProb, maxPopularConsProb)
        popularConsonants += nextPhoneme + " "
    else:
        consonantProbs[nextPhoneme] = random.uniform(minRegularConsProb, maxRegularConsProb)
    totalConsonantProbs += consonantProbs[nextPhoneme]
# Normalise consonant probabilities
for cons in consonantProbs:
    consonantProbs[cons] /= totalConsonantProbs
#print consonantProbs
#print "Total Cons probs: " + str( sum(consonantProbs.values()) )
print("Popular consonants: " + popularConsonants)



print("\nGenerated words: ")
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
                chosenVowel = vowel
                cumVowelProbs += vowelProbs[vowel]
                if vSample < cumVowelProbs:
                    # sample is within interval, retain this vowel as chosen
                    break
            if chosenVowel == "":
                print("ERROR: empty vowel choice! Word so far: " + finishedWord)
                print("  vSample: " + str(vSample) + ", cumVowelProbs: " + str(cumVowelProbs))
            ##vowelsIndex = random.randint(0, len(vowelPhonemes)-1)

            ##print("Vowel chosen (" + str(vowelsIndex) + ": " + vowelPhonemes[vowelsIndex] + ")")
            
            finishedWord += chosenVowel

            # Continue vowel streak/break consonant streak
            wasVowel = True
            vowelStreak += 1
            consonantStreak = 0
        else:
            #print("Chose consonant")
            # Choose a consonant
            symbolString += "c"

            chosenConsonant = ""
            # Generate a random to sample from consonant pdf
            cSample = random.random()
            cumConsProbs = 0
            # Move through vowel probs, checking if sample is within interval
            for cons in consonantProbs:
                chosenConsonant = cons
                cumConsProbs += consonantProbs[cons]
                if cSample < cumConsProbs:
                    # sample is within interval, retain this consonant as chosen
                    break
            if chosenConsonant == "":
                print("ERROR: empty consonant choice! Word so far: " + finishedWord)
                print("  cSample: " + str(cSample) + ", cumConsProbs: " + str(cumConsProbs))
            finishedWord += chosenConsonant
            # Continue vowel streak/break consonant streak
            wasVowel = False
            consonantStreak += 1
            vowelStreak = 0

    finishedWord = str.capitalize(finishedWord)
    # Print finished word
    print(finishedWord)
    #print(" (" + symbolString + ": " + probabilityString + ")")
