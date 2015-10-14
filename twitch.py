import socket, string, time, nltk, re
from textblob import TextBlob

HOST = 'irc.twitch.tv'
PORT = 6667
NICK = 'sjaoudi'
PASS = 'oauth:03nj467om5d8sm9dgrllor2a97zie4'
CHAN = '#syndicate'

s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))

# CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
CHAT_MSG=re.compile(r":\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

# blob = TextBlob('happy')
# print(blob.sentences[0].sentiment)

while True:
    response = s.recv(1024).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        # print(response)
        message = CHAT_MSG.sub('', response)

        blob = TextBlob(message)

        #for sentence in blob.sentences:
        #    print(sentence, sentence.sentiment)

        print(message)
