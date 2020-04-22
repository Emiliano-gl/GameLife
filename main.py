import pygame
import numpy as np
import time

pygame.init()

# Ancho y alto de la pantalla
width, height = 900, 900
# Creación de la pantalla
screen = pygame.display.set_mode((height, width))

# Color de la pantalla
bg = 38, 38, 38
# Coloreado de la pantalla
screen.fill(bg)

# Cantidad de celdas
nxC, nyC = 50, 50

# Dimensiones de las celdas
dimCW = width / nxC
dimCH = height / nyC

# Estado de las celdas, Viva = 1, Muerta = 0
gameState = np.zeros((nxC, nyC))

# Control de ejecución del juego
pauseExect = False

# Bucle de ejecución
while True:

    newGameState = np.copy(gameState)
    screen.fill(bg)
    time.sleep(0.1)

    # Registramos los eventos
    ev = pygame.event.get()

    for event in ev:
        # Detectamos si se presiona una tecla
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        # Detectamos si se quiere salir del programa
        if event.type == pygame.QUIT:
            pygame.quit()

        # Detectamos si se presiona el mouse
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY  = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]


    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExect:

                # Calculamos los vecinos cercanos
                n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
                    gameState[(x) % nxC, (y-1) % nyC] + \
                    gameState[(x+1) % nxC, (y-1) % nyC] + \
                    gameState[(x-1) % nxC, (y) % nyC] + \
                    gameState[(x+1) % nxC, (y) % nyC] + \
                    gameState[(x-1) % nxC, (y+1) % nyC] + \
                    gameState[(x) % nxC, (y+1) % nyC] + \
                    gameState[(x+1) % nxC, (y+1) % nyC]

                # Regla #1: Una célula muerta con exactamente 3 vecinas vivas, "Revive"
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # Regla #2: Una célula viva con menos de 2 o mas de 3 vecinas vivas, "Muere"
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            # Creamos el polígono de cada celda a dibujar
            poly = [
                ((x) * dimCW, y * dimCH),
                ((x+1) * dimCW, y * dimCH),
                ((x+1) * dimCW, (y+1) * dimCH),
                ((x) * dimCW, (y+1) * dimCH)
            ]

            # Dibujamos la celda para cada par de x e y
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (89, 89, 89), poly, 1)
            else:
                pygame.draw.polygon(screen, (217, 217, 217), poly, 0)

    # Actualizamos el estado del juego
    gameState = np.copy(newGameState)

    # Actualizamos la pantalla
    pygame.display.flip()
