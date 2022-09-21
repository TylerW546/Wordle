import pygame
from Key import Key

keyboardKeys = ["QWERTYUIOP",
                "ASDFGHJKL",
                "0ZXCVBNM1"]

class Keyboard():
    def setup(screen):
        Keyboard.keys = [[] for i in range(3)]
        
        Keyboard.surface = pygame.Surface((10*(43+2*Key.marginLR), 3*(Key.height + 2*Key.marginTB)))
        Keyboard.surface.fill((255,255,255))
        
        Keyboard.rect = Keyboard.surface.get_rect(center=(screen.get_width()/2,screen.get_height()-Keyboard.surface.get_rect().height/2))
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
    
    def draw(screen):
        for row in Keyboard.keys:
            for key in row:
                key.draw(Keyboard.surface)
        screen.blit(Keyboard.surface, Keyboard.rect)
