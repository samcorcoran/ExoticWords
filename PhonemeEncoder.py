print("This program will prompt you for details about a phoneme, and encode that information in a file so that it can be automatically loaded by the Exotic Words projects.\n")

# Open the file
with open("encodedPhonemes.txt", "a") as outputFile:
    repeat = True
    while(repeat):
        print("Specifying new phoneme!\n")
        # Encoding a new phoneme, reset variables
        phonemeSymbol = ""
        phonemeType = ""
        phonemeExample = ""
        graphemes = ""

        print("Phoneme symbol: ")
        phonemeSymbol = raw_input()
        if phonemeSymbol == "":
            print("Error: No phoneme symbol provided.\n")
            # Jump through to next beginning of loop
            continue 

        print("Vowel or consonant (v/c): ")
        phonemeType = raw_input()
        
        if phonemeType == "v":
            # Vowel. Append
            print("Vowel height (e.g. close-mid): ")
            phonemeType += ":" + raw_input()
            
            print("Vowel backness (e.g. near-back): ")
            phonemeType += ":" + raw_input()
            
        elif phonemeType == "c":
            # Consonant. Append Manner (e.g. nasal) and place (e.g. dental)
            print("Consonant manner (e.g. nasal): ")
            phonemeType += ":" + raw_input()
            
            print("Consonant place (e.g. dental): ")
            phonemeType += ":" + raw_input()
            
        else:
            print("Error: Invalid phoneme type provided. Must be v or c.\n")
            # Jump through to next beginning of loop
            continue

        print("Example word: ")
        phonemeExample = raw_input()
        if phonemeExample == "":
            print("Error: No phoneme example provided\n")
            # Jump through to next beginning of loop
            continue

        print("Graphemes (comma separated): ")
        graphemes = raw_input()
        if graphemes == "":
            print("Error: No graphemes provided.\n")
            # Jump through to next beginning of loop
            continue

        # Info must be correct for this point to have been reached
        print("\nWriting phoneme to file...\n")

        outputFile.write("\n<START PHONEME>")
        outputFile.write("\nphonemeSymbol:"+phonemeSymbol)
        outputFile.write("\nphonemeType:"+phonemeType)
        outputFile.write("\nphonemeExample:"+phonemeExample)
        outputFile.write("\ngraphemes:"+graphemes)
        outputFile.write("\n<END PHONEME>")

        print("Another? (y/n)")
        if not raw_input() == "y":
            repeat = False
