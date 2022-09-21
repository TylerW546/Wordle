import pygame

from LetterBox import LetterBox
from Alert import Alert
from Keyboard import Keyboard

import config

class WordInput():
    inputs = []
    wordLength = config.targetWordLength
    
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
        """From the string of the word, fill the individual letter objects with characters"""
        for i in range(len(self.word)):
            self.letters[i].setLetter(self.word[i])
        for i in range(len(self.word), WordInput.wordLength):
            self.letters[i].setLetter('')
    
    def sendWord(self):
        """Attempts to submit the word"""
        if len(self.word) != WordInput.wordLength:
            Alert("Not enough letters")
        elif self.word not in config.validWords:
            Alert("Not in word list")
        else:
            # This word is now complete
            self.complete = True
            config.guesses += 1
            # Set correctness of letters
            if self.judgeCorrectness():
                # Win
                Alert(config.guessStrings[(config.guesses-1)*(len(config.guessStrings)-1)//(config.totalTries-1)])
            else:
                # Set focus to next word
                WordInput.focusNext()
    
    def judgeCorrectness(self):
        """Returns whether the word is correct, and sets the individual correctness value for each letter in the word."""
        target = config.targetWord
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
                
                
        return self.word == config.targetWord
            
    def drawIncomplete(self, screen):
        """Draws the word when it is in progress (not yet submitted)"""
        for letter in self.letters:
            letter.drawIncomplete(screen)
    
    def drawComplete(self, screen):
        """Draws the word when it has been already submitted"""
        for letter in self.letters:
            letter.drawComplete(screen)
            
    @staticmethod
    def drawAll(screen):
        """Loops over all words, draws them while considering whether they are complete or incomplete"""
        for input in WordInput.inputs:
            if input.complete:
                input.drawComplete(screen)
            else:
                input.drawIncomplete(screen)
    
    @staticmethod
    def focusNext():
        """Set the focused word to be the next in the stack"""
        focusedIndex = WordInput.inputs.index(WordInput.focused)
        if focusedIndex == len(WordInput.inputs)-1: # If ran out of attempts
            Alert(config.targetWord) # Give a passive game-over message by simply telling the user the word
        else:
            WordInput.focused = WordInput.inputs[focusedIndex+1] # Focus next words
