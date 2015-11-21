import socket, string, time, nltk, re, requests, json, pprint, time
from datetime import datetime
from collections import deque

from classifiers import HypeClassifier
from timing import TimingFuncs
from twitchAPI import TwitchAPIFuncs
from wordFixer import WordFixer

hype = HypeClassifier()
timing = TimingFuncs()
twitch = TwitchAPIFuncs()
wordFix = WordFixer()

HOST = 'irc.twitch.tv'
PORT = 6667
NICK = 'sjaoudi'
PASS = 'oauth:03nj467om5d8sm9dgrllor2a97zie4'

#channel = raw_input("Enter a channel: ").lower()
channel = "c9sneaky"

CHAN = '#%s' % channel
twitch.checkIfLive(channel)

hype_classifier = hype.classifier
emotes = twitch.getEmoticons()

s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))

CHAT_MSG = re.compile(r":\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

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
        emotesCount = 0

        newMessage = []
        for part in message.split():
            if part in emotes: # emote found
                emotesCount += 1
                # continue
                # pass
            newMessage.append(part)
        message = ' '.join(newMessage)

        print(message), hype_classifier.prob_classify(hype.hypeFeatures(message.split())).prob('hype')
        #print(message)

        #print datetime.now().strftime(FMT)
        currentTime = datetime.now().strftime(FMT)

        tdelta = (datetime.strptime(currentTime, FMT) -
                  datetime.strptime(prevTime, FMT))

        timing.appendTdelta(tdelta, tdeltas, 20)

        if len(tdeltas) >= 20:
            print 'AVG', timing.calcAvgTdelta(tdeltas)

        if message.split():
            # emotesToWords = float(emotesCount/len(message.split()))
            # print "emotesToWords: ", emotesToWords
            print emotesCount

        print '\n'
        #rateArray.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f'))
        #findAverage()

        #f.write(message+'\n')
