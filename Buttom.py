# Clase Button
# argumentos: colorone, colortwo, cord, rangeX, rangeY, text
# metodos:
# setCords(x,y) setea las coordenadas donde va a aparecer el button
# setrangeEnd(rangeEndX, rangeEndY) setea los margenes de la imagen para saber hsata donde llega
# draw(window, pos) dibuja en la ventana indicada la imagen segun la posicion del raton
# pressed(pos) obtiene si el button fue presionado

import pygame
import sys

pygame.init()
pygame.mixer.init()

buttom_sound = pygame.mixer.Sound('Sonidos/buttom.wav')
arialfont = pygame.font.SysFont('arial', 30)

class Button():

    def __init__(self, text):
        self.colorone = arialfont.render(text, 0, (255,255,255))
        self.colortwo = arialfont.render(text, 0, (0,0,255))

    #set coords
    def setCords(self,x,y):
        self.cord = (x,y)

    #set dimentions
    def setrangeEnd(self, rangeEndX, rangeEndY):
        self.rangeX, self.rangeY = rangeEndX, rangeEndY

    #draw de bottom in the window
    def draw(self, window, pos):
        if pos[0] in range(self.cord[0], self.cord[0] + self.rangeX) and pos[1] in range(self.cord[1], self.cord[1] + self.rangeY):
            window.blit(self.colortwo, self.cord)
        else:
            window.blit(self.colorone, self.cord)

    #get if button presed 
    def pressed(self, pos):
        if pos[0] in range(self.cord[0], self.cord[0] + self.rangeX) and pos[1] in range(self.cord[1], self.cord[1] + self.rangeY):
            buttom_sound.play()
            return True
        else:
            return False
