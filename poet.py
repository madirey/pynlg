from MarkovWordGenerator import *
import string

def stripToNSyllables(s, n):
    # Takes a string s and returns the first n syllables.

    vowels = 'aeiouy'
    stringOfVowels = 0
    syllables = 0
    listOfWords = s.split(' ')

    for i in range(len(listOfWords)):
        word = listOfWords[i]
        
        for j in range(len(word)):
            if word[j] in vowels and not stringOfVowels:
                syllables = syllables + 1
                stringOfVowels = 1

                if syllables == n:
                    return string.join(listOfWords[0:i+1], ' ')

            elif word[j] not in vowels:
                stringOfVowels = 0

    # If we make it here, then return the entire string
    return s
    
    
def writeHaiku(wordGenerator):
    line = wordGenerator.generate(5, MarkovChain.WEIGHTED)
    print stripToNSyllables(line, 5)

    line = wordGenerator.generate(7, MarkovChain.WEIGHTED)
    print stripToNSyllables(line, 7)

    line = wordGenerator.generate(5, MarkovChain.WEIGHTED)
    print stripToNSyllables(line, 5)

def main():
    fileName = raw_input("Enter the filename: ")
    file = open(fileName)
    textToken = file.read()
    file.close()
    
    generator = MarkovWordGenerator(textToken, 3)

    while 1:
        print "\n"
        writeHaiku(generator)
        x = raw_input("\nContinue? ")

        if x == 'n' or x == 'N':
            break

main()
