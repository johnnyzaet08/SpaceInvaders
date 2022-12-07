# Clase Invader
# argumentos: posx, posy, level, imageInvasive, imageInvasiveS, imageDeath, rect, life, shoting, count
# metodos:
# set_Image(level) setea las imagenes necesarias segun el nivel del juego
# shot(x, y) crea un nuevo proyectil en las coordenadas seleccionadas
# draw(window) dibuja en la ventana indicada al objeto
# drawM(window) actuliza la imagen y la dibuja en la ventana indicada

from Proyectile import Proyectile
import pygame

shotList = []
class Invasive(pygame.sprite.Sprite):
    '''Invasive class'''
    def __init__(self,posx, posy, level):
        pygame.sprite.Sprite.__init__(self)

        self.imageInvasive = pygame.image.load("Imagenes/Invader" + level + ".png")
        self.imageInvasiveS = pygame.image.load("Imagenes/Invader" + level + "S.png")
        self.ImageDeath = pygame.image.load("Imagenes/InvaderDeath.png")
        self.rect = self.imageInvasive.get_rect()
        
        self.life = True
        self.shoting = False
        self.count = 0

        self.rect.top = posy
        self.rect.left = posx
    
    def set_Image(self, level):
        self.imageInvasive = pygame.image.load("Imagenes/Invader" + level + ".png")
        self.imageInvasiveS = pygame.image.load("Imagenes/Invader" + level + "S.png")
        
    
    def shot(self, x, y):
        shot = Proyectile(x, y, "Invasive")
        shotList.append(shot)
        self.shoting = True
    
    def draw(self, window):
        if self.shoting == False:
            window.blit(self.imageInvasive, self.rect)
        elif self.shoting == True:
            window.blit(self.imageInvasiveS, self.rect)
            self.count += 1
            if self.count == 50:
                self.shoting = False
                self.count = 0
    
    def drawM(self, window):
        window.blit(self.ImageDeath, self.rect)