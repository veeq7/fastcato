import pygame
import Game

screen = pygame.display.set_mode((1600, 900))



def screenInitialize():
    pygame.display.set_caption('Cat Game')
    icon = pygame.image.load(f"images/gameIcon.png")
    pygame.display.set_icon(icon)


#Checks if user pressed 'X' button
def screenUpdate():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.Game.isRunning = False
        # TODO: remove
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            Game.Game.isRunning = False

    Game.Game.keyPressed = pygame.key.get_pressed()

def screenRender():
    pygame.display.update()
