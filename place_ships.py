from audioop import add
import math
from matplotlib.pyplot import pause
from numpy import place
import pygame
import sys
import battleship
import add_text

def placePlayer1Ships(screen, ships, placedShips, shipBoard):
    shipsCopy = ships
    index = 0
    shipLength = shipsCopy[0]
    initialLength = shipLength
    while len(shipsCopy) > 0:
        if(shipLength > 0):
            stringofint = (str)(initialLength)
            toDisplay = 'Player 1, place your ship of length ' + stringofint
            add_text.add_text(screen, toDisplay)
            add_text.add_labels_ships(screen)
            add_text.add_labels_middle(screen)
            pos = pygame.mouse.get_pos()
            battleship.printShipBoard(shipBoard, placedShips)
            # createPlayer1ShipGrid()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    attempt = addShip(shipBoard, placedShips, index, pos)
                    placedShips = attempt[0]
                    wasPlaced = attempt[1]
                    if(wasPlaced):
                        shipLength = shipLength - 1
            pygame.display.update()
        else:
            shipsCopy.pop(0)
            print(len(shipsCopy))
            if(len(shipsCopy) != 0):
                shipLength = shipsCopy[0]
                initialLength = shipLength
                index = index + 1

def placePlayer2Ships(screen, ships, placedShips, shipBoard):
    shipsCopy = ships
    index = 0
    shipLength = shipsCopy[0]
    initialLength = shipLength
    while len(shipsCopy) > 0:
        if(shipLength > 0):
            stringofint = (str)(initialLength)
            toDisplay = 'Player 2, place your ship of length ' + stringofint
            add_text.add_text(screen, toDisplay)
            pos = pygame.mouse.get_pos()
            battleship.printShipBoard(shipBoard, placedShips)
            # createPlayer1ShipGrid()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    attempt = addShip(shipBoard, placedShips, index, pos)
                    placedShips = attempt[0]
                    wasPlaced = attempt[1]
                    if(wasPlaced):
                        shipLength = shipLength - 1
                   
            pygame.display.update()
        else:
            shipsCopy.pop(0)
            print(len(shipsCopy))
            if(len(shipsCopy) != 0):
                shipLength = shipsCopy[0]
                initialLength = shipLength
                index = index + 1

def addShip(shipBoard, placedShips, index, pos):
    shipAdded = False
    currentShip = placedShips[index]
    rect = battleship.getRectangle(shipBoard, pos)
    if battleship.getRow(shipBoard, rect) == -1 or battleship.getCol(shipBoard, rect) == -1:
        return(placedShips, shipAdded) 
    if(len(currentShip) == 0):
        alreadyPlaced = inShips(placedShips, pos)
        if not alreadyPlaced:
            currentShip = addToShips(placedShips, pos, currentShip, shipBoard)
            shipAdded = True
    else:
        alreadyPlaced = inShips(placedShips, pos)
        if not alreadyPlaced:
            touchesShipCheck = touchesShip(shipBoard, placedShips, index, pos)
            if touchesShipCheck:
                currentShip = addToShips(placedShips, pos, currentShip, shipBoard)
                shipAdded = True

    placedShips[index] = currentShip
    return (placedShips, shipAdded)

def touchesShip(shipBoard, placedShips, index, pos):
    currentShip = placedShips[index]
    rect = battleship.getRectangle(shipBoard, pos)
    row = battleship.getRow(shipBoard, rect)
    col = battleship.getCol(shipBoard, rect)
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




def inShips(placedShips, pos):
    for x in range(0, len(placedShips)):
        for y in range(0, len(placedShips[x])):
            tempRect = (placedShips[x])[y]
            if tempRect.collidepoint(pos):
                return True
    return False

def addToShips(placedShips, pos, currentShip, shipBoard):
    for x in range(0, 10):
        for y in range(0, 10):
            tempRect = (shipBoard[x])[y]
            if tempRect.collidepoint(pos):
                currentShip.append(tempRect)
                return currentShip
    return currentShip
    
