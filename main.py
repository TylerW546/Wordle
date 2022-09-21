# -----------------------------------------------------------
# Description: A recreation of the well-known game Wordle. Uses the complete scrabble dictionary to pick words. 
# Word length and number of tries per game can be modified. 
# This is done by changing the top two variables in config.py.
# Date Started: February 12, 2022
# Name: Tyler Weed
# -----------------------------------------------------------

import pygame
pygame.init()
pygame.font.init()

import random
import math
import time

from WordInput import WordInput
from LetterBox import LetterBox
from Keyboard import Keyboard
from Alert import Alert

import config

WIDTH = max(500,20+int(config.targetWordLength*(LetterBox.surfaceWidth+2*LetterBox.marginLR)))
HEIGHT = max(700,304+int(config.totalTries*(LetterBox.surfaceHeight+2*LetterBox.marginTB)))

def generateGame(validWords, screen):
    config.targetWord = random.choice(validWords)
    global guesses
    guesses = 0
    
    WordInput.inputs = []
    for i in range(1,config.totalTries+1):
        WordInput(WIDTH/2-WordInput.width/2, WordInput.height*i, config.targetWord)
    WordInput.focused = WordInput.inputs[0]

    Keyboard.setup(screen)


white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

titleFont = pygame.font.SysFont('Times New Roman', 50, bold=True)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
    pygame.display.set_caption('Wordle')
    pygame.display.set_icon(pygame.image.load("icon.png"))
    screen.fill(white)

    title = titleFont.render("Wordle", False, black)
    titleRect = title.get_rect(center=(WIDTH/2, WordInput.height/2))

    generateGame(config.validWords, screen)
    while (True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    generateGame(config.validWords, screen)
            
            WordInput.focused.handleEvent(event)
            Keyboard.handleEvent(event)
        screen.fill(white)
        
        screen.blit(title, titleRect)
        
        WordInput.drawAll(screen)
        Alert.update(screen)
        Keyboard.draw(screen)
        
        pygame.display.update()
        time.sleep(.01)

if __name__ == '__main__':
    main()