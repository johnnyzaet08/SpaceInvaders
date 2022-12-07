# Clase Spaceship
# argumentos: ImageShip, rect, shotList, life, speed
# metodos:
# movement(): verifica que la nave no salga de los margenes de la pantalla de juego
# shot(x, y): agrega un proyectil saliendo de la nave en la posicion deseada
# draw(window): dibuja la nave en la ventana indicada

from Proyectile import Proyectile
import pygame

class SpaceShip(pygame.sprite.Sprite):
    '''Spaceships class'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.ImageShip = pygame.image.load("Imagenes/Spaceship.png")
        
        self.rect = self.ImageShip.get_rect()
        self.rect.centerx = 400
        self.rect.centery = 570

        self.shotList = []

        self.life = True
        self.speed = 20
    
    def movement(self):
        if self.life == True:
            if self.rect.left <= 0:
                self.rect.left = 0
            elif self.rect.right >= 800:
                self.rect.right = 800

    def shot(self, x, y):
        shot = Proyectile(x, y, "Spaceship")
        self.shotList.append(shot)

    def draw(self, window):
        if self.life == True:
            window.blit(self.ImageShip, self.rect)
        else:
            pass