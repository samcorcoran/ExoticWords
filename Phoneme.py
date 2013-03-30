import random

# A phoneme exists as a unit
class Phoneme:
    #Phonemes can be vowel phonemes or consonant phonemes

    # Phoneme symbol
    __phonemeSymbol = ""
    # Phoneme vowel/consonant indicator
    __phonemeType = ""
    # Phoneme example word - a human readable example of the phoneme
    __phonemeExample = ""
    # Successor phonemes - permissable nodes to follow this one, and their probabilities
    __successors = dict()
    __successorProbabilities = dict()
    # Predecessor phonemes - nodes which lead to this one
    __predecessors = dict()
    # Positional probability distribution
    #  a proportion-through-word converts to a list indices to retrieve interpolation between consecutive listed probabilities
    __positionalProbabilities = []
    # Possible Graphemes - written representations of phoneme
    __graphemes = []
    
    def __init__(self, newSymbol, newType, newExample, newPosProbs, newGraphemes):
        self.phonemeSymbol = newSymbol
        self.phonemeType = newType
        self.phonemeExample = newExample
        self.successors = dict()
        self.successorProbabilities = dict()
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
        # Construct ad-hoc CDF by iterating through normalized successors, stopping when sample falls inside an interval
        for phonemeKey in self.successors:
            # 'choose' phoneme for next interval, and if loop ends before break then last phoneme in successors dict will be chosen by default
            chosenPhoneme = self.successors[phonemeKey]
            cumulativeProbability += self.successorProbabilities[phonemeKey]
            if randSample < cumulativeProbability:
                # sample has fallen within the interval of this phoneme, thereby selecting it, so terminate search
                break
            ignoredItems += phonemeKey
        if debugMode: print("Current phoneme '" + self.phonemeSymbol + "' chose '" + chosenPhoneme.phonemeSymbol + "' cumProb: " + str(cumulativeProbability) + " > sample: " + str(randSample))
        if debugMode: print(" ignoredItems (" + str(len(ignoredItems)) + "): " + ", ".join(ignoredItems))
        # Return chosen successor
        return chosenPhoneme

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
            successorString += nextSuccessor + " "
        if verbose:
            print("\tSuccessors (" + str(len(self.successors)) + "): " + successorString)
        else:
            print("\tTotalSuccessors: " + str(len(self.successors)))
        print("\tGraphemes: " + "".join(self.graphemes))
        
        

        # Print the info message
        #print(nodeInfo)
