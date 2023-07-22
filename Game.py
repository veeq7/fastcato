import pygame
import asyncio

import src.EventHandler as EventHandler
from src.CatSmall import CatSmall
from src.Credits import Credits
from src.Icons import Icons
from src.CloudManager import CloudManager
from src.Bird import Bird
from src.Block import Block
from src.Camera import Camera
from src.Decorations import Decorations
from src.GameInfo import GameInfo
from src.HUD.BirdCounter import BirdCounter
from src.HUD.Deadline import Deadline
from src.InGameMenu import InGameMenu
from src.InnerTimer import InnerTime
from src.LevelManager import LevelManager
from src.MainMenu import MainMenu
from src.Music import Music
from src.Obstacles.ObstacleManager import ObstacleManager
from src.Player import Player
from src.Result import Result
from src.Screen import screenRender, screenInitialize
from src.Background import Background

class Game:
    isRunning = True
    keyPressed = None

    def __init__(self):
        self._maxFps = 120
        self._clock = pygame.time.Clock()
        GameInfo.load()
        Music.start()
        LevelManager.initialize()
        screenInitialize()
        CloudManager.initialize()


    def update(self):
        InnerTime.update()
        #InnerTime.showFps()
        EventHandler.update()
        if MainMenu.state is not MainMenu.state.CLOSED:
            MainMenu.update()
        else:
            if InGameMenu.state == InGameMenu.State.OPEN:
                InGameMenu.update(Game.keyPressed)
                Game.keyPressed = None
            if Result.state == Result.State.OPEN:
                Game.keyPressed = None
            LevelManager.update()
            ObstacleManager.updateAll()
            Player.getInstance().update(Game.keyPressed)
            CatSmall.getInstance().update()
            Bird.updateAll()
            Camera.update(Player.getInstance())  # must be called after player update
            Background.getInstance().update()
            Deadline.update(Game.keyPressed)

    def render(self):
        if MainMenu.state is not MainMenu.state.CLOSED:
            MainMenu.render()
        else:
            Background.getInstance().render()
            if LevelManager.currentLevel == 7:
                Credits.renderText()
            Block.renderBackground()
            Icons.renderAll()
            Decorations.renderAll()
            Player.getInstance().render()
            CatSmall.getInstance().render()
            ObstacleManager.renderAll()
            Bird.renderAll()
            Block.renderBlocks()
            if LevelManager.currentLevel == 7:
                Credits.renderFade()
            if Result.state == Result.State.CLOSED:
                Deadline.render()
                BirdCounter.render()
            if InGameMenu.state == InGameMenu.State.OPEN:
                InGameMenu.render()
            elif Result.state == Result.State.OPEN:
                Result.render()
        screenRender()

    def delay(self):
        self._clock.tick(self._maxFps)

    def exit(self):
        pygame.quit()

async def main():
    game = Game()
    while Game.isRunning:
        game.update()
        game.render()
        await asyncio.sleep(0)
        game.delay()

    game.exit()

asyncio.run(main())