import pygame

wrongColor = (119,125,127)
wrongSpotColor = (201,180,88)
rightSpotColor = (106,169,100)

keyboardLetterFont = pygame.font.SysFont('Helvetica', 15, bold=True)

class Key():
    backgroundColor = (210,214,218)
    letterColor = (0,0,0)
    
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
        self.clickRect = pygame.Rect(self.x+keyboardx,self.y+keyboardy,self.width,Key.height)
    
    def sendLetter(self):
        if self.string == "ENTER":
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        elif self.string == "DEL":
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE))
        else:
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, unicode = self.string, key=0))

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

