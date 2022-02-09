import copy
from operator import truediv
from matplotlib.pyplot import pause
import pygame
import sys
import add_text
import place_ships

# following code is inspired and similar to thread on creating a grid for a snake game in pygane
# https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 430
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
def main():
    global SCREEN, CLOCK
    pygame.init()
    #SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    # font text is from https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
    player1ShipBoard = createPlayer1ShipGrid() # 2-D array with rects stored in it
    player1TargetBoard = createPlayer1TargetGrid() # 2-D array with rects stored in it
    player1hits=[]
    player1misses=[]
    player1ships = [4,4,2,2]
    player1placedShips = [[],[],[],[]]
    copyPlayer1placedShips = []
    player2ShipBoard = createPlayer1ShipGrid() # 2-D array with rects stored in it
    player2TargetBoard = createPlayer1TargetGrid() # 2-D array with rects stored in it
    player2hits=[]
    player2misses=[]
    player2ships = [4,4,2,2]
    player2placedShips = [[],[],[],[]]
    copyPlayer2placedShips = []
    player1Turn = True
    player1ready = False
    player2ready = False
    gameover = False
    #print(getRow(player1ShipBoard, (player1ShipBoard[1])[0]))
    #print(len(player1ShipBoard))
    
    while not gameover:
        pos = pygame.mouse.get_pos()
        if not player1ready:
            place_ships.placePlayer1Ships(SCREEN, player1ships, player1placedShips, player1ShipBoard)
            player1ready = True
            copyPlayer1placedShips = createShallowCopy(player1placedShips)  
        if not player2ready:
            place_ships.placePlayer2Ships(SCREEN, player2ships, player2placedShips, player2ShipBoard)
            player2ready = True
            copyPlayer2placedShips = createShallowCopy(player2placedShips)  
        add_text.add_text(SCREEN, 'Battleship')
        if(player1Turn):
            add_text.add_text(SCREEN, 'Player 1 Turn')
            printShipBoard(player1ShipBoard, player1placedShips)
            printBoard(player1TargetBoard, player1hits, player1misses)
        else:
            add_text.add_text(SCREEN, 'Player 2 Turn')
            printShipBoard(player2ShipBoard, player2placedShips)
            printBoard(player2TargetBoard, player2hits, player2misses)
        # createPlayer1ShipGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #player1hits.append((player1ShipBoard[0])[0])
                if(player1Turn):
                    played = checkForCollision(player1TargetBoard, player2ShipBoard, pos, player1hits, player1misses, player2placedShips, copyPlayer2placedShips)
                    if played: 
                        printShipBoard(player1ShipBoard, player1placedShips)
                        printBoard(player1TargetBoard, player1hits, player1misses)
                        pygame.display.update()
                        sunkenShip = shipSunk(copyPlayer2placedShips)
                        if(sunkenShip):
                            add_text.add_text(SCREEN, 'You sunk a ship!')
                            pygame.display.update()
                            ended = gameIsOver(copyPlayer2placedShips)
                            if ended:
                                gameover = True
                                add_text.add_text(SCREEN, 'Player 1 won!')
                                pygame.display.update()
                        pause(3)
                        player1Turn = False
                else:
                    played = checkForCollision(player2TargetBoard, player1ShipBoard, pos, player2hits, player2misses, player1placedShips, copyPlayer1placedShips)
                    if played:
                        printShipBoard(player2ShipBoard, player2placedShips)
                        printBoard(player2TargetBoard, player2hits, player2misses)
                        pygame.display.update()
                        sunkenShip = shipSunk(copyPlayer1placedShips)
                        if(sunkenShip):
                            add_text.add_text(SCREEN, 'You sunk a ship!')
                            pygame.display.update()
                            ended = gameIsOver(copyPlayer1placedShips)
                            if ended:
                                gameover = True
                                add_text.add_text(SCREEN, 'Player 2 won!')
                                pygame.display.update()
                        pause(3)
                        player1Turn = True
                #player1Turn = switchTurn(player1Turn)

        pygame.display.update()

def createShallowCopy(ships):
    temp = []
    temp2 = []
    for x in ships:
        temp2 = []
        for y in x:
            temp2.append(y)
        temp.append(temp2)
    return temp

def checkForCollision(targetBoard, shipBoard, pos, hits, misses, shipsPlaced, shipsCopy):
    hit = False
    rect = getRectangle(targetBoard, pos)
    row = getRow(targetBoard, rect)
    col = getCol(targetBoard, rect)
    if row == -1 or col == -1:
        return False
    else:
        tempRectTarget = (targetBoard[row])[col]
        tempRectShip = (shipBoard[row])[col]
        alreadyHit = inHits(hits, tempRectShip)
        alreadyMissed = inMisses(misses, tempRectShip)
        if alreadyHit or alreadyMissed: 
            return False
        inShipsList = inShips(shipsPlaced, tempRectShip)
        if inShipsList:
            add_text.add_text(SCREEN, 'You hit a ship!')
            hits.append(tempRectTarget)
            hits.append(tempRectShip)
            removeFromShipsCopy(tempRectShip, shipsCopy)

        else:
            add_text.add_text(SCREEN, 'You did not hit a ship!')
            misses.append(tempRectTarget)
            misses.append(tempRectShip)
    return True
    
def removeFromShipsCopy(rect, shipsCopy):
    for x in shipsCopy:
        for y in x:
            if rect == y:
                x.remove(y)

def shipSunk(shipsCopy):
    for x in shipsCopy:
        if(len(x) == 0):
            shipsCopy.remove(x)
            return True
    return False

def gameIsOver(shipsCopy):
    if(len(shipsCopy) == 0):
        return True
    else:
        return False

def getRectangle(board, pos):
    for x in range(0, len(board)):
        for y in range(0, len(board)):
            tempRect = (board[x])[y]
            if tempRect.collidepoint(pos):
                return tempRect

def getRow(board, rect):
    tempRect = None
    for x in range(0, 10):
        for y in range(0,10):
            tempRect = (board[x])[y]
            if tempRect == rect:
                return x
    #print(tempRect)
    return -1

def getCol(board, rect):
    tempRect = None
    for x in range(0, 10):
        for y in range(0,10):
            tempRect = (board[x])[y]
            if tempRect == rect:
                return y
    #print(tempRect)
    return -1

def inHits(board, rect):
    for x in board:
        if rect == x:
            return True
    return False

def inMisses(board, rect):
    for x in board:
        if rect == x:
            return True
    return False

def inShips(board, rect):
    for x in board:
        for y in x:
            if rect == y:
                return True
    return False

def inHitShips(hits, rect):
    for x in hits:
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


def printBoard(board, hits, misses):
    for x in board:
        for y in x:
            if(inHits(hits, y)):
                pygame.draw.rect(SCREEN, RED, y, 1)
            elif(inMisses(misses, y)):
                pygame.draw.rect(SCREEN, GREEN, y, 1)
            else:
                pygame.draw.rect(SCREEN, WHITE, y, 1)

def printShipBoard(board, ships):
    for x in board:
        for y in x:
            if(inShips(ships, y)):
                pygame.draw.rect(SCREEN, BLUE, y, 1)
            else:
                pygame.draw.rect(SCREEN, WHITE, y, 1)


if __name__ == "__main__":
    main()
