# Clase Proyectile
# argumentos: id, imageProyectile, rect, speedProyectile
# metodos:
# travel(): crea la trayectoria del proyectil segun el id del objeto que lo llamo
# draw(window): dibuja la figura de proyectil en la ventana indicada

import pygame

class Proyectile(pygame.sprite.Sprite):
    '''Proyectile class'''
    def __init__(self, posx, posy, who):
        pygame.sprite.Sprite.__init__(self)

        self.id = who
        if who == "Spaceship":
            self.imageProyectile = pygame.image.load("Imagenes/Proyectile.jpg")
        elif who == "Invasive":
            self.imageProyectile = pygame.image.load("Imagenes/Proyectile1.jpg")
        
        self.rect = self.imageProyectile.get_rect()

        self.speedProyectile = 2

        self.rect.top = posy
        self.rect.left = posx

    def travel(self):
        if self.id == "Spaceship":
            self.rect.top = self.rect.top - self.speedProyectile
        elif self.id == "Invasive":
            self.rect.top = self.rect.top + self.speedProyectile
    
    def draw(self, window):
        window.blit(self.imageProyectile, self.rect)
