from analysisModel import *

class TextGenerator:
   def __init__(self, analysisModel):
       self._analysisModel = analysisModel

   def generateWords(self, initialWord, amount):
##        if self._analysisModel.isTagged():
##        temporary fix:
       if isinstance(self._analysisModel, WeightedTaggedTScoreModel):
           word = initialWord[0]
           tag = initialWord[1]
           print word,

           for i in range(amount):
               (word,tag) = self._analysisModel.chooseNextWord((word,tag))
               print word,
       else:
           word = initialWord
           print word,

           for i in range(amount):
               word = self._analysisModel.chooseNextWord(word)
               print word,




