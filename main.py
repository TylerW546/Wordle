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

targetWordLength = 7
totalTries = 8

validWords = []
for word in wordslist:
    if len(word) == targetWordLength:
        validWords.append(word)

guessStrings = ["Genius", "Magnificent", "Impressive", "Splendid", "Great", "Phew"]

targetWord = None
guesses = 0

def generateGame():
    global targetWord
    targetWord = random.choice(validWords)
    print(targetWord)
    global guesses
    guesses = 0
    
    WordInput.inputs = []
    for i in range(1,totalTries+1):
        WordInput(WIDTH/2-WordInput.width/2, WordInput.height*i, targetWord)
    WordInput.focused = WordInput.inputs[0]

    Keyboard.setup()
    
class LetterBox():
    innerWidth = 60
    innerHeight = 60
    border = 2
    marginLR = 2.5
    marginTB = 3
    
    surfaceWidth = innerWidth + 2*(border)
    surfaceHeight = innerHeight + 2*(border)
    
    emptyBoxColor = (210, 214,218)
    fullBoxColor = (135,138,140)
    
    def __init__(self, x=100, y=100):
        self.x = x
        self.y = y
        self.letter=''
        
        self.correctness = 0
        
        self.surface = pygame.Surface((LetterBox.surfaceWidth, LetterBox.surfaceHeight))
    
    def setLetter(self, letter):
        self.letter = letter
    
    def setCorrectness(self, c):
        self.correctness = c
    
    def drawIncomplete(self):
        if self.letter == '':
            self.surface.fill(LetterBox.emptyBoxColor)
            pygame.draw.rect(self.surface, white, (LetterBox.border,LetterBox.border,self.surfaceWidth-2*LetterBox.border,self.surfaceHeight-2*LetterBox.border),0)
        else:
            self.surface.fill(LetterBox.fullBoxColor)
            pygame.draw.rect(self.surface, white, (LetterBox.border,LetterBox.border,self.surfaceWidth-2*LetterBox.border,self.surfaceHeight-2*LetterBox.border),0)
            textSurface = letterFont.render(self.letter, False, black)
            rect = textSurface.get_rect(center=(LetterBox.surfaceWidth/2, LetterBox.surfaceHeight/2+5))
            self.surface.blit(textSurface, rect)
        
        screen.blit(self.surface, (self.x, self.y))

    def drawComplete(self):
        if self.correctness == 0:
            self.surface.fill(wrongColor)
        elif self.correctness == 1:
            self.surface.fill(wrongSpotColor)
        elif self.correctness == 2:
            self.surface.fill(rightSpotColor)
            
        textSurface = letterFont.render(self.letter, False, white)
        rect = textSurface.get_rect(center=(LetterBox.surfaceWidth/2, LetterBox.surfaceHeight/2+5))
        self.surface.blit(textSurface, rect)
            
        screen.blit(self.surface, (self.x, self.y))

class WordInput():
    inputs = []
    wordLength=targetWordLength
    
    width = LetterBox.surfaceWidth*wordLength   +   2*LetterBox.marginLR*wordLength
    height = LetterBox.surfaceHeight   +   2*LetterBox.marginTB
    
    focused = None
    
    def __init__(self,x,y,target):
        self.x = x
        self.y = y
        
        self.complete = False
        
        self.word = ""
        self.letters = []
        for i in range(WordInput.wordLength):
            self.letters.append(LetterBox(self.x + LetterBox.marginLR + (LetterBox.surfaceWidth + 2*LetterBox.marginLR)*i, self.y+LetterBox.marginTB))
        
        WordInput.inputs.append(self)
    
    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if WordInput.focused == self:
                if event.key == pygame.K_RETURN:
                    self.sendWord()
                elif event.key == pygame.K_BACKSPACE:
                    if len(self.word) > 0:
                        self.word = self.word[0:-1]
                else:
                    if event.unicode.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                        self.word += event.unicode.upper()
                if len(self.word) > WordInput.wordLength:
                    self.word = self.word[:-1]
            self.wordToLetters()
    
    def wordToLetters(self):
        for i in range(len(self.word)):
            self.letters[i].setLetter(self.word[i])
        for i in range(len(self.word), WordInput.wordLength):
            self.letters[i].setLetter('')
    
    def sendWord(self):
        if len(self.word) != WordInput.wordLength:
            Alert("Not enough letters")
        elif self.word not in validWords:
            Alert("Not in word list")
        else:
            # This word is now complete
            self.complete = True
            global guesses
            guesses += 1
            # Set correctness of letters
            if self.judgeCorrectness():
                # Win
                Alert(guessStrings[(guesses-1)*(len(guessStrings)-1)//(totalTries-1)])
            else:
                # Set focus to next word
                WordInput.focusNext()
    
    def judgeCorrectness(self):
        target = targetWord
        word = self.word
        
        for letter in self.word:
            Keyboard.setLetterCorrectness(letter, 0)
        
        for i in range(len(word)):
            if word[i] == target[i]:
                self.letters[i].setCorrectness(2)
                Keyboard.setLetterCorrectness(word[i], 2)
                
                target = target[:i] + "0" + target[i+1:]
                word = word[:i] + "1" + word[i+1:]
        for i in range(len(word)):
            if word[i] in target:
                self.letters[i].setCorrectness(1)
                Keyboard.setLetterCorrectness(word[i], 1)
                target = target[:target.index(word[i])] + "0" + target[target.index(word[i])+1:]
                word = word[:i] + "1" + word[i+1:]
                
                
        return self.word == targetWord
            
    def drawIncomplete(self):
        for letter in self.letters:
            letter.drawIncomplete()
    
    def drawComplete(self):
        for letter in self.letters:
            letter.drawComplete()
            
    @staticmethod
    def drawAll():
        for input in WordInput.inputs:
            if input.complete:
                input.drawComplete()
            else:
                input.drawIncomplete()
    
    @staticmethod
    def focusNext():
        focusedIndex = WordInput.inputs.index(WordInput.focused)
        if focusedIndex == len(WordInput.inputs)-1:
            Alert(targetWord)
        else:
            WordInput.focused = WordInput.inputs[focusedIndex+1]

WIDTH = max(500,20+int(targetWordLength*(LetterBox.surfaceWidth+2*LetterBox.marginLR)))
HEIGHT = max(700,304+int(totalTries*(LetterBox.surfaceHeight+2*LetterBox.marginTB)))

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

wrongColor = (119,125,127)
wrongSpotColor = (201,180,88)
rightSpotColor = (106,169,100)
    
pygame.init()
pygame.font.init()

letterFont = pygame.font.SysFont('Helvetica', 50,)
alertFont = pygame.font.SysFont('Helvetica', 20,)
keyboardLetterFont = pygame.font.SysFont('Helvetica', 15, bold=True)
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
    
    def __init__(self, string, lifetime=1):
        self.string = string
        
        self.timeOfDeath = time.time() + lifetime
        
        textSurf = alertFont.render(self.string, False, Alert.letters)
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


class Key():
    backgroundColor = (210,214,218)
    letterColor = black
    
    marginLR = 3
    marginTB = 4
    
    height=58
    
    def __init__(self, x, y, string='', width=43):
        self.x = x
        self.y = y
        
        self.string = string
        self.width = width
        
        self.correctness = -1
        
        self.surface = pygame.Surface((self.width, Key.height))
        self.surface.fill(Key.backgroundColor)
        self.textSurf = keyboardLetterFont.render(self.string, False, Key.letterColor)
        self.rect = self.textSurf.get_rect(center=(self.width/2,Key.height/2))
        self.surface.blit(self.textSurf, self.rect)
    
    def setClickableRect(self, keyboardx, keyboardy):
        self.clickRect = Rect(self.x+keyboardx,self.y+keyboardy,self.width,Key.height)
    
    def sendLetter(self):
        if self.string == "ENTER":
            pygame.event.post(pygame.event.Event(KEYDOWN, key=pygame.K_RETURN))
        elif self.string == "DEL":
            pygame.event.post(pygame.event.Event(KEYDOWN, key=pygame.K_BACKSPACE))
        else:
            pygame.event.post(pygame.event.Event(KEYDOWN, unicode = self.string, key=0))

    def changeCorrectness(self, correctness):
        self.correctness = max(self.correctness, correctness)
        
        color = Key.backgroundColor
        if self.correctness == 0:
            color = wrongColor
        elif self.correctness == 1:
            color = wrongSpotColor
        elif self.correctness == 2:
            color = rightSpotColor
        
        self.surface.fill(color)
        self.surface.blit(self.textSurf, self.rect)
    
    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.clickRect.collidepoint(event.pos):
                self.sendLetter()
                
    def draw(self, surface):
        surface.blit(self.surface, (self.x,self.y))

keyboardKeys = ["QWERTYUIOP",
                "ASDFGHJKL",
                "0ZXCVBNM1"]

class Keyboard():
    def setup():
        Keyboard.keys = [[] for i in range(3)]
        
        Keyboard.surface = pygame.Surface((10*(43+2*Key.marginLR), 3*(Key.height + 2*Key.marginTB)))
        Keyboard.surface.fill(white)
        
        Keyboard.rect = Keyboard.surface.get_rect(center=(WIDTH/2,HEIGHT-Keyboard.surface.get_rect().height/2))
        Keyboard.startx = Keyboard.rect.x
        Keyboard.starty = Keyboard.rect.y
        
        for i in range(len(keyboardKeys)):
            for j in range(len(keyboardKeys[i])):
                inRowSoFar = 0
                for key in Keyboard.keys[i]:
                    inRowSoFar += key.width+2*Key.marginLR
                
                if keyboardKeys[i][j] == "0":
                    Keyboard.keys[i].append(Key(inRowSoFar+Key.marginLR, (Key.height + 2*Key.marginTB)*i, "ENTER", width = 65))
                elif keyboardKeys[i][j] == "1":
                    Keyboard.keys[i].append(Key(inRowSoFar+Key.marginLR, (Key.height + 2*Key.marginTB)*i, "DEL", width = 65))
                else:
                    Keyboard.keys[i].append(Key(inRowSoFar+Key.marginLR, (Key.height + 2*Key.marginTB)*i, keyboardKeys[i][j]))
                
                if i == 1:
                    Keyboard.keys[i][j].x += 22
                
                Keyboard.keys[i][j].setClickableRect(Keyboard.startx, Keyboard.starty)
    
    def setLetterCorrectness(letter, correctness):
        for row in Keyboard.keys:
            for key in row:
                if key.string == letter:
                    key.changeCorrectness(correctness)
    
    def handleEvent(event):
        for row in Keyboard.keys:
            for key in row:
                key.handleEvent(event)
    
    def draw():
        for row in Keyboard.keys:
            for key in row:
                key.draw(Keyboard.surface)
        screen.blit(Keyboard.surface, Keyboard.rect)

title = titleFont.render("Wordle", False, black)
titleRect = title.get_rect(center=(WIDTH/2, WordInput.height/2))


generateGame()
while (True):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                generateGame()
        
        WordInput.focused.handleEvent(event)
        Keyboard.handleEvent(event)
    screen.fill(white)
    
    screen.blit(title, titleRect)
    
    WordInput.drawAll()
    Alert.update()
    Keyboard.draw()
    
    pygame.display.update()
    time.sleep(.01)