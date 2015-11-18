word = [
    "OMGOMGOMGOMGOMGOMG",
    "LOLOLLLOLOOL",
    "LOOOOOOOL",
    "WTFFF",
    "WTFF",
    "HOLYSHIT",
    "FUUUUUUUUCK",
    "HAHAHAHAHA",
    "AHAHA",
    "WOWOWOW",
    "COOL"
]

"OMG"
"LOL"
"LOL"

"LOLOL"
"HAHAHA"
"WOWOW"
"OMGOMGOMG"


def removeRepeatedLetters(word):
    letters = ""
    for i in range(len(word) - 1):
        if word[i] != word[i + 1]:
            letters += word[i]

    return letters + word[-1]

def removeRepeatedWords(word):
    letters = ""
    for letter in word:
        letters += letter
        if len(letters) > 2 and removeRepeatedLetters(letters + letters) \
                             in removeRepeatedLetters(word + word):
           return removeRepeatedLetters(letters + word[-1])

def fixWord(word):
    removedLetters = removeRepeatedLetters(word)
    removedWords = removeRepeatedWords(removedLetters)
    return removedWords


print fixWord("")
