class Fileio(object):

  def importMessages(self, filename, sentiment):
      messageFile = open(filename, 'r')
      messages = []
      for message in messageFile:
          messageDict = [word for word in message.split()]
          messages.append((messageDict, sentiment))
      return messages

  def getWordsFromFile(self, filename, sentiment):

      messages = self.importMessages(filename, sentiment)
      return self.getWordsFromMessages(messages)

  def getWordsFromMessages(self, messages):
      allWords = []
      for (message, sentiment) in messages:
          allWords.extend(message)
      return allWords
