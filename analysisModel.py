from nltk.tokenizer import *
from nltk.probability import *
from random import randint
import string

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class AnalysisModel:
   """A Base class for analyzing documents and producing useful
      probability distributions and collocational information about the
      documents."""

   def __init__(self, corpusToken, SUBTOKENS='SUBTOKENS'):
   ##    Precondition: corpusToken must already be Tokenized... it must be
   ##    a Token that has already been formatted by an NLTK tokenizer
   ##    object.
       self._wordPairDist = ConditionalFreqDist()
       self._wordDist = FreqDist()
       self._SUBTOKENS = SUBTOKENS
       self._corpus = corpusToken

       self._totalTokens = float(len(self._corpus[self._SUBTOKENS]))

   def getWordDist(self):
       return self._wordDist

   def getWordPairDist(self):
       return self._wordPairDist

   def _chooseWeighted(self, choices, probabilities):
       from random import uniform
       n = uniform(0,1)
       i = 0

       for weight in probabilities:
           if n < weight:
               return choices[i]
           n = n - weight
           i = i + 1
       print "Error in _chooseWeighted..."
       raise RunTimeError

   def _chooseUnWeighted(self, choices, frequencies):
       max = min(frequencies)
       maxPos = 0
       i = 0
       for freq in frequencies:
           if freq > max:
               max = freq
               maxPos = i
           i = i + 1

       return choices[maxPos]

   def chooseNextWord(self, word1):
       raise NotImplementedError

   def _runAnalysis(self):
       raise NotImplementedError


##    def tagText(self, tagger=None):
##        from nltk.tagger import *
##
##        if tagger == None:
##            tagger1 = NthOrderTagger(1)
##            tagger2 = UnigramTagger()
##            tagger3 = RegexpTagger([(r'^[0-9]+(.[0-9]+)?$', 'cd'), (r'.*', 'nn')])
##
##            tagger1.train(self._trainingDoc)
##            tagger2.train(self._trainingDoc)
##            tagger = BackoffTagger([tagger1, tagger2, tagger3])
##
##        tagger.tag(self._corpus)
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class ProbabilityModel(AnalysisModel):
   def __init__(self, corpusToken, SUBTOKENS='SUBTOKENS'):
       AnalysisModel.__init__(self, corpusToken, SUBTOKENS)
       self._runAnalysis()

   def _runAnalysis(self):
       prev = None
       for word in self._corpus[self._SUBTOKENS]:
           self._wordPairDist[prev].inc(word['TEXT'])
           prev = word['TEXT']

   def chooseNextWord(self, word1):
       raise NotImplementedError
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# ----------------------------------------------------------------------
class WeightedProbabilityModel(ProbabilityModel):
   def __init__(self, corpusToken, SUBTOKENS='SUBTOKENS'):
       ProbabilityModel.__init__(self, corpusToken, SUBTOKENS)

   def chooseNextWord(self, word1):
       keys = self._wordPairDist[word1].samples()
       total = float(reduce(lambda x,y: x+y,                                       \
                      [self._wordPairDist[word1].count(val) for val in             \
                       [word for word in self._wordPairDist[word1].samples()]]))
       probabilities = [self._wordPairDist[word1].count(key)/total for key in keys]

       ### Test Case ###
       if __name__ == "__main__":
           assert abs( reduce(lambda x,y: x+y, probabilities) - 1) < .05, \
                   "Probabilities do not add up to 1."
       ### End Test ###

       return self._chooseWeighted(keys, probabilities)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
class UnWeightedProbabilityModel(ProbabilityModel):
   def __init__(self, corpusToken, SUBTOKENS='SUBTOKENS'):
       ProbabilityModel.__init__(self, corpusToken, SUBTOKENS)

   def chooseNextWord(self, word1):
       keys = self._wordPairDist[word1].samples()
       return self._chooseUnWeighted(
           keys,
           [self._wordPairDist[word1].count(val) for val in keys])
# ----------------------------------------------------------------------

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class MutualInformationModel(AnalysisModel):
   def __init__(self, corpusToken, minFreq=10):
       AnalysisModel.__init__(self, corpusToken)
       self._MIDict = {}
       self._minFreq = minFreq
       self._runAnalysis()

   def _runAnalysis(self):
       prev = None
       self._wordDist.inc(prev)
       visited = {} # use dictionary, as a lookup is O(1)
       for word in self._corpus['SUBTOKENS']:
           if not visited.get(prev,False):
               self._MIDict[prev] = {}
               visited[prev] = True
##            if prev not in self._MIDict.keys(): # This is O(n)
##                self._MIDict[prev] = {}
           #self._MIDict[prev][word['TEXT']] = 0 # Initialize dictionary of dictionary
           self._wordPairDist[prev].inc(word['TEXT'])
           self._wordDist.inc(word['TEXT'])
           prev = word['TEXT']

       visited = {}        # use dictionary, as a lookup is O(1)
       subtokens = self._corpus['SUBTOKENS']
       pos = 0

       while pos < len(self._corpus['SUBTOKENS']) - 1:
           if not visited.get((subtokens[pos]['TEXT'],subtokens[pos+1]['TEXT']),False):
               f_x = self._wordDist.count(subtokens[pos]['TEXT'])
               f_y = self._wordDist.count(subtokens[pos+1]['TEXT'])
               f_xy = self._wordPairDist[subtokens[pos]['TEXT']].count(            \
                   subtokens[pos+1]['TEXT'])
               self._MIDict[subtokens[pos]['TEXT']][subtokens[pos+1]['TEXT']] =    \
                   self._mutualInformationIndex(f_x,f_y,f_xy)
               visited[(subtokens[pos]['TEXT'],subtokens[pos+1]['TEXT'])] = True
           pos = pos + 1
##
##        for initialWord in self._MIDict.keys():
##            for finalWord in self._MIDict[initialWord].keys():
##                f_x = self._wordDist.count(initialWord)
##                f_y = self._wordDist.count(finalWord)
##                f_xy = self._wordPairDist[initialWord].count(finalWord)
##                self._MIDict[initialWord][finalWord] = self._mutualInformationIndex(f_x,f_y,f_xy)

   def _mutualInformationIndex(self, f_x, f_y, f_xy):
       """Computes the mutual information index for two words, x and y, given
       the frequency of x (f_x), the frequency of y (f_y), the frequency
       of x directly followed by y (f_xy), and the total number of words
       in the analyzed corpus.  The higher the index returned from this
       function, the greater the likelihood that their co-occurrence is
       not coincidental.  Returns 0 if either of the individual frequencies
       are less than minFreq                                            """

       return float(f_x > self._minFreq)*float(f_y > self._minFreq) *      \
              math.log( (f_xy / self._totalTokens) /                       \
                        ( (f_x*f_y) / self._totalTokens**2), 2)

   def chooseNextWord(self, word1):
       raise NotImplementedError
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# ----------------------------------------------------------------------
class WeightedMutualInformationModel(MutualInformationModel):
   def __init__(self, corpusToken, minFreq=10):
       MutualInformationModel.__init__(self, corpusToken, minFreq)

   def chooseNextWord(self, word1):
       keys = self._MIDict[word1].keys()
       total = float(reduce(lambda x,y: x+y,
                   [self._MIDict[word1][word2] for word2 in keys]))
       if total != 0:
           probabilities = [self._MIDict[word1][word2]/total for word2 in keys]
       else:
           probabilities = [1.0 / len(keys) for i in range(len(keys))]

       return self._chooseWeighted(keys, probabilities)
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
class UnWeightedMutualInformationModel(MutualInformationModel):
   def __init__(self, corpusToken, minFreq=10):
       MutualInformationModel.__init__(self, corpusToken, minFreq)

   def chooseNextWord(self, word1):
       keys = self._MIDict[word1].keys()
       return self._chooseUnWeighted(
                   keys,
                   [self._MIDict[word1][word2] for word2 in keys]  )
# ----------------------------------------------------------------------

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class TScoreModel(AnalysisModel):
   def __init__(self, corpusToken=None, SUBTOKENS='SUBTOKENS'):
       AnalysisModel.__init__(self, corpusToken, SUBTOKENS)
       self._tScoreDict = {}
       self._SUBTOKENS = SUBTOKENS

       if corpusToken != None:
          self._runAnalysis()

##    def _runAnalysis(self):
##        prev = None
##        self._wordDist.inc(prev)
##        for word in self._corpus['SUBTOKENS']:
##            if prev not in self._tScoreDict.keys():
##                self._tScoreDict[prev] = {}
##            self._tScoreDict[prev][word['TEXT']] = 0 # Initialize dictionary of dictionary
##            self._wordPairDist[prev].inc(word['TEXT'])
##            self._wordDist.inc(word['TEXT'])
##            prev = word['TEXT']
##
##        for initialWord in self._tScoreDict.keys():
##            for finalWord in self._tScoreDict[initialWord].keys():
##                f_x = self._wordDist.count(initialWord)
##                f_y = self._wordDist.count(finalWord)
##                f_xy = self._wordPairDist[initialWord].count(finalWord)
##                self._tScoreDict[initialWord][finalWord] = self._tScore(f_x,f_y,f_xy)

   def _runAnalysis(self):
       prev = None
       self._wordDist.inc(prev)
       visited = {} # use dictionary, as a lookup is O(1)
       for word in self._corpus[self._SUBTOKENS]:
           if not visited.get(prev,False):
               self._tScoreDict[prev] = {}
               visited[prev] = True
           self._wordPairDist[prev].inc(word['TEXT'])
           self._wordDist.inc(word['TEXT'])
           prev = word['TEXT']

       visited = {}        # use dictionary, as a lookup is O(1)
       subtokens = self._corpus[self._SUBTOKENS]
       pos = 0

       while pos < len(self._corpus[self._SUBTOKENS]) - 1:
           if not visited.get((subtokens[pos]['TEXT'],subtokens[pos+1]['TEXT']),False):
               f_x = self._wordDist.count(subtokens[pos]['TEXT'])
               f_y = self._wordDist.count(subtokens[pos+1]['TEXT'])
               f_xy = self._wordPairDist[subtokens[pos]['TEXT']].count(            \
                   subtokens[pos+1]['TEXT'])
               self._tScoreDict[subtokens[pos]['TEXT']][subtokens[pos+1]['TEXT']] =    \
                   self._tScore(f_x,f_y,f_xy)
               visited[(subtokens[pos]['TEXT'],subtokens[pos+1]['TEXT'])] = True
           pos = pos + 1

   def _tScore(self, f_x, f_y, f_xy):
       return ( f_xy/self._totalTokens - (f_x/self._totalTokens) * (f_y/self._totalTokens)) / \
              math.sqrt(f_xy/self._totalTokens)

   def chooseNextWord(self, word1):
       raise NotImplementedError
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# ----------------------------------------------------------------------
class WeightedTScoreModel(TScoreModel):
   def __init__(self, corpusToken, SUBTOKENS='SUBTOKENS'):
       TScoreModel.__init__(self, corpusToken, SUBTOKENS)
       self._SUBTOKENS = SUBTOKENS

   def chooseNextWord(self, word1):
       keys = self._tScoreDict[word1].keys()
       total = float(reduce(lambda x,y: x+y,
                   [self._tScoreDict[word1][word2] for word2 in keys]))
       probabilities = [self._tScoreDict[word1][word2]/total for word2 in keys]

       return self._chooseWeighted(keys, probabilities)
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
class UnWeightedTScoreModel(TScoreModel):
   def __init__(self, corpusToken):
       TScoreModel.__init__(self, corpusToken)

   def chooseNextWord(self, word1):
       keys = self._tScoreDict[word1].keys()
       return self._chooseUnWeighted(
                   keys,
                   [self._tScoreDict[word1][word2] for word2 in keys]  )
# ----------------------------------------------------------------------

class WeightedTaggedTScoreModel(WeightedTScoreModel):
   def __init__(self, corpusToken, SUBTOKENS='SUBTOKENS'):
       WeightedTScoreModel.__init__(self, corpusToken, SUBTOKENS)
       self._SUBTOKENS = SUBTOKENS

   def chooseNextWord(self, word1):
       text = word1[0]
       tag = word1[1]
       keys = self._tScoreDict[(text,tag)].keys()

       total = float(reduce(lambda x,y: x+y,
               [self._tScoreDict[(text,tag)][word2] for word2 in keys]))
       probabilities = [self._tScoreDict[(text,tag)][word2]/total for word2 in keys]
     
       return self._chooseWeighted(keys, probabilities)

   def _runAnalysis(self):
       visited = {} # use dictionary, as a lookup is O(1)
       prev = self._corpus[self._SUBTOKENS][0]
       self._wordDist.inc((prev['TEXT'], prev['TAG']))
       self._tScoreDict[(prev['TEXT'], prev['TAG'])] = {}
       visited[(prev['TEXT'], prev['TAG'])] = True

       for word in self._corpus[self._SUBTOKENS][1:]:
           if not visited.get((word['TEXT'], word['TAG']),False):
               self._tScoreDict[(word['TEXT'], word['TAG'])] = {}
               visited[(word['TEXT'], word['TAG'])] = True
           self._wordPairDist[(prev['TEXT'],prev['TAG'])].inc(     \
                              (word['TEXT'], word['TAG']))
           self._wordDist.inc((word['TEXT'], word['TAG']))
           prev = word

       visited = {}        # use dictionary, as a lookup is O(1)
       subtokens = self._corpus[self._SUBTOKENS]
       pos = 0

       while pos < len(subtokens) - 1:
           text1 = subtokens[pos]['TEXT']
           text2 = subtokens[pos+1]['TEXT']
           tag1 = subtokens[pos]['TAG']
           tag2 = subtokens[pos+1]['TAG']

           if not visited.get(((text1, tag1),(text2, tag2)),False):
               f_x = self._wordDist.count((text1, tag1))
               f_y = self._wordDist.count((text2, tag2))
               f_xy = self._wordPairDist[(text1, tag1)].count((text2, tag2))
               self._tScoreDict[(text1,tag1)][(text2,tag2)] = self._tScore(f_x,f_y,f_xy)
               visited[((text1,tag1),(text2,tag2))] = True
           pos = pos + 1

if __name__ == "__main__":
   FILE_NAME = "c:\\documents and settings\\mcaldwell\desktop\\alice.txt"
   #FILE_NAME = "/home/mcaldwell/capstone/corpora/alice.txt"
   TOKENIZER = WhitespaceTokenizer(SUBTOKENS='SUBTOKENS')
   TEST_WORD = "alice"
   file = open(FILE_NAME)
   tokenized = Token(TEXT=string.lower(file.read()))
   TOKENIZER.tokenize(tokenized)
   file.close()

   def WeightedProbabilityTest():
       print "Testing WeightedProbabilityModel on '" + TEST_WORD + "'..."
       model = WeightedProbabilityModel(tokenized)
       for i in range(5):
           print model.chooseNextWord(TEST_WORD)
       print "Test finished... results reasonable?\n"

   def UnWeightedProbabilityTest():
       print "Testing UnWeightedProbabilityModel on '" + TEST_WORD + "'..."
       model = UnWeightedProbabilityModel(tokenized)
       words = []
       for i in range(5):
           words.append(model.chooseNextWord(TEST_WORD))
       assert words[0] == words[1] == words[2] == words[3] == words[4],\
           """UnWeightedProbabilityTest.chooseNextWord() should return
              the same result every time.  Test failed."""
       print words
       print "Test passed.  Results reasonable?\n"

   def WeightedMutualInformationTest():
       print "Testing WeightedMutualInformationModel on '" + TEST_WORD + "'..."
       model = WeightedMutualInformationModel(tokenized)
       for i in range(5):
           print model.chooseNextWord(TEST_WORD)
       print "Test finished... results reasonable?\n"

   def UnWeightedMutualInformationTest():
       print "Testing UnWeightedMutualInformationModel on '" + TEST_WORD + "'..."
       model = UnWeightedMutualInformationModel(tokenized)
       for i in range(5):
           print model.chooseNextWord(TEST_WORD)
       print "Test finished... results reasonable?\n"

   def WeightedTScoreTest():
       print "Testing WeightedTScoreModel on '" + TEST_WORD + "'..."
       model = WeightedTScoreModel(tokenized)
       for i in range(5):
           print model.chooseNextWord(TEST_WORD)
       print "Test finished... results reasonable?\n"

   def UnWeightedTScoreTest():
       print "Testing UnWeightedTScoreModel on '" + TEST_WORD + "'..."
       model = UnWeightedTScoreModel(tokenized)
       for i in range(5):
           print model.chooseNextWord(TEST_WORD)
       print "Test finished... results reasonable?\n"

   WeightedProbabilityTest()
   UnWeightedProbabilityTest()
   WeightedMutualInformationTest()
   UnWeightedMutualInformationTest()
   WeightedTScoreTest()
   UnWeightedTScoreTest()


