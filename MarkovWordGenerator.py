from MarkovChain import *
from random import randint
import string

class MarkovWordGenerator:
    """ This class builds a Markov chain out of some input text and
        spits out something that is hopefully intelligible."""
    
    def __init__(self, inputText, n=1):
        inputText = string.replace(inputText, "\n"," ")
        self._inputText = string.split(inputText, " ")

        # Remove blanks from the list
        try:
            while 1:
                self._inputText.remove('')

        except ValueError:
            pass

        # allow for circular treatment of text, so that every
        # state will lead to at least one other state
        self._inputText = self._inputText + self._inputText[0:n+1]
        self._n = n
        self._markovChain = MarkovChain()
        self.__buildMarkovChain()

    def __buildMarkovChain(self):
        # Build a Markov chain with each set of adjacent n words
        # representing a state in the chain.

        nGram1 = tuple(self._inputText[0: self._n])
        i = 1

        # Cycle through the n-grams in the text and add each n-gram,
        # along with adjacent n-grams, to the markov chain.
        
        while i < (len(self._inputText) - self._n):
            nGram2 = tuple(self._inputText[i: i + self._n])
            self._markovChain.add(nGram1, nGram2)
            nGram1 = nGram2
            i = i + 1

    def generate(self, numWords, method = MarkovChain.MOST_LIKELY):
        # Generate numWords words based on the Markov Chain model.
            
        # Randomly pick the first word generated
        r = randint(0, len(self._inputText) - (self._n + 1))     
        state = tuple(self._inputText[r: r + self._n])
        outputText = string.join([word for word in state], " ")

        # Output each new word based on the previous state        
        for i in range(numWords):
            state = self._markovChain.next(state, method)
            outputText = outputText + ' ' + state[-1]

        return outputText

# For testing and debugging purposes only
if __name__ == "__main__":
    FILE_NAME = "alice.txt"
    file = open(FILE_NAME)
    textToken = file.read()
    file.close()
    generator = MarkovWordGenerator(textToken, 1)
    print '\n', generator.generate(100, MarkovChain.WEIGHTED)
##    generator = MarkovWordGenerator(textToken, 2)
##    print '\n', generator.generate(100)
##    generator = MarkovWordGenerator(textToken, 3)
##    print '\n', generator.generate(100)
##    generator = MarkovWordGenerator(textToken, 4)
##    print '\n', generator.generate(100)
##    generator = MarkovWordGenerator(textToken, 20)
##    print '\n', generator.generate(250)

