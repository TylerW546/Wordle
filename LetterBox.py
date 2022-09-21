import pygame

letterFont = pygame.font.SysFont('Helvetica', 50)
from Key import wrongColor, rightSpotColor, wrongSpotColor

background = (255,255,255)

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
        """Sets the box's letter to given letter."""
        self.letter = letter
    
    def setCorrectness(self, c):
        """Sets the corectness value of the letter. 3 possible values -- 
        1: Letter is not in word 
        2: Letter is in wrong spot 
        3: Letter is in right spot"""
        self.correctness = c
    
    def drawIncomplete(self, screen):
        """Draws when the letter is not a part of a submitted word"""
        if self.letter == '':
            self.surface.fill(LetterBox.emptyBoxColor)
            pygame.draw.rect(self.surface, background, (LetterBox.border,LetterBox.border,self.surfaceWidth-2*LetterBox.border,self.surfaceHeight-2*LetterBox.border),0)
        else:
            self.surface.fill(LetterBox.fullBoxColor)
            pygame.draw.rect(self.surface, background, (LetterBox.border,LetterBox.border,self.surfaceWidth-2*LetterBox.border,self.surfaceHeight-2*LetterBox.border),0)
            textSurface = letterFont.render(self.letter, False, (0,0,0))
            rect = textSurface.get_rect(center=(LetterBox.surfaceWidth/2, LetterBox.surfaceHeight/2+5))
            self.surface.blit(textSurface, rect)
        
        screen.blit(self.surface, (self.x, self.y))

    def drawComplete(self, screen):
        """Draws when the letter is a part of a submitted word"""
        if self.correctness == 0:
            self.surface.fill(wrongColor)
        elif self.correctness == 1:
            self.surface.fill(wrongSpotColor)
        elif self.correctness == 2:
            self.surface.fill(rightSpotColor)
            
        textSurface = letterFont.render(self.letter, False, background)
        rect = textSurface.get_rect(center=(LetterBox.surfaceWidth/2, LetterBox.surfaceHeight/2+5))
        self.surface.blit(textSurface, rect)
            
        screen.blit(self.surface, (self.x, self.y))
