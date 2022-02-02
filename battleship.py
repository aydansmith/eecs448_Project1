from matplotlib.pyplot import pause
import pygame
import sys

# following code is inspired and similar to thread on creating a grid for a snake game in pygane
# https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 430

def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    player1ShipBoard = createPlayer1ShipGrid() # 2-D array with rects stored in it
    player1TargetBoard = createPlayer1TargetGrid() # 2-D array with rects stored in it
    player2ShipBoard = createPlayer1ShipGrid() # 2-D array with rects stored in it
    player2TargetBoard = createPlayer1TargetGrid() # 2-D array with rects stored in it
    player1hits=[]
    player1misses=[]
    player2hits=[]
    player2misses=[]
    #print(getRow(player1ShipBoard, (player1ShipBoard[1])[0]))
    #print(len(player1ShipBoard))
    while True:
        pos = pygame.mouse.get_pos()
        printBoard(player1ShipBoard, player1hits)
        printBoard(player1TargetBoard, player1hits)
        # createPlayer1ShipGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #player1hits.append((player1ShipBoard[0])[0])
                player1hits = checkForCollision(player1TargetBoard, pos, player1hits)

        pygame.display.update()

def checkForCollision(board, pos, hits):
    for x in range(0, len(board)):
        for y in range(0, len(board)):
            tempRect = (board[x])[y]
            if tempRect.collidepoint(pos):
                hits.append(tempRect)
                return(hits)
    return hits

def getRow(board, rect):
    for x in range(0, (len(board))):
        for y in range(0,(len(board))):
            tempRect = (board[x])[y]
            if tempRect == rect:
                return x
    return -1

def getCol(board, rect):
    for x in range(0, 9):
        for y in range(0,9):
            tempRect = (board[x])[y]
            if tempRect == rect:
                return y
    return -1

def inHits(board, rect):
    for x in board:
        if rect == x:
            return True
    return False


def createPlayer1ShipGrid():
    blockSize = 20 #Set the size of the grid block
    playerBoard = []
    for x in range(0, 200, blockSize):
        subBoard = []
        for y in range(100, 300, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            subBoard.append(rect)
            #pygame.draw.rect(SCREEN, WHITE, rect, 1)
        playerBoard.append(subBoard)
    return playerBoard

def createPlayer1TargetGrid():
    blockSize = 20 #Set the size of the grid block
    playerBoard = []
    for x in range(230, WINDOW_WIDTH, blockSize):
        subBoard = []
        for y in range(100, 300, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            subBoard.append(rect)
            #pygame.draw.rect(SCREEN, WHITE, rect, 1)
        playerBoard.append(subBoard)
    return playerBoard


def printBoard(board, hits):
    for x in board:
        for y in x:
            if(inHits(hits, y)):
                pygame.draw.rect(SCREEN, RED, y, 1)
            else:
                pygame.draw.rect(SCREEN, WHITE, y, 1)

def createPlayer1ShipGridNew():
    blockSize = 20 #Set the size of the grid block
    playerBoard = []
    for x in range(0, 200, blockSize):
        for y in range(100, 300, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            playerBoard.append(rect)
            #pygame.draw.rect(SCREEN, WHITE, rect, 1)
    
    for x in range(230, WINDOW_WIDTH, blockSize):
        for y in range(100, 300, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            #pygame.draw.rect(SCREEN, WHITE, rect, 1)


main()
