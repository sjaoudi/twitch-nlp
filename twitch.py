import socket, string, time, nltk, re, requests
import json, pprint
#from nltk.corpus import stopwords
import time
from datetime import datetime
from collections import deque

def checkIfLive(channel):
    apiUrl = "https://api.twitch.tv/kraken/streams/%s" % channel
    r = requests.get(apiUrl)
    content = json.loads(r.content)
    if 'message' in content:
        print content['message']
        exit()
    elif content['stream'] is None:
        print "Stream is offline."
        exit()

HOST = 'irc.twitch.tv'
PORT = 6667
NICK = 'sjaoudi'
PASS = 'oauth:03nj467om5d8sm9dgrllor2a97zie4'

channel = raw_input("Enter a channel: ").lower()

CHAN = '#%s' % channel

checkIfLive(channel)

# def getStopwords():
#     stopwordsArray = stopwords.words('english')
#     stopwordsUpper = [word.upper() for word in stopwordsArray]
#     stopwordsArray.extend(stopwordsUpper)
#     return stopwordsArray

def getEmoticons(): # make api call to get list of chat emotes
    r = requests.get("https://api.twitch.tv/kraken/chat/emoticon_images")
    content = json.loads(r.content)
    emotes = []
    for emote in content['emoticons']:
        emotes.append(emote['code'])
    return emotes

def splitMessages(sentenceArray):
    wordArray = []

    stopwords = getStopwords()
    print stopwords
    #for (message, sentiment) in sentenceArray:
    #    words = [word for word in message.split() if word not in stopwords] # filter stopwords?
    #    wordArray.append((words, sentiment))
    for message in sentenceArray:
        #words = [word for word in message.split()]
        words = {word for word in message.split() if word not in stopwords}
        wordArray.append(words)
    return wordArray

def importMessages(fileName, sentiment):
    messageFile = open(fileName, 'r')
    #stopwords = getStopwords()
    #messageArray = []
    #for message in messageFile:
    #    messageArray.append((message, sentiment))
    messageArray = []
    for message in messageFile:
        messageDict = [word for word in message.split()]
        messageArray.append((messageDict, sentiment))
    return messageArray
    #return messageDict

def getWordsFromMessages(messageArray):
    allWords = []
    for (message, sentiment) in messageArray:
    #for message in messageArray:
        allWords.extend(message)
    return allWords

def getWordDist(words):
    wordDist = nltk.FreqDist(words)
    return wordDist.keys()

def wordFeatures(document):
    document_words = set(document)
    features = {}
    for word in hypeWords:
        features['contains(%s)' % word] = (word in document_words)
    return features

def checkIfLive(channel):
    apiUrl = "https://api.twitch.tv/kraken/streams/%s" % channel
    r = requests.get(apiUrl)
    content = json.loads(r.content)
    print content['stream']
    exit()

def appendTdelta(tdelta, tdeltas, tdeltasCapacity):
    if len(tdeltas) < tdeltasCapacity:
        tdeltas.append(tdelta)
    else:
        tdeltas.rotate()
        tdeltas[0] = tdelta

def calcAvgTdelta(tdeltas):
    sum = 0
    for tdelta in tdeltas:
        sum += tdelta.microseconds

    avgTdelta = sum/len(tdeltas)
    return avgTdelta


hypeWords = getWordsFromMessages(importMessages('hype.txt','hype'))
hype_messages = importMessages('hype.txt', 'hype')

normalWords = getWordsFromMessages(importMessages('normal.txt', 'normal'))
normal_messages = importMessages('normal.txt', 'normal')

global wordList
wordList = hypeWords + normalWords

#print imported_messages
cutoff = int(len(hype_messages)*0.75)


train_messages = hype_messages[:cutoff] + normal_messages[:cutoff]
test_messages = hype_messages[cutoff:] + normal_messages[cutoff:]
#print len(train_messages), len(test_messages)

training_set = nltk.classify.util.apply_features(wordFeatures,train_messages)
classifier = nltk.NaiveBayesClassifier.train(training_set)
#print classifier.show_most_informative_features()

test_set = nltk.classify.util.apply_features(wordFeatures, test_messages)
#print nltk.classify.util.accuracy(classifier, test_set)

#print classifier.classify(wordFeatures(['lol']))
#print wordFeatures(['rofl'])

emotes = getEmoticons()

s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))

CHAT_MSG=re.compile(r":\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

tdeltas = deque([])

FMT = '%Y-%m-%d %H:%M:%S:%f'


while True:
    try:
        prevTime = currentTime
    except:
        prevTime = datetime.now().strftime(FMT)

    response = s.recv(1024)#.decode("utf-8")

    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        message = CHAT_MSG.sub('', response)
        newMessage = []
        for part in message.split():
            if part in emotes: #emote found
                continue
            newMessage.append(part)
        message = ' '.join(newMessage)
        #message += '\n'

        #print(message), classifier.prob_classify(wordFeatures(message.split())).prob('hype')
        print(message)

        #print datetime.now().strftime(FMT)
        currentTime = datetime.now().strftime(FMT)

        tdelta = (datetime.strptime(currentTime, FMT) -
                  datetime.strptime(prevTime, FMT)
                  )

        appendTdelta(tdelta, tdeltas, 20)

        if len(tdeltas) >= 20:
            print 'AVG', calcAvgTdelta(tdeltas)

        print '\n'
        #rateArray.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f'))
        #findAverage()

        #f.write(message+'\n')
