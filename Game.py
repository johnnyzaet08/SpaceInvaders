from Spaceship import SpaceShip
from InputBox import InputBox
from Invader import Invasive
from Invader import shotList
from random import randint
from Buttom import Button
import pygame
import sys

backgroundGame = pygame.image.load('Imagenes/BackgroundGame.jpg')

#////////////////////////////////////////Main Menu/////////////////////////////////////////
# Contiene la ventana del menu principal y los botones para llamar a las otras ventanas
def menu():
    pygame.init()
    menu = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Space Invaders: Menu")
    menu.blit(backgroundGame, (0,0))
    
    #Buttons
    SingleB = Button("Single Player")
    SingleB.setCords(60,120), SingleB.setrangeEnd(145,35)
    MultiB = Button("Multiplayer")
    MultiB.setCords(60,210), MultiB.setrangeEnd(120,35)
    ScoresB = Button("HighScores")
    ScoresB.setCords(60,300), ScoresB.setrangeEnd(135, 35)
    HelpB = Button("Help")
    HelpB.setCords(60,390), HelpB.setrangeEnd(50, 35)

    Running = True
    while Running:
        pos = pygame.mouse.get_pos()                                #funtions by print and upgrade
        
        SingleB.draw(menu, pos)
        MultiB.draw(menu, pos)
        ScoresB.draw(menu, pos)
        HelpB.draw(menu, pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SingleB.pressed(pos):
                    Running = False
                    game(1)
                if MultiB.pressed(pos):
                    Running = False
                    game(2)
                if ScoresB.pressed(pos):
                    Running = False
                    ranking()
                if HelpB.pressed(pos):
                    Running = False
                    help()
        
        pygame.display.update()
    pygame.quit()

#///////////////////////////////////////Game Window////////////////////////////////////////
# Contiene toda la ventana del juego y la logica de todo el juego con sus clases
def game(players):
    pygame.init()
    game = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Space Invaders: Game")
    
    arialfont = pygame.font.SysFont('Aparajita', 40)              #Text's font

    pygame.mixer.init()
    nivel_music = 'Sonidos/nivel.mp3'
    pygame.mixer.music.load(nivel_music)
    pygame.mixer.music.play(-1)

    if players == 1:
        playerone = SpaceShip()
    elif players == 2:
        playerone = SpaceShip()
        playerone.rect.centerx = 300
        playertwo = SpaceShip()
        playertwo.rect.centerx = 500
    
    Level = "Level1"
    Invader = [Invasive(50, 100, Level), Invasive(200, 100, Level), Invasive(350, 100, Level), Invasive(500, 100, Level), Invasive(650, 100, Level),
                Invasive(50, 200, Level), Invasive(200, 200, Level), Invasive(350, 200, Level), Invasive(500, 200, Level), Invasive(650, 200, Level),
                Invasive(50, 300, Level), Invasive(200, 300, Level), Invasive(350, 300, Level), Invasive(500, 300, Level), Invasive(650, 300, Level)] #instancias de invasor
    
    Invaders = []
    for Inva in Invader:
        Invaders.append(Inva)

    limit = 3
    score = 0

    initialTime = pygame.time.get_ticks() / 1000

    Running = True
    while Running:
        time = (pygame.time.get_ticks() / 1000) - initialTime
        time = ((time * 100) // 1) / 100

        if Invaders == []:                          #Verifica si aun hay invasores vivos
            playerone.shotList = []
            if players == 2:
                playertwo.shotList = []
            if Level == "Level1":                       #Verifica nivel para cambiarlo o para pasar a la pantalla de ganar
                Level = "Level2"
                for Inva in Invader:
                    Inva.life = True
                    Inva.set_Image(Level)
                    Invaders.append(Inva)
            elif Level == "Level2":
                Level = "Level3"
                for Inva in Invader:
                    Inva.life = True
                    Inva.set_Image(Level)
                    Invaders.append(Inva)
            elif Level == "Level3":
                Running = False
                pygame.mixer.music.stop()
                win(time)

        if playerone.life == False:                             #Verifica si los jugadores siguen vivos
            if players == 2 and playertwo.life == False:
                Running = False
                pygame.mixer.music.stop()
                lost()
            elif players == 1:
                Running = False
                pygame.mixer.music.stop()
                lost()

        for event in pygame.event.get():                        #Capturas los eventos de la pantalla
            if event.type == pygame.QUIT:
                Running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:                                #Analiza movimientos del jugador 1
                if event.key == pygame.K_LEFT and playerone.life == True:
                    playerone.rect.left -= playerone.speed
                elif event.key == pygame.K_RIGHT and playerone.life == True:
                    playerone.rect.right += playerone.speed
                elif event.key == pygame.K_UP and playerone.life == True:
                    x, y = playerone.rect.center
                    playerone.shot(x,y)
                elif players == 2:              #Verifica si el jugador 2 esta activo y si hay que moverlo
                    if event.key == pygame.K_a and playertwo.life == True:
                        playertwo.rect.left -= playertwo.speed
                    elif event.key == pygame.K_d and playertwo.life == True:
                        playertwo.rect.right += playertwo.speed
                    elif event.key == pygame.K_w and playertwo.life == True:
                        x, y = playertwo.rect.center
                        playertwo.shot(x,y)

            
            
        game.blit(backgroundGame, (0,0))

        if players == 2:  #Verifica si el jugador 2 esta activo
            playertwo.draw(game)
            playertwo.movement()
            if len(playertwo.shotList) > 0:   #Verifica la lista de disparos
                for shots in playertwo.shotList:
                    shots.draw(game)
                    shots.travel()
                    if shots.rect.top < -10:
                        playertwo.shotList.remove(shots)
                    for inva in Invaders:
                        if inva.rect.centery >= shots.rect.top and shots.rect.centerx >= inva.rect.left and shots.rect.centerx <= inva.rect.right and inva.life == True:
                            inva.life = False
                            score += 1
                            playertwo.shotList.remove(shots)
        
        playerone.draw(game)#Dibuja al jugador en la ventana game
        playerone.movement()# El jugador no se se salga del rango de la ventana
        if len(playerone.shotList) > 0:#Analiza los disparos del jugador y verifica si choca con algu invasor 
            for shots in playerone.shotList:
                shots.draw(game)#Dibuja los disparos en la ventana
                shots.travel()#Le da el camino a seguir
                if shots.rect.top < -10: #Verifica si se salio de la ventana
                    playerone.shotList.remove(shots)
                for inva in Invaders:#Recorre todos los invasores para analizar si choca con algun invasor
                    if inva.rect.centery >= shots.rect.top and shots.rect.centerx >= inva.rect.left and shots.rect.centerx <= inva.rect.right and inva.life == True:
                        inva.life = False
                        score += 1 #Aumenta el score en 1
                        playerone.shotList.remove(shots)#remueve de la lista al disparo

        if time // 1 == limit:  #tiempo de disparo de invasores y analiza los cuantos van a disparar segun el nivel
            limit += 3
            if Level == "Level1" and Invaders != []:
                pos = randint(0, len(Invaders)-1)
                invade = Invaders[pos]
                x, y = invade.rect.center
                invade.shot(x, y)
            elif Level == "Level2" and Invaders != []:
                for i in range(0,2):
                    pos = randint(0, len(Invaders)-1)
                    invade = Invaders[pos]
                    x, y = invade.rect.center
                    invade.shot(x, y)
            elif Level == "Level3" and Invaders != []:
                for i in range(0,3):
                    pos = randint(0, len(Invaders)-1)
                    invade = Invaders[pos]
                    x, y = invade.rect.center
                    invade.shot(x, y)
        
        for invaders in Invaders:       #Analiza la vida de los invasores
            if invaders.life == True:
                invaders.draw(game)
            elif invaders.life == False:
                invaders.drawM(game)
                Invaders.remove(invaders)

        for shoots in shotList:        #Analiza los disparos de los invasores        
            shoots.draw(game)
            shoots.travel()
            if shoots.rect.bottom > 610:
                shotList.remove(shoots)
            if players == 2:
                if playertwo.rect.centery <= shoots.rect.bottom and shoots.rect.centerx >= playertwo.rect.left and shoots.rect.centerx <= playertwo.rect.right and playertwo.life == True:
                    playertwo.life = False
                    shotList.remove(shoots)
            if playerone.rect.centery <= shoots.rect.bottom and shoots.rect.centerx >= playerone.rect.left and shoots.rect.centerx <= playerone.rect.right and playerone.life == True:
                playerone.life = False
                shotList.remove(shoots)                            

        TimeText = arialfont.render(("Time: " + str(time)), 0, (255, 255, 255))
        ScoreText = arialfont.render(("Score: " + str(score)) , 0, (255,255,255))
        LevelText = arialfont.render(Level, 0, (255,255,255))
        game.blit(ScoreText, (50, 20))
        game.blit(LevelText, (350, 20))
        game.blit(TimeText, (600, 20))

        pygame.display.update()
    pygame.quit()

#////////////////////////////////////////Lost Window///////////////////////////////////////
# Contiene la ventana cuando el jugador pierde para regresar al menu principal
def lost():
    pygame.init()
    lost = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Space Invaders: Lost")
    lost.blit(backgroundGame, (0,0))

    arialfont = pygame.font.SysFont('arial', 70)
    GameOverText = arialfont.render("Game Over" , 0, (255,255,255))
    TryAgainText = arialfont.render("Tray Again", 0, (255,255,255))

    pygame.mixer.init()
    gameover_sound = pygame.mixer.Sound('Sonidos/gameoversound.wav')
    gameover_sound.play()

    ReturnB = Button("Return to menu")
    ReturnB.setCords(325,440), ReturnB.setrangeEnd(145,35)

    Running = True
    while Running:
        pos = pygame.mouse.get_pos()

        ReturnB.draw(lost, pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ReturnB.pressed(pos):
                    Running = False
                    menu()

        lost.blit(GameOverText, (265, 100))
        lost.blit(TryAgainText, (280, 250))

        pygame.display.update()
    pygame.quit()

#/////////////////////////////////////////Win Window///////////////////////////////////////
# Contiene la ventana cuando el jugador gana y la logica para guardar el resultado
def win(time):
    pygame.init()
    win = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Space Invaders: Winner")                   
    #Se define la ventana

    pygame.mixer.init()
    win_sound = pygame.mixer.Sound('Sonidos/winsound.wav')
    win_sound.play()

    arialfont = pygame.font.SysFont('arial', 70)
    arialfontS = pygame.font.SysFont('arial', 30)
    CongratsText = arialfont.render("Congratsss!!" , 0, (255,255,255))
    NameText = arialfontS.render("Add your name", 0, (255,255,255))

    ReturnB = Button("Return to menu")
    ReturnB.setCords(310,440), ReturnB.setrangeEnd(145,35)

    SummitB = Button("Summit")
    SummitB.setCords(355, 380), SummitB.setrangeEnd(100,35)

    InputB = InputBox(320, 280, 150, 30, "")

    Saved = False
    Running = True
    while Running:
        pos = pygame.mouse.get_pos()
        win.blit(backgroundGame, (0,0))

        for event in pygame.event.get():
            InputB.handle_event(event)
            InputB.update()

            if event.type == pygame.QUIT:
                Running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ReturnB.pressed(pos):
                    Running = False
                    menu()
                if SummitB.pressed(pos) and Saved == False:
                    Saved = True
                    if InputB.get_text() != "":
                        data = open("ranking.txt", "a")
                        data.write("\nName: " + InputB.get_text() + "    Time: " + str(time))
                        data.close()
                        
                    
        if Saved == False:
            SummitB.draw(win, pos)
        ReturnB.draw(win, pos)
        InputB.draw(win)
        win.blit(NameText, (310, 240))
        win.blit(CongratsText, (235, 100))

        pygame.display.update()
    pygame.quit()

#//////////////////////////////////////Ranking Window//////////////////////////////////////
# Contiene la ventana para observar el ranking, carga toda la base de datos
def ranking():
    pygame.init()
    rankingW = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Space Invaders: Ranking")
    rankingW.blit(backgroundGame, (0,0))

    ReturnB = Button("Return to menu")
    ReturnB.setCords(610,550), ReturnB.setrangeEnd(145,35)

    param = 10
    arialfont = pygame.font.SysFont('arial', 30)

    data = open("ranking.txt", "r")
    dataL = data.readlines()
    for text in dataL:
        DataText = arialfont.render(text, 0, (255,255,255))
        param += 40
        rankingW.blit(DataText, (50, param))
    data.close()

    Running = True
    while Running:
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                Running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ReturnB.pressed(pos):
                    Running = False
                    menu()
                        
                    
        ReturnB.draw(rankingW, pos)

        pygame.display.update()
    pygame.quit()

#////////////////////////////////////////Help Window///////////////////////////////////////
# Contiene la ventana con la informacion de ayuda
def help():
    pygame.init()
    helpW = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Space Invaders: Help")
    backgroundHELP = pygame.image.load('Imagenes/BackgroundHELP.jpg') 
    helpW.blit(backgroundHELP, (0,0))

    ReturnB = Button("Return to menu")
    ReturnB.setCords(610,560), ReturnB.setrangeEnd(145,35)

    Running = True
    while Running:
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                Running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ReturnB.pressed(pos):
                    Running = False
                    menu()
                        
                    
        ReturnB.draw(helpW, pos)
        pygame.display.update()

    pygame.quit()

#//////////////////////////////////////////////////////////////////////////////////////////
# Se encarga de iniciar la funcion de menu solo una vez despues de compilar todo el archivo
if __name__ == "__main__":
    menu()