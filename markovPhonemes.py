# CMU Phoneme Dictionary:
# http://www.speech.cs.cmu.edu/cgi-bin/cmudict

import random
import string
import math
import Phoneme
import Language
import utils

def printGeneratedWords(generatedWords):
    print("\nGenerated words:")
    for nextWord in generatedWords:
        print("\t" + str.capitalize(nextWord))

# Generates and prints words to fill multiple lines of given character length, placing spaces between words and occassional full stops
def generateAndPrintParagraph(totalLines, lineWidth, language):
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
            # Generate sanother word for this line
            wordLength = int(utils.sampleTruncatedNormalDist(0, 7, 3, 2)) + 1
            # Generate word
            word, symbolString = language.generateWord(wordLength, measureWordLengthInPhonemes)
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

firstLang = Language.Language()
#secondLang = Language.Language()

# Generate words from network
totalWords = 20
generatedWords = []
firstLang.generateWords(generatedWords, totalWords)

# Print successor-usage information for each phoneme
#newLang.printSuccessorUsages()

# Print generated list
printGeneratedWords(generatedWords)

#generatedWords = []
#secondLang.generateWords(generatedWords, totalWords)
#printGeneratedWords(generatedWords)

# Generate a paragraph of given line length and character width
paragraphTotalLines = 5
paragraphWidth = 65
generateAndPrintParagraph(paragraphTotalLines, paragraphWidth, firstLang)
#generateAndPrintParagraph(paragraphTotalLines, paragraphWidth, secondLang)


# Test a distribution (iterations, min, max, mean, sd, normalisation)
# Note: These are some tests previously performed and left here in case revisiting them is useful (saving on some typing)
#utils.testNormalDist(5000, 0, 1, 0.5, 0.1, True)
#utils.testNormalDist(5000, 0.5, 1, 0.8, 0.08, True)
#utils.testNormalDist(5000, 0, 0.1, 0.01, 0.05, True)
#utils.testNormalDist(5000, 0.5, 1.5, 1, 0.1, True)
#utils.testNormalDist(5000, 0, 7, 2, 2, True)
#utils.testNormalDist(5000, 3, 10, 4.5, 2, True)
#utils.testNormalDist(5000, 0, 2, 1, 0.25, True)
# Testing attenuateSuccessorsOnType() like-typed attentuation
#utils.testNormalDist(5000, 0, 1, 0.05, 0.1, True)

# Testing generation of discrete distributions lists
# Params: totalIntervals, meanInterval, meanIntervalProb, falloff, isNormalised
# Test for 'early phoneme' positional probabilities
#utils.testHistogramFrequencyGeneration(10, 0, 1, 0.5, False, 3)

#newLang.printPhonemesInStoreFormat()
