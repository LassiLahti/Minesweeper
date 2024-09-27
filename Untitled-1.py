import pygame
import sys
import random

BLACK = (0,0,0)
WHITE = (200,200,200)
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
leftClickedSquares = []
rigtClickedSquares = []

def main():

    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(WHITE)
    size = 20
    mines = 40
    grid = create_grid(size, mines)
    countSurroundingMines(grid, size)

    while True:
        
        drawGrid(grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    square = getClickedSquare(grid, x, y)
                    if square is not None:
                        square['color'] = (0,255,0)
                        leftClickedSquares.append(square)
                        pygame.draw.rect(SCREEN, square['color'], square['rect'])
                        square['color'] = BLACK
                        pygame.draw.rect(SCREEN, square['color'], square['rect'], 1)
                if event.button == 3:
                    x, y = pygame.mouse.get_pos()
                    square = getClickedSquare(grid, x, y)
                    if square not in leftClickedSquares:
                        if square is not None:
                            rigtClickedSquares.append(square)
                    if square in rigtClickedSquares and square['has_flag']:
                        square['has_flag'] = False
                        square['color'] = WHITE
                        pygame.draw.rect(SCREEN, square['color'], square['rect'])
                        square['color'] = BLACK
                        pygame.draw.rect(SCREEN, square['color'], square['rect'], 1)
                                
        pygame.display.update()
        CLOCK.tick(60)

def create_grid(gridsize, amount):
    size = gridsize
    grid = []
    for x in range(0, WINDOW_WIDTH, size):
        for y in range(0, WINDOW_HEIGHT, size):
            rect = pygame.Rect(x, y, size, size)
            grid.append({'rect': rect, 'color': BLACK, 'is_mine' : False, 'surround': 0, 'has_flag': False})
    placeMines(grid, amount)
    return grid

def drawGrid(grid):

    font = pygame.font.Font(None, 20)
    mine_image = pygame.image.load('mine.png')
    mine_image = pygame.transform.scale(mine_image, (20, 20))
    flag_image = pygame.image.load('flag.png')
    flag_image = pygame.transform.scale(flag_image, (20, 20))

    for square in grid:
        if square['is_mine'] and square in leftClickedSquares:
            square['color'] = (255,0,0)
            pygame.draw.rect(SCREEN, square['color'], square['rect'])
            SCREEN.blit(mine_image, square['rect'])
            square['color'] = BLACK
            pygame.draw.rect(SCREEN, square['color'], square['rect'], 1)
        if square in rigtClickedSquares and not square['has_flag']:
            square['has_flag'] = True
            SCREEN.blit(flag_image, square['rect'])

        pygame.draw.rect(SCREEN, square['color'], square['rect'], 1)
        if square['surround'] != 0 and square in leftClickedSquares:
            text = font.render(str(square['surround']), True, BLACK)
            cent = text.get_rect(center=square['rect'].center)
            SCREEN.blit(text,cent)

def getClickedSquare(grid, x, y):
    
    for square in grid:
        if square['rect'].collidepoint(x, y):
            return square
    return None

def countSurroundingMines(grid, size):
    for square in grid:
        x, y = square['rect'].x // size, square['rect'].y // size
        surrounding_mines = 0

        for i in range(-1, 2): 
            for j in range(-1, 2):
                if 0 <= x + i < WINDOW_WIDTH // size and 0 <= y + j < WINDOW_HEIGHT // size:
                    idx = (x + i) * (WINDOW_HEIGHT // size) + (y + j)
                    if grid[idx]['is_mine']: 
                        surrounding_mines += 1
        if not square['is_mine']:
            square['surround'] = surrounding_mines

def placeMines(grid, amount):
    minePos = random.sample(range(len(grid)), amount)
    for pos in minePos:
        grid[pos]['is_mine'] = True

main()