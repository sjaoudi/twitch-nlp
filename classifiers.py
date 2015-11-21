from fileio import Fileio
import nltk


class HypeClassifier(object):
    def __init__(self):
        io = Fileio()

        self.hype_messages = io.importMessages('hype.txt', 'hype')
        self.hype_words = io.getWordsFromFile('hype.txt', 'hype')

        self.normal_messages = io.importMessages('normal.txt', 'normal')
        self.normal_words = io.getWordsFromFile('normal.txt', 'normal')

        self.wordList = self.hype_words + self.normal_words

        self.classifier = self.trainHypeClassifier()


    def hypeFeatures(self, document):
        document_words = set(document)
        features = {}
        for word in self.hype_words:
            features['contains(%s)' % word] = (word in document_words)
        return features


    def trainHypeClassifier(self):

        cutoff = int(len(self.hype_messages)*0.75)

        train_messages = self.hype_messages[:cutoff] + self.normal_messages[:cutoff]
        test_messages = self.hype_messages[cutoff:] + self.normal_messages[cutoff:]

        training_set = nltk.classify.util.apply_features(self.hypeFeatures, train_messages)
        classifier = nltk.NaiveBayesClassifier.train(training_set)
        test_set = nltk.classify.util.apply_features(self.hypeFeatures, test_messages)

        # print nltk.classify.util.accuracy(classifier, test_set)

        return classifier



class SeriousClassifier(object):
    def __init__():
        io = Fileio()

        self.serious_messages = io.importMessages('serious.txt', 'serious')
        self.serious_words = io.getWordsFromFile('serious.txt', 'serious')

        self.idiotic_messages = io.importMessages('idiotic.txt', 'idiotic')
        self.idiotic_words = io.getWordsFromFile('idiotic.txt', 'idiotic')

        self.wordList = self.serious_words + self.idiotic_words

        self.classifier = self.trainSeriousClassifier()


    def seriousFeatures(self, document):
        document_words = set(document)
        features = {}
        for word in self.serious_words:
            features['contains(%s)' % word] = (word in document_words)
        return features


    def trainSeriousClassifier(self):

        cutoff = int(len(self.serious_messages)*0.75)

        train_messages = self.serious_messages[:cutoff] + self.idiotic_messages[:cutoff]
        test_messages = self.serious_messages[cutoff:] + self.idiotic_messages[cutoff:]

        training_set = nltk.classify.util.apply_features(self.seriousFeatures, train_messages)
        classifier = nltk.NaiveBayesClassifier.train(training_set)

        test_set = nltk.classify.util.apply_features(self.seriousFeatures, test_messages)
        # print nltk.classify.util.accuracy(classifier, test_set)

        return classifier
