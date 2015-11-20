import requests
import json

class TwitchAPIFuncs:

    def checkIfLive(self, channel):
        apiUrl = "https://api.twitch.tv/kraken/streams/%s" % channel
        r = requests.get(apiUrl)
        content = json.loads(r.content)
        if 'message' in content:
            print content['message']
            exit()
        elif content['stream'] is None:
            print "Stream is offline."
            exit()

    def getEmoticons(self): # make api call to get list of chat emotes
        r = requests.get("https://api.twitch.tv/kraken/chat/emoticon_images")
        content = json.loads(r.content)
        emotes = []
        for emote in content['emoticons']:
            emotes.append(emote['code'])
        return emotes
