# Word length
targetWordLength = 5
# Total tries before game is over
totalTries = 6

# Messages to be printed out depending on how many guesses it takes
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

# Will be a list of words that could be the target word.
validWords = handleWords()

# Number of guesses used so far
guesses = 0

# The word to be guessed. Will be defined in main
targetWord = None