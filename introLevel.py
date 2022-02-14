import pygame
from pygame.locals import *
import random
import math
import time

import os
import shutil

wordsFile = open("words.txt", "r")
words = wordsFile.read()
wordsFile.close()

wordslist = words.split("\n")

validWords = []
for word in wordslist:
    if len(word) == 5:
        validWords.append(word)

guessStrings = ["Genius", "Magnificent", "Impressive", "Splendid", "Great", "Phew"]

targetWord = random.choice(validWords)
guesses = 0

WIDTH = 500
HEIGHT = 700

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

wrongColor = (119,125,127)
wrongSpotColor = (201,180,88)
rightSpotColor = (106,169,100)
    
pygame.init()
pygame.font.init()

letterFont = pygame.font.SysFont('Helvetica', 50)
titleFont = pygame.font.SysFont('Times New Roman', 50, bold=True)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
pygame.display.set_caption('Wordle')
pygame.display.set_icon(pygame.image.load("icon.png"))
screen.fill(white)

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

title = titleFont.render("Wordle", False, black)
titleRect = title.get_rect(center=(WIDTH/2, 30))


startY = 90
guessHeight = 65

currentGuess = ""
currentGuessY = startY

coloredGuesses = []


def judgeGuess(guess, target):
    values = [0,0,0,0,0]

    for i in range(len(guess)):
        if guess[i] == target[i]:
            values[i] = 2
            target = target[:i] + "0" + target[i+1:]
            guess = guess[:i] + "1" + guess[i+1:]
    for i in range(len(guess)):
        if guess[i] in target:
            values[i] = 1
            target = target[:target.index(guess[i])] + "0" + target[target.index(guess[i])+1:]
            guess = guess[:i] + "1" + guess[i+1:]
    return values

colors = [wrongColor, wrongSpotColor, rightSpotColor]

def trySendGuess(guess):
    if len(guess) != 5:
        Alert("Not enough letters")
    elif guess not in validWords:
        Alert("Not in word list")
    else:
        sendGuess(guess)
        return True

def sendGuess(guess):
    surface = pygame.Surface((250,60))
    surface.fill(white)

    values = judgeGuess(guess, targetWord)
    for i in range(len(guess)):
        letter = letterFont.render(guess[i], False, colors[values[i]])
        surface.blit(letter, (50*i,0))
    
    coloredGuesses.append(surface)

won = False
while (guesses < 6):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if currentGuess == targetWord:
                    won = True
                if trySendGuess(currentGuess):
                    guesses += 1
                    currentGuessY += guessHeight
                    currentGuess = ""
            elif event.key == pygame.K_BACKSPACE:
                if len(currentGuess) > 0:
                    currentGuess = currentGuess[0:-1]
            else:
                if event.unicode.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    currentGuess += event.unicode.upper()
            if len(currentGuess) > 5:
                currentGuess = currentGuess[:-1]

    screen.fill(white)
    
    for i in range(len(coloredGuesses)):
        rect = coloredGuesses[i].get_rect(center=(WIDTH/2, startY+guessHeight*i))
        screen.blit(coloredGuesses[i], rect)

    currentGuessSurface = letterFont.render(currentGuess, False, black)
    currentGuessLocation = currentGuessSurface.get_rect(center=(WIDTH/2, currentGuessY))
    screen.blit(currentGuessSurface, currentGuessLocation)

    screen.blit(title, titleRect)

    Alert.update()
    
    if won:
        Alert(guessStrings[guesses])
    elif guesses == 6:
        Alert(targetWord)

    pygame.display.update()
    time.sleep(.01)