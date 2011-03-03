import sys
sys.path.append('/home/mcaldwell/capstone/libs')
from textGenerator import *
from nltk.corpus import brown

ALICE = \
   "c:\\documents and settings\\matt\\desktop\\Capstone\\corpora\\alice.txt"
TWENTY_THOUSAND_LEAGUES = \
   "c:\\documents and settings\\matt\\desktop\\Capstone\\corpora\\twentyThousandLeagues.txt"

FILE_NAME = ALICE
INITIAL_WORD = "alice"
LENGTH = 100
#tokenizer = WhitespaceTokenizer()
regexp = r'(\w+)|(\$\d+\.\d+)|([^\w\s]+)|(\.+)|([\.,:;\"\`!()?])|(([Mm]r|[Mm]s|[Mm]rs|[Dd]r)\.)'
tokenizer = RegexpTokenizer(regexp)

def showExamples():
   print "UnWeightedProbabilityModel...\n"
   model = UnWeightedProbabilityModel(FILE_NAME, tokenizer)
   TextGenerator(model).generateWords(INITIAL_WORD, LENGTH)
   print "\n\nWeightedProbabilityModel...\n"
   model = WeightedProbabilityModel(FILE_NAME, tokenizer)
   TextGenerator(model).generateWords(INITIAL_WORD, LENGTH)
   print "\n\nUnWeightedMutualInformationModel...\n"
   model = UnWeightedMutualInformationModel(FILE_NAME, tokenizer)
   TextGenerator(model).generateWords(INITIAL_WORD, LENGTH)
   print "\n\nWeightedMutualInformationModel...\n"
   model = WeightedMutualInformationModel(FILE_NAME, tokenizer)
   TextGenerator(model).generateWords(INITIAL_WORD, LENGTH)
   print "\n\nUnWeightedTScoreModel...\n"
   model = UnWeightedTScoreModel(FILE_NAME, tokenizer)
   TextGenerator(model).generateWords(INITIAL_WORD, LENGTH)
   print "\n\nWeightedTScoreModel...\n"
   model = WeightedTScoreModel(FILE_NAME, tokenizer)
   TextGenerator(model).generateWords(INITIAL_WORD, LENGTH)

def testLengthOfText(brownSection):
    items = brown.items(brownSection)
    textToken = brown.read(items[0])
    
    for i in range(len(items)):
        print "\n\nWeightedTaggedTScoreModel\n"
        model = WeightedTaggedTScoreModel(textToken, SUBTOKENS='WORDS')
        TextGenerator(model).generateWords(('the','at'),100)
        textToken['WORDS'] = textToken['WORDS'] + brown.read(items[i+1])['WORDS']

      
def main():

  print "\n\nWeightedTaggedTScoreModel\n"
  items = brown.items('fiction: general')
  textToken = brown.read(items[0])
  for item in items[1:]:
      textToken['WORDS'] = textToken['WORDS'] + brown.read(item)['WORDS']

  model = WeightedTaggedTScoreModel(textToken, SUBTOKENS='WORDS')
  TextGenerator(model).generateWords(('the','at'), 200)
  print "\n\nWeightedTScoreModel...\n"
  model = WeightedTScoreModel(textToken, SUBTOKENS='WORDS')
  TextGenerator(model).generateWords('the',200)

#   from nltk.corpus import genesis
#   textToken = genesis.read('english-kjv.txt')
#   #model = UnWeightedProbabilityModel(textToken, SUBTOKENS='WORDS')
#   #TextGenerator(model).generateWords('God', 100)
#   model = WeightedProbabilityModel(textToken, SUBTOKENS = 'WORDS')
#   TextGenerator(model).generateWords('God', 100)
#   print "\n"
#   model = WeightedTScoreModel(textToken, SUBTOKENS='WORDS')
#   TextGenerator(model).generateWords('the', 100)
#main()
testLengthOfText('fiction: general')
#testVerySmallTexts('fiction: general')




