import numpy
import sys
import pygame
pygame.init()
pygame.font.init()

def gameOver():
    for i in range(4):
        for j in range(4):
            if grid[i][j] == 0:
                return False
            if (i != 3) and (grid[i][j] == grid[i+1][j]):
                return False
            if (j != 3) and (grid[i][j] == grid[i][j+1]):
                return False
    return True

def winner():
    return numpy.isin(2048, grid)

def addNumber():
    empty = numpy.where(grid == 0)
    index = numpy.random.randint(len(empty[0]))
    r = numpy.random.uniform()
    grid[empty[0][index]][empty[1][index]] = 2 if r > 0.1 else 4

def slide(arr):
    arr = numpy.array(arr, dtype=int)
    arr = arr[arr != 0]
    missing = 4 - len(arr)
    zeros = numpy.zeros(missing, dtype=int)
    arr = numpy.concatenate((zeros, arr), axis=0)
    return arr

def combine(arr):
    for i in range(3, 0, -1):
        a = arr[i]
        b = arr[i-1]
        if a == b:
            arr[i] = a + b
            global score
            score += arr[i]
            arr[i-1] = 0
    return arr

def operate(grid):
    for i in range(4):
        grid[i] = slide(grid[i])
        grid[i] = combine(grid[i])
        grid[i] = slide(grid[i])
    return grid

def flipGrid(grid):
    return numpy.fliplr(grid)

def rotateGrid(grid):
    return grid.T

def updateCanvas():
    canvas.fill((250, 255, 240))
    game_surface.fill((171, 153, 138))
    title = title_text.render("2048", True, (51, 51, 51))
    w_title, h_title = tuple(title.get_rect())[2:4]
    Score = score_text.render("SCORE: {}".format(score), True, (100, 100, 100))
    w_score, h_score = tuple(Score.get_rect())[2:4]
    done = score_text.render("GAME OVER", True, (80, 80, 80))
    victory = score_text.render("YOU WON!", True, (80, 80, 80))
    w_victory, h_victory = tuple(victory.get_rect())[2:4]

    if gameOver():
        canvas.blit(done, (width / 2 + w_score, 10 + h_title + 10))

    if winner():
        canvas.blit(victory, (width / 2 - w_victory - 100, 10 + h_title + 10))

    canvas.blit(title, (width / 2 - w_title / 2, 10))
    canvas.blit(Score, (width / 2 - w_score / 2, 10 + h_title + 10))
    for i in range(4):
        for j in range(4):
            pygame.draw.rect(game_surface, (145, 130, 115), (i*w, j*w, w, w), lw)
            if grid[i][j] != 0:
                s = len(str(grid[i][j]))
                fs = [64, 60, 50, 40]
                game_text = pygame.font.SysFont("Arial", fs[s-1], True)
                number = game_text.render(str(grid[i][j]), True, (255, 255, 255))
                w_, h_ = tuple(number.get_rect())[2:4]
                game_surface.blit(number, (i*w + w / 2 - w_/2, j*w + w / 2 - h_/2))
    canvas.blit(game_surface, (50, 170))
    pygame.display.update()    

# Setup
lw = 10
size = width, height = 500, 600
canvas = pygame.display.set_mode(size)
pygame.display.set_caption("2048")
game_surface = pygame.Surface((400, 400))
grid = numpy.zeros(shape=(4, 4), dtype=int) 
addNumber()
addNumber()
w = 400 / 4
title_text = pygame.font.SysFont("Arial", 100, True)
score_text = pygame.font.SysFont("Arial", 20)
score = 0
updateCanvas()

# Draw
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            past = numpy.copy(grid)
            flipped = False
            rotated = False
            played = True

            # DOWN
            if event.key == 274:
                pass

            # UP
            elif event.key == 273:
                grid = flipGrid(grid)
                flipped = True

            # RIGHT
            elif event.key == 275:
                grid = rotateGrid(grid)
                rotated = True

            # LEFT
            elif event.key == 276:
                grid = rotateGrid(grid)
                grid = flipGrid(grid)
                rotated = True
                flipped = True

            else:
                played = False

            if played:
                grid = operate(grid)
                
                if flipped:
                    grid = flipGrid(grid)
                if rotated:
                    grid = rotateGrid(grid)
                if not numpy.array_equal(grid, past):
                    addNumber()
            updateCanvas()
