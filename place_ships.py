from audioop import add
import math
from matplotlib.pyplot import pause
from numpy import place
import pygame
import sys
import battleship
import add_text
import time
from random import randint

# handles placing of player 1s ships
def placePlayer1Ships(screen, ships, placedShips, shipBoard):
    shipsCopy = ships
    index = 0
    shipLength = shipsCopy[0]
    initialLength = shipLength
    # timing from https://stackoverflow.com/questions/7370801/how-to-measure-elapsed-time-in-python
    # tracks time to place a ship
    startTime = time.time()
    # while the length of ships copy is greater than zero, we need to add ships
    while len(shipsCopy) > 0:
        # check on time
        currentTime = time.time()
        # if it is greater than 15 sec, exit the game
        if currentTime - startTime > 15:
            add_text.time_out(screen)
            pygame.display.update()
            pause(3)
            pygame.quit()
            sys.exit()
        # if shipLength is greater than zero, we need to add ships
        if(shipLength > 0):
            # display that ship needs to be added
            stringofint = (str)(initialLength)
            toDisplay = 'Player 1, place your ship of length ' + stringofint
            add_text.add_text(screen, toDisplay)
            add_text.add_labels_ships(screen)
            add_text.add_labels_middle(screen)
            # get mouse position
            pos = pygame.mouse.get_pos()
            # print ship board for player 1
            battleship.printShipBoard(shipBoard, placedShips, [], [])
            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # if the mouse was clicked, check that the ship placement is valid
                    # returns a 2 tuple with placedShips and a bool of if it was placed
                    attempt = addShip(shipBoard, placedShips, index, pos, shipLength)
                    placedShips = attempt[0]
                    wasPlaced = attempt[1]
                    # if it was placed, updaate start time and decrease ship length
                    if(wasPlaced):
                        startTime = time.time()
                        shipLength = shipLength - 1
            pygame.display.update()
        else:
            # if ship is placed, move on to the next ship
            shipsCopy.pop(0)
            if(len(shipsCopy) != 0):
                shipLength = shipsCopy[0]
                initialLength = shipLength
                index = index + 1
    battleship.printShipBoard(shipBoard, placedShips, [], [])
    pygame.display.update()
    pause(1)

# same as above but for player 2
def placePlayer2Ships(screen, ships, placedShips, shipBoard):
    shipsCopy = ships
    index = 0
    shipLength = shipsCopy[0]
    initialLength = shipLength
    startTime = time.time()
    while len(shipsCopy) > 0:
        currentTime = time.time()
        if currentTime - startTime > 15:
            add_text.time_out(screen)
            pygame.display.update()
            pause(3)
            pygame.quit()
            sys.exit()
        if(shipLength > 0):
            stringofint = (str)(initialLength)
            toDisplay = 'Player 2, place your ship of length ' + stringofint
            add_text.add_text(screen, toDisplay)
            add_text.add_labels_ships(screen)
            add_text.add_labels_middle(screen)
            pos = pygame.mouse.get_pos()
            battleship.printShipBoard(shipBoard, placedShips, [], [])
            # createPlayer1ShipGrid()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    attempt = addShip(shipBoard, placedShips, index, pos, shipLength)
                    placedShips = attempt[0]
                    wasPlaced = attempt[1]
                    if(wasPlaced):
                        startTime = time.time()
                        shipLength = shipLength - 1
                   
            pygame.display.update()
        else:
            shipsCopy.pop(0)
            print(len(shipsCopy))
            if(len(shipsCopy) != 0):
                shipLength = shipsCopy[0]
                initialLength = shipLength
                index = index + 1
    battleship.printShipBoard(shipBoard, placedShips, [], [])
    pygame.display.update()
    pause(1)

#places the ships for the AI randomly
# !!!! still needs to implement a check to see if a ship will fit before starting to place
def placeAiShips(screen, ships, placedShips, shipBoard):
    shipsCopy = ships
    index = 0
    shipLength = shipsCopy[0]
    initialLength = shipLength
    startTime = time.time()
    while len(shipsCopy) > 0:
        currentTime = time.time()
        if currentTime - startTime > 15:
            add_text.time_out(screen)
            pygame.display.update()
            pause(3)
            pygame.quit()
            sys.exit()
        if(shipLength > 0):
            stringofint = (str)(initialLength)
            screen.fill(battleship.BLACK, (0,0, 490, 400))
            toDisplay = 'Computer is placing ships'
            add_text.add_text(screen, toDisplay)
            # pos = pygame.mouse.get_pos()
            x = randint(30, 230)
            y = randint(100, 300)
            pos = (x, y)
            # battleship.printShipBoard(shipBoard, placedShips, [], [])   
            attempt = addShip(shipBoard, placedShips, index, pos, shipLength)
            placedShips = attempt[0]
            wasPlaced = attempt[1]
            if(wasPlaced):
                startTime = time.time()
                shipLength = shipLength - 1

            pygame.display.update()
        else:
            shipsCopy.pop(0)
            print(len(shipsCopy))
            if(len(shipsCopy) != 0):
                shipLength = shipsCopy[0]
                initialLength = shipLength
                index = index + 1
    pygame.display.update()
    print("AI placement successful")
    pause(1)


# handles logic for adding ship
def addShip(shipBoard, placedShips, index, pos, shipLength):
    # starts at false
    shipAdded = False
    # gets the current ship
    currentShip = placedShips[index]
    # get rectangle that was selected
    rect = battleship.getRectangle(shipBoard, pos)
    # if row is invalid, make user click new spot
    if battleship.getRow(shipBoard, rect) == -1 or battleship.getCol(shipBoard, rect) == -1:
        return(placedShips, shipAdded) 

    # otherwise if it is a new ship make sure it is not already placed
    if(len(currentShip) == 0):
        alreadyPlaced = inShips(placedShips, pos)
        valid = validPlacement(shipBoard, placedShips, index, pos, shipLength)
        if ((not alreadyPlaced) and valid):
            currentShip = addToShips(placedShips, pos, currentShip, shipBoard)
            shipAdded = True
    else:
        # if ship already exists, check that new addition isn't already placed and check that it touches the current ship
        alreadyPlaced = inShips(placedShips, pos)
        valid = validPlacement(shipBoard, placedShips, index, pos, shipLength)
        if ((not alreadyPlaced) and valid):
            touchesShipCheck = touchesShip(shipBoard, placedShips, index, pos)
            if touchesShipCheck:
                currentShip = addToShips(placedShips, pos, currentShip, shipBoard)
                shipAdded = True
    # add current ship to placedships
    placedShips[index] = currentShip
    # return placed ships and a bool of if it was added
    print(shipAdded)
    return (placedShips, shipAdded)

# checks that your placement touches the part of the ship already placed
def touchesShip(shipBoard, placedShips, index, pos):
    currentShip = placedShips[index]
    rect = battleship.getRectangle(shipBoard, pos)
    row = battleship.getRow(shipBoard, rect)
    col = battleship.getCol(shipBoard, rect)
    # if length is 1, it can be above, below, or either side
    if len(currentShip) == 1:
        for ship in currentShip:
            currentRow = battleship.getRow(shipBoard, ship)
            currentCol = battleship.getCol(shipBoard, ship)
            if row == currentRow:
                difference = abs(col-currentCol)
                if difference == 1:
                    return True
            elif col == currentCol:
                difference = abs(row-currentRow)
                if difference == 1:
                    return True
    else:
        # if length isn't one you need to check that it is aligned with currentship
        ship1 = currentShip[0]
        ship2 = currentShip[1]
        ship1row = battleship.getRow(shipBoard, ship1)
        ship2row = battleship.getRow(shipBoard, ship2)
        ship1col = battleship.getCol(shipBoard, ship1)
        ship2col = battleship.getCol(shipBoard, ship2)
        if ship1row == ship2row:
            for ship in currentShip:
                shiprow = battleship.getRow(shipBoard, ship)
                if row == shiprow:
                    shipcol = battleship.getCol(shipBoard, ship)
                    difference = abs(shipcol-col)
                    if difference == 1:
                        return True
        elif ship2col == ship1col:
            for ship in currentShip:
                shipcol = battleship.getCol(shipBoard, ship)
                if col == shipcol:
                    shiprow = battleship.getRow(shipBoard, ship)
                    difference = abs(shiprow-row)
                    if difference == 1:
                        return True
    return False



# checks if rect has already been placed
def inShips(placedShips, pos):
    for x in range(0, len(placedShips)):
        for y in range(0, len(placedShips[x])):
            tempRect = (placedShips[x])[y]
            if tempRect.collidepoint(pos):
                return True
    return False

# adds ship to current ship
def addToShips(placedShips, pos, currentShip, shipBoard):
    for x in range(0, 10):
        for y in range(0, 10):
            tempRect = (shipBoard[x])[y]
            if tempRect.collidepoint(pos):
                currentShip.append(tempRect)
                return currentShip
    return currentShip
    

def validPlacement(shipBoard, placedShips, index, pos, shipLength):
    counter = 0
    currentShip = placedShips[index]
    rect = battleship.getRectangle(shipBoard, pos)
    row = battleship.getRow(shipBoard, rect)
    col = battleship.getCol(shipBoard, rect)

    
    if len(currentShip) == 0:
        if spaceHorz(row, col, placedShips, shipLength) or spaceVert(row, col, placedShips, shipLength):
            return(True)
        else:
            return(False)
    return(True)
    '''
    else:
        ship1 = currentShip[0]
        ship1row = battleship.getRow(shipBoard, ship1)
        ship1col = battleship.getCol(shipBoard, ship1)
        if ship1row == row:
            if validHorz(ship1row, ship1col, placedShips, shipLength):
                return(True)
        if ship1col == col:
            if validVert(ship1row, ship1col, placedShips, shipLength):
                return(True)
        return(False)
        '''

# checks if there is enough horizontal space for the whole ship
def spaceHorz(row, col, placedShips, shipLength):
    check1 = True
    check2 = True
    print(shipLength)
    for stepper in range(0, shipLength):
        tempcol = col + stepper
        tempPos = ((30 + row*20), (100 + tempcol*20))
        alreadyPlaced = inShips(placedShips, tempPos)
        if alreadyPlaced or (tempcol >= 10):
            check1 = False
    for stepper in range(0, shipLength):
        tempcol = col - stepper
        tempPos = ((30 + row*20), (100 + tempcol*20))
        alreadyPlaced = inShips(placedShips, tempPos)
        if alreadyPlaced or (tempcol < 0):
            check2 = False
    return(check1 or check2)

#checks if there is enough vertical space for the entire ship
def spaceVert(row, col, placedShips, shipLength):
    check1 = True
    check2 = True
    print(shipLength)
    for stepper in range(0, shipLength):
        temprow = row + stepper
        tempPos = ((30 + temprow*20), (100 + col*20))
        alreadyPlaced = inShips(placedShips, tempPos)
        if alreadyPlaced or (temprow >= 10):
            check1 = False
    for stepper in range(0, shipLength):
        temprow = row - stepper
        tempPos = ((30 + temprow*20), (100 + col*20))
        alreadyPlaced = inShips(placedShips, tempPos)
        if alreadyPlaced or (temprow < 0):
            check2 = False
    return(check1 or check2)


    

def validHorz(row, col, placedShips, shipLength):
    counter = 0
    print(shipLength)
    for stepper in range(1, shipLength+1):
        tempcol = col + stepper
        tempPos = ((30 + row*20), (100 + tempcol*20))
        alreadyPlaced = inShips(placedShips, tempPos)
        if not (alreadyPlaced or (tempcol >= 10) or (tempcol < 0)):
            counter = counter + 1
    for stepper in range(1, shipLength+1):
        tempcol = col - stepper
        tempPos = ((30 + row*20), (100 + tempcol*20))
        alreadyPlaced = inShips(placedShips, tempPos)
        if not (alreadyPlaced or (tempcol >= 10) or (tempcol < 0)):
            counter = counter + 1
    if counter < shipLength:
        return(False)
    return(True)

def validVert(row, col, placedShips, shipLength):
    counter = 0
    print(shipLength)
    for stepper in range(1, shipLength+1):
        temprow = row + stepper
        tempPos = ((30 + temprow*20), (100 + col*20))
        alreadyPlaced = inShips(placedShips, tempPos)
        if not (alreadyPlaced or (temprow >= 10) or (temprow < 0)):
            counter = counter + 1
    for stepper in range(1, shipLength+1):
        temprow = row - stepper
        tempPos = ((30 + temprow*20), (100 + col*20))
        alreadyPlaced = inShips(placedShips, tempPos)
        if not (alreadyPlaced or (temprow >= 10) or (temprow < 0)):
            counter = counter + 1
    if counter < shipLength:
        return(False)
    return(True)


    '''
    check1 = True
    check2 = True
    print(shipLength)
    for stepper in range(1, shipLength):
        temprow = row + stepper
        tempPos = ((30 + temprow*20), (100 + col*20))
        alreadyPlaced = inShips(placedShips, tempPos)
        if alreadyPlaced or (temprow >= 10):
            check1 = False
    for stepper in range(1, shipLength):
        temprow = row - stepper
        tempPos = ((30 + temprow*20), (100 + col*20))
        alreadyPlaced = inShips(placedShips, tempPos)
        if alreadyPlaced or (temprow < 0):
            check2 = False
    return(check1 or check2)
    



    elif len(currentShip) == 1:
        ship1 = currentShip[0]
        ship1row = battleship.getRow(shipBoard, ship1)
        ship1col = battleship.getCol(shipBoard, ship1)
        if ship1row == row:
            if validHorz(row, col, placedShips, shipLength):
                return(True)
        elif ship1col == col:
            if validVert(row, col, placedShips, shipLength):
                return(True)
        return(False)
    


    counter = 0
    start = currentShip[0]
    end = currentShip[len(currentShip)-1]

    ship1row = battleship.getRow(shipBoard, start)
    ship1col = battleship.getCol(shipBoard, start)

    for stepper in range(1, shipLength):
        tempcol = col + stepper
        tempPos = ((30 + row*20), (100 + tempcol*20))
        alreadyPlaced = inShips(placedShips, tempPos)
        if alreadyPlaced or (tempcol >= 10):
            check1 = False
    for stepper in range(1, shipLength):
        tempcol = col - stepper
        tempPos = ((30 + row*20), (100 + tempcol*20))
        alreadyPlaced = inShips(placedShips, tempPos)
        if alreadyPlaced or (tempcol < 0):
            check2 = False
    

        for stepper in range(1, shipLength*2):
            temprow = ship1row + stepper
            tempcol = ship1col + stepper
            if ship1row == row:
                tempPos = ((30 + (pos[0])*20), (100 + tempcol*20))
                alreadyPlaced = inShips(placedShips, tempPos)
                if alreadyPlaced:
                    counter = counter + 1
            elif ship1col == col:
                tempPos = ((30 + temprow*20), (100 + (pos[1])*20))
                alreadyPlaced = inShips(placedShips, tempPos)
                if alreadyPlaced:
                    counter = counter + 1
        if counter == 0:
            return(True)
    # return(False)
        
    counter = 0
    for stepper in range(1, shipLength*2):
        tempcol = col - shipLength + stepper
        tempPos = ((30 + row*20), (100 + tempcol*20))
        alreadyPlaced = inShips(placedShips, tempPos)
        if not (alreadyPlaced or (tempcol >= 10) or (tempcol < 0)):
            counter = counter + 1
        print(counter)
    if counter < shipLength:
        return(False)
    return(True)
    

    counter = 0
    for stepper in range(1, shipLength*2):
        temprow = row - shipLength + stepper
        tempPos = ((30 + temprow*20), (100 + col*20))
        alreadyPlaced = inShips(placedShips, tempPos)
        if not (alreadyPlaced or (temprow >= 10) or (temprow < 0)):
            counter = counter + 1
        print(counter)
    if counter < shipLength:
        return(False)
    return(True)
    

    for stepper in range(1, shipLength*2):
        counter = 0
        start = col - shipLength + stepper
        for i in range(0, shipLength):
            tempcol = start + i
            print(tempcol)
            tempPos = ((30 + row*20), (100 + tempcol*20))
            alreadyPlaced = inShips(placedShips, tempPos)
            if not (alreadyPlaced or (tempcol >= 10) or (tempcol < 0)):
                counter = counter + 1
            if counter == shipLength:
                return(True)
    return(False)
    '''