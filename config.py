# Word length
targetWordLength = 5
# Total tries before game is over
totalTries = 6

guessStrings = ["Genius", "Magnificent", "Impressive", "Splendid", "Great", "Phew"]

def handleWords():
    validWords = []
    wordsFile = open("words.txt", "r")
    words = wordsFile.read()
    wordsFile.close()

    wordsList = words.split("\n")
    
    for word in wordsList:
        if len(word) == targetWordLength:
            validWords.append(word)

    return validWords

validWords = handleWords()

guesses = 0

targetWord = None