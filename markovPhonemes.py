import random
import string

## Phoneme Lists
vowelPhonemes = ['a', 'e', 'i', 'o', 'u', 'ae', 'ee', 'ie', 'oe', 'ue', 'oo', 'ar', 'ur', 'or', 'au', 'er', 'ow', 'oi', 'air', 'ear']
# Note: This contains graphemes which are not distinct phonemes, such as "c" which shares the phoneme "k"
consonantPhonemes = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z', 'wh', 'th', 'ch', 'sh', 'zh', 'ng']


# A phoneme exists as a unit 
class Phoneme:
    #Phonemes can be vowel phonemes or consonant phonemes
    __phonemeType = ""
    def __init__(self, newPhonemeType):
        self.phonemeType = newPhonemeType
        
    def getPhonemeType(self):
        return __self.phonemeType
