
class WordFixer:

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
        removedLetters = self.removeRepeatedLetters(word.lower())
        removedWords = self.removeRepeatedWords(removedLetters)

        return removedWords


#wordFix = wordFixer()
#print wordFixer.fixWord(wordFix, "LOLOLLLLL")
