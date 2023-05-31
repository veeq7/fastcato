import pygame

import BirdCounter
import Camera
import CloudManager
import Deadline
import Bird
import GameInfo
import MainMenu
import Player
import Block
from Obstacles import ObstacleManager
from Obstacles.Dog import Dog
from Obstacles.Hedgehog import Hedgehog


class LevelManager:
    IMG_LEVELS = []

    #SPECIAL COLORS
    PLAYER_SPAWN = (255, 0, 0, 255)
    FINISH_LINE = (200, 200, 0, 255)

    #BLOCKS
    GRASS = (80, 40, 40, 255)

    #ENITIES
    HEADGEHOG = (200, 100, 100, 255)
    DOG = (200, 120, 100, 255)

    currentLevel = 1
    currentLevelImg = pygame.image.load("images/levels/1.bmp")
    player = None

    @staticmethod
    def initialize():
        LevelManager.currentLevel = 0
        LevelManager._loadImages()
        LevelManager.restartLevel()

    @staticmethod
    def update():
        #print("update")
        if Bird.Bird.birdsOnMap() is 0:
            #if new record, then save it
            if GameInfo.GameInfo.levelTime[LevelManager.currentLevel] == 0.0 or \
                    GameInfo.GameInfo.levelTime[LevelManager.currentLevel] > Deadline.Deadline.time():
                GameInfo.GameInfo.levelTime[LevelManager.currentLevel] = Deadline.Deadline.time()
                GameInfo.GameInfo.saveSave()
            if Deadline.Deadline.time() <= 60:
                LevelManager.nextLevel()
            else:
                LevelManager.restartLevel()


    @staticmethod
    def restartLevel():
        Player.Player.getInstance().restart()
        Block.Block.allBlocks.clear()
        ObstacleManager.ObstacleManager.allObstacles.clear()
        Bird.Bird.allBirds.clear()

        try:
            LevelManager.currentLevelImg = LevelManager.IMG_LEVELS[LevelManager.currentLevel]
        except:
            LevelManager.currentLevelImg = LevelManager.IMG_LEVELS[1]

        if LevelManager.currentLevel == 0:
            Player.Player._instance = None
            MainMenu.MainMenu.open()
        else:
            LevelManager.loadLevel()

    @staticmethod
    def nextLevel():
        LevelManager.currentLevel += 1
        LevelManager.restartLevel()

    @staticmethod
    def loadLevel():
        for i in range(LevelManager.currentLevelImg.get_width()):
            for j in range(20):
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.GRASS:
                    Block.Block.createBlock(Block.BlockType.GRASS, (i, j))
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.PLAYER_SPAWN:
                    Player.Player.getInstance().startingPosition = (i * 50, j * 50)
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.HEADGEHOG:
                    obj = Hedgehog((i, j))
                    ObstacleManager.ObstacleManager.addObstackle(obj)
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.DOG:
                    obj = Dog((i, j))
                    ObstacleManager.ObstacleManager.addObstackle(obj)
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.FINISH_LINE:
                    Bird.Bird.create((i, j))

        Camera.Camera.borderRight = LevelManager.currentLevelImg.get_width() * 50 - 100
        BirdCounter.BirdCounter.restart()
        Block.Block.setBlocks()
        Player.Player.getInstance().restart()

    @staticmethod
    def _loadImages():
        try:
            LevelManager.IMG_LEVELS.append(None)
            for i in range(GameInfo.GameInfo.NUMBER_OF_LEVELS):
                img = pygame.image.load(f"images/levels/{i+1}.bmp")
                LevelManager.IMG_LEVELS.append(img)
        except:
            print("Not all levels *.bmp files are existing!")


