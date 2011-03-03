OUTPUT_FILE = "WeightedPureProb.py"
group = raw_input("Group of training corpus: ")
corpus = raw_input("Name of training corpus: ")
lengthOfText = input("Desired length of text: ")
initialWord = raw_input("Initial word: ")

outStream = open(OUTPUT_FILE, "w")
outStream.write(
"""from nltk.probability import ConditionalFreqDist
from nltk.corpus import %s
from random import uniform
corpus = %s.read('%s')
cfdist = ConditionalFreqDist()
prev = None
for token in corpus['WORDS']:
   word = token['TEXT']
   cfdist[prev].inc(word)
   prev = word
word = '%s'
for i in range(%d):
   print word,
   topFive = cfdist[word].sorted_samples()[0:5]
   topFiveFreq = map(lambda x: cfdist[word].count(x), topFive)
   # Find probabilities of each of the top 5 results
   topFiveProbabilities = map(lambda x: float(x) / reduce(lambda x,y: x+y, topFiveFreq), topFiveFreq)
   # Choose a word based on those probabilities
   n = uniform(0,1)
   i = 0
   for weight in topFiveProbabilities:
      if n < weight:
         break
      n = n - weight
      i = i + 1
   word = topFive[i]""" % (group, group, corpus, initialWord, lengthOfText,))
outStream.close()
execfile(OUTPUT_FILE)

