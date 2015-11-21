
class WordFixer(object):

    def removeRepeatedLetters(self, word):
        letters = ""
        for i in range(len(word) - 1):
            if word[i] != word[i + 1]:
                letters += word[i]

        return letters + word[-1]

    def removeRepeatedWords(self, word):
        letters = ""
        for letter in word:
            letters += letter
            if len(letters) > 2 and self.removeRepeatedLetters(letters + letters) \
                                 in self.removeRepeatedLetters(word + word):
               return self.removeRepeatedLetters(letters + word[-1])

    def fixWord(self, word):
        if len(word) <= 4:
            return word
        repeatedLettersRemoved = self.removeRepeatedLetters(word.lower())
        repeatedWordsRemoved = self.removeRepeatedWords(removedLetters)

        return {'fixed_word' : repeatedWordsRemoved,
                'removed_letters' : len(word) - len(repeatedLettersRemoved)
               }

    def uniqueWords(self, message):
        # Determine uniqueness of a message (e.g. spammed words or emotes)
        pass


    def messageCase(self, message):
        # Determine the ratio of upper / lowercase words in a message
        pass


#wordFix = wordFixer()
#print wordFixer.fixWord(wordFix, "LOLOLLLLL")
