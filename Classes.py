import pygame as pg
import random
import time

class Menu:

    def __init__(self, windowWidth, windowHeight):
        self.difficulty = {'Easy' : 1, 'Normal' : 2, 'Hard' : 3}
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight

    def chooseDifficulty(self):
        pass

    def start(self):
        pass

    def gameOver(self, screen):
        time.sleep(1)
        WHITE= (255,255,255)
        rect = pg.Rect(0,0, 200, 200)
        rect.center = (self.windowWidth / 2, self.windowHeight / 2)
        pg.draw.rect(screen, WHITE, rect)

class Square:
    
    def __init__(self, x, y, size):
        self.rect = pg.Rect(x, y, size, size)
        self.revealed = False
        self.isMine = False
        self.hasFlag = False
        self.surrounding = 0
        self.clicked = False
        self.color = (200,200,200)
    
    def redrawSquare(self, screen):
        pg.draw.rect(screen, self.color, self.rect)
        pg.display.flip()

    def drawImage(self,screen, flagged = False):
            mine_image = pg.image.load('mine.png')
            mine_image = pg.transform.scale(mine_image, (20, 20))
            flag_image = pg.image.load('flag.png')
            flag_image = pg.transform.scale(flag_image, (20, 20))

            if not flagged:
                screen.blit(mine_image, self.rect)
            if flagged:
                screen.blit(flag_image, self.rect)

class Grid:

    def __init__(self, windowWidth, windowHeight, gridsize):
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.gridsize = gridsize
        self.grid = []

        self.menu = Menu(windowWidth, windowHeight)
    
    def createWindow(self):
        pg.init()
        SCREEN = pg.display.set_mode((self.windowWidth, self.windowHeight))
        CLOCK = pg.time.Clock()
        SCREEN.fill((200,200,200))

        return SCREEN, CLOCK
    
    def createGrid(self):
        for x in range(0, self.windowWidth, self.gridsize):
            row = []
            for y in range(0, self.windowHeight, self.gridsize):
                square = Square(x , y, self.gridsize)
                row.append(square)
            self.grid.append(row)
        
        return self.grid
    
    def drawGrid(self, screen):
        for row in self.grid:
            for square in row:
                pg.draw.rect(screen, (0,0,0), square.rect, 1)

    
    def run(self, mineAmount = 10):
        screen, clock = self.createWindow()
        handler = GridHandler(grid, mineAmount)
        gameOver = False

        font = pg.font.Font(None, 20)

        handler.randomizeMines() 

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.MOUSEBUTTONDOWN and not gameOver:
                    clickedSquare = handler.getClickedSquare(*event.pos)
                    if event.button == 1:
                        handler.countSurroundingMines()
                        
                        if not clickedSquare.isMine and not clickedSquare.clicked and clickedSquare.surrounding != 0:
                            clickedSquare.clicked = True
                            text = font.render(str(clickedSquare.surrounding), True, (0,0,0))
                            screen.blit(text, (clickedSquare.rect.x + 5, clickedSquare.rect.y + 5)) 
                        
                        if clickedSquare.isMine:
                            handler.hitMine(clickedSquare)
                            clickedSquare.redrawSquare(screen)
                            clickedSquare.drawImage(screen)
                            self.menu.gameOver(screen)
                            gameOver = True
                    if event.button == 3:
                        if not clickedSquare.hasFlag:
                            clickedSquare.drawImage(screen, True)
                        elif clickedSquare.hasFlag:
                            handler.removeFlag(clickedSquare)
                            clickedSquare.redrawSquare(screen)
                            clickedSquare.hasFlag = False
                        
                

                            
            
            self.drawGrid(screen)
            pg.display.flip()
            clock.tick(60)
        
        pg.quit()


class GridHandler:
    def __init__(self, grid, num_mines=10):
        self.grid = grid
        self.mines = num_mines

    def getClickedSquare(self, x, y):
        gridX = x // self.grid.gridsize
        gridY = y // self.grid.gridsize
        return self.grid.grid[gridX][gridY]

    def randomizeMines(self):
        minePos = random.sample(
            range(
                self.grid.windowWidth // self.grid.gridsize * self.grid.windowHeight // self.grid.gridsize
            ),
            self.mines,
        )
        for pos in minePos:
            x = pos // (self.grid.windowWidth // self.grid.gridsize)
            y = pos % (self.grid.windowWidth // self.grid.gridsize)
            self.grid.grid[x][y].isMine = True
        
    def countSurroundingMines(self):
        for row in self.grid.grid:
            for square in row:
                x, y = square.rect.x // self.grid.gridsize, square.rect.y // self.grid.gridsize
                surroundingMines = 0

                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0 <= x + i < self.grid.windowWidth // self.grid.gridsize and 0 <= y + j < self.grid.windowHeight // self.grid.gridsize:
                            if self.grid.grid[x + i][y + j].isMine:
                                surroundingMines += 1
                if not square.isMine:
                    square.surrounding = surroundingMines
    
    def hitMine(self, square):
        square.color = (255,0,0)

    def removeFlag(self, square):
        square.color = (255,255,255)


grid = Grid(400, 400, 20)
grid.createGrid()

grid.run()