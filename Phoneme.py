import random
import math

# A phoneme exists as a unit
class Phoneme:
    #Phonemes can be vowel phonemes or consonant phonemes

    # Phoneme symbol
    __phonemeSymbol = ""
    # Phoneme vowel/consonant indicator
    __phonemeType = ""
    # Phoneme example word - a human readable example of the phoneme
    __phonemeExample = ""
    # Standalone commonness of phoneme
    __baseProbability = 1
    # Successor phonemes - permissable nodes to follow this one, and their probabilities
    __successors = dict()
    __successorProbabilities = dict()
    # For diagnostic purposes, track how many times each successor has been selected for this phoneme
    __successorUsage = dict()
    # Predecessor phonemes - nodes which lead to this one
    __predecessors = dict()
    # Positional probability distribution
    #  a proportion-through-word converts to a list indices to retrieve interpolation between consecutive listed probabilities
    __positionalProbabilities = []
    # Possible Graphemes - written representations of phoneme
    __graphemes = []
    
    def __init__(self, newSymbol, newType, newExample, newProbability, newPosProbs, newGraphemes):
        self.phonemeSymbol = newSymbol
        self.phonemeType = newType
        self.phonemeExample = newExample
        self.baseProbability = newProbability
        self.successors = dict()
        self.successorProbabilities = dict()
        self.successorUsage = dict()
        self.predecessors = dict()
        self.positionalProbabilities = newPosProbs
        self.graphemes = newGraphemes
        
    def getPhonemeType(self):
        return __self.phonemeType

    def addSuccessor(self, newSuccessorPhoneme, selectionProbability):
        # Add phoneme to list of successors, keyed on its unique symbol
        self.successors[newSuccessorPhoneme.phonemeSymbol] = newSuccessorPhoneme
        # Use phoneme symbol as key for accessing probabilities also
        self.successorProbabilities[newSuccessorPhoneme.phonemeSymbol] = selectionProbability

    # Removes listed keys from node's permissable successor
    def removeSuccessors(self, keysForRemoval):
        debugMode = False
        for key in keysForRemoval:
            if debugMode: print("From node '" + self.phonemeSymbol + "', removing successor: " + key)
            del self.successors[key]
            if debugMode: print("From node '" + self.phonemeSymbol + "', removing successorProbability: " + key)
            del self.successorProbabilities[key]

    # Prompts phoneme to select a successor based on stored probabilities
    def chooseSuccessor(self, phonemePosition, wordLength):
        debugMode = False
        # Phoneme position within word is used for positional probabilities
        randSample = random.random()
        # Sum probabilities of possible successor phonemes
        cumulativeProbability = 0
        # Take any phoneme to act as temporary value
        chosenPhoneme = next(iter(self.successors.values()))
        ignoredItems = []
        adjustedSuccessorProbabilities = self.adjustProbabilities(phonemePosition, wordLength)
        # Construct ad-hoc CDF by iterating through normalized successor probabilities, stopping when sample falls inside an interval
        for phonemeKey in self.successors:
            # 'choose' phoneme for next interval, and if loop ends before break then last phoneme in successors dict will be chosen by default
            chosenPhoneme = self.successors[phonemeKey]
            cumulativeProbability += adjustedSuccessorProbabilities[phonemeKey]
            if randSample < cumulativeProbability:
                # sample has fallen within the interval of this phoneme, thereby selecting it, so terminate search
                break
            ignoredItems += phonemeKey
            
        # Record this choice for diagnostic purposes
        if not chosenPhoneme.phonemeSymbol in self.successorUsage:
            # First time successor was selected for this phoneme, so register one use
            self.successorUsage[chosenPhoneme.phonemeSymbol] = 1
        else:
            # Successor has been chosen before; counter is incremented
            self.successorUsage[chosenPhoneme.phonemeSymbol] += 1       
        
        if debugMode: print("Current phoneme '" + self.phonemeSymbol + "' chose '" + chosenPhoneme.phonemeSymbol + "' cumProb: " + str(cumulativeProbability) + " > sample: " + str(randSample))
        if debugMode: print(" ignoredItems (" + str(len(ignoredItems)) + "): " + ", ".join(ignoredItems))
        # Return chosen successor
        return chosenPhoneme

    # Incorporates variable factors into successor probabilities, such as positionalProbabilities, and returns new normalised probabilities
    def adjustProbabilities(self, phonemePosition, wordLength):
        adjustedProbabilities = dict()
        # Adjust each probability and store it in new dictionary
        cumulativeProbability = 0
        for successorKey, successorProb in self.successorProbabilities.items():
            adjustedProbabilities[successorKey] = successorProb * self.successors[successorKey].getPositionalModifier(phonemePosition, wordLength)
            cumulativeProbability += adjustedProbabilities[successorKey]
        # Normalise new probability values
        normalisingScale = cumulativeProbability / len(adjustedProbabilities.keys())
        for successorKey, adjustedProb in adjustedProbabilities.items():
            adjustedProb *= normalisingScale
        return adjustedProbabilities

    # Converts distance through word into sample from positionalProbabilities, normalised and ready to be applied
    def getPositionalModifier(self, phonemePosition, wordLength):
        if len(self.positionalProbabilities) != 0:
            # Calculate proportion of distance through word that this position appears at
            wordDistance = float(phonemePosition)/wordLength
            # Number of positionalProbability entries determines how 'wide' each interval is
            intervalWidth = 1.0/len(self.positionalProbabilities)
            # Determine which interval the wordDistance sample point falls into
            positionalIndex = int(math.floor(wordDistance/intervalWidth))
            # Fix final phoneme position so that it falls in the last interval
            if wordDistance == 1.0:
                positionalIndex = len(self.positionalProbabilities) - 1
            return self.positionalProbabilities[positionalIndex]
        else:
            # No positional probabilities, so return no-modifier of '1'
            return 1
        

    def getRandomGrapheme(self):
        debugMode = False
        chosenGrapheme = random.choice(self.graphemes)
        if debugMode: print("Grapheme '" + chosenGrapheme + "' selected")
        return chosenGrapheme

    def reportPhonemeInfo(self, verbose):
        # Print info about this node, with additional lines if verbosity was requested
        print("Phoneme: '" + self.phonemeSymbol + "'")
        if verbose: print("\tExample word: " + self.phonemeExample)
        print("\tType: " + self.phonemeType)
        successorString = ""
        for nextSuccessor in self.successors:
            successorString += nextSuccessor + "(" + str(round(self.successorProbabilities[nextSuccessor], 2)) + ") "
        if verbose:
            print("\tSuccessors (" + str(len(self.successors)) + "): " + successorString)
        else:
            print("\tTotalSuccessors: " + str(len(self.successors)))
        print("\tGraphemes: " + "".join(self.graphemes))

    # For each node, provide info about how much it was used
    def reportPhonemeSuccessorUsage(self):
        # Iterate through successor usage stats to determine percentage uses
        totalSuccessors = 0
        for nextSuccessor in self.successorUsage:
            totalSuccessors += self.successorUsage[nextSuccessor]
        print("Phoneme '" + self.phonemeSymbol + "' successors (" + str(totalSuccessors) + " cases):")
        deviation = []
        # Safe-guard against division-by-zero; 'no successors' can be reported immediately
        if totalSuccessors > 0:
            for nextSuccessor in self.successorProbabilities:
                successorProbability = self.successorProbabilities[nextSuccessor]
                successorUses = 0
                # If successor was used then obtain accurate number of uses
                if nextSuccessor in self.successorUsage:
                    successorUses = self.successorUsage[nextSuccessor]
                # Calculate observed frequency
                observedFrequency = float(successorUses) / totalSuccessors
                # Print info about probability versus frequency
                print("\t" + nextSuccessor + " (p = " + str(round(successorProbability, 2)) + ") total uses: " + str(successorUses) + " (" + str(round(observedFrequency, 2)) + ")")
                # Calculate standardised deviation between this successor's expected frequency and observed frequency
                nextDeviation = (observedFrequency-successorProbability)/successorProbability                
                deviation.append(nextDeviation)
            # Display standard deviation for this phoneme's successors from their intended probabilities (i.e. frequencies)
            print("\tDeviation: " + str(round(sum(deviation)/len(deviation), 2)))
        else:
            print("\tNo successors.")
        

        
