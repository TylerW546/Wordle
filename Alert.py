import pygame
import time

alertFont = pygame.font.SysFont('Helvetica', 20)

class Alert():
    alerts = []
    
    background = (0,0,0)
    letters = (255,255,255)
    
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
    
    def draw(self, x, y, screen):
        rect = self.surface.get_rect(center=(x, y))
        screen.blit(self.surface, rect)
    
    @staticmethod
    def update(screen):
        now = time.time()
        i = 0
        while i < len(Alert.alerts):
            if Alert.alerts[i].timeOfDeath < now:
                Alert.alerts.pop(i)
                i-=1
            else:
                Alert.alerts[i].draw(screen.get_width()/2, 2*Alert.height+(Alert.height+2*Alert.margin)*i, screen)
            i+=1