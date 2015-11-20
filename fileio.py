class Fileio():

  def importMessages(self, filename, sentiment):
      messageFile = open(filename, 'r')
      messages = []
      for message in messageFile:
          messageDict = [word for word in message.split()]
          messages.append((messageDict, sentiment))
      return messages
