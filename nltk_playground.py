import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

def word_feats(words):
  return dict([(word, True) for word in words])

def get_word_features(wordlist):
  wordlist = nltk.FreqDist(wordlist)
  word_features = wordlist.keys()
  return word_features



def extract_features(document):
  document_words = set(document)
  features = {}
  for word in word_features:
    features['contains(%s)' % word] = (word in document_words)
  return features

negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')

negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

negcutoff = len(negfeats)*3/4
poscutoff = len(posfeats)*3/4
   
trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]

#print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
    
classifier = NaiveBayesClassifier.train(trainfeats)
#print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
#classifier.show_most_informative_features()
print 'here'
words = ['bad']
words1 = ['good']
words2 = ['decent']
words3 = ['love']
words4 = ['serious']

sentence =  word_feats(words)
sentence1 =  word_feats(words1)
sentence2 =  word_feats(words2)
sentence3 =  word_feats(words3)
sentence4 =  word_feats(words4)

print classifier.classify(sentence)
print classifier.classify(sentence1)
print classifier.classify(sentence2)
print classifier.classify(sentence3)
print classifier.classify(sentence4)



