from fileio import Fileio
import nltk


class NltkFuncs:

    def __init__(self):
        io = Fileio()

        self.hype_messages = io.importMessages('hype.txt', 'hype')
        self.hype_words = self.getWordsFromMessages(io.importMessages('hype.txt','hype'))

        self.normal_messages = io.importMessages('normal.txt', 'normal')
        self.normal_words = self.getWordsFromMessages(io.importMessages('normal.txt', 'normal'))

        self.wordList = self.hype_words + self.normal_words

    def getWordsFromMessages(self, messages):
        allWords = []
        for (message, sentiment) in messages:
        #for message in messageArray:
            allWords.extend(message)
        return allWords

    def getWordDist(self, words):
        wordDist = nltk.FreqDist(words)
        return wordDist.keys()

    def wordFeatures(self, document):
        document_words = set(document)
        features = {}
        for word in hype_words:
        # for word in wordList:
            features['contains(%s)' % word] = (word in document_words)
        return features

    # global wordList

    def getHypeMessages(self):
        io = Fileio()
        global hype_nessages
        hype_messages = io.importMessages('hype.txt', 'hype')
        global hype_words
        hype_words = self.getWordsFromMessages(io.importMessages('hype.txt','hype'))
        global normal_messages
        normal_messages = io.importMessages('normal.txt', 'normal')
        normal_words = self.getWordsFromMessages(io.importMessages('normal.txt', 'normal'))
        global wordList
        wordList = hype_words + normal_words

    def trainHypeClassifier(self):

        self.getHypeMessages()

        cutoff = int(len(self.hype_messages)*0.75)

        train_messages = self.hype_messages[:cutoff] + self.normal_messages[:cutoff]
        test_messages = self.hype_messages[cutoff:] + self.normal_messages[cutoff:]
        #print len(train_messages), len(test_messages)

        training_set = nltk.classify.util.apply_features(self.wordFeatures, train_messages)
        classifier = nltk.NaiveBayesClassifier.train(training_set)
        #print classifier.show_most_informative_features()

        test_set = nltk.classify.util.apply_features(self.wordFeatures, test_messages)
        print nltk.classify.util.accuracy(classifier, test_set)

        return classifier
