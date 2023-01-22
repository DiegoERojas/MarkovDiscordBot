import random

class MarkovComposer:
    def __init__(self, listOfWords, lengthOfChain):
        self.listOfWords = listOfWords
        """
        A dictionary to hold all adjacent words with that word. Every pair of words will have their own key 
        and value (which will be their probability). Probability will scale linearly and by increments of one.
        
        """
        self.adjacentWords = {}
        self.numberOfValues = 0
        self.output = ""
        self.lengthOfChain = lengthOfChain
        self.CHAINCONSTANT = lengthOfChain

    def setLengthOfChain(self, length):
        self.lengthOfChain = length

    def setOutput(self, value):
        self.output = value

    def getOutput(self):
        return self.output

    def settingKeyValues(self):
        # Getting every overlapping pair of words in listOfWords
        for currentWord, nextWord in zip(self.listOfWords[:-1], self.listOfWords[1:]):
            currentKey = (currentWord, nextWord)
            self.numberOfValues += 1
            if currentKey in self.adjacentWords:
                self.adjacentWords[currentKey] += 1
                continue
            self.adjacentWords[currentKey] = 1
        return self.adjacentWords

    def markovOutput(self):
        # Storing each the dict. keys and values in their own list
        keyList = []
        valueList = []
        for key in self.adjacentWords.keys():
            keyList.append(key)
        for value in self.adjacentWords.values():
            valueList.append(value)
        resultingString = random.choices(keyList, weights=valueList, k=self.numberOfValues)
        print(f"keyList: {keyList}\nvalueList: {valueList}")
        self.setOutput(resultingString)
        return self.getOutput()

    def unpackingResult(self):
        finalPhrase = ""
        """
        Loop amount is determined on how many pairs there is divided by the 
        length of the chain set in discordBotFunctionality
        """
        for number in range(self.numberOfValues // self.CHAINCONSTANT):
            pairOfWords = " ".join(self.getOutput()[number])
            finalPhrase = finalPhrase + " " + pairOfWords
        return finalPhrase

