# -----------------------------------------------------------
# Description: This is a one file version of the entire Wordle project. 
# It is more suitable for an intro to python class, as it is intended to be used
# Date Started: February 14, 2022
# Name: Tyler Weed
# -----------------------------------------------------------



import pygame
from pygame.locals import *
import random
import time

# Accessing word file, store words of the right length in a list called validWords
wordsFile = open("words.txt", "r")
words = wordsFile.read()
wordsFile.close()

wordslist = words.split("\n")

validWords = []
for word in wordslist:
    if len(word) == 5:
        validWords.append(word)

# Initialize Pygame    
pygame.init()
pygame.font.init()

# Define Colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

wrongColor = (119,125,127)
wrongSpotColor = (201,180,88)
rightSpotColor = (106,169,100)

# Set up Fonts
letterFont = pygame.font.SysFont('Helvetica', 50)
titleFont = pygame.font.SysFont('Times New Roman', 50, bold=True)

# Screen sizes
WIDTH = 500
HEIGHT = 700

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
pygame.display.set_caption('Wordle')
pygame.display.set_icon(pygame.image.load("icon.png"))

class Alert():
    alerts = []
    
    background = black
    letters = white
    
    height = 50
    margin = 10

    alertFont = pygame.font.SysFont('Helvetica', 20)
    
    def __init__(self, string, lifetime=1):
        self.string = string
        
        self.timeOfDeath = time.time() + lifetime
        
        textSurf = Alert.alertFont.render(self.string, False, Alert.letters)
        self.surface = pygame.Surface((textSurf.get_rect().width+20, Alert.height))
        self.surface.fill(Alert.background)
        rect = textSurf.get_rect(center = (self.surface.get_rect().width/2, Alert.height/2))
        self.surface.blit(textSurf, rect)
        
        Alert.alerts.insert(0,self)
    
    def draw(self, x, y):
        rect = self.surface.get_rect(center=(x, y))
        screen.blit(self.surface, rect)
    
    @staticmethod
    def update():
        now = time.time()
        i = 0
        while i < len(Alert.alerts):
            if Alert.alerts[i].timeOfDeath < now:
                Alert.alerts.pop(i)
                i-=1
            else:
                Alert.alerts[i].draw(WIDTH/2, 2*Alert.height+(Alert.height+2*Alert.margin)*i)
            i+=1

# guessStrings defines what will be printed out if the word is guessed at a specific number of guesses
guessStrings = ["Genius", "Magnificent", "Impressive", "Splendid", "Great", "Phew"]

# Set up a title surface to be blit every frame
title = titleFont.render("Wordle", False, black)
titleRect = title.get_rect(center=(WIDTH/2, 30))

# Set the target word and create a variable to count guesses
targetWord = random.choice(validWords)
guesses = 0

# The Y value of the first guess
startY = 90

# The height of each guess
guessHeight = 65

# A string that stores the user's input for the active guess
currentGuess = ""
# Where the current guess input feild is placed on the screen, increases by guessHeight each time a guess is submitted
currentGuessY = startY

# A list of surfaces. The surfaces contain color-coded guesses.
coloredGuesses = []


def judgeGuess(guess, target):
    '''Given a guess and a target, return the values of the guess's letters. 
    0 - wrong letter, 
    1 - right letter wrong spot, 
    2 - right letter right spot'''

    # Set values to all zero
    values = [0,0,0,0,0]

    # Note: When a match is found, the characters of the match are removed from the target and guess strings to prevent double-dipping.
    # The characters aren't actually, removed, they are just set to irrelevant characters to preserve letter locations

    # Run through all and see if they match perfectly
    for i in range(len(guess)):
        if guess[i] == target[i]:
            # The value that corresponds to this letter of guess is 2: Perfect match
            values[i] = 2

            # Set the matched characters to 0s in target and 1s in guess
            target = target[:i] + "0" + target[i+1:]
            guess = guess[:i] + "1" + guess[i+1:]
    
    # Run through remaining and see if they match with anything at all.
    for i in range(len(guess)):
        if guess[i] in target:
            # The value that corresponds to this letter of guess is 1: Wrong spot match
            values[i] = 1

            # Set the matched characters to 0s in target and 1s in guess
            target = target[:target.index(guess[i])] + "0" + target[target.index(guess[i])+1:]
            guess = guess[:i] + "1" + guess[i+1:]
    return values

# Storing previously defined colors in a list to access them easier
colors = [wrongColor, wrongSpotColor, rightSpotColor]

def trySendGuess(guess):
    '''Alerts if the guess is invalid. Submits the guess and returns true if valid.'''
    if len(guess) != 5:
        Alert("Not enough letters")
    elif guess not in validWords:
        Alert("Not in word list")
    else:
        sendGuess(guess)
        return True

def sendGuess(guess):
    '''Creates a surface for the guess and adds it to the coloredGuesses list'''
    # Surface is 250 pixels wide (contains 5 50px wide characters)
    # Surface is 60 pixels high (so characters must be at most 60 pixels high)
    surface = pygame.Surface((250,60))
    # Fill surface with white
    surface.fill(white)

    # Judge the word. This will give the colors for each letter
    values = judgeGuess(guess, targetWord)
    # Run through every index in the length of guess
    for i in range(len(guess)):
        # Render the letter at that index
        letter = letterFont.render(guess[i], False, colors[values[i]])
        # Place the letter at an x value of 50*i and a y value of 0 on the previously made surface
        surface.blit(letter, (50*i,0))
    
    # Add the surface to the list of scored guesses
    coloredGuesses.append(surface)

# This will be set to True when the user wins
won = False
while (True):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        # Will not take user input after the user wins/loses
        if not(won) and guesses < 6:
            # If a key is pressed
            if event.type == pygame.KEYDOWN:
                # If that key is return
                if event.key == pygame.K_RETURN:
                    # If the user guessed exactly right, set won to true
                    if currentGuess == targetWord:
                        won = True
                    # Check validity of guess, if valid...
                    if trySendGuess(currentGuess):
                        # Add 1 to guesscount
                        guesses += 1
                        # Increase the y location of the input feild
                        currentGuessY += guessHeight
                        # Clear the user's input from the input feild
                        currentGuess = ""
                    
                    # If won, give the user their win message.
                    # Win message is found at the index of guessStrings that corresponds to the number of guesses it took (-1)
                    if won:
                        Alert(guessStrings[guesses-1], 10)
                    # If lost, guesses will = 6, so tell the user the real word
                    elif guesses == 6:
                        Alert(targetWord, 10)

                # If that key is a backspace, remove the last letter of guess
                elif event.key == pygame.K_BACKSPACE:
                    if len(currentGuess) > 0:
                        currentGuess = currentGuess[0:-1]
                # If the key is in the alphabet, add the letter to the guess
                elif event.unicode.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                        currentGuess += event.unicode.upper()
                
                # If the user types more than 5 characters, remove extra
                if len(currentGuess) > 5:
                    currentGuess = currentGuess[0:5]

    # Clear the screen
    screen.fill(white)
    
    # Draw in the title
    screen.blit(title, titleRect)
    
    # Draw the past (color-coded) guesses of the user
    for i in range(len(coloredGuesses)):
        # This will store the x and y values that put that surface's center in the middle horizontally and at the proper y value.
        # Y value is dependent on the position in the list. Newest guesses will be later in the list, therefore i will be higher, so the y value is higher
        rect = coloredGuesses[i].get_rect(center=(WIDTH/2, startY+guessHeight*i))

        # Draw the guess at that location
        screen.blit(coloredGuesses[i], rect)

    # Render the user's current typed text
    currentGuessSurface = letterFont.render(currentGuess, False, black)
    # Find the location that puts the input feild in the right location
    currentGuessLocation = currentGuessSurface.get_rect(center=(WIDTH/2, currentGuessY))
    # Place the rendered text at that location
    screen.blit(currentGuessSurface, currentGuessLocation)

    
    # Updates Alerts and screen, set a frame delay
    Alert.update()
    pygame.display.update()
    time.sleep(.01)