import random
import string
import math
import Phoneme
import utils

# A language object holds a single generation configuration and produces themed words
class Language:

    # Language initialises by setting configuration
    def __init__(self):
        print("Initialising Language...")
        # All phoneme objects must be held together in a list
        self.phonemeObjects = dict()
        self.setupLanguage(debugMode = False)
        
    def setupLanguage(self, debugMode):      
        # Create phoneme objects from file representations
        self.createPhonemesFromFile("phonemeStoreBasic.txt")

        # Assign random base probabilities
        self.grantPhonemesRandomBaseProbabilities()

        # Assigns random positional probabilities
        self.grantPhonemesRandomPositionalProbabilities()

        # Test the contents of the phoneme objects
        if debugMode: printPhonemes(False)

        # Create fully connected network
        self.fullyConnectNetwork()

        # Test the contents of the phoneme objects
        if debugMode: printPhonemes(True)

        # Remove connections between like-typed nodes
        #self.removeSameTypeConnections()

        # Reduce probability for connections between like-typed nodes
        self.attenuateSuccessorsOnType()

        # Add empty-string phoneme as initiation point
        self.addEmptyInitiator(self.phonemeObjects)

        # Remove successor connections from network if they are zero-probability
        self.pruneNetwork()

        # Normalise successor probabilities for all nodes
        self.normaliseSuccessorProbabilities()

        # Print information on each phoneme in the network, including
        if debugMode: self.printPhonemes(True)
        
    # Loads file at filepath, parses for phonemes info and adds Phoneme objects to ongoing dictionary
    def createPhonemesFromFile(self, filePath):
        print("Loading phonemes from file (" + filePath + "):")
        file = open(filePath, "r")
        # Flag indicates whether info for a phoneme is currently being parsed
        processingPhoneme = False
        # During parsing phoneme info must be held
        currentSymbol, currentType, currentExample, currentGraphemes = "", "", "", ""
        #Iterate through lines of file
        for line in file.readlines():
            # Remove and trailing whitespace
            line = string.strip(line)
            if processingPhoneme:
                # Check if phoneme ends on this line
                if line == "<END PHONEME>":
                    # Create and add Phoneme object if enough information was collected
                    if not (currentSymbol == "" or currentType == "" or currentExample == "" or currentGraphemes == ""):
                        # Phoneme information is complete; creation can proceed
                        graphemeParts = string.split(currentGraphemes, ',')
                        graphemes = []
                        for grapheme in graphemeParts:
                            # Convert each comma separated grapheme into a tuple with a probability
                            graphemes.append((grapheme, 1))
                        # Create grapheme object
                        newPhoneme = Phoneme.Phoneme(currentSymbol, currentType, currentExample, 1, [], graphemes)
                        # Add grapheme object to dict
                        self.phonemeObjects[newPhoneme.phonemeSymbol] = newPhoneme
                    # Even if no phoneme is created, end tag ends processing of this phoneme
                    processingPhoneme = False
                elif line == "<START PHONEME>":
                    # This should not have been encountered as no end tag as yet been encountered
                    print("Error: Encountered second <START PHONEME> tag before end tag was found.")
                    # Re-initialise collected info, ready for new collection
                    currentSymbol, currentType, currentExample, currentGraphemes = "", "", "", ""
                else:
                    # Attempt to collect phoneme information from this line, splitting on its first colon (enforced by maxSplits)
                    parts = string.split(line, ':' , 1)
                    if parts[0] == "phonemeSymbol":
                        currentSymbol = parts[1]
                    elif parts[0] == "phonemeType":
                        currentType = parts[1]
                    elif parts[0] == "phonemeExample":
                        currentExample = parts[1]
                    elif parts[0] == "graphemes":
                        currentGraphemes = parts[1]
            else:
                # Check if a phoneme begins on this line
                if line == "<START PHONEME>":
                    processingPhoneme = True
                elif line == "<END PHONEME>":
                    # This should not have been encountered as no start tag as yet been encountered
                    print("Error: Encountered <END PHONEME> tag before start tag was found.")
                    # Assigns each phoneme a random list of positional probabilities

    def grantPhonemesRandomPositionalProbabilities(self):
        for phonemeKey in self.phonemeObjects:
            # Positional probabilities apply modifiers that incline certain phonemes towards certain positional occurrences
            positionalProbabilities = []
            positionalRand = random.random()
            if positionalRand > 0.7:
                # Phoneme will be an 'late' one, appearing more frequently at the end of a word
                print("Phoneme '" + self.phonemeObjects[phonemeKey].phonemeSymbol + "' is late")
                positionalProbabilities = utils.generateHistogramFrequencies(10, 9, 1, 0.5, False)
            elif positionalRand < 0.3:
                # Phoneme will be an 'early' one, appearing more frequently at the beginning of a word
                positionalProbabilities = utils.generateHistogramFrequencies(10, 0, 1, 0.5, False)
                print("Phoneme '" + self.phonemeObjects[phonemeKey].phonemeSymbol + "' is early")
            else:
                # Phoneme will be given an even likelihood to occur throughout a word
                positionalProbabilities = []
            # Assign the positional probabilities to the phoneme object            
            self.phonemeObjects[phonemeKey].positionalProbabilities = positionalProbabilities

    # Assigns each phoneme a new baseProbability, 
    def grantPhonemesRandomBaseProbabilities(self):
        for phonemeKey in self.phonemeObjects:
            self.phonemeObjects[phonemeKey].baseProbability = utils.determinePopularityProbability()

    # Prints information for each of language's phoneme objects
    def printPhonemes(self, verbose):
        print("Total phonemeObjects: " + str(len(phonemeObjects)))
        # For testing, print out contents of phoneme objects
        print("Testing phoneme objs:")
        for phonemeKey in self.phonemeObjects:
            phonemeObjects[phonemeKey].reportPhonemeInfo(verbose)

    # Adds all phonemes as successors to all other phonemes with a probability of 1
    def fullyConnectNetwork(self):
        debugMode = False
        print("Fully connecting set of (" + str(len(self.phonemeObjects)) + ") phoneme objects...")
        for phonemeKey, phonemeObj in self.phonemeObjects.items():
            # Give phonemeObj every other phonemeObject as a successor
            for successorKey, successorObj in self.phonemeObjects.items():
                # Add this object as successor
                if debugMode: print(phonemeObj.phonemeSymbol + " adding phoneme " + successorObj.phonemeSymbol + " as successor.")
                successorProbability = successorObj.getNoiseAlteredBaseProb()
                phonemeObj.addSuccessor(successorObj, successorProbability)

    # Removes from each node's listed successors
    def removeSameTypeConnections(self):
        print("Removing same-typed successions...")
        debugMode = False
        for key in self.phonemeObjects.keys():
            phonemeObj = self.phonemeObjects[key]
            if debugMode: print("'" + phonemeObj.phonemeSymbol + "(" + phonemeObj.phonemeType + ") being checked for like-typed successors.")
            # retain only differently typed objects
            keysForRemoval = []
            # accumulate probabilities of retained objects
            cumulativeProb = 0
            for key in phonemeObj.successors.keys():
                if phonemeObj.successors[key].phonemeType == phonemeObj.phonemeType:
                    # remove phoneme item from dict
                    keysForRemoval.append(key)
                else:
                    # add retained keys probability to cumulative
                    cumulativeProb += phonemeObj.successorProbabilities[key]
            if debugMode: print("...deleting keys: " + ",".join(keysForDeletion))
            # Prompt node to eject keys from successor dicts
            phonemeObj.removeSuccessors(keysForRemoval)
            if debugMode: print("...keys after deletion: " + ",".join(phonemeObj.successors.keys()))

    # Given a dict of phonemes, each phoneme's successor probabilities are modifed based on the successor's phonemeType
    def attenuateSuccessorsOnType(self):
        for key, phoneme in self.phonemeObjects.items():
            # Each successor must have its probability review
            for successorKey, successor in phoneme.successors.items():
                # Modifier is initially neutral
                modifier = 1
                # Compare phoneme types
                if phoneme.phonemeType == successor.phonemeType:
                    # Phonemes are same type; probability should be drastically reduced
                    modifier = utils.sampleTruncatedNormalDist(0, 1, 0.05, 0.1)
                phoneme.successorProbabilities[successorKey] *= modifier

    # Initiator phoneme is the starting state for word generation, with all possible first-phonemes as its successors
    def addEmptyInitiator(self, successorObjects):
        print("Adding empty initiator phoneme...")
        # Create empty-phoneme object
        emptySymbol = ""
        emptyType = "initiator"
        emptyExample = "not applicable"
        baseProbability = 0
        positionalProbability = 1
        emptyGraphemes = [("", utils.determinePopularityProbability())]
        emptyInitiator = Phoneme.Phoneme(emptySymbol, emptyType, emptyExample, baseProbability, positionalProbability, emptyGraphemes)
        # Provide all phonemes as successors of the initiator with equal probability
        baseProbability = 1.0
        # Probability that for each successor stored in dict, keyed on successor phonemeSymbol
        successorProbabilities = dict()
        for successorKey in successorObjects:
            successorProbabilities[successorKey] = successorObjects[successorKey].getNoiseAlteredBaseProb()
        # Place empty initiator as single phoneme in list,
        # Corresponding list with recently created dict of successor probabilities also placed in list
        self.addSequenceOfSuccessors([emptyInitiator], [successorProbabilities], successorObjects)
        # Add the empty initiator to dictionary
        self.phonemeObjects[""] = emptyInitiator

    # Given list of phoneme takes all in given dict as successors
    # For use in cases such as the emptyInitiator, which should have all phoneme objects as successors
    # - predecessorPhonemeObjects: list of phoneme objects
    # - successorProbabilities: list (corresponding with predecessor list) of dicts, containing probabilities keyed on successor phonemeSymbols
    # - successorPhonemeObjects: dict of phonemes using symbol as key
    def addSequenceOfSuccessors(self, predecessorPhonemeObjects, successorProbabilities, successorPhonemeObjects):
        for predecessorIndex in range(len(predecessorPhonemeObjects)):
            phoneme = predecessorPhonemeObjects[predecessorIndex]
            # Collect dict of successor probabilities
            nextSuccessorProbabilities = successorProbabilities[predecessorIndex]
            # Iterate through successors, attaching each to the current phoneme
            for successorKey, successorPhoneme in successorPhonemeObjects.items():
                if successorKey in nextSuccessorProbabilities.keys():
                    probability = nextSuccessorProbabilities[successorKey]
                    predecessorPhonemeObjects[predecessorIndex].addSuccessor(successorPhoneme, probability)
                else:
                    print("Error: Phoneme '" + phoneme.phonemeSymbol + "' successor '" + successorKey + "' not added; no probability provided.")

    # Remove zero-probability successors
    def pruneNetwork(self):
        debugMode = False
        print("Pruning network of zero-probability successions...")
        for phonemeKey in self.phonemeObjects:
            keysForRemoval = []
            for successorKey in self.phonemeObjects[phonemeKey].successors:
                # Check probability of successor
                if self.phonemeObjects[phonemeKey].successorProbabilities[successorKey] == 0:
                    # Add to removal list
                    keysForRemoval.append(successorKey)
            if debugMode: print("Phoneme '" + phonemeKey + "' is losing " + str(len(keysForRemoval)) + " of " + str(len(phonemeObjects[phonemeKey].successors.keys())) + " successors.")
            self.phonemeObjects[phonemeKey].removeSuccessors(keysForRemoval)

    def normaliseSuccessorProbabilities(self):
        debugMode = False
        # Perform function for each node...
        for phonemeKey in self.phonemeObjects:
            # Calculate sum of phoneme's successorProbabilities
            summedProbabilities = 0
            for successorProbability in self.phonemeObjects[phonemeKey].successorProbabilities.values():
                summedProbabilities += successorProbability
            if debugMode: print("Unnormalised probability for '" + phonemeObjects[phonemeKey].phonemeSymbol + "': " + str(summedProbabilities))
            # Divide each probability by this total
            if summedProbabilities != 0:
                for successorKey in self.phonemeObjects[phonemeKey].successorProbabilities:
                    self.phonemeObjects[phonemeKey].successorProbabilities[successorKey] /= summedProbabilities
            if debugMode:
                summedProbabilities = 0
                for successorProbability in self.phonemeObjects[phonemeKey].successorProbabilities.values():
                    summedProbabilities += successorProbability
                print("Normalised probability for '" + self.phonemeObjects[phonemeKey].phonemeSymbol + "': " + str(summedProbabilities))

    def testSuccessorNormalisation(phoneme):
        debugMode = False
        cumulativeProb = 0
        keyCounter = 0
        for key in phoneme.successorProbabilities:
            cumulativeProb += phoneme.successorProbabilities[key]
            keyCounter += 1
        if debugMode: print("Phoneme '" + phoneme.phonemeSymbol + "' cumulativeProb: " + str(cumulativeProb) + " (from " + str(keyCounter) + " successors)")

    # Generate a list of words
    def generateWords(self, generatedWords, totalWords):
        debugMode = False
        print("Generating (" + str(totalWords) + ") words...")
        for nextWordIndex in range(totalWords):
            if debugMode: print("Generating word " + str(nextWordIndex))
            wordLength = int(utils.sampleTruncatedNormalDist(3, 10, 4.5, 2))
            # Indicate if word length will be calculted in characters or phonemes
            measureLengthInPhonemes = False
            # Call generator function
            finishedWord, symbolString = self.generateWord(wordLength, measureLengthInPhonemes)
            # Add generated word to list
            generatedWords.append(finishedWord)

    # Generates a single word, with wordlength measured in characters or phonemes
    #  Measuring length in characters gives tighter control over string length, but may prevent the last
    #  phoneme generated from knowing it is the terminating phoneme which may affect positional probabilities)
    def generateWord(self, desiredWordLength, measureLengthInPhonemes):
        debugMode = False
        word = ""
        currentLength = 0
        symbolString = ""
        # The empty-string phoneme is used to initiate process
        latestPhoneme = self.phonemeObjects[""]
        while currentLength < desiredWordLength:
            if latestPhoneme.successors:
                if debugMode: print("Successors: " + ", ".join(latestPhoneme.successors))
                chosenPhoneme = latestPhoneme.chooseSuccessor(currentLength+1, desiredWordLength)
                word += chosenPhoneme.chooseGrapheme()
                symbolString += chosenPhoneme.phonemeType
                latestPhoneme = chosenPhoneme
                # Increase length counter, so word knows when to stop selecting successors
                if measureLengthInPhonemes:
                    # If length is counter in phonemes, increase length counter by 1, regardless of number of characters in grapheme
                    currentLength += 1
                else:
                    # If length is counted in characters, set it equal to current length of string
                    currentLength = len(word)
            else:
                print("Error: '" + latestPhoneme.phonemeSymbol + "' has no successors (failed on phoneme " + str(nextPhonemeIndex + 1) + " of " + str(wordLength) + ")")
        if word == "":
            print("Error: Empty word was generated. (Symbol string: '" + symbolString + "')")
        return word, symbolString

    def printSuccessorUsages(self):
        print("\nPhoneme usage information:\n")
        for phonemeKey, phoneme in self.phonemeObjects.items():
            phoneme.reportPhonemeSuccessorUsage()

    # Prompts each phoneme to print its contents, formatted in pre-defined way that can be pasted into a file and later read back out
    def printPhonemesInStoreFormat(self):
        for phonemeKey, phonemeObj in self.phonemeObjects.items():
            phonemeObj.printPhonemeInStoreFormat()
