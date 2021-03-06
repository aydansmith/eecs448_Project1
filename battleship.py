import copy
from operator import truediv
from matplotlib.pyplot import pause
import pygame
import sys
import add_text
import place_ships
import get_ships_num

#colors in RGB form
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
# height of window for pygame
WINDOW_HEIGHT = 400
#width of window for pygame
WINDOW_WIDTH = 490
#initializes screen in pygame
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# main handles all the logic and passing between files
def main():
    # following code is inspired and similar to thread on creating a grid for a snake game in pygane
    # https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
    global SCREEN, CLOCK
    # initializes pygame
    pygame.init()
    # creates clock in pygame
    CLOCK = pygame.time.Clock()
    #fill screen to black
    SCREEN.fill(BLACK)

    player1ShipBoard = createPlayer1ShipGrid() # 2-D array with rects stored in it, represents player1board for their own ships
    player1TargetBoard = createPlayer1TargetGrid() # 2-D array with rects stored in it, represents the targets for player 1
    player1hits=[] # will store rect objects of hits
    player1misses=[] # will store rect objects of misses
    player1ships = [] # will hold the sizes for ships
    player1placedShips = [[],[],[],[]]  # 2d array that will hold the placed ships for player 1
    copyPlayer1placedShips = [] # non pointer copy of player1placedShips
    # same as objects above but for player 2
    player2ShipBoard = createPlayer1ShipGrid() # 2-D array with rects stored in it
    player2TargetBoard = createPlayer1TargetGrid() # 2-D array with rects stored in it
    player2hits=[]
    player2misses=[]
    player2ships = []
    player2placedShips = [[],[],[],[]]
    copyPlayer2placedShips = []
    # keeps track of if it is player 1 turn
    player1Turn = True
    # track if ships have been placed
    player1ready = False
    player2ready = False
    # track if game is over
    gameover = False
    # get the number of ships that the user wants for the game and returns a 4 tupe with size and empty placed ships array
    arrays = get_ships_num.get_ships(player1ships, player2ships, SCREEN, player1placedShips, player2placedShips)
    player1ships = arrays[0]
    player2ships = arrays[1]
    player1placedShips = arrays[2]
    player2placedShips = arrays[3]
    
    #run while the game is not ended
    while not gameover:
        # gets the position of the mouse on the screen
        pos = pygame.mouse.get_pos()
        # if player 1 is not ready, pass to place_ships and have player 1 place their ships
        if not player1ready:
            place_ships.placePlayer1Ships(SCREEN, player1ships, player1placedShips, player1ShipBoard)
            player1ready = True
            #create non pointer copy
            copyPlayer1placedShips = createShallowCopy(player1placedShips)  
        # repeat for player 2
        if not player2ready:
            place_ships.placePlayer2Ships(SCREEN, player2ships, player2placedShips, player2ShipBoard)
            player2ready = True
            copyPlayer2placedShips = createShallowCopy(player2placedShips)  
        # add text saying battleship and add rows and cols
        add_text.add_text(SCREEN, 'Battleship')
        add_text.add_labels_targets(SCREEN)
        # if it is player 1 turn, say that and print their boards
        if(player1Turn):
            add_text.add_text(SCREEN, 'Player 1 Turn')
            printShipBoard(player1ShipBoard, player1placedShips, player2hits)
            printBoard(player1TargetBoard, player1hits, player1misses)
            add_text.add_labels_middle(SCREEN)
            add_text.add_labels_ships(SCREEN)
        # if it is player 2 turn, say that and print their boards
        else:
            add_text.add_text(SCREEN, 'Player 2 Turn')
            printShipBoard(player2ShipBoard, player2placedShips, player1hits)
            printBoard(player2TargetBoard, player2hits, player2misses)
            add_text.add_labels_middle(SCREEN)
            add_text.add_labels_ships(SCREEN)
        # handles events in pygame
        for event in pygame.event.get():
            # if the user wants to quit, close pygame
            # if the user clicks, we respond accordingly
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # if it is player 1 turn, check for a hit and checkForCollision will handle all the logic for updating hits and misses
                if(player1Turn):
                    played = checkForCollision(player1TargetBoard, player2ShipBoard, pos, player1hits, player1misses, player2placedShips, copyPlayer2placedShips)
                    if played: 
                        # if they made a valid move, update the boards
                        printShipBoard(player1ShipBoard, player1placedShips, player2hits)
                        printBoard(player1TargetBoard, player1hits, player1misses)
                        add_text.add_labels_middle(SCREEN)
                        add_text.add_labels_ships(SCREEN)
                        pygame.display.update()
                        # check for a sunk ship
                        sunkenShip = shipSunk(copyPlayer2placedShips)
                        # if they sunk a ship, check if all ships are sunk
                        if(sunkenShip):
                            add_text.add_text(SCREEN, 'You sunk a ship!')
                            pygame.display.update()
                            ended = gameIsOver(copyPlayer2placedShips)
                            if ended:
                                gameover = True
                                add_text.add_text(SCREEN, 'Player 1 won!')
                                pygame.display.update()
                        # wait for three seconds and switch turn
                        pause(3)
                        if not gameover:
                            add_text.add_black_screen(SCREEN)
                            pygame.display.update()
                            pause(2)
                        player1Turn = False
                else:
                    # otherwise repeat for player 2
                    played = checkForCollision(player2TargetBoard, player1ShipBoard, pos, player2hits, player2misses, player1placedShips, copyPlayer1placedShips)
                    if played:
                        printShipBoard(player2ShipBoard, player2placedShips, player1hits)
                        printBoard(player2TargetBoard, player2hits, player2misses)
                        add_text.add_labels_middle(SCREEN)
                        add_text.add_labels_ships(SCREEN)
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
                        if not gameover:
                            add_text.add_black_screen(SCREEN)
                            pygame.display.update()
                            pause(2)
                        player1Turn = True

        pygame.display.update()

# creates a shallow copy of a 2d array
def createShallowCopy(ships):
    temp = []
    temp2 = []
    for x in ships:
        temp2 = []
        for y in x:
            temp2.append(y)
        temp.append(temp2)
    return temp

# handles logic for user click
def checkForCollision(targetBoard, shipBoard, pos, hits, misses, shipsPlaced, shipsCopy):
    hit = False 
    # get the rect object and row and col
    rect = getRectangle(targetBoard, pos)
    row = getRow(targetBoard, rect)
    col = getCol(targetBoard, rect)
    # if you have an invalid row, then you did not hit anything and need new user input
    if row == -1 or col == -1:
        return False
    else:
        # otherwisecheck if you already hit the ship or already missed it, since you would need new user input
        tempRectTarget = (targetBoard[row])[col]
        tempRectShip = (shipBoard[row])[col]
        alreadyHit = inHits(hits, tempRectShip)
        alreadyMissed = inMisses(misses, tempRectShip)
        if alreadyHit or alreadyMissed: 
            return False
        # if it is in their ships, you have a hit
        inShipsList = inShips(shipsPlaced, tempRectShip)
        if inShipsList:
            add_text.add_text(SCREEN, 'You hit a ship!')
            hits.append(tempRectTarget)
            hits.append(tempRectShip)
            removeFromShipsCopy(tempRectShip, shipsCopy)
        else:
            # otherwise you missed
            add_text.add_text(SCREEN, 'You did not hit a ship!')
            misses.append(tempRectTarget)
            misses.append(tempRectShip)
    # return true since if you make it this far is was a valud move
    return True

# removes rect from the copy so that you can track what ships have been hit    
def removeFromShipsCopy(rect, shipsCopy):
    for x in shipsCopy:
        for y in x:
            if rect == y:
                x.remove(y)

#checks if an array within 2-d array is empty. If so you have a sunk ship
def shipSunk(shipsCopy):
    for x in shipsCopy:
        if(len(x) == 0):
            shipsCopy.remove(x)
            return True
    return False

# if shipsCopy has length 0 then all ships are sunk and game is over
def gameIsOver(shipsCopy):
    if(len(shipsCopy) == 0):
        return True
    else:
        return False

# return rect object given the board and mouse position
# based off of https://stackoverflow.com/questions/7415109/creating-a-rect-grid-in-pygame
def getRectangle(board, pos):
    for x in range(0, len(board)):
        for y in range(0, len(board)):
            tempRect = (board[x])[y]
            if tempRect.collidepoint(pos):
                return tempRect

# return row of a rectangle
def getRow(board, rect):
    tempRect = None
    for x in range(0, 10):
        for y in range(0,10):
            tempRect = (board[x])[y]
            if tempRect == rect:
                return x
    #print(tempRect)
    return -1

# return column of a rectangle
def getCol(board, rect):
    tempRect = None
    for x in range(0, 10):
        for y in range(0,10):
            tempRect = (board[x])[y]
            if tempRect == rect:
                return y
    #print(tempRect)
    return -1

# check if a rectangle is in the hits array
def inHits(board, rect):
    for x in board:
        if rect == x:
            return True
    return False

# check if a rectangle is in the misses array
def inMisses(board, rect):
    for x in board:
        if rect == x:
            return True
    return False

# check if a rectangle is in the ships 2-d array
def inShips(board, rect):
    for x in board:
        for y in x:
            if rect == y:
                return True
    return False

# check if a rectangle is in the hit ships array
def inHitShips(hits, rect):
    for x in hits:
        if rect == x:
            return True
    return False

# following code is inspired and similar to thread on creating a grid for a snake game in pygane
# https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
# creates grid (10x10) with width and height of 20 for each block
def createPlayer1ShipGrid():
    blockSize = 20 #Set the size of the grid block
    playerBoard = []
    for x in range(30, 230, blockSize):
        subBoard = []
        for y in range(100, 300, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            subBoard.append(rect)
            #pygame.draw.rect(SCREEN, WHITE, rect, 1)
        playerBoard.append(subBoard)
    return playerBoard

# following code is inspired and similar to thread on creating a grid for a snake game in pygane
# https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
# creates grid (10x10) with width and height of 20 for each block
def createPlayer1TargetGrid():
    blockSize = 20 #Set the size of the grid block
    playerBoard = []
    for x in range(260, WINDOW_WIDTH-30, blockSize):
        subBoard = []
        for y in range(100, 300, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            subBoard.append(rect)
            #pygame.draw.rect(SCREEN, WHITE, rect, 1)
        playerBoard.append(subBoard)
    return playerBoard

# following code is inspired and similar to thread on creating a grid for a snake game in pygane
# https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
# prints a board given 2-d array created in above functions. checks for hits and misses and changes color accordingly
def printBoard(board, hits, misses):
    for x in board:
        for y in x:
            if(inHits(hits, y)):
                pygame.draw.rect(SCREEN, RED, y, 1)
            elif(inMisses(misses, y)):
                pygame.draw.rect(SCREEN, GREEN, y, 1)
            else:
                pygame.draw.rect(SCREEN, WHITE, y, 1)

# following code is inspired and similar to thread on creating a grid for a snake game in pygane
# https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
# prints a board given 2-d array created in above functions. shows which of your ships have been hit
def printShipBoard(board, ships, hits):
    for x in board:
        for y in x:
            if(inShips(ships, y)):
                if(inHits(hits, y)):
                    pygame.draw.rect(SCREEN, RED, y, 1)
                else:
                    pygame.draw.rect(SCREEN, BLUE, y, 1)
            else:
                pygame.draw.rect(SCREEN, WHITE, y, 1)

# so that each import does not call main function
if __name__ == "__main__":
    main()
